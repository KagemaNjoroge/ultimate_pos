from django.shortcuts import redirect
from django.contrib import messages


class BranchSelectionMiddleware:
    """
    Middleware to ensure users have selected a branch before accessing the application.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # URLs that don't require branch selection
        self.exempt_urls = [
            "/users/",  # Authentication URLs
            "/company/setup/",  # Company setup
            "/company/select-current-branch/",  # Branch selection
            "/admin/",  # Django admin
            "/static/",  # Static files
            "/media/",  # Media files
            "/api/",  # API endpoints
        ]

    def __call__(self, request):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Check if URL requires branch selection
            if not self._is_exempt_url(request.path):
                # Check if user has selected a branch
                current_branch_id = request.session.get("current_branch_id")

                if not current_branch_id:
                    # Check if there are any branches available
                    from company.models import Branch

                    if Branch.objects.exists():
                        messages.info(request, "Please select a branch to continue.")
                        return redirect("company:select_current_branch")
                    else:
                        # No branches exist, redirect to setup if user has permission
                        if request.user.is_staff or request.user.is_superuser:
                            messages.warning(
                                request,
                                "No branches found. Please set up your company first.",
                            )
                            return redirect("company:setup")
                        else:
                            messages.error(
                                request,
                                "No branches available. Please contact your administrator.",
                            )
                            return redirect("authentication:login")

        response = self.get_response(request)
        return response

    def _is_exempt_url(self, path):
        """Check if the URL is exempt from branch selection requirement."""
        return any(path.startswith(exempt_url) for exempt_url in self.exempt_urls)
