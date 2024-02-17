
from django.contrib import admin

from .models import Price, Product, ProductTag, Key, LLM, InferenceServer, PromptResponse, CustomTemplate

class PriceAdmin(admin.StackedInline):
    model = Price

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (PriceAdmin,)

    class Meta:
        model = Product

admin.site.register(ProductTag)
admin.site.register(Price)
admin.site.register(Key)
admin.site.register(LLM)
admin.site.register(CustomTemplate)
admin.site.register(InferenceServer)
admin.site.register(PromptResponse)