from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from .models import PosterDetail
from django.conf import settings
from PIL import Image,ImageOps,ImageDraw,ImageFont
import io
import os
from django.contrib import messages

# Create your views here.

class PosterForm(forms.ModelForm):
    class Meta:
        model = PosterDetail
        fields = "__all__"
        labels = {
            'first': 'First Name',
            'last': 'Last Name',
            'img': 'Upload Image'
        }
        widgets = {
            'first': forms.TextInput(attrs={
                'placeholder': 'Enter your first name',
                'class': 'form-control'
            }),
            'last': forms.TextInput(attrs={
                'placeholder': 'Enter your last name',
                'class': 'form-control'
            }),
            'img': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    

def makeposter(request):
    if request.method == "POST":
        form = PosterForm(request.POST,request.FILES)
        if form.is_valid():
            print("valid")
            img = form.cleaned_data["img"]
            template_path = os.path.join(settings.BASE_DIR, 'myenv', 'static','myenv','1.png')

            posterim = Image.open(template_path)
            userim = Image.open(img)
            target_size = (700, 700)

            r = ImageOps.cover(userim,target_size)
            posterim.paste(r,(50,625))
            imfortext = ImageDraw.Draw(posterim)
            font = ImageFont.truetype("verdana.ttf", 80)
            first = form.cleaned_data["first"]
            last = form.cleaned_data["last"]
            imfortext.text((1180,748),first,font=font)
            imfortext.text((1180,840),last,font=font)
            
            tempdir = os.path.join(settings.BASE_DIR, 'myenv', 'temp','poster.png')
            posterim.save(tempdir)

            with open(tempdir, 'rb') as file:
                response = HttpResponse(file.read(), content_type='image/png')
                response['Content-Disposition'] = 'attachment; filename=poster.png'
            
            messages.success(request,"Poster is Downloaded")

            os.remove(tempdir)

            return response
            
        
        else:
            print(form.errors)
    else:
        form = PosterForm()
    
    ctx = {"form":form}
    
    return render(request,"myenv/poster.html",context=ctx)