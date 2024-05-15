from django.shortcuts import render

from suppliers.models import Supplier

# Create your views here.


def index(request):
    suppliers = Supplier.objects.all()
    return render(request, "suppliers/index.html", {"suppliers": suppliers})
