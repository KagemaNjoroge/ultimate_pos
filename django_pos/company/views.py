from django.shortcuts import get_object_or_404


from .serializers import CompanySerializer, BranchSerializer, Branch, Company

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet


class BranchesViewSet(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer


class CompanyView(APIView):
    def get(self, request, id: int):
        company = get_object_or_404(Company, pk=id)
        serialized_data = CompanySerializer(company).data
        return Response(serialized_data)

    def put(self, request, id: int):
        company = get_object_or_404(Company, pk=id)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def post(self, request):
        # since only one company can be created
        if Company.objects.exists():
            return Response({"error": "Company already exists."}, status=400)
        else:
            serializer = CompanySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
