from django.contrib import admin
from .models import Tours, Category, Account
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ToursForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        model = Tours
        fields = '__all__'



class ToursInlineAdmin(admin.StackedInline):
    model = Tours
    fk_name = 'category'


class TourAppAdminSite(admin.AdminSite):
    site_header = 'Hệ thống quản lý du lịch'


admin_site = TourAppAdminSite(name='myadmin')


class ToursAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'finish_date', 'price', 'active']
    search_fields = ['name', 'start_date', 'price']
    readonly_fields = ['avatar']
    form = ToursForm
    def avatar(self, tours):
        return mark_safe("<img src='/static/{photos_img}' alt={alt} width='120'>".format(photos_img=tours.photos.name, alt=tours.name))


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    inlines = [ToursInlineAdmin, ]


class AccountAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_superuser']
    search_fields = ['name']


#admin.site.register(Tours, ToursAdmin)
#admin.site.register(Category, CategoryAdmin)
#admin.site.register(Account, AccountAdmin)
admin_site.register(Tours, ToursAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(Account, AccountAdmin)