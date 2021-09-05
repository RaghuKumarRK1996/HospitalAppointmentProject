from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from HospitalAppointmentApplication import views
from django.urls import path, include
from rest_framework import routers
from .views import login_user



"""For auto config the urls Router will be use
and in router views need to register"""

router = routers.DefaultRouter()
router.register('patient', views.PatientViewSet)
router.register('doctor', views.DoctorViewSet)
router.register('appointment', views.AppointmentViewSet)

"""all the urls mapping done in urlpatters"""

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include(router.urls)),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),

]
