from django.urls import path
from .views import Storage, TextileReview, StorageTextileAdd, StorageTextileRemove, Reserve, StorageTextileEdit

app_name = 'storage'


urlpatterns = [
    path('', Storage, name="storage"),
    path('reserve/', Reserve, name="reserve"),
    path('textile/review/<collection_id>/<model_id>/', TextileReview, name="review_textile"),
    path('textile/add/<id>/', StorageTextileAdd, name="add_textile"),
    path('textile/edit/<id>/', StorageTextileEdit, name="edit_textile"),
    path('textile/remove/<id>/', StorageTextileRemove, name="remove_textile"),

]