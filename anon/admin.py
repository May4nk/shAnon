from django.contrib import admin
from .models import Suser,Post,Follow
# Register your models here.

admin.site.register(Suser)
admin.site.register(Post)
admin.site.register(Follow)
