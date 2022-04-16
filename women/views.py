from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Women
from .serializers import WomenSerializer


#######################################################################


class WomenAPIView_aaa(generics.ListAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer


#######################################################################


class WomenAPIView_bbb(APIView):
    def get(self, request):
        return Response({'имя':'Яна'})
    def post(self, request):
        return Response({'имя': 'Янка'})


#######################################################################


class WomenAPIView_ccc(APIView):

    def get(self, request):
        lst = Women.objects.all().values() # потому что без values это queryset, а нам нужен набор значений
        return Response({'посты':list(lst)})

    def post(self, request):
        post_new = Women.objects.create(
            title=request.data['title'],
            content=request.data['content'],
            category_id=request.data['category_id'], # почему-то с "_id", без этого не работает
        )
        return Response({'пост': model_to_dict(post_new)})


#######################################################################


class WomenAPIView(APIView):

    def get(self, request):
        lst = Women.objects.all() # queryset
        return Response({'посты': WomenSerializer(lst,many=True).data}) # many=True потому что список записей, а не одна






