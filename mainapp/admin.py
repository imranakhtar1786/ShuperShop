from django.contrib import admin
from .models import *
#admin.site.register((Maincategory,Subcategory,Brand,Product,Buyer,Wishlist,Checkout,CheckoutProduct,Contact,NewsLatter))
@admin.register(Maincategory)
class MaincategoryAdmin(admin.ModelAdmin):
    list_display=["id","name"]

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display=["id","name"]

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display=["id","name","pic"]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=["id","name","maincategory","subcategory","brand","color","size","baseprice","discount","finalprice","stock","pic1","pic2","pic3","pic4"]

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display=["id","name","username","email","phone","address","pin","city","state","pic"]

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display=["id","product","buyer"]

@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display=["id","buyer","orderstatus","Paymentstatus","paymentmode","subtotal","shipping","total","rppid","date"]

@admin.register(CheckoutProduct)
class CheckoutProductAdmin(admin.ModelAdmin):
    list_display=["id","checkout","product","qty","total"]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display=["id","name","email","phone","subject","message","status","date"]

@admin.register(NewsLatter)
class NewsLatterAdmin(admin.ModelAdmin):
    list_display=["id","email"]

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display=["id","name","message","pic"]
