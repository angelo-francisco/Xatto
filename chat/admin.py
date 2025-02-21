from django.contrib import admin
from .models import Room, Message, Contact

admin.site.register([Room, Message, Contact])