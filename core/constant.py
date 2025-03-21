from enum import Enum

MAX_IMAGE_SIZE = 3 * 1024 * 1024
ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp"]
EXCLUDE_AUTH_PATH = [
    "api/v1/auth/login",
    "api/v1/auth/register",
    "api/v1/auth/refresh",
]


class RepairFormStatusEnum(Enum):
    PENDING = 1
    APPROVAL = 2
    DECLINE = 3
    FIXED = 4
    UNREPAIRABLE = 5
