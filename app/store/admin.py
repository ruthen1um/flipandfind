from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_exclude(request, obj)
        if request.user.is_authenticated and request.user.role == 'SELLER':
            return ['seller']
        return super().get_exclude(request, obj)

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return request.user.is_authenticated and request.user.role == 'SELLER'

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.seller != request.user:
            return False
        return request.user.is_authenticated and request.user.role == 'SELLER'

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.seller != request.user:
            return False
        return request.user.is_authenticated and request.user.role == 'SELLER'

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.is_authenticated and request.user.role == 'SELLER'

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and obj.seller != request.user:
            return False
        return request.user.is_authenticated and request.user.role == 'SELLER'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_authenticated and request.user.role == 'SELLER':
            return qs.filter(seller=request.user)
        return qs.none()

    def save_model(self, request, obj, form, change):
        if not change and not obj.seller_id:
            obj.seller = request.user
        super().save_model(request, obj, form, change)


class ProductPhotoAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.is_authenticated and request.user.role == 'SELLER':
            return qs.filter(product__seller=request.user)
        return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product":
            if request.user.is_superuser:
                kwargs["queryset"] = models.Product.objects.all()
            elif request.user.is_authenticated and request.user.role == 'SELLER':
                kwargs["queryset"] = models.Product.objects.filter(seller=request.user)
            else:
                kwargs["queryset"] = models.Product.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return request.user.is_authenticated and request.user.role == 'SELLER'

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.product.seller != request.user:
            return False
        return request.user.is_authenticated and request.user.role == 'SELLER'

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj and obj.product.seller != request.user:
            return False
        return request.user.is_authenticated and request.user.role == 'SELLER'

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.is_authenticated and request.user.role == 'SELLER'

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductPhoto, ProductPhotoAdmin)
admin.site.register(models.ProductCategory)
admin.site.register(models.Review)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.Delivery)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
admin.site.register(models.Card)
admin.site.register(models.Payment)
admin.site.register(models.User)
admin.site.register(models.BuyerProfile)
admin.site.register(models.SellerProfile)
