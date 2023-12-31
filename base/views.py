from django.shortcuts import render
from base.models import Task
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .decorators import *
import logging
import json
logger = logging.getLogger(__name__)
# Create your views here.

@csrf_exempt
@timed
@get_only
def get_tasks(request):
    try:
        tasks = Task.objects.values("title","description","complete")
        return JsonResponse({"success": True, "info": list(tasks)})
    except Exception as e:
        logger.warning(str(e))
        return JsonResponse({"success":False,"info":"Cannot fetch Tasks now"})
    

@csrf_exempt
@check_fields(["title","description"])
@sanitize(["title","description"])
@optimized_execution
@post_only
def create_task(request):
    try:
        data = json.loads(request.body)
        title = data.get("title")
        description = data.get("description")

        Task.objects.create(title=title,description=description)
        return JsonResponse({"success": True, "info": "Task created"})
    except Exception as e:
        logger.warning(str(e))
        return JsonResponse({"success":False,"info":"Unable to create Task"})


