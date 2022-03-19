from datetime import date
from django.db.models import fields

from django.http.response import JsonResponse
from Authentication.views import verify_jwt_token_local
from Authentication.models import OrgAccount
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from backend.settings import *
import json
import jwt
from backend import error_codes
from .models import *
from django.core import serializers

def index(request):
    return HttpResponse('Home page')
def __get_email_from_token(token):
    return ((jwt.decode(token,SECRET_KEY,algorithm="HS256"))['id'])

@csrf_exempt
def create_campaign(request):
    if(request.method=="POST"):

        try:
            data = json.loads(request.body.decode('utf-8'))
            print(data)
            token = request.headers['Authorization']
            print(token)

            if(not verify_jwt_token_local(token)):
                HttpResponse.status_code=int(error_codes.invalid_jwt_token())
                return HttpResponse("Invalid jwt token")
            
            email=__get_email_from_token(token)

            try:
                org_account = OrgAccount.objects.get(email=email)
            except OrgAccount.DoesNotExist as e:
                HttpResponse.status_code=int(error_codes.bad_request())
                return HttpResponse('Access denied')
            location=data.get('location')
            skills=data.get('skills')
            date=data.get('date')
            time=data.get('time')
            description=data.get('description')
            title=data.get('title')
            duration=int(data.get('duration'))
            volunteer_count=int(data.get('volunteer_count'))
            minimum_age=int(data.get('minimum_age'))
            new_campaign = Campaign(organisation_email=email,location=location,skills=skills,date=date,time=time,description=description,title=title,duration=duration,volunteer_count=volunteer_count,minimum_age=minimum_age)
            new_campaign.save()
            HttpResponse.status_code=int(error_codes.api_success())
            return HttpResponse('Campaign Created')
        
        except Exception as e:
            HttpResponse.status_code = int(error_codes.bad_request())
            return HttpResponse('Deserialisation error '+str(e))
    
    else:
        HttpResponse.status_code = int(error_codes.bad_request())
        return HttpResponse('404 error')

@csrf_exempt
def update_org_details(request):
    if(request.method=="POST"):
    
        try:
            data = json.loads(request.body.decode('utf-8'))
            token = request.headers['Authorization']

            if(not verify_jwt_token_local(token)):
                HttpResponse.status_code=int(error_codes.invalid_jwt_token())
                return HttpResponse("Invalid jwt token")
            
            email=__get_email_from_token(token)
            try:
                org_account = OrgAccount.objects.get(email=email)
            except OrgAccount.DoesNotExist as e:
                HttpResponse.status_code=int(error_codes.bad_request())
                return HttpResponse('Access denied')
            
            name=data.get('name')
            address=data.get('address')
            org_account.name=name
            org_account.address=address
            org_account.save()
            HttpResponse.status_code=int(error_codes.api_success())
            return HttpResponse('Details Changed')
        
        except Exception as e:
            HttpResponse.status_code = int(error_codes.bad_request())
            return HttpResponse('Deserialisation error '+str(e))

    else:
        HttpResponse.status_code = int(error_codes.bad_request())
        return HttpResponse('404 error')

@csrf_exempt
def update_campaign_details(request):

    if(request.method=="POST"):
        
        try:
            data = json.loads(request.body.decode('utf-8'))
            token = request.headers['Authorization']

            if(not verify_jwt_token_local(token)):
                HttpResponse.status_code=int(error_codes.invalid_jwt_token())
                return HttpResponse("Invalid jwt token")
            
            email=__get_email_from_token(token)

            try:
                org_account = OrgAccount.objects.get(email=email)
            except OrgAccount.DoesNotExist as e:
                HttpResponse.status_code=int(error_codes.bad_request())
                return HttpResponse('Access denied')
            
            campaign_id=data.get('campaign_id')

            try:
                campaign=Campaign.objects.get(campaign_id=campaign_id)
            
            except Campaign.DoesNotExist as e:
                HttpResponse.status_code=int(error_codes.invalid_campaign())
                return HttpResponse('Invalid Campaign')
            
            if(campaign.organisation_email != email):
                HttpResponse.status_code=int(error_codes.bad_request())
                return HttpResponse('Access denied')
            
            campaign.location=data.get('location')
            campaign.skills=data.get('skills')
            campaign.date=data.get('date')
            campaign.time=data.get('time')
            campaign.description=data.get('description')
            campaign.title=data.get('title')
            campaign.duration=data.get('duration')
            campaign.volunteer_count=data.get('volunteer_count')
            campaign.minimum_age=data.get('minimum_age')
            campaign.save()
            HttpResponse.status_code=int(error_codes.api_success())
            return HttpResponse('Campaign Updated')

        except Exception as e:
            HttpResponse.status_code = int(error_codes.bad_request())
            return HttpResponse('Deserialisation error '+str(e))

    else:
        HttpResponse.status_code = int(error_codes.bad_request())
        return HttpResponse('404 error')

@csrf_exempt
def get_all_campaign_details_for_org(request):
    if(request.method=="GET"):
        
        try:
            token = request.headers['Authorization']

            if(not verify_jwt_token_local(token)):
                HttpResponse.status_code=int(error_codes.invalid_jwt_token())
                return HttpResponse("Invalid jwt token")
            
            email=__get_email_from_token(token)

            try:
                org_account = OrgAccount.objects.get(email=email)
            except OrgAccount.DoesNotExist as e:
                HttpResponse.status_code=int(error_codes.bad_request())
                return HttpResponse('Access denied')
            
            all_campaigns_of_current_org = Campaign.objects.filter(organisation_email=email)
            JsonResponse.status_code=int(error_codes.api_success())
            serialized_campaign_data = serializers.serialize('json',all_campaigns_of_current_org,fields=('campaign_id','organisation_email','location','skills','date','time','description','title','duration','volunteer_count','minimum_age','status'))
            return JsonResponse(serialized_campaign_data,safe=False)
            
        except Exception as e:
            HttpResponse.status_code = int(error_codes.bad_request())
            return HttpResponse('Deserialisation error '+str(e))

    else:
        HttpResponse.status_code = int(error_codes.bad_request())
        return HttpResponse('404 error')

@csrf_exempt
def get_all_past_campaign_details_for_org(request):
    if(request.method=="GET"):
        
        try:
            token = request.headers['Authorization']

            if(not verify_jwt_token_local(token)):
                HttpResponse.status_code=int(error_codes.invalid_jwt_token())
                return HttpResponse("Invalid jwt token")
            
            email=__get_email_from_token(token)
            
            try:
                org_account = OrgAccount.objects.get(email=email)
            except OrgAccount.DoesNotExist as e:
                HttpResponse.status_code=int(error_codes.bad_request())
                return HttpResponse('Access denied')
            
            all_campaigns_of_current_org = Campaign.objects.filter(organisation_email=email,status='C')
            all_campaigns_completed_but_not_updates = Campaign.objects.filter(organisation_email_email=email,status='U')

            #TODO : Test this
            for element in all_campaigns_completed_but_not_updates.iterator():
                if(element.get('time')<datetime.now):
                    element.status='C'
                    element.save()
            JsonResponse.status_code=int(error_codes.api_success())
            serialized_campaign_data = serializers.serialize('json',all_campaigns_of_current_org,fields=('campaign_id','organisation_email','location','skills','date','time','description','title','duration','volunteer_count','minimum_age'))
            return JsonResponse(serialized_campaign_data,safe=False)
            
        except Exception as e:
            HttpResponse.status_code = int(error_codes.bad_request())
            return HttpResponse('Deserialisation error '+str(e))

    else:
        HttpResponse.status_code = int(error_codes.bad_request())
        return HttpResponse('404 error')

@csrf_exempt
def get_all_upcoming_campaign_details_for_org(request):
    if(request.method=="GET"):
        
        try:
            token = request.headers['Authorization']

            if(not verify_jwt_token_local(token)):
                HttpResponse.status_code=int(error_codes.invalid_jwt_token())
                return HttpResponse("Invalid jwt token")
            
            email=__get_email_from_token(token)
            
            try:
                org_account = OrgAccount.objects.get(email=email)
            except OrgAccount.DoesNotExist as e:
                HttpResponse.status_code=int(error_codes.bad_request())
                return HttpResponse('Access denied')
            
            all_campaigns_of_current_org = Campaign.objects.filter(organisation_email=email,status='U')
            JsonResponse.status_code=int(error_codes.api_success())
            serialized_campaign_data = serializers.serialize('json',all_campaigns_of_current_org,fields=('campaign_id','organisation_email','location','skills','date','time','description','title','duration','volunteer_count','minimum_age'))
            return JsonResponse(serialized_campaign_data,safe=False)
            
        except Exception as e:
            HttpResponse.status_code = int(error_codes.bad_request())
            return HttpResponse('Deserialisation error '+str(e))

    else:
        HttpResponse.status_code = int(error_codes.bad_request())
        return HttpResponse('404 error')
        
@csrf_exempt
def delete_org_account(request):
    pass

@csrf_exempt
def view_org_notifs(request):
    if(request.method=="GET"):
        
        try:
            token = request.headers['Authorization']

            if(not verify_jwt_token_local(token)):
                HttpResponse.status_code=int(error_codes.invalid_jwt_token())
                return HttpResponse("Invalid jwt token")
            
            email=__get_email_from_token(token)
            
            try:
                org_account = OrgAccount.objects.get(email=email)
            except OrgAccount.DoesNotExist as e:
                HttpResponse.status_code=int(error_codes.bad_request())
                return HttpResponse('Access denied')
            org_id=OrgAccount.objects.get(email=email)
            notifs_for_current_org=OrgNotif.objects.filter(org_id=org_id)
            JsonResponse.status_code=int(error_codes.api_success())
            serialized_notif_data = serializers.serialize('json',notifs_for_current_org,fields=('campaign_id','user_id','status'))
            return JsonResponse(serialized_notif_data,safe=False)
        
        except Exception as e:
            HttpResponse.status_code = int(error_codes.bad_request())
            return HttpResponse('Deserialisation error '+str(e))

    else:
        HttpResponse.status_code = int(error_codes.bad_request())
        return HttpResponse('404 error')

@csrf_exempt
def approve_or_reject_user_campaign_registration(request):
    if(request.method=="POST"):
        
        try:
            data = json.loads(request.body.decode('utf-8'))
            token = request.headers['Authorization']

            if(not verify_jwt_token_local(token)):
                HttpResponse.status_code=int(error_codes.invalid_jwt_token())
                return HttpResponse("Invalid jwt token")
            
            email=__get_email_from_token(token)

            try:
                org_account = OrgAccount.objects.get(email=email)

            except OrgAccount.DoesNotExist as e:
                HttpResponse.status_code=int(error_codes.bad_request())
                return HttpResponse('Access denied')
            
            campaign_id=data.get('campaign_id')
            user_id=data.get('user_id')

            try:
                check_if_org_created_campaign=Campaign.objects.get(campaign_id=campaign_id,organisation_email=email)
            except Campaign.DoesNotExist as e:
                HttpResponse.status_code=int(error_codes.bad_request())
                return HttpResponse('Access denied')
            
            status=data.get('status')

            try:
                notif=OrgNotif.objects.get(campaign_id=campaign_id,user_id=user_id)
            except OrgNotif.DoesNotExist as e:
                HttpResponse.status_code=int(error_codes.bad_request())
                return HttpResponse('Access denied')

            if(status=='R'):
                notif.delete()
                add_rejected_user = RejectedUsers(campaign_id=campaign_id,user_id=user_id)
                add_rejected_user.save()
                HttpResponse.status_code=int(error_codes.request_rejected())
                return HttpResponse('User added to rejected')

            elif(status=='A'):
                notif.delete()
                add_accepted_user = AcceptedUsers(campaign_id=campaign_id,user_id=user_id)
                add_accepted_user.save()
                HttpResponse.status_code=int(error_codes.request_accepted())
                return HttpResponse('User added to accepted')
            
            else:
                HttpResponse.status_code=int(error_codes.bad_request())
                return HttpResponse('Invalid status')
        
        except Exception as e:
            HttpResponse.status_code = int(error_codes.bad_request())
            return HttpResponse('Deserialisation error '+str(e))

    else:
        HttpResponse.status_code = int(error_codes.bad_request())
        return HttpResponse('404 error')