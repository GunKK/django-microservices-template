from datetime import datetime
from decimal import Decimal
from typing import List

from django.core.cache import cache
from django.db.models import Model, Q
from django.utils import timezone
from PIL import Image
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response


def response_errors(errors):
    error_message = next(iter(errors.values()))[0]
    if isinstance(error_message, list):
        error_message = error_message[0]
    return Response(
        {"status": False, "message": error_message},
        status=status.HTTP_400_BAD_REQUEST,
    )


def convert_to_dict(error_list):
    if isinstance(error_list, list):
        error_dict = {}
        for error in error_list:
            if isinstance(error, dict):
                error_dict.update(error)
        return error_dict
    return error_list


def format_response(errors):
    error_message = next(iter(errors.values()))[0]
    return error_message


# A simple function to blacklist the access token
def blacklist_token(token):
    cache.set(
        f"blacklisted_access_token_{token}", True, timeout=60 * 60
    )  # Example: 1 hours


def end_of_today():
    return timezone.now().replace(hour=24, minute=59, second=59, microsecond=59)


def update_name_with_count(model, name, obj):
    """
    Updates the name of a model instance by appending a count of objects
    with the same name excluding the given object_id.
    """
    # Count the number of objects with the same name excluding the current object
    count_global = model.global_objects.filter(
        Q(name__regex=f"^{name}\\(\\d*\\)$") | Q(name=name)
    ).count()
    count = model.objects.filter(
        Q(name__regex=f"^{name}\\(\\d*\\)$") | Q(name=name)
    ).count()
    count_deleted = model.deleted_objects.filter(
        Q(name__regex=f"^{name}\\(\\d*\\)$") | Q(name=name)
    ).count()

    if count == 0 or count_global < 1:
        return

    if count_global > 1:
        obj.name = f"{obj.name}({str(count_global - count_deleted)})"
        obj.save()
    elif count_global == 0:
        return Response(
            {"status": False, "message": "Name is invalid value!"},
            status=status.HTTP_400_BAD_REQUEST,
        )


def upload_to_directory(instance, filename):
    # Build storage paths based on instance information
    return (
        f"uploads/{instance.owner.id}/{instance.__class__.__name__.lower()}/{filename}"
    )


def process_image(path):
    img = Image.open(path)
    return img.resize((800, 800))  # Resize image 800x800


def snake_to_lowercase(name):
    return name.replace("_", "")


def get_instance(model: Model, pk: int = None):
    try:
        instance = model.objects.get(pk=pk)
        return instance
    except model.DoesNotExist:
        raise NotFound(
            {
                "status": False,
                "message": f"No {model.__class__} matches the given query!",
            }
        )
    except ValueError:
        raise ParseError({"status": False, "message": f"Invalid {model.__class__} ID!"})


def get_deleted_instance(model: Model, pk: int = None):
    try:
        instance = model.deleted_objects.get(pk=pk)
        return instance
    except model.DoesNotExist:
        raise NotFound(
            {
                "status": False,
                "message": f"No {model.__class__} matches the given query!",
            }
        )
    except ValueError:
        raise ParseError({"status": False, "message": f"Invalid {model.__class__} ID!"})


def get_global_instance(model: Model, pk: int = None):
    try:
        instance = model.global_objects.get(pk=pk)
        return instance
    except model.DoesNotExist:
        raise NotFound(
            {
                "status": False,
                "message": f"No {model.__class__} matches the given query!",
            }
        )
    except ValueError:
        raise ParseError({"status": False, "message": f"Invalid {model.__class__} ID!"})


def calculate_average_percent(list):
    if list.count() == 0:
        return 0.00

    total_percent = sum(Decimal(item.completion_percent) for item in list)
    average_percent = total_percent / list.count()

    return round(float(average_percent), 2)


def path_is_excluded(current_route, list) -> bool:
    return any(current_route.startswith(path) for path in list)


def validate_max_length(value, max_length, field_name):
    if value and len(value) > max_length:
        raise serializers.ValidationError(
            f"{field_name} exceeds maximum length of {max_length} characters!"
        )
    return value

def format_date_filter(date_from: str, date_to: str) -> List[str]:
    try:
        target_date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
        target_date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
    except ValueError:
        raise ParseError(
            {"status": False, "message": "Date is not match format yyyy-mm-dd"}
        )

    start_of_day = datetime.combine(target_date_from, datetime.min.time())  # 00:00:00
    end_of_day = datetime.combine(
        target_date_to, datetime.max.time()
    )  # 23:59:59.999999

    # Ensure the format matches the expected format: "YYYY-MM-DD HH:MM:SS.ffffff+00:00"
    start_of_day_str = start_of_day.strftime("%Y-%m-%d %H:%M:%S.%f%z")
    end_of_day_str = end_of_day.strftime("%Y-%m-%d %H:%M:%S.%f%z")
    return [start_of_day_str, end_of_day_str]
