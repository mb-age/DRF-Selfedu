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


class WomenAPIView_ddd(APIView):

    def get(self, request):
        lst = Women.objects.all() # queryset
        return Response({'посты': WomenSerializer(lst,many=True).data}) # many=True потому что список записей, а не одна

    def post(self, request):
        serializer = WomenSerializer(data=request.data) # проверка
        serializer.is_valid(raise_exception=True) # проверка (если мы чего-то не написали, то не error, а сообщение "обязательное поле")

        post_new = Women.objects.create(
            title=request.data['title'],
            content=request.data['content'],
            category_id=request.data['category_id']
        )
        return Response({'пост': WomenSerializer(post_new).data})


#######################################################################


class WomenAPIView(APIView):

    def get(self, request): # read
        lst = Women.objects.all() # queryset
        return Response({'посты': WomenSerializer(lst,many=True).data}) # many=True потому что список записей, а не одна

    def post(self, request): # create
        serializer = WomenSerializer(data=request.data) # проверка
        serializer.is_valid(raise_exception=True) # в этом моменте формируется словарь validated_data
        serializer.save() # вызывает метов create из сериализатора
        return Response({'пост': serializer.data}) # коллекция data будет ссылаться на новый созданный объект

    def put(self, request, *args, **kwargs): # update
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PUT is not allowed'})

        try:
            instance = Women.objects.get(pk=pk)
        except:
            return Response({'error': 'Object does not exist'})

        serializer = WomenSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # метод save вызовет у сериализатора метод update. Потому что в сериализатор мы передали два параметра (data и instance) и у update два параметра. Если мы передаем в сериализатор один параметр как в post (data), то вызывается метод create (у него тоже один параметр)
        return Response({'пост': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method DELETE is not allowed'})

        try:
            instance = Women.objects.get(pk=pk)
        except:
            return Response({'error': 'Object does not exist'})

        instance.delete()
        return Response({'пост': f'delete post #{pk}'})


##############################################################################

