from django.db import models
from django.forms import ModelForm
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from validatedfile.fields import ValidatedFileField
from django.core.exceptions import ValidationError
from django.contrib import messages
import ftplib, os, time, moviepy
from moviepy.editor import VideoFileClip
import base64


def content_file_name(instance, filename):
    ip_to_use1 = "10.0.0.53"
    ip_to_use = str(instance.location)
    #checking ="echo 'aaltofi123' | sshfs root@" + ip_to_use + ":/home /home/hassaan/sample/media -o workaround=rename -o password_stdin -o nonempty" 
    checking ="echo 'Hassaan47' | sudo -S sshfs -o allow_other,IdentityFile=/home/hassaan/Aalto_AmazonAWS_KeyPair.pem ubuntu@" + ip_to_use + ":/var/CDN/input /home/hassaan/sample/media -o nonempty" 
    os.system(checking)
    time.sleep(1)
    return '/'.join([filename])



class Upload(models.Model):

    def validate_file_extension(value):
        ext = os.path.splitext(value.name)[1]
        valid_extensions = ['.mp4', '.mkv', '.flv', '.mpeg', '.mp2', '.avi', '.vob', '.wmv', '.mpg', '.3gp', '.avchd', '.swf']
        if not ext in valid_extensions:
            raise ValidationError(u'File not supported!')

    Video_Name = models.TextField(max_length=100, db_column="Video_Name")
    Author = models.TextField(max_length=100, db_column="Author")
    pic = models.FileField("Image", upload_to=content_file_name, validators=[validate_file_extension])
    os.system("echo 'Hassaan47' | sudo -S umount -f /home/hassaan/sample/media")             #fusermount -u /home/hassaan/sample/media")
    upload_date=models.DateTimeField(auto_now_add =True)
    Size = models.IntegerField(db_column="Size")
    Region = models.CharField(max_length=100)
    Qualities = models.CharField(max_length=100)
    Transcoder_IP = models.CharField(max_length=256)
    Streamer_IP = models.CharField(max_length=256)
    Cache_IP = models.CharField(max_length=256)


    _image = models.TextField(
            db_column='image',
            blank=True)

    def set_image(self, image):
        self._image = base64.encodestring(image)

    def get_image(self):
        return self._image

    image = property(get_image, set_image)


# FileUpload form class.
class UploadForm(ModelForm):
    class Meta:
        model = Upload
        fields = ['Video_Name', 'Author', 'pic']



class User(models.Model):
    login =models.CharField(max_length=200, db_column="login")
    password =models.CharField(max_length=200, db_column="password")
    class Meta:
        db_table='user'



class AuthForm(ModelForm):
    class Meta:
        model = User
	fields = "__all__" 



class Cdn(models.Model):
    IDCDN =models.IntegerField(db_column="IDCDN", primary_key=True)
    IDUser =models.IntegerField(db_column="IDUser", primary_key=True)
    class Meta:
        db_table='cdn'



class Machines(models.Model):
    MachineUUID =models.CharField(db_column="MachineUUID", max_length=128, primary_key=True)
    MachineImageID =models.CharField(db_column="MachineImageID", max_length=256)
    MachineName =models.CharField(db_column="MachineName", max_length=256)
    MachineFlavorID =models.CharField(db_column="MachineFlavorID", max_length=256)
    IDCDN =models.IntegerField(db_column="IDCDN")
    IDCloud =models.IntegerField(db_column="IDCloud")
    Deleted =models.IntegerField(db_column="Deleted")
    MachinePublic_IP =models.CharField(db_column="MachinePublic_IP", max_length=256)
    class Meta:
        db_table='machines'



class Machinetype(models.Model):
    MachineImageID =models.CharField(db_column="MachineImageID", max_length=128, primary_key=True)
    TypeName =models.CharField(db_column="TypeName", max_length=256)
    class Meta:
        db_table='machinetype'



class Cloud(models.Model):
    IDCloud =models.IntegerField(db_column="IDCloud", primary_key=True)
    Continent =models.CharField(db_column="Continent", max_length=256)
    Country =models.CharField(db_column="Country", max_length=256)
    class Meta:
        db_table='cloud'



class Flavors(models.Model):
    FlavorID =models.CharField(db_column="FlavorID", max_length=128, primary_key=True)
    FlavorDisk =models.IntegerField(db_column="FlavorDisk")
    IDCloud =models.IntegerField(db_column="IDCloud")
    class Meta:
        db_table='flavors'



class Node_Info(models.Model):
    Machine_Name =models.CharField(db_column="Machine_Name", max_length=256)
    Machine_Type =models.CharField(db_column="Machine_Type", max_length=256)
    Public_IP =models.CharField(db_column="Public_IP", max_length=256)
    Private_IP =models.CharField(db_column="Private_IP", max_length=256)
    Continent =models.CharField(db_column="Continent", max_length=256)
    IDCloud =models.IntegerField(db_column="IDCloud")
    class Meta:
        db_table='Node_Info'










 
