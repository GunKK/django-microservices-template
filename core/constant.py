from enum import Enum

USER_DEFAULT_SYSTEM = 3
MAX_IMAGE_SIZE = 3 * 1024 * 1024
ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp"]
EXCLUDE_AUTH_PATH = [
    "api/v1/auth/login",
    "api/v1/auth/register",
    "api/v1/auth/refresh",
]

EXCLUDE_ACTIVE_PATH = [
    *EXCLUDE_AUTH_PATH,
    "api/v1/auth/logout",
    "api/v1/users/request_active_account",
    "api/v1/notifications/",
    "api/v1/users/",
    "api/v1/auth/me/",
]

class NotificationTypeEnum(Enum):
    # system notification 1-20
    SYSTEM_NOTIFICATION = 1
    # define here


PERMISSIONS_LIST = []

permissions_enum_dict = {
    name.upper().replace(" ", "_"): idx + 1
    for idx, name in enumerate(PERMISSIONS_LIST)
    if "future use" not in name.lower()
}

PermissionsEnum = Enum("PermissionsEnum", permissions_enum_dict)


UI_PERMISSION_MAPPING = {}
DEFAULT_PERMISSION_CLASSES = 2

DIR_TO_UPLOAD_MAPPER = {"user": "pk"}