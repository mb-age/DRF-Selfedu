from django.forms import model_to_dict
from rest_framework import generics, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Women, Category
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
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


class WomenAPIList_aaa(generics.ListCreateAPIView):
    # ListCreateAPIView реализует методы get и post
    # list - прочесть все записи
    # retrieve - прочесть конкретную запись
    queryset = Women.objects.all()
    serializer_class = WomenSerializer


class WomenAPIUpdate_aaa(generics.UpdateAPIView):
    # UpdateAPIView реализует put-запрос
    queryset = Women.objects.all()
    serializer_class = WomenSerializer


class WomenAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer


##############################################################################


class WomenViewSet_aaa(viewsets.ModelViewSet):
    # ModelViewSet - read, create, update, delete
    queryset = Women.objects.all()
    serializer_class = WomenSerializer


class WomenViewSet_bbb(viewsets.ReadOnlyModelViewSet):
    # ReadOnlyModelViewSet - read (list, retrieve)
    queryset = Women.objects.all()
    serializer_class = WomenSerializer

class WomenViewSet_ccc(mixins.CreateModelMixin, # создание "своего" вьюсета
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   # mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer


###############################################################################


class WomenViewSet(viewsets.ModelViewSet):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer

    """ Если стандартных url недостаточно, можно определить новые с помощью декоратора action"""
    @action(methods=['get'], detail=False)
    def categories(self, request):
        """ Возвращает список категорий (актрисы, певицы) """
        # api/v1/womenrouter/categories (имя функции)
        categories = Category.objects.all()
        return Response({'категории': [c.name for c in categories]})

    @action(methods=['get'], detail=True)
    def category(self, request, pk=None):
        """ Возвращает одну категорию по id """
        # api/v1/womenrouter/1/category - категория с id 1
        # api/v1/womenrouter/2/category - категория с id 2
        categories = Category.objects.get(pk=pk)
        return Response({'категория': categories.name})


    """ Иногда по определенному url запросу нужно возвращать не все записи, а только определенные, по какому-то условию"""
    def get_queryset(self):
        """ Переопределяем метод get_queryset. Возвращаем только первые три записи """
        # теперь можно убрать атрибут queryset из класса, но тогда в роуте нужно будет прописать basename
        pk = self.kwargs.get('pk') # получаем pk если он ЕСТЬ в url
        if not pk:
            return Women.objects.all()[:3]
        return Women.objects.filter(pk=pk) # filter потому что он возвращает список из одной записи, а нам нужен список, потому что get_queryset должен возвращать список, если не будет списка, то error


##################################################################################################################


"""  Permissions: 
- AllowAny (default)
- IsAuthenticated
- IsAdminUser
- IsAuthenticatedOrReadOnly 
"""

class WomenAPIList(generics.ListCreateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

class WomenAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    # permission_classes = (IsOwnerOrReadOnly, )
    permission_classes = (IsAuthenticated, )
    # authentication_classes = (TokenAuthentication, ) # указать способ аутентификации на уровне отдельных представлений

class WomenAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsAdminOrReadOnly, )





