import json 
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token 
from django.views.decorators.csrf import csrf_exempt
from ..models import Provider, Client

@csrf_exempt
def register_provider(request): 
    req_body = json.loads(request.body.decode())

    new_user = User.objects.create_user( 
        username=req_body['username'],
        email=req_body['email'], 
        password=req_body['password'], 
        first_name=req_body['first_name'], 
        last_name=req_body['last_name'],
        is_staff=req_body['is_staff'] 
    )
    provider = Provider.objects.create(
        phone_number=req_body['phone_number'], 
        practice_name=req_body['practice_name'],
        practice_address=req_body['practice_address'], 
        provider_type_id=req_body['provider_type_id'],
        user=new_user
    )

    provider.save()
    # Creates association with token and user
    token = Token.objects.create(user=new_user)
    # Django way of converting to JSON
    data = json.dumps({"token": token.key})

    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def register_client(request): 
    req_body = json.loads(request.body.decode())

    new_user = User.objects.create_user( 
        username=req_body['username'],
        email=req_body['email'], 
        password=req_body['password'], 
        first_name=req_body['first_name'], 
        last_name=req_body['last_name'],
        is_staff=req_body['is_staff'] 
    )
    client = Client.objects.create(
        phone_number=req_body['phone_number'], 
        address=req_body['address'],
        birth_date=req_body['birth_date'], 
        height=req_body['height'],
        weight=req_body['weight'],
        user=new_user
    )

    client.save()
    # Creates association with token and user
    token = Token.objects.create(user=new_user)
    # Django way of converting to JSON
    data = json.dumps({"token": token.key})

    return HttpResponse(data, content_type='application/json')

@csrf_exempt
def login_provider(request): 
    req_body = json.loads(request.body.decode())

    if request.method == 'POST': 
        email = req_body['email']
        user_obj = User.objects.filter(email=email)
        username = user_obj[0]
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)
        # If the authenticated user already exists
        if authenticated_user is not None: 
            # Retrieve their token
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key, "provider_id": authenticated_user.provider.id})
            return HttpResponse(data, content_type="application/json")
        else: 
            data = json.dumps({"valid": False, 'request': req_body})
            return HttpResponse(data, content_type="application/json")
