from django.shortcuts import render
from uploader.models import UploadForm, Upload, User, AuthForm, Cdn, Machines, Machinetype, Cloud, Flavors, content_file_name, Node_Info
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Sum
import os, time, moviepy
from moviepy.editor import VideoFileClip, concatenate
from django.contrib import messages
import cv2
import re
#from RequestTranscode import RequestTranscode



# Create your views here.
def addvideo(request):
    request.session.set_expiry(2000)
    if request.session.get('user_auth') == 'yes':
        total_minus_used=[]
        video_types = ['240p', '360p', '720p', '1080p', '4k']
        resolutions =''
        storing_resolution=['144p']

        getting_IDCloud_Comparison=Node_Info.objects.all().filter(Machine_Type='Coordinator')
        for f in getting_IDCloud_Comparison:
            idcloud_coordinator = f.IDCloud


        getting_machine_types=[]
        vm_type_amount = [0,0,0,0]
        getting_region_continents=[]
        getting_total_storage_machines=[]
        getting_used_storage_machines=[]
        getting_total_storage=[]
        getting_used_storage=[]
        total_used_storage=[0]
        total_machines_storage=[0]
        available_storage_machine=[]
        getting_transcoder_choice=[]
        getting_streamer_choice=[]


        getting_total_capacities=[]
        getting_regions_choice=[]
        vm_region_continent_amount = [0,0,0,0,0,0]
        cm_region_continent_total_storage = [0,0,0,0,0,0]

        if True:
            getting_machine_details=Node_Info.objects.all()
            for e in getting_machine_details:

                if str(e.Machine_Type)=='Cache':
                    vm_type_amount[0] +=1
                    size = os.popen('echo "Hassaan47" | sudo -S ssh -i /home/hassaan/Aalto_AmazonAWS_KeyPair.pem ubuntu@' + str(e.Public_IP) + ' "df -B MB /dev/xvda1"').read()
                    available = re.split('.*?([0-9][0-9]+MB)+', size)[5]
                    available_storage_machine.append(round(float(available[0:len(available)-2])/1024, 2))
                    getting_regions_choice.append(e.Machine_Name)
                if str(e.Machine_Type)=='Streamer':
                    getting_streamer_choice.append(e.Machine_Name)
                if str(e.Machine_Type)=='Transcoder':
                    getting_transcoder_choice.append(e.Machine_Name)
################################################

        regions_list=getting_regions_choice
####################################################


        if request.method=="POST":
            img = UploadForm(request.POST, request.FILES) 
            if img.is_valid():
                imgfile = Upload(pic=request.FILES['pic'])
                imgfile.Size = imgfile.pic.size
                imgfile.Video_Name = request.POST['Video_Name']
                imgfile.Author = request.POST['Author']
                imgfile.Region = request.POST['Region']
                imgfile.Streamer_IP = request.POST['Streamer']
                imgfile.Transcoder_IP = request.POST['Transcoder']
                imgfile.Qualities = request.POST.getlist('resolutions')
                resolution_for_transcoder=imgfile.Qualities

                getting_IP_Address=Node_Info.objects.all().filter(Machine_Name=imgfile.Region)
                for m in getting_IP_Address:
                    ip_vm_to_upload_video = str(m.Public_IP)
                imgfile.location=[ip_vm_to_upload_video]


                getting_IP_Address=Node_Info.objects.all().filter(Machine_Name=imgfile.Region)
                for m in getting_IP_Address:
                    if (int(m.IDCloud)==int(idcloud_coordinator)):
                        ip_vm_to_upload_video = str(m.Private_IP)
                    else:
                        ip_vm_to_upload_video = str(m.Public_IP)
                imgfile.Cache_IP=ip_vm_to_upload_video


                getting_IP_Address=Node_Info.objects.all().filter(Machine_Name=imgfile.Streamer_IP)
                for m in getting_IP_Address:
                    if (int(m.IDCloud)==int(idcloud_coordinator)):
                        ip_vm_to_upload_video = str(m.Private_IP)
                    else:
                        ip_vm_to_upload_video = str(m.Public_IP)
                imgfile.Streamer_IP = ip_vm_to_upload_video


                getting_IP_Address=Node_Info.objects.all().filter(Machine_Name=imgfile.Transcoder_IP)
                for m in getting_IP_Address:
                    if (int(m.IDCloud)==int(idcloud_coordinator)):
                        ip_vm_to_upload_video = str(m.Private_IP)
                    else:
                        ip_vm_to_upload_video = str(m.Public_IP)
                imgfile.Transcoder_IP = ip_vm_to_upload_video
                

                for i in range (0,len(imgfile.Qualities)):
                    storing_resolution.append(str(imgfile.Qualities[i][0:len(imgfile.Qualities[i])-1]))
                imgfile.Qualities=storing_resolution
                print 'hassaan'
                print imgfile.Qualities
                for x in range (0,len(regions_list)):
                    if str(regions_list[x])==str(imgfile.Region):
                        if float(available_storage_machine[x]*1073741824)>float(imgfile.Size):
                            imgfile.save()
                            name=content_file_name(imgfile, request.POST['Video_Name'])
                            vc = cv2.VideoCapture(imgfile.pic.path)
                            if vc.isOpened():
                                rval , frame = vc.read()
                            else:
                                rval = False
                            rval, frame = vc.read()
                            cv2.imwrite(imgfile.pic.path +'.jpg',frame)
                            cv2.waitKey(1)
                            vc.release()
                            with open(imgfile.pic.path +'.jpg', 'rb') as p:
                                img = p.read()
                                imgfile.image = img
                                imgfile.save()

                        else:
                            messages.add_message(request, messages.ERROR, 'Oooppsssss, Format Mismatch')
                for i in range (0,len(imgfile.Qualities)):
                    resolutions += str(imgfile.Qualities[i]) + ','
                resolutions = resolutions[0:len(resolutions)-1]
                print resolutions
              #  RTX = RequestTranscode(imgfile.Transcoder_IP)
              #  RTX.sendMessage(imgfile.Cache_IP, imgfile.pic , imgfile.Qualities)
                return HttpResponseRedirect('../list_videos')
        else:
            img=UploadForm()
        images=Upload.objects.all()
        sending = zip(getting_regions_choice,available_storage_machine) 
        return render(request,'addvideo.html',{'form':img,'images':images, 'regions':sending, 'types':video_types, 'streamer_list':getting_streamer_choice, 'transcoder_list':getting_transcoder_choice})
    return HttpResponseRedirect('../login')





def list_videos(request):
    request.session.set_expiry(2000)
    os.system("echo 'Hassaan47' | sudo -S umount -f /home/hassaan/sample/media")
    try:
        if request.session.get('user_auth') == 'yes':
            if request.method=="POST":
                return HttpResponseRedirect(request)
            else:
                img=UploadForm()
            images=Upload.objects.all()
            messages.add_message(request, messages.INFO, 'Hello world.')
            return render(request,'list_videos.html',{'form':img,'images':images})
        return HttpResponseRedirect('../login')
    except:
        return HttpResponseRedirect('../login')


def streamer(request):
    request.session.set_expiry(2000)
    os.system("echo 'Hassaan47' | sudo -S umount -f /home/hassaan/sample/media")
    try:
        if True:
            if request.method=="POST":
                return HttpResponseRedirect(request)
            else:
                img=UploadForm()
            images=Upload.objects.all()
            messages.add_message(request, messages.INFO, 'Hello world.')
            return render(request,'streamer.html',{'form':img,'images':images})
        return HttpResponseRedirect('../login')
    except:
        return HttpResponseRedirect('../login')




def cache(request):
    request.session.set_expiry(2000)
    try:
        if request.session.get('user_auth') == 'yes':
            if request.method=="POST":
                return HttpResponseRedirect(request)
            else:
                img=UploadForm()
            images=Upload.objects.all()
            return render(request,'cache.html',{'form':img,'images':images})
        return HttpResponseRedirect('../login')
    except:
        return HttpResponseRedirect('../login')




def listoriginal(request,file2delete,id2delete):
    request.session.set_expiry(2000)
    try:
        getting_region_of_video=Upload.objects.all().filter(id=int(id2delete))
        for y in getting_region_of_video:
            region_of_video = str(y.Region)

        getting_IP_Address=Node_Info.objects.all().filter(Machine_Name=region_of_video)
        for m in getting_IP_Address:
            ip_vm_to_upload_video = str(m.Public_IP)
        #ip_vm_to_upload_video = 'hassaan'#ip_vm_to_upload_video='10.0.0.53' #[showing1][ip_vm_to_upload_video] #
        checking ="echo 'Hassaan47' | sudo -S sshfs -o allow_other,IdentityFile=/home/hassaan/Aalto_AmazonAWS_KeyPair.pem ubuntu@" + ip_vm_to_upload_video  + ":/var/CDN/input /home/hassaan/sample/media -o nonempty" 
        os.system(checking)
        time.sleep(0.5)
        os.remove(os.path.join('media', file2delete))
        os.remove(os.path.join('media', file2delete + '.jpg'))
        aaa = Upload.objects.get(id=id2delete)
	aaa.delete()
        time.sleep(0.2)
    except:
	pass
    aaa=0
    return HttpResponseRedirect(reverse('list_videos')) #redirect('uploader.views.list_videos')





def main(request):
        request.session.set_expiry(2000)
    #try:
        if request.session.get('user_auth') == 'yes':
            getting_machine_types=[]
            vm_type_amount = [0,0,0,0]
            getting_region_continents=[]
            getting_total_storage_machines=[]
            getting_used_storage_machines=[]
            getting_total_storage=[]
            getting_used_storage=[]
            total_used_storage=[0]
            total_machines_storage=[0]


            getting_total_capacities=[]
            getting_regions_choice=[]
            vm_region_continent_amount = [0,0,0,0,0,0]
            cm_region_continent_total_storage = [0,0,0,0,0,0]

            if True:
                getting_machine_details=Node_Info.objects.all()
                for e in getting_machine_details:
                    if str(e.Machine_Type)=='Cache':
                        vm_type_amount[0] +=1
                        size = os.popen('echo "Hassaan47" | sudo -S ssh -i /home/hassaan/Aalto_AmazonAWS_KeyPair.pem ubuntu@' + str(e.Public_IP) + ' "df -B MB /dev/xvda1"').read()
                        total = re.split('.*?([0-9][0-9]+MB)+', size)[1]
                        used = re.split('.*?([0-9][0-9]+MB)+', size)[3]
                        getting_total_storage_machines.append(round(float(total[0:len(total)-2])/1024, 2))
                        total_machines_storage[0] += round(float(total[0:len(total)-2])/1024 , 2)
                        getting_used_storage_machines.append(round(float(used[0:len(used)-2])/1024,2))
                        total_used_storage[0] += round(float(used[0:len(used)-2])/1024 , 2)
                    if str(e.Machine_Type)=='Coordinator':
                        vm_type_amount[1] +=1
                    if str(e.Machine_Type)=='Streamer':
                        vm_type_amount[2] +=1
                    if str(e.Machine_Type)=='Transcoder':
                        vm_type_amount[3] +=1

################################################

                    getting_region_continents.append(str(e.Continent))
    
                    if str(e.Continent) == 'Europe':
                        vm_region_continent_amount[0] +=1
                    elif str(e.Continent) == 'Asia':
                        vm_region_continent_amount[1] +=1
                    elif str(e.Continent) == 'Africa':
                        vm_region_continent_amount[2] +=1
                    elif str(e.Continent) == 'America':
                        vm_region_continent_amount[3] +=1
                    elif str(e.Continent) == 'Australia':
                        vm_region_continent_amount[4] +=1
                    elif str(e.Continent) == 'Antarctica':
                        vm_region_continent_amount[5] +=1
                    else:
                        pass
                    request.session['regionsofmachines'] = vm_region_continent_amount

################################################
                    if e.Machine_Type == 'Cache':
                        getting_regions_choice.append(e.Machine_Name)
        
                    request.session['user_totalstorage'] = getting_total_storage_machines
                    request.session['region_choices'] = getting_regions_choice
####################################################
                request.session['total_storage_capacities'] = getting_total_storage_machines
                request.session['typesofmachines'] = vm_type_amount
                request.session['total_vms'] = vm_type_amount[0] + vm_type_amount[1] + vm_type_amount[2] + vm_type_amount[3]    

                totalsending = zip(request.session.get('region_choices'), getting_total_storage_machines,  getting_used_storage_machines)
                return render(request,'main.html', {'user':request.session.get('typesofmachines'), 'locations':request.session.get('regionsofmachines'), 'total_vm':request.session.get('total_vms'), 'totalusage':total_machines_storage, 'total_used_space':total_used_storage, 'machine_details': totalsending})
        return HttpResponseRedirect('../login')
  #  except:
        return HttpResponseRedirect('../login')





def cdndatabase(request):
    request.session.set_expiry(2000)
    getting_UserID=User.objects.using('userstats').all().filter(UserName='mohsinm1')
    for a in getting_UserID:
        IDUser_current = a.IDUser
        getting_IDCDN=Cdn.objects.using('userstats').all().filter(IDUser=IDUser_current)
        showing=''
        for b in getting_IDCDN:
            showing1 = str(b.IDCDN)
            showing += showing1 + ','
        return render(request,'cdndatabase.html', {'user':request.session.get('typesofmachines'), 'locations':request.session.get('regionsofmachines')})





def login(request):
    try:
        if (request.session['user_auth'] != 'yes'):
            return render(request,'login.html')
        else:
            return HttpResponseRedirect('../')
    except:
        return render(request,'login.html')



def loginfailed(request):
    try:
        if (request.session['user_auth'] != 'yes'):
            return render(request,'loginfailed.html')
        else:
            return HttpResponseRedirect('../')
    except:
        return render(request,'loginfailed.html')




def verify(request):
    request.session.set_expiry(2000)
    username = request.POST['username']
    password = request.POST['password']
    user_valid=User.objects.all().filter(login=username, password=password)

    if len(user_valid)>0:
        request.session['user_auth'] = 'yes'
        return HttpResponseRedirect('../') #render(request,'list.html')
    return render(request,'loginfailed.html')





def logout(request):
    request.session['user_auth'] = 'no'
    request.session['user_id'] = ''
    request.session['user_totalstorage'] = ''
    request.session['regionsofmachines'] = ''
    request.session['typesofmachines'] = ''
    request.session['total_vms'] = '' 
    return HttpResponseRedirect('../list_videos')

