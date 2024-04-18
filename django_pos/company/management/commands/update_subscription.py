from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from company.models import Subscription, Company
from datetime import timedelta


class UpdateSubscription(BaseCommand):
    help = "Updates the start_date and end_date of a Subscription"

    def add_arguments(self, parser):
        parser.add_argument(
            "company_id",
            type=int,
            help="ID of the Company whose Subscription needs to be updated",
        )
        parser.add_argument(
            "days", type=int, help="Number of days to extend the Subscription"
        )

    def handle(self, *args, **options):
        company_id = options["company_id"]
        days = options["days"]

        try:
            company = Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            raise CommandError('Company "%s" does not exist' % company_id)

        try:
            subscription = Subscription.objects.get(company=company, is_active=True)
        except Subscription.DoesNotExist:
            raise CommandError(
                'Active Subscription for company "%s" does not exist' % company_id
            )

        subscription.start_date = timezone.now()
        subscription.end_date = timezone.now() + timedelta(days=days)
        subscription.save()

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully updated Subscription for company "%s"' % company_id
            )
        )
