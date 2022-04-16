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
    """ Кодирование, Преобразование объекта WomenModel в json формат  """
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
    """ Обратное преобразование из json-строки в объект класса WomenModel """
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


class WomenSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    time_create = serializers.DateTimeField()
    time_update = serializers.DateTimeField()
    is_published = serializers.BooleanField(default=True)
    category_id = serializers.IntegerField()





