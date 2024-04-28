from django.contrib import admin
from orders.models import Order,OrderedItem
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_filter=[
        "owner",
        "order_status",
        
    ]
    search_fields = (
    "id",  # Example of a field suitable for icontains lookup
    "owner__name",  # ForeignKey field with a related CharField 'name'
)


admin.site.register(Order,OrderAdmin)

# admin.site.register(OrderedItem)
