from django.core.management.base import BaseCommand
from django.core.management import call_command
from bson import ObjectId


class Command(BaseCommand):
    help = "Seed the database with initial data"

    def handle(self, *args, **kwargs):
        json_files = ["bookManagementApi/fixtures/Books.json"]

        for json_file in json_files:
            try:
                call_command("loaddata", json_file)
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully loaded {json_file}")
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error loading {json_file}: {e}"))
