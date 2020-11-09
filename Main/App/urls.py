from django.urls import path
from .views import snippets, image

urlpatterns = [
    path('snippets/', snippets.SnippetList.as_view()),
    path('image/', image.FileUpload.as_view()),
]
