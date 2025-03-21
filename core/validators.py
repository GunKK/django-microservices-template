import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CustomPasswordValidator:
    def validate(self, password, user=None):
        errors = []

        if not re.search(r"[A-Z]", password):
            errors.append(
                _("This password must contain at least one uppercase letter!")
            )

        if not re.search(r"\d", password):
            errors.append(_("This password must contain at least one digit!"))

        if not re.search(r"[\W_]", password):
            errors.append(
                _("This password must contain at least one special character!")
            )
        if errors:
            raise ValidationError(errors, code="password_requirement")

    def get_help_text(self):
        return _(
            "Your password must contain at least 8 characters, one uppercase letter, one digit, and one special character!"
        )
