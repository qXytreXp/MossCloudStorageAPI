from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Document
from .serializers import DocumentListSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.generic import View
import os


class UserRegisterView(APIView):
    def post(self, request):
        data = request.data

        user = authenticate(username=data['username'], password=data['password'])

        if user == None:
            return Response({'detail': 'User does not exists!'}, status=500)
        
        return Response({'detail': 'User does exists!'}, status=200)


class DocumentListView(APIView):
    def post(self, request):
        data = request.data

        if data['token'] == '43880072':  
            user = User.objects.get(username=data['username'])

            documents = Document.objects.filter(user=user.id).order_by('-id')
            serializer = DocumentListSerializer(documents, many=True)

            # replace unintelligible characters with clear ones
            for num in range(len(serializer.data)):
                serializer.data[num]['document'] = str(documents[num].document)

            return Response(serializer.data)


class AddDocumentView(APIView):
    def post(self, request):
        data = request.data
        file = request.FILES

        if data['token'] == '43880072':  
            user = User.objects.get(username=data['username'])
      
            model = Document(user=user)
            filename = file['document']


            type_file = str(filename).split(".")[-1] 
            model.type_file = type_file
            model.document.save(file['document'], file['document'])

            model.save()

            return Response(status=200)


class DownloadDocView(View):
    def get(self, request, username, token, filename):  
        if token == '43880072':  
            user = User.objects.get(username=username)

            path = f'{settings.MEDIA_ROOT}/{username}/{filename}'

            with open(path, 'rb') as file:
                response = HttpResponse(content_type="application/octet-stream")
                response['Content-Disposition'] = f"attachment; filename={filename}"
                response.write(file.read())

                return response


class DeleteDocumentView(APIView):
    def post(self, request):
        data = request.data

        if data['token'] == '43880072':  
            user = User.objects.get(username=data['username'])

            # remove file in data base
            model = Document.objects.get(document=f'{user.username}/' + data['document'])
            os.remove(settings.MEDIA_ROOT + '/' + str(model.document).replace('\\', '/'))
            model.delete()

            # if in folder user none files then folder will be remove
            if len(os.listdir(f'{settings.MEDIA_ROOT}/{user.username}/')) == 0:
                os.rmdir(f'{settings.MEDIA_ROOT}/{user.username}/')

            return Response({'detail': 'Document delete!'}, status=200)
  
