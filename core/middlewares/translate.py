import json
import logging

from django.utils.deprecation import MiddlewareMixin

from core.google_trans import translator

logger = logging.getLogger(__name__)


class TranslateMiddleware(MiddlewareMixin):

    async def __call__(self, request):

        response = await self.get_response(request)

        # Check for the Accept-Language header
        accept_language = request.META.get("HTTP_ACCEPT_LANGUAGE", "en").split(",")[0]

        # If the response is JSON, translate the message
        if response["Content-Type"].startswith("application/json"):
            response_data = json.loads(response.content)
            if response_data.get("message", None) is not None:
                res = await self.translate_message(
                    response_data.get("message"), accept_language
                )
                if res is not None:
                    response_data["message"] = res
                response.content = json.dumps(response_data).encode("utf-8")
        return response

    async def translate_message(self, text, target_lang):
        if not text:
            return text

        try:
            if target_lang == "en":
                return text

            translated = await translator.translate(text, dest=target_lang)

            return translated.text

        except Exception as e:
            print(f"Translation failed: {e}")
