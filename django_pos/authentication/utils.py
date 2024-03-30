from django.contrib.auth import get_user_model
from django.contrib import auth


def get_all_permissions():
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
        and not p.startswith("etims")
        and not p.startswith("auth")
        and not p.startswith("company")
    ]

    return sorted_list_of_permissions
