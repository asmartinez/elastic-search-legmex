from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import DocumentoSerializer
from .models import Biblioteca
from .documents import BibliotecaDocument
from rest_framework.parsers import MultiPartParser, FormParser


@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def SubirDocumento(request):
    """
    Funcion para subir documento en formato formulario html
    {
        "id": "",
        "dispositionTitle": "",
        "date": "",
        "volume": "",
        "pageNumbers": "",
        "legislationTranscriptOriginal": "documentoPDF",
        "legislationTranscriptCopy": "",
        "place": "",
        "dispositionNumber": "",
        "dispositionTypeId": "",
        "affairId": "",
    }
    """
    serializerUpload = DocumentoSerializer(
        data = request.data
    )  # Serializar datos del request
    if serializerUpload.is_valid():  # Se valida la data
        serializerUpload.save()  # Se guardan los datos en db y elastic search
        return Response(serializerUpload.data, status = status.HTTP_200_OK)
    return Response(serializerUpload.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def BuscarDocumento(request):
    """
    Funcion para busqueda de documentos en la base de datos en un formulario
        "search":"<palabra_a_buscar>",
        "fields":"dispositionTitle,date,volume" # Si no se envia en la peticion GET se hace
                    una busqueda en todos los campos, se tiene que separar con coma ( , )
                    cada campo especifico en donde deseas buscar #
    """

    # Revisa si se mandan los campos especificos a buscar
    if request.GET.get("search") and request.GET.get("fields"):
        searchString = request.query_params["search"]  # Asigna palabra a buscar

        fieldToSearch = request.query_params["fields"].split(
            ","
        )  # Combierte el string a un array

    # Revisa si por lo menos se manda el campo search para hacer la busqueda en todos los campos
    elif request.GET.get("search"):
        searchString = request.query_params["search"]
        fieldToSearch = [
            "dispositionTitle",
            "date",
            "volume",
            "pageNumbers",
            "legislationTranscriptCopy",
            "place",
            "dispositionNumber",
        ]

    # Devuelve un error si no se manda ningun argumento
    else:
        return Response(
            {"message": "Error, no se mando ningun argumento de busqueda"},
            status = status.HTTP_400_BAD_REQUEST,
        )

    # ------ Query de busqueda en elastic search y se guardan los resultados en response ---------
    searchQuery = BibliotecaDocument.search().query(
        "multi_match", query = searchString, fields = fieldToSearch
    )
    responseQuery = searchQuery.execute()
    # --------------------------------------------------------------------------------------------

    # Deserializacion de resultados de busqueda --------------------------------------------------
    deSerializer = DocumentoSerializer(responseQuery.hits, many = True)
    # --------------------------------------------------------------------------------------------

    # ------ Por falla en deserializacion no manda el link del documento, ------------------------
    # ------ asi que se usa la respuesta de elastic para llenar ese campo ------------------------
    for i in range(0, len(deSerializer.data)):
        deSerializer.data[i]["legislationTranscriptOriginal"] = responseQuery.hits[i][
            "legislationTranscriptOriginal"
        ]

    return Response(deSerializer.data, status = status.HTTP_200_OK)


class ModificarDocumento(APIView):
    """
    Funcion para eliminar un documento por su id, en la url se puede meter este valor
    """
    parser_classes = [FormParser, MultiPartParser]
    def delete(self, request, id):
        try:
            documentByID = Biblioteca.objects.get(id = id)
        except:
            return Response(
                {"message": "Error, no se encontro el documento"},
                status = status.HTTP_400_BAD_REQUEST,
            )
        documentByID.delete()
        return Response(
            {"message": "Se elimino correctamente el documento"},
            status = status.HTTP_200_OK,
        )
    def put(self, request, id):
        try:
            documentByID = Biblioteca.objects.get(id = id)
        except:
            return Response(
                {"message": "Error, no se encontro el documento"},
                status = status.HTTP_400_BAD_REQUEST,
            )
        documentUpdate = DocumentoSerializer(documentByID, data = request.data)
        if documentUpdate.is_valid():
            documentUpdate.save()
            return Response(documentUpdate.data, status = status.HTTP_200_OK)
        return Response(documentUpdate.errors, status = status.HTTP_400_BAD_REQUEST)
    def get(self, request, id):
        try: 
            documentByID = Biblioteca.objects.get(id = id)
        except:
            return Response(
                {"message": "Error, no se encontro el documento"},
                status = status.HTTP_400_BAD_REQUEST,
            )
        document = DocumentoSerializer(documentByID)
        return Response(document.data, status = status.HTTP_200_OK)


@api_view(["GET"])
def NumeroDocumentos(request):
    """
    Funcion para devolver el numero de documentos que hay para cada disposicion
    """
    pass

        