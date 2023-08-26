from django.db import models
from PIL import Image
import io
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.base import ContentFile


from PIL import Image,ImageOps
class Our_team(models.Model):
    Name = models.CharField(max_length=100)
    Role = models.CharField(max_length=50)
    image = models.ImageField(upload_to='projects')
    fb = models.CharField(max_length=200, null=True, blank=True)
    linkedin = models.CharField(max_length=100, null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Open the image using Pillow
        image = Image.open(self.image)

        # Get the dimensions of the original image
        width, height = image.size

        # Determine the desired size for cropping
        crop_size = min(width, height)

        # Calculate the coordinates for cropping the image
        left = (width - crop_size) // 2
        top = (height - crop_size) // 2
        right = left + crop_size
        bottom = top + crop_size

        # Crop the image
        cropped_image = image.crop((left, top, right, bottom))

        # Resize the cropped image to a desired size
        desired_size = (350, 350)
        cropped_image.thumbnail(desired_size, Image.ANTIALIAS)

        # Optimize the image to reduce file size
        optimized_image = ImageOps.exif_transpose(cropped_image)
        optimized_image.save(self.image.path, optimize=True)

        # Save the rest of the model
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Name;


class testimony(models.Model):

    name=models.CharField(max_length=100,null=True)
    comments = models.TextField(max_length=1000)


    def __str__(self):
        return self.name;


class Service(models.Model):
    project_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='projects')

    project_Description = models.TextField(max_length=2000)

    def __str__(self):
        return self.project_name;


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    publication_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='projects', null=True)
    is_published = models.BooleanField(default=False)
    published_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Publisher_image = models.ImageField(upload_to='projects', null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publication_date']


class Feature(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Package(models.Model):
    name = models.CharField(max_length=100)
    package_flaticon_icon_class = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    features = models.ManyToManyField(Feature)

    def __str__(self):
        return self.name


class Slide(models.Model):
    image_title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='carousel')
    def save(self, *args, **kwargs):
        # Open the original image using Pillow
        original_image = Image.open(self.image)

        # Optimize the image to reduce file size
        optimized_image = ImageOps.exif_transpose(original_image)

        # Create an in-memory file-like object to save the optimized image
        image_io = BytesIO()
        optimized_image.save(image_io, format='JPEG', optimize=True)

        # Create an InMemoryUploadedFile from the optimized image
        optimized_image_file = InMemoryUploadedFile(
            image_io,
            None,
            self.image.name,
            'image/jpeg',
            optimized_image.tell,
            None
        )

        # Save the optimized image to the image field
        self.image = optimized_image_file

        super().save(*args, **kwargs)

    def __str__(self):
        return self.image_title
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
import imghdr


def validate_svg(value):
    if value and hasattr(value.file, 'content_type') and value.file.content_type != 'image/svg+xml':
        raise ValidationError("Only SVG files are allowed.")


class SVGField(models.FileField):
    def __init__(self, *args, **kwargs):
        kwargs['upload_to'] = 'logo'  # Set the upload directory as per your requirements
        super().__init__(*args, **kwargs)

    def clean(self, value, *args, **kwargs):
        if value and hasattr(value, 'file') and not default_storage.exists(value.name):
            # New file uploaded or existing file changed, perform validation
            validate_svg(value)

        return super().clean(value, *args, **kwargs)

from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models

class about_us(models.Model):
    image = models.ImageField(upload_to='projects/carousel/', max_length=255, null=True)
    Company_name = models.CharField(max_length=100, null=True)
    logo = SVGField(null=True)
    Title = models.CharField(max_length=100, null=True)
    years_of_experience = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=1000, null=True)
    Total_projects = models.CharField(max_length=20, null=True)

    def save(self, *args, **kwargs):
        # Open the original image using Pillow
        original_image = Image.open(self.image)

        # Optimize the image to reduce file size
        optimized_image = ImageOps.exif_transpose(original_image)

        # Create an in-memory file-like object to save the optimized image
        image_io = BytesIO()
        optimized_image.save(image_io, format='JPEG', optimize=True)

        # Create an InMemoryUploadedFile from the optimized image
        optimized_image_file = InMemoryUploadedFile(
            image_io,
            None,
            self.image.name,
            'image/jpeg',
            optimized_image.tell,
            None
        )

        # Save the optimized image to the image field
        self.image = optimized_image_file

        super().save(*args, **kwargs)


    def __str__(self):
        return self.Company_name



class Appointment(models.Model):
    name = models.CharField(max_length=100)
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=20)
    services = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# class Availability(models.Model):
#     day = models.CharField(max_length=20)
#     morning = models.BooleanField(default=False)
#     noon = models.BooleanField(default=False)
#     night = models.BooleanField(default=False)
#     custom_time_slot = models.CharField(max_length=100, blank=True)
#
# class FormSubmission(models.Model):
#     firstname = models.CharField(max_length=50)
#     lastname = models.CharField(max_length=50)
#     contact = models.CharField(max_length=50)
#     email = models.EmailField()
#     country = models.CharField(max_length=50)
#     city = models.CharField(max_length=50)
#     birthdate = models.DateField(blank=True, null=True)
#     passportnumber = models.CharField(max_length=50)
#     TFN = models.CharField(max_length=50)
#     policeChecks = models.CharField(max_length=10)
#     wwcc = models.CharField(max_length=10)
#     covidVaccination = models.CharField(max_length=20, choices=[("firstDose", "First Dose"), ("secondDose", "Second Dose")], blank=True)
#     account_holder_name = models.CharField(max_length=50)
#     bsbnumber = models.CharField(max_length=20)
#     accountnumber = models.CharField(max_length=50)
#     emergency_contact_person = models.CharField(max_length=50)
#     emergency_contact_number = models.CharField(max_length=50)
#     availability = models.ManyToManyField(Availability)
#
#     def __str__(self):
#         return f"{self.firstname} {self.lastname}"


from django.core.files.base import ContentFile


import io



class Availability(models.Model):
    day = models.CharField(max_length=20)
    morning = models.BooleanField(default=False)
    noon = models.BooleanField(default=False)
    night = models.BooleanField(default=False)
    customTimeSlot = models.CharField(max_length=100, blank=True)
    def __str__(self):
        return self.day



class FormSubmission(models.Model):
    firstname = models.CharField(max_length=100,null=True)
    lastname = models.CharField(max_length=100,null=True)
    contact = models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True)
    country = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100,null=True)
    birthdate = models.DateField(blank=True, null=True)
    passportnumber = models.CharField(max_length=100, blank=True)
    TFN = models.CharField(max_length=100, blank=True)
    account_holder_name = models.CharField(max_length=100, blank=True)
    bsb_number = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=100, blank=True)
    emergency_contact_person = models.CharField(max_length=100, blank=True)
    emergency_contact_number = models.CharField(max_length=100, blank=True)
    wwcc = models.CharField(max_length=100, blank=True)
    wwccnumber=models.CharField(max_length=100,null=True)
    policeChecks=models.CharField(max_length=100, blank=True)
    policeChecksnumber=models.CharField(max_length=100,null=True)
    covidVaccination=models.CharField(max_length=200,null=True)
    availabilities = models.ManyToManyField(Availability)
    def __str__(self):
        return self.firstname

from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils import six
# class TokenGenerator(PasswordResetTokenGenerator):
#     def _make_hash_value(self, user, timestamp):
#         return (
#             six.text_type(user.pk) + six.text_type(timestamp) +
#             six.text_type(user.is_active)
#         )
# account_activation_token = TokenGenerator()

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')