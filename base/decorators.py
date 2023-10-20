from functools import wraps
from django.http import JsonResponse
import json
import logging

logger = logging.getLogger(__name__)
import bleach
import time


def check_fields(view_func):
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

            # Check if the 'description' and title keys exists in the request data and is not empty.
            if "description" not in request_data or not request_data["description"]:
                return JsonResponse(
                    {
                        "success": False,
                        "info": "Description is required and cannot be empty",
                    }
                )

            if "title" not in request_data or not request_data["title"]:
                return JsonResponse(
                    {"success": False, "info": "Title is required and cannot be empty"}
                )

        return view_func(request, *args, **kwargs)

    return wrapped_view


# TODO:update this function
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
