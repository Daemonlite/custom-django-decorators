from functools import wraps
from django.http import JsonResponse
import json
import logging

logger = logging.getLogger(__name__)
import bleach
import time


def check_fields(required_fields):
    def checker(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.method in ["POST", "GET"]:
                try:
                    request_data = json.loads(request.body)
                except Exception as e:
                    logger.warning(str(e))
                    return JsonResponse(
                        {"success": False, "info": "Unable to fetch request data"}
                    )
            else:
                return JsonResponse(
                    {"success": False, "info": "Requests method is not allowed"}
                )
                # Check if the required fields are present and not empty in the request data.
            for field in required_fields:
                if field not in request_data or not request_data[field]:
                    return JsonResponse(
                        {
                            "success": False,
                            "info": f"{field} is required and cannot be empty",
                        }
                    )

            return view_func(request, *args, **kwargs)

        return wrapped_view

    return checker


def get_only(view_func):
    def wrapped(request,*args,**kwargs):
        if request.method != 'GET':
            return JsonResponse(
                {"success": False, "info": "Request method is not allowed"}
            )
        return view_func(request,*args,**kwargs)
    return wrapped

def post_only(view_func):
    def wrapped(request,*args,**kwargs):
        if request.method != 'POST':
            return JsonResponse(
                {"success": False, "info": "Request method is not allowed"}
            )
        return view_func(request,*args,**kwargs)
    return wrapped


def sanitize(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.method in ["POST", "GET"]:
            try:
                request_data = json.loads(request.body)
            except Exception as e:
                logger.warning(str(e))
                return JsonResponse(
                    {"success": False, "info": "Unable to fetch request data"}
                )

            # Sanitize the 'title' and 'description' fields and assign them back to request_data
            request_data["title"] = bleach.clean(request_data.get("title"))
            request_data["description"] = bleach.clean(request_data.get("description"))

        return view_func(request, *args, **kwargs)

    return wrapped_view


def timed(inner_func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = inner_func(*args, **kwargs)
        end = time.time()
        print(
            f"Function {inner_func.__name__} took {end - start:.3f} seconds to complete"
        )
        return result

    return wrapper


def optimized_execution(inner_func):
    results = {}

    def wrapped_func(*args, **kwargs):
        if args in results:
            return results[args]
        start = time.time()
        result = inner_func(*args, **kwargs)
        end = time.time()
        duration_secs = end - start
        print(f"Executed {inner_func.__name__} in {duration_secs:.3f} secs")
        results[args] = result
        return result

    return wrapped_func


@optimized_execution
def fibonacci(n: int):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
