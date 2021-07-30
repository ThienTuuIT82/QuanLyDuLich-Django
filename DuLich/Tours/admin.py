from django.contrib import admin
from .models import Tours, Category, Account
from django.utils.html import mark_safe


class TourAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống quản lý du lịch'


admin_site = TourAppAdminSite(name='myadmin')


class ToursAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'finish_date', 'price', 'active']
    search_fields = ['name', 'start_date', 'price']
    readonly_fields = ['avatar']


    def avatar(self, tours):
        return mark_safe("<img src='/static/{photos_img}' alt={alt} width='120'>".format(photos_img=tours.photos.name, alt=tours.name))


admin_site.register(Tours, ToursAdmin)
admin_site.register(Category)
admin_site.register(Account)