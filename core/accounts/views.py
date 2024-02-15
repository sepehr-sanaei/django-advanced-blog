from django.shortcuts import render
from django.shortcuts import HttpResponse
from .tasks import sendEmail
# Create your views here.
def sendmail(request):
    sendEmail.delay()
    return HttpResponse("sending email is done")