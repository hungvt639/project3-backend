from django.contrib import admin
from .models.Snippets import Snippet
from .models.image import File

admin.site.register(Snippet)
admin.site.register(File)