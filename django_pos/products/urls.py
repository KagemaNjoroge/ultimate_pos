from django.urls import path
from .api import CategoryView, ProductView

from . import views

app_name = "products"
urlpatterns = [
    # List categories
    path("categories", views.categories_list_view, name="categories_list"),
    # Add category
    path("categories/add", views.categories_add_view, name="categories_add"),
    # Update category
    path(
        "categories/update/<str:category_id>",
        views.categories_update_view,
        name="categories_update",
    ),
    # Delete category
    path(
        "categories/delete/<str:category_id>",
        views.categories_delete_view,
        name="categories_delete",
    ),
    # List products
    path("", views.products_list_view, name="products_list"),
    # Add product
    path("add", views.products_add_view, name="products_add"),
    # Update product
    path("update/<str:product_id>", views.products_update_view, name="products_update"),
    # Delete product
    path("delete/<str:product_id>", views.products_delete_view, name="products_delete"),
    # Get products AJAX
    path("get", views.get_products_ajax_view, name="get_products"),
    # upload excel
    path("upload_excel", views.upload_excel_view, name="upload_excel"),
    # download excel
    path("download_template", views.download_template, name="download_template"),
    # product details
    path("details/<str:product_id>", views.product_detail_view, name="product_details"),
]


# experimental api
urlpatterns += [
    path("api/categories/", CategoryView.as_view(), name="api_categories"),
    path("api/products/", ProductView.as_view(), name="api_products"),
    path("api/products/<int:id>/", ProductView.as_view()),
    path("api/category/<int:pk>/", CategoryView.as_view()),
]
