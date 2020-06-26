"""recovery_management_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
from emr_app.views import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'user', Users, 'user')
router.register(r'provider', Providers, 'provider')
router.register(r'client', Clients, 'client')
router.register(r'unassigned_clients', UnassignedClients, 'unassignedclient')
router.register(r'provider_client', ProviderClients, 'providerclient')
router.register(r'provider_type', ProviderTypes, 'providertype')
router.register(r'appointment', Appointments, 'appointment')
router.register(r'client_appointment', ClientAppointments, 'clientappointment')
router.register(r'note_template', NoteTemplates, 'notetemplate')
router.register(r'note', Notes, 'note')

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('register_provider/', register_provider),
    path('register_client/', register_client),
    path('login/', login_provider),
    path('admin_login/', login_admin)
]
