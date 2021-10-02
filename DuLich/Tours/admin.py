from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Tours, Category, Account, Payment, TourBooking, RateTour, CommentTour, Tag, Blog, RateBlog, \
    CommentBlog, Province
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
        return mark_safe("<img src='/{photos_img}' alt={alt} width='120'>".format(photos_img=tours.photos.name, alt=tours.name))


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    inlines = [ToursInlineAdmin, ]


class AccountAdmin(admin.ModelAdmin):
    list_display = ['username', 'role', 'email', 'is_active', 'is_superuser']
    search_fields = ['username']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['created_date', 'price', 'description', 'user', 'tour', 'method']
    search_fields = ['date', 'price', 'user__username', 'tour__name', 'method']


class TourBookingAdmin(admin.ModelAdmin):
    list_display = ['created_date', 'price', 'user', 'status']
    search_fields = ['user', 'status', 'user__username']


class RateTourAdmin(admin.ModelAdmin):
    list_display = ['rate', 'user', 'tour']
    search_fields = ['rate', 'user__username', 'tour__name']


class CommentTourAdmin(admin.ModelAdmin):
    list_display = ['content', 'user', 'tour', 'created_date', 'updated_date']
    search_fields = ['content', 'user__username', 'tour__name']


class BlogAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_date', 'user', 'description']
    search_fields = ['name', 'created_date']


class RateBlogAdmin(admin.ModelAdmin):
    list_display = ['rate', 'user', 'blog']
    search_fields = ['rate', 'user__username', 'blog__name']


class CommentBlogAdmin(admin.ModelAdmin):
    list_display = ['comment', 'photo', 'user', 'blog']
    search_fields = ['comment', 'photo', 'user__username', 'blog__name']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


admin.site.register(Tours, ToursAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(TourBooking, TourBookingAdmin)
admin.site.register(RateTour, RateTourAdmin)
admin.site.register(CommentTour, CommentTourAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(RateBlog, RateBlogAdmin)
admin.site.register(CommentBlog, CommentBlogAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(Permission)
# admin_site.register(Tours, ToursAdmin)
# admin_site.register(Category, CategoryAdmin)
# admin_site.register(Account, AccountAdmin)
# admin_site.register(Payment, PaymentAdmin)
# admin_site.register(TourBooking, TourBookingAdmin)
# admin_site.register(RateTour, RateTourAdmin)
# admin_site.register(CommentTour, CommentTourAdmin)
# admin_site.register(Tag, TagAdmin)
# admin_site.register(Blog, BlogAdmin)
# admin_site.register(RateBlog, RateBlogAdmin)
# admin_site.register(CommentBlog, CommentBlogAdmin)
# admin_site.register(Province, ProvinceAdmin)
