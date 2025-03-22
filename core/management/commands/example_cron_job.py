from django.core.management.base import BaseCommand
from django.db.models import Q

class Command(BaseCommand):
    help = "Example cron job test schedule"

    def handle(self, *args, **kwargs):
        try:
            print("example command")
            self.stdout.write(
                self.style.SUCCESS("Cron jobs run: succeeded")
            )
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Cron jobs run: failed - {str(e)}")
            )
        except ValueError as e:
            self.stderr.write(
                self.style.ERROR(
                    f"Cron jobs run: failed - Invalid status {str(e)}"
                )
            )
