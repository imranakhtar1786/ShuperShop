
from django.contrib import admin
from django.urls import path
from mainapp import views as mainview
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",mainview.index,name="home"),
    path("cart/",mainview.cart,name="cart"),
    path("add-to-cart/",mainview.addtocart,name="add-to-cart"),
    path("checkout/",mainview.checkout,name="checkout"),
    path('payment-success/<int:id>/<str:rppid>/<str:rpoid>/<str:rpsid>/', mainview.paymentSuccessPage,name="payment-success"),
    path('re-payment/<int:id>/', mainview.rePaymentPage,name="re-payment"),
    path("confirmation/<int:id>/",mainview.confirmation,name="confirmation"),
    path("contact/",mainview.contact,name="contact"),
    path("login/",mainview.loginPage,name="login"),
    path("delete-cart/<str:id>/",mainview.deletecart,name="delete-cart"),
    path("update-cart/<str:id>/<str:op>/",mainview.Updatecart,name="update-cart"),
    path("logout/",mainview.logoutPage,name="logout"),
    path("signup/",mainview.signup,name="signup"),
    path("profile/",mainview.profile,name="profile"),
    path("shop/<str:mc>/<str:sc>/<str:br>/",mainview.shop,name="shop"),
    path("single-product/<int:id>/",mainview.singleproduct,name="single-product"),
    path("about/",mainview.about,name="about"),
    path("update-profile/",mainview.Updateprofile,name="update-profile"),
    path("add-to-Wishlist/<int:id>/",mainview.wishlistPage,name="add-to-Wishlist"),
    path("delete-wishlist/<int:id>/",mainview.deletewishlist,name="delete-Wishlist"),
    path("newslatter/subscribe/",mainview.newsLatter,name="newslatter-subscribe"),
    path("search/",mainview.searchPage,name="search-page"),
    path("forget-password1/",mainview.forgetPass1,name="forget-password1"),
    path("forget-password2/",mainview.forgetPass2,name="forget-password2"),
    path("forget-password3/",mainview.forgetPass3,name="forget-password3"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)