
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


app_name = 'djangoapp'
urlpatterns = [
    # # path for registration
    path('login', views.login_user, name='login'),
    path('login/', views.login_user, name='login_slash'),
    path('logout', views.logout_user, name='logout'),
    path('logout/', views.logout_user, name='logout_slash'),
    path('register', views.register_user, name='register'),
    path('register/', views.register_user, name='register_slash'),
    path(route='get_cars', view=views.get_cars, name='getcars'),



    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
