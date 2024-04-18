from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from company.models import Subscription, Company
from datetime import timedelta


class Command(BaseCommand):
    help = "Creates a Subscription for a Company"

    def add_arguments(self, parser):
        parser.add_argument(
            "company_id",
            type=int,
            help="ID of the Company for which to create the Subscription",
        )
        parser.add_argument(
            "days", type=int, help="Number of days for the Subscription"
        )

    def handle(self, *args, **options):
        company_id = options["company_id"]
        days = options["days"]

        try:
            company = Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            raise CommandError('Company "%s" does not exist' % company_id)

        if Subscription.objects.filter(company=company).exists():
            raise CommandError(
                'Subscription for company "%s" already exists' % company_id
            )

        Subscription.objects.create(
            company=company,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=days),
            is_active=True,
        )

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully created Subscription for company "%s"' % company_id
            )
        )
