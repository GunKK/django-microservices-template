# import os

# from django.core.mail import send_mail, send_mass_mail
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags


class MailService:

    @staticmethod
    def send_password_reset_link(user, domain, uid, token, protocol):
       pass

    @staticmethod
    def active_account_success(user, domain, protocol):
       pass

    @staticmethod
    def request_active_account(user_admin, domain, user, protocol):
       pass
