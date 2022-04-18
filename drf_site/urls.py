"""drf_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from women.views import *

# c viewset'ами лучше использовать роутеры
router = routers.SimpleRouter()
router.register(r'womenrouter', WomenViewSet)

"""
url name по умолчанию model_name плюс -list или -detail (если pk)
можно задать свое:
router.register(r'womenrouter', WomenViewSet, basename='xxx')
name будет xxx-list
basename ОБЯЗАТЕЛЕН если во ViewSet мы не указываем атрибут queryset


Разница SimpleRouter и DefaultRouter:
Simple список маршрутов: /api/v1/women/,  /api/v1/women/pk
Defaut: то же самое плюс  /api/v1/
"""


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/womenlist', WomenAPIView.as_view()), # get, post
    path('api/v1/womenlist/<int:pk>', WomenAPIView.as_view()), # put, delete

    path('api/v1/womenlistcreate/', WomenAPIList.as_view()),
    path('api/v1/womenlistcreate/<int:pk>/', WomenAPIUpdate.as_view()),
    path('api/v1/womendetail/<int:pk>/', WomenAPIDetailView.as_view()),

    path('api/v1/womenviewset/', WomenViewSet.as_view({'get':'list'})), # get - тип запроса, list - метод вызываемый в самом вьюсете для обработки запроса
    path('api/v1/womenviewset/<int:pk>/', WomenViewSet.as_view({'put':'update'})),

    path('api/v1/', include(router.urls)), # http://127.0.0.1:8000/api/v1/womenrouter/(id)

    path('api/v1/women/', WomenAPIList.as_view()),
    path('api/v1/women/<int:pk>/', WomenAPIUpdate.as_view()),
    path('api/v1/womendelete/<int:pk>/', WomenAPIDestroy.as_view()),

    path('api/v1/session-auth/', include('rest_framework.urls')), # подключаем авторизацию на основе сессии cook (только эта одна строчка)
    # авторизация на основе сессии привязана к домену, к браузеру, к устройству

    path('api/v1/token-auth/', include('djoser.urls')),
    re_path(r'^token-auth/', include('djoser.urls.authtoken')), # ...8000/token-auth/token/login (без api/v1/)

    path('api/v1/jwt-auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # JWT - Json Web Token
    path('api/v1/jwt-auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/jwt-auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
]


###############################################################################


""" Создание своего класса роутеров: 
читает список статей либо конкретную статью по id"""
class MyCustomRouter(routers.SimpleRouter):
    routes = [
        routers.Route(url=r'^{prefix}$', # еще где-то тут слеш в конце прописать может понадобиться...
                      mapping={'get': 'list'},
                      name='{basename}-list',
                      detail=False,
                      initkwargs={'suffix': 'List'}),
        routers.Route(url=r'^{prefix}/{lookups}$',
                      mapping={'get': 'retrieve'},
                      name='{basename}-detail',
                      detail=True,
                      initkwargs={'suffix': 'Detail'}),
    ]


