import os
import re
import shutil
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List

from django.db.models import Model, Q
from django.utils import timezone
from PIL import Image
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response

from core.constant import DIR_TO_UPLOAD_MAPPER, PERMISSIONS_LIST, UI_PERMISSION_MAPPING


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


def convert_to_snake_case(text):
    if isinstance(text, str):
        text = text.strip()
        text = re.sub(r"[^a-zA-Z0-9._-]", "_", text)
        text = text.lower()
    return text


def upload_to_directory(instance, filename):
    # Build storage paths based on instance information
    identify_code = convert_to_snake_case(
        getattr(instance, DIR_TO_UPLOAD_MAPPER[instance.__class__.__name__.lower()])
    )
    # uploads/device/MC1/file_xxxx.jpg
    return f"uploads/{instance.__class__.__name__.lower()}/{identify_code}/{filename}"


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
        raise NotFound(f"No {model.__name__} matches the given query!")
    except ValueError:
        raise ParseError(f"Invalid {model.__name__} ID!")


def get_deleted_instance(model: Model, pk: int = None):
    try:
        instance = model.deleted_objects.get(pk=pk)
        return instance
    except model.DoesNotExist:
        raise NotFound(f"No {model.__name__} matches the given query!")
    except ValueError:
        raise ParseError(f"Invalid {model.__name__} ID!")


def get_global_instance(model: Model, pk: int = None):
    try:
        instance = model.global_objects.get(pk=pk)
        return instance
    except model.DoesNotExist:
        raise NotFound(f"No {model.__name__} matches the given query!")
    except ValueError:
        raise ParseError(f"Invalid {model.__name__} ID!")


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
        raise ParseError("Date is not match format yyyy-mm-dd")

    start_of_day = datetime.combine(target_date_from, datetime.min.time())  # 00:00:00
    end_of_day = datetime.combine(
        target_date_to, datetime.max.time()
    )  # 23:59:59.999999

    # Ensure the format matches the expected format: "YYYY-MM-DD HH:MM:SS.ffffff+00:00"
    start_of_day_str = start_of_day.strftime("%Y-%m-%d %H:%M:%S.%f%z")
    end_of_day_str = end_of_day.strftime("%Y-%m-%d %H:%M:%S.%f%z")
    return [start_of_day_str, end_of_day_str]


def convert_bin_to_hex(bin_number):
    return hex(int(bin_number, 2))[2:].upper()


def convert_hex_to_bin(hex_number):
    return bin(int(hex_number, 16))[2:].zfill(len(PERMISSIONS_LIST))


def is_hex(value):
    pattern = r"^[0-9A-Fa-f]+$"
    return bool(re.match(pattern, value))


def check_permissions_by_hex(hex_num, id_permission) -> bool:
    bin_num = convert_hex_to_bin(hex_num)
    return bool(int(bin_num[-int(id_permission)]))


def get_current_shift_start(current_time):
    # Determine the start time of the current shift
    hour = current_time.hour

    # Day shift: 8:00 - 20:00, night shift: 20:00 - 8:00
    if 8 <= hour < 20:
        # Day shift
        return current_time.replace(hour=8, minute=0, second=0, microsecond=0)
    else:
        # Night shift
        if hour < 8:
            # If it's after midnight but before 8:00 AM
            return (current_time - timedelta(days=1)).replace(
                hour=20, minute=0, second=0, microsecond=0
            )
        else:
            # If it's after 8:00 PM
            return current_time.replace(hour=20, minute=0, second=0, microsecond=0)


def get_start_of_shift():
    return get_current_shift_start(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")


def get_start_of_day():
    return (
        datetime.now()
        .replace(hour=0, minute=0, second=0, microsecond=0)
        .strftime("%Y-%m-%d %H:%M:%S")
    )


def get_start_of_week():
    return (
        (datetime.now() - timedelta(days=datetime.now().weekday()))
        .replace(hour=0, minute=0, second=0, microsecond=0)
        .strftime("%Y-%m-%d %H:%M:%S")
    )


def get_start_of_month():
    return (
        datetime.now()
        .replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        .strftime("%Y-%m-%d %H:%M:%S")
    )


def fix_vector(vector, dim=10000):
    vector = vector[:dim]
    return vector + [0.0] * (dim - len(vector))


def check_ui_permission(user, ui_permission_key):
    """
    Kiểm tra xem người dùng có quyền UI cụ thể không
    """
    if ui_permission_key not in UI_PERMISSION_MAPPING:
        return False

    backend_perm_value = UI_PERMISSION_MAPPING[ui_permission_key]
    return check_permissions_by_hex(user.role.permissions, backend_perm_value)


def get_access_token_from_request(request):
    """
    Extracts the JWT token from the request header.
    Assumes the token is in the Authorization header.
    """
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]
    return None


def extract_first_error_message(errors):
    """
    Extract the first error message from nested serializer errors structure
    """
    if isinstance(errors, dict):
        for key, value in errors.items():
            if isinstance(value, dict):
                result = extract_first_error_message(value)
                if result:
                    return result
            elif isinstance(value, list) and value:
                if isinstance(value[0], str):
                    return value[0]
                else:
                    result = extract_first_error_message(value[0])
                    if result:
                        return result
    elif isinstance(errors, list) and errors:
        if isinstance(errors[0], str):
            return errors[0]
        else:
            return extract_first_error_message(errors[0])
    return None


def global_response_errors(errors):
    error_message = extract_first_error_message(errors)
    return Response({
        "status": False,
        "message": error_message
        },status=status.HTTP_400_BAD_REQUEST)