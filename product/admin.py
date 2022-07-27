from django.contrib import admin

# Register your models here.
from product.models import *

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Like)