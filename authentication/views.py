from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import User, APIKey, ServiceUsage
import json

def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            company = data.get('company', '')
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                company=company
            )
            
            # Create default API key
            APIKey.objects.create(
                user=user,
                name='Default API Key'
            )
            
            return JsonResponse({'message': 'User created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return render(request, 'auth/register.html')

def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({'message': 'Login successful'})
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return render(request, 'auth/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def manage_api_keys(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            
            api_key = APIKey.objects.create(
                user=request.user,
                name=name
            )
            
            return JsonResponse({
                'id': api_key.id,
                'name': api_key.name,
                'key': api_key.key,
                'created_at': api_key.created_at.isoformat()
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    api_keys = APIKey.objects.filter(user=request.user)
    return render(request, 'auth/api_keys.html', {'api_keys': api_keys})

@login_required
def profile(request):
    usage_stats = ServiceUsage.objects.filter(user=request.user)
    return render(request, 'auth/profile.html', {
        'user': request.user,
        'usage_stats': usage_stats
    })
