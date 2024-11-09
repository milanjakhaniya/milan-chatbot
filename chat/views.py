import json
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from chat.tasks import process_message
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from chat.models import Message
from django.contrib.auth.decorators import login_required

###################################################################################
def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass1']

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password")
            return redirect('Login')

        else:
            login(request,user)
            return redirect('chatbot')
        
    return render(request, 'login.html')

def Logout(request):
    logout(request)
    messages.success(request, "You have successfully signed out")
    return redirect('Login')

##############################################################################################

@login_required
@csrf_exempt
def process_user_input(request):
    if request.method == 'POST':
        try:
            
            data = json.loads(request.body)
            user_message = data.get('user_message', '')
            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)

            user = User.objects.get(id=request.user.id)
            
            task = process_message.apply_async(args=[user_message])
            bot_response = task.id
            messagesData = Message(
                query=user_message,
                task_id=bot_response,
                user=user,
                created_by=user,
                last_modified_by=user
                )
            messagesData.save()
            
            return JsonResponse({'task_id': bot_response})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
@csrf_exempt  
def fetch_response_by_task_id(request, task_id):
    if request.method == 'GET':
        try:
            
            if not task_id:
                return JsonResponse({'error': 'Task ID not provided'}, status=400)
            
            task = process_message.AsyncResult(task_id)
            
            queryResponse = task.get()  
            user = User.objects.get(id=request.user.id)
            print('.........GET ', user)
            messagesData = Message.objects.get(task_id=task_id)
            messagesData.query_response = queryResponse
            messagesData.last_modified_by = user
            messagesData.save()                
            
            bot_response = {
                    "user_name": user.username.capitalize(),
                    "query_response": queryResponse,
                }
            return JsonResponse({'bot_response': bot_response})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
@csrf_exempt
def fetch_all_messages(request):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=request.user.id)
            print('.........', user)
            messagesData = Message.objects.filter(user=user)
            
            responseMessages = []
            for message in messagesData:
                responseMessages.append({
                    "user_name": user.username.capitalize(),
                    "query": message.query,
                    "query_response": message.query_response,
                })
            
            return JsonResponse({'messages': responseMessages})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def chatbot(request):

    return render(request, 'chatbot.html')
