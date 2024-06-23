from company.models import Company, Branch, Subscription
from company.serializers import (
    CompanySerializer,
    BranchSerializer,
    SubscriptionSerializer,
)

from rest_framework import viewsets


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
