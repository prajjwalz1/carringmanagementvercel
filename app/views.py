from django.shortcuts import render
from .models import Blog,Our_team,Feature,testimony,about_us,Slide,Service,Package,FormSubmission,Availability
# Create your views here.
def home(request):
  slide=Slide.objects.all()
  try:
    about = about_us.objects.get(logo__isnull=False)
    logo = about.logo
  except about_us.DoesNotExist:
    logo = None
  about=about_us.objects.all()

  team=Our_team.objects.all()
  testimonies=testimony.objects.all()
  services=Service.objects.all()


  Context={'slides':slide,'about':about,'services':services,'team':team,'testimonies':testimonies,'logo':logo,'Services':services

  }
  return render(request,'index.html',Context)


def recent_blogs(request):
  blogs = Blog.objects.filter(is_published=True).order_by('-publication_date')[:3]
  return render(request, 'blog/recent_blogs.html', {'blogs': blogs})


from .models import Appointment
from django.http import HttpResponse


def make_appointment(request):
  if request.method == 'POST':
    name = request.POST.get('name')
    phone = request.POST.get('phone')
    services = request.POST.get('services')
    email = request.POST.get('email')
    print(name)
    appointment = Appointment(name=name, phone=phone, services=services, email=email)
    appointment.save()

    return HttpResponse('success')
  else:
    return HttpResponse('Invalid Request')
  # messages.success(request, 'appointment fixed')

def about(request):
  try:
    about = about_us.objects.get(logo__isnull=False)
    logo = about.logo
  except about_us.DoesNotExist:
    logo = None
  slide = Slide.objects.get(id=2)
  abouts=about_us.objects.all()
  team = Our_team.objects.all()
  testimonies = testimony.objects.all()
  services=Service.objects.all()
  Context={
    'about':abouts,'team':team,'testimonies':testimonies,'services':services,'slides':slide,'logo':logo
  }
  return render(request,'about.html',Context)

def service_view(request):
  try:
    about =about_us.objects.get(logo__isnull=False)
    logo = about.logo
  except about_us.DoesNotExist:
    logo = None

  slide = Slide.objects.get(id=3)
  services = Service.objects.all()
  package = Package.objects.all()
  Context={
    'services':services,'package':package,'slides':slide,'logo':logo
  }
  return render(request,'services.html',Context)


def Portfolio_view(request):
  try:
    about = about_us.objects.get(logo__isnull=False)
    logo = about.logo
  except about_us.DoesNotExist:
    logo = None
  projects=Project.objects.all()
  slide = Slide.objects.get(id=3)


  Context={
    'projects':projects,'slides':slide,'logo':logo
  }
  return render(request,'portfolio.html',Context)

def Package_view(request):
  package=Package.objects.all()


  Context={
    'package':package
  }
  return render(request,'pricing.html',Context)

def blog_view(request):
  try:
    about = about_us.objects.get(logo__isnull=False)
    logo = about.logo
  except about_us.DoesNotExist:
    logo = None
  slide = Slide.objects.get(id=4)
  blogs=Blog.objects.all()

  Context={
   'blogs':blogs,'slides':slide,'logo':logo
  }
  return render(request,'blog.html',Context)

def contact_view(request):
  try:
    about = about_us.objects.get(logo__isnull=False)
    logo = about.logo
  except about_us.DoesNotExist:
    logo = None
  blogs=Blog.objects.all()
  slide = Slide.objects.get(id=3)


  Context={
   'blogs':blogs,'slides':slide,'logo':logo
  }
  return render(request,'contact.html',Context)

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse
import time
def contact_form(request):
  if request.method == 'POST':
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')
    print(name)
    print(email)
    print(message)

    # Send email
    send_mail(
      'Contact Form Submission',
      f'Name: {name}\nEmail: {email}\nMessage: {message}',
      settings.DEFAULT_FROM_EMAIL,
      [settings.DEFAULT_FROM_EMAIL,'consignsolution@gmail.com','bpn.dahal36@gmail.com','sauravrauniyar111@gmail.com'],
      fail_silently=False,
    )
    messagesucces = "Message sent successfully"

    return render(request,'contact.html',{'message':messagesucces })
  return render(request, 'contact.html')

def enquiry(request):
  return render(request,'enquiryform.html')


from django.db import models
from django.views import View
from django.http import HttpResponse
import json

# from .models import FormSubmission,Availability


class FormSubmissionView(View):
  def post(self, request, *args, **kwargs):
    # Process the form data
    form_data = request.POST.dict()
    availability_data = json.loads(form_data['availability'])
    del form_data['availability']
    print(form_data)

    # Create a new FormSubmission instance
    form_submission = FormSubmission.objects.create(**form_data)

    # Process and save the availability data
    for availability in availability_data:
      availability_obj = Availability.objects.create(
        day=availability['day'],
        morning=availability['morning'],
        noon=availability['noon'],
        night=availability['night'],
        customTimeSlot=availability['customTimeSlot']
      )
      form_submission.availabilities.add(availability_obj)

    # Return a success response
    return HttpResponse('success')

def form_submission_data(request):
    form_submissions = FormSubmission.objects.all()

    return render(request, 'vacancy_apply.html', {'form_submissions': form_submissions})


def servicedetails(request,id):
  services=Service.objects.get(id=id)
  context={
    'services':services
  }
  return render(request, 'servicedetails.html', context)