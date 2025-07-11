from ..models import Branch, Company


def get_current_branch(request):
    """
    Get the current branch from session.
    Returns the Branch object if found, None otherwise.
    """
    current_branch_id = request.session.get("current_branch_id")
    if current_branch_id:
        try:
            return Branch.objects.get(id=current_branch_id)
        except Branch.DoesNotExist:
            # Clean up invalid session data
            clear_current_branch(request)
    return None


def set_current_branch(request, branch):
    """
    Set the current branch in session.
    """
    if isinstance(branch, Branch):
        request.session["current_branch_id"] = branch.id
        request.session["current_branch_name"] = branch.branch_name
        request.session["current_branch_address"] = branch.address
        request.session["current_branch_phone"] = branch.phone_number
        request.session["current_branch_is_headquarter"] = branch.is_headquarter
        return True
    return False


def clear_current_branch(request):
    """
    Clear current branch from session.
    """
    session_keys = [
        "current_branch_id",
        "current_branch_name",
        "current_branch_address",
        "current_branch_phone",
        "current_branch_is_headquarter",
    ]

    for key in session_keys:
        request.session.pop(key, None)


def ensure_default_branch():
    """
    Ensure there's at least one branch for the company.
    Creates a default branch if none exists.
    """
    company = Company.objects.first()
    if company and not Branch.objects.exists():
        Branch.objects.create(
            company=company,
            branch_name=f"{company.company_name} - Main Branch",
            phone_number=company.phone_number,
            email=company.email,
            address=company.address,
            branch_id="MAIN001",
            is_headquarter=True,
        )
        return True
    return False
