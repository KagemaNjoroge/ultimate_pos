from django.http import HttpRequest
from django.shortcuts import redirect
from django.contrib import messages
from company.models import Branch, Company


class BranchSelectionMiddleware:
    """
    Middleware to ensure users have selected a branch before accessing the application.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # URLs that don't require branch selection
        self.exempt_urls = [
            "/accounts/",  # Authentication URLs
            "/company/setup/",  # Company setup
            "/company/select-current-branch/",  # Branch selection
            "/admin/",  # Django admin
            "/static/",  # Static files
            "/media/",  # Media files
            "/api/",  # API endpoints
            "/company/branches/add/",  # Add branch
            "notifications/",  # Notifications
            "/docs/",  # Documentation
            "/company/api/",  # Company API endpoints
            "/company/branches/",  # Branches List endpoints
            "/company/branch/api/",  # Branch API endpoints
            # django debug toolbar URLs
            "/__debug__/",
            "/debug_toolbar/",
            # sales pdf
            "/sales/pdf/",
        ]

    def __call__(self, request: HttpRequest):
        # Check if user is authenticated
        if request.user.is_authenticated:
            # Check if URL requires branch selection
            if not self._is_exempt_url(request.path):
                # Check if user has selected a branch
                current_branch_id = request.session.get("current_branch_id")

                if not current_branch_id:
                    # Check if there are any branches available
                    company = Company.objects.first()

                    if not company:
                        messages.error(
                            request=request,
                            message="No company setup found. Please set up your company first.",
                            extra_tags="danger",
                        )
                        return redirect("company:setup")

                    if Branch.objects.exists():

                        messages.info(request, "Please select a branch to continue.")
                        return redirect("company:select_current_branch")
                    else:
                        # No branches exist, redirect to branches setup if user has permission
                        if request.user.is_staff or request.user.is_superuser:
                            # clear other messages
                            messages.get_messages(request).used = True

                            messages.warning(
                                request=request,
                                message="No branches found. Please add a branch to continue.",
                                extra_tags="warning",
                            )
                            return redirect("company:add_branch")
                        else:
                            messages.error(
                                request,
                                "No branches available. Please contact your administrator.",
                            )
                            # TODO redirect to 'contact admin' page or similar
                            return redirect("authentication:login")

        response = self.get_response(request)
        return response

    def _is_exempt_url(self, path):
        """Check if the URL is exempt from branch selection requirement."""
        return any(path.startswith(exempt_url) for exempt_url in self.exempt_urls)
