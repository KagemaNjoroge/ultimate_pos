from .models import Branch


def current_branch_context(request):
    """
    Context processor to add current branch information to all templates.
    """
    context = {
        "current_branch": None,
        "current_branch_name": None,
        "current_branch_id": None,
    }

    if hasattr(request, "session"):
        current_branch_id = request.session.get("current_branch_id")

        if current_branch_id:
            try:
                branch = Branch.objects.get(id=current_branch_id)
                context.update(
                    {
                        "current_branch": branch,
                        "current_branch_name": branch.branch_name,
                        "current_branch_id": branch.id,
                    }
                )
            except Branch.DoesNotExist:
                # Clear invalid branch from session
                request.session.pop("current_branch_id", None)
                request.session.pop("current_branch_name", None)
                request.session.pop("current_branch_address", None)
                request.session.pop("current_branch_phone", None)

    return context
