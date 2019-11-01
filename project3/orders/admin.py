from django.contrib import admin
from .models import Category, Product, Topping, Addition, Order, Item

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', ]


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'size', 'price', 'n_topping', 
                    'n_addition', 'created', 'updated']
    list_filter = ['category', 'size', 'created', 'updated']
    list_editable = ['price', 'size', 'n_topping', 'n_addition', ]


admin.site.register(Product, ProductAdmin)


class ToppingAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    list_editable = ['price', ]


admin.site.register(Topping, ToppingAdmin)


class AdditionAdmin(admin.ModelAdmin):
    list_display = ['name', 'size', 'price']
    list_filter = ['size',]
    list_editable = ['size', 'price', ]


admin.site.register(Addition, AdditionAdmin)


class OrderItemInline(admin.TabularInline):
    model = Order.item.through
    readonly_fields = ['item', 'quantity',]
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'quantity', 'price', 'status', 'created', 'updated']
    list_editable = ['status', ]
    readonly_fields = ['user', 'quantity', 'price', ]
    inlines = (OrderItemInline, )


admin.site.register(Order, OrderAdmin)