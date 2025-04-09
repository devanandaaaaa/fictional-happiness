from django.shortcuts import render, redirect
from .forms import ResumeForm,RegisterForm
from .models import Resume
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'resumesite/index.html')

@login_required
def resume_form(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES) 
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return render(request, 'resumesite/success.html', {'resume': resume}) 
        else:
            print(form.errors) 
    else:
        form = ResumeForm()
    return render(request, 'resumesite/resume_form.html', {'form': form})

def success(request):
    return render(request, 'resumesite/success.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'resumesite/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'resumesite/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def export_pdf(request, pk):
    resume = Resume.objects.get(pk=pk)
    template = get_template('resumesite/resume_pdf.html')
    html = template.render({'resume': resume})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="{resume.full_name}_resume.pdf"'
    pisa.CreatePDF(html, dest=response)
    return response

def resume_public(request, public_id):
    resume = Resume.objects.get(public_id=public_id)
    return render(request, 'resumesite/resume_public.html', {'resume': resume})

def success(request):
    return render(request, 'resumesite/success.html')
