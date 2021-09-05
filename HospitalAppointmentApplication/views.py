from django.contrib.auth import authenticate, login
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from .serializers import *
from .models import *
from .forms import *


# Create your views here.

""" This function is for login page using default Django login views"""
def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            retrived_data = form.cleaned_data
            user = authenticate(request,
                                username=retrived_data['username'],
                                password=retrived_data['password'])
            if user is not None:
                login(request, user)
                return HttpResponse('Authentication was successfull')
            else:
                return HttpResponse('Authentication failed, Please try again')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


"""queryset is used to get list of patient details and
serializer_class used to translate patient details from django to other formats like Json"""
class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

"""queryset is used to get list of doctor details and
serializer_class used to translate doctor details from django to other formats like Json"""
class DoctorViewSet(ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

"""queryset is used to get list of appointment details and
serializer_class used to translate appointment details from django to other formats like Json"""
class AppointmentViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def perform_create(self, serializer):
        """doctor variable is used to get list of doctor details from models,
        patient variable is used to get list of patient details from models,
        today_date variable is used to get date of appointment from models,
        appointment_filter variable  is used to patient canot take second appointmnet with same doctor on any particular day """

        doctor = self.request.data["doctor"]
        patient = self.request.data["patient"]
        today_date = self.request.data["date_appointment"]
        appointment_filter = Appointment.objects.filter(doctor=doctor, patient=patient, date_appointment=today_date)
        if len(appointment_filter) > 0:
            print("Appointment already booked on ", today_date)
        else:
            print("Appointment booked successfully", today_date)
            serializer.save()
