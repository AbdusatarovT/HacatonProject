from django.contrib import admin
from product.models import *

class ImageInAdmin(admin.TabularInline):
    model = Image
    fields = ['image']
    max_num = 4

class ProsuctAdmn(admin.ModelAdmin):
    inlines = [ImageInAdmin]


admin.site.register(Category)
admin.site.register(Product, ProsuctAdmn)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Rating)

