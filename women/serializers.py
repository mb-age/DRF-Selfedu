import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Women


########################################################################


class WomenSerializer_aaa(serializers.ModelSerializer):
    class Meta:
        model = Women
        fields = ('title', 'category_id')


#########################################################################


class WomenModel_bbb:
    """    Имитирует модель    """
    def __init__(self, title, content):
        self.title = title
        self.content = content

class WomenSerializer_bbb(serializers.Serializer):
    title = serializers.CharField(max_length=255) # проверка прямо в сериализаторе, что поле title не превышает 255 символов
    content = serializers.CharField()

def encode_bbb():
    """ Кодирование, Преобразование объекта WomenModel в json формат
    Функция get во views"""
    model = WomenModel_bbb('Angie', 'Content - Angie')
    model_serializer = WomenSerializer_bbb(model) # объект сериализации
    # тут мы КОдируем, так что просто передаем параметр model, для ДЕкодирования нужно передавать именованный параметр data=
    print(model_serializer.data)
    # {'title': 'Angie', 'content': 'Content - Angie'}
    print(type(model_serializer.data))
    # <class 'rest_framework.utils.serializer_helpers.ReturnDict'>
    json = JSONRenderer().render(model_serializer.data) # словарь преобразовываем в json строку
    print(json)
    # b'{"title":"Angie","content":"Content - Angie"}' - "b" в начале

def decode_bbb():
    """ Обратное преобразование из json-строки в объект класса WomenModel
    Функция post во views"""
    stream = io.BytesIO(b'{"title":"Angie","content":"Content - Angie"}') # поток содержащий json строку
    # имитируем поступление json-строки от клиента
    data = JSONParser().parse(stream) # формируем из него словарь
    serializer = WomenSerializer_bbb(data=data) # получаем объект сериализации
    # чтобы сериализатор ДЕкодировал данные, нужно использовать именованный параметр data=
    print(serializer)
    # WomenSerializer_bbb(data={'title': 'Angie', 'content': 'Content - Angie'}):
    #     title = CharField(max_length=255)
    #     content = CharField()
    serializer.is_valid() # проверяем корректность принятых данных
    print(serializer.validated_data) # после того, как метод .is_valid отработает, в сериализаторе появится коллекция validated_data - результат декодирования json-строки
    # OrderedDict([('title', 'Angie'), ('content', 'Content - Angie')])


########################################################################


class WomenSerializer_ccc(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    time_create = serializers.DateTimeField(read_only=True) # чтобы не надо было их заполнять при добавлении записи в бд?
    time_update = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=True)
    category_id = serializers.IntegerField()


########################################################################

""" 
 В сериализатор можно прописывать методы create и update:
 create(self, validated_data) - для добавления (создания) записи
 update(self, instance, validated_data) - для изменения записи

"""

class WomenSerializer_ddd(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    time_create = serializers.DateTimeField(read_only=True)
    time_update = serializers.DateTimeField(read_only=True)
    is_published = serializers.BooleanField(default=True)
    category_id = serializers.IntegerField()

    def create(self, validated_data): # post
        return Women.objects.create(**validated_data)

    def update(self, instance, validated_data): # put
        # instance - ссылка на обьект модели Women
        # val_data - словарь из проверенных даных, которые нужно изменить в базе данных
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.time_update = validated_data.get('time_update', instance.time_update)
        instance.is_published = validated_data.get('is_published', instance.is_published)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.save()
        return instance


#############################################################################


class WomenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Women
        fields = '__all__'
        # fields = ('title', 'content', 'category')


#############################################################################



