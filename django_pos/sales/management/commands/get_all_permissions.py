from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Get a list of all permissions available in the system."

    def handle(self, *args, **options):
        permissions = set()

        tmp_superuser = get_user_model()(is_active=True, is_superuser=True)

        for backend in auth.get_backends():
            if hasattr(backend, "get_all_permissions"):
                permissions.update(backend.get_all_permissions(tmp_superuser))

        sorted_list_of_permissions = sorted(list(permissions))

        sorted_list_of_permissions = [
            p
            for p in sorted_list_of_permissions
            if not p.startswith("contenttypes.")
            and not p.startswith("admin.")
            and not p.startswith("sessions.")
        ]

        # Send a joined list of permissions to a command-line output.
        self.stdout.write("\n".join(sorted_list_of_permissions))
