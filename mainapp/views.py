from django.shortcuts import render,HttpResponseRedirect
from django.contrib.messages import success,error
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import Paginator
import razorpay

def index(Request):
    product=Product.objects.all()[::-1][:12:]
    testimonial=Testimonial.objects.all().order_by("-id")
    return render(Request,"index.html",{"product":product,"testimonial":testimonial})

def addtocart(Request):
    if(Request.method=="POST"):
        cart=Request.session.get("cart",None)
        id=Request.POST.get("id")
        qt=int(Request.POST.get("qty"))
        try:
            P=Product.objects.get(id=id)
            if(cart):
                if(str(id) in cart.keys()):
                    item=cart[str(id)]
                    item["qty"]=item["qty"]+qt
                    item["total"]=item["total"]+qt*item["price"]
                    cart[str(id)]=item
                else:
                    cart.setdefault(str(id),{"product_id:":id,"name":P.name,"brand":P.brand.name,"color":P.color,"size":P.size,"price":P.finalprice,"qty":qt,"total":qt*P.finalprice,"pic":P.pic1.url})
            else:
                try:
                    cart={str(id):{"product_id:":id,"name":P.name,"brand":P.brand.name,"color":P.color,"size":P.size,"price":P.finalprice,"qty":qt,"total":qt*P.finalprice,"pic":P.pic1.url}}
                except:
                    cart={}
            Request.session["cart"]=cart
            Request.session.set_expiry(60*60*24*30)
        except:
            pass
    return HttpResponseRedirect("/cart/")

def cart(Request):
    cart=Request.session.get("cart")
    subtotal=0
    shipping=0
    total=0
    if(cart):
        for value in cart.values():
            subtotal=subtotal+value["total"]
        if(subtotal>0 and subtotal<1000):
            shipping=150
        total=shipping+subtotal
    return render(Request,"cart.html",{"cart":cart,"subtotal":subtotal,"shipping":shipping,"total":total})

def deletecart(Request,id):
    cart=Request.session.get("cart",None)
    if(cart):
        del cart[id]
        Request.session["cart"]=cart
    return HttpResponseRedirect("/cart/")

def Updatecart(Request,id,op):
    cart=Request.session.get("cart",None)
    if(cart):
        item=cart[id]
        if(op=="dec" and item["qty"]==1):
            return HttpResponseRedirect("/cart/")
        else:
            if(op=="dec"):
                item["qty"]=item["qty"]-1
                item["total"]=item["total"]-item["price"]
            else:
                item["qty"]=item["qty"]+1
                item["total"]=item["total"]+item["price"]
        cart[id]=item
        Request.session["cart"]=cart
    return HttpResponseRedirect("/cart/")

client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY,settings.RAZORPAY_API_SECRET_KEY))
@login_required(login_url="/login/")
def checkout(Request):
    try:
        buyer=Buyer.objects.get(username=Request.user.username)
        cart=Request.session.get("cart",None)
        subtotal=0
        shipping=0
        total=0
        if(cart):
            for value in cart.values():
                subtotal=subtotal+value["total"]
            if(subtotal>0 and subtotal<1000):
                shipping=150
            total=shipping+subtotal
        if(Request.method=="POST"):
            mode=Request.POST.get("mode")
            checkout=Checkout()
            checkout.buyer=buyer
            checkout.subtotal=subtotal
            checkout.shipping=shipping
            checkout.total=total
            checkout.save()
            for key,value in cart.items():
                p=Product.objects.get(id=int(key))
                cp=CheckoutProduct()
                cp.checkout=checkout
                cp.product=p
                cp.qty=value["qty"]
                cp.total=value["total"]
                cp.save()
            Request.session["cart"]={}
            if(mode=="COD"):
                return HttpResponseRedirect("/confirmation/"+str(checkout.id)+"/")
            else:
                orderAmount = checkout.total*100
                orderCurrency = "INR"
                paymentOrder = client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
                paymentId = paymentOrder['id']
                checkout.paymentmode=1
                checkout.save()
                return render(Request,"pay.html",{
                    "amount":orderAmount,
                    "displayAmount":checkout.total,
                    "api_key":settings.RAZORPAY_API_KEY,
                    "order_id":paymentId,
                    "User":buyer,
                    "id":checkout.id
                })
        return render(Request,"checkout.html",{"buyer":buyer ,"cart":cart,"subtotal":subtotal,"total":total,"shipping":shipping})
    except:
        return HttpResponseRedirect("/admin/")

@login_required(login_url='/login/')
def paymentSuccessPage(request,id,rppid,rpoid,rpsid):
    check = Checkout.objects.get(id=id)
    check.rppid=rppid
    check.Paymentstatus=1
    check.save()
    return HttpResponseRedirect('/confirmation/'+str(id)+"/")

@login_required(login_url='/login/')
def rePaymentPage(Request,id):
    try:
        checkout = Checkout.objects.get(id=id)
        buyer = Buyer.objects.get(username=Request.user.username)
        orderAmount = checkout.total*100
        orderCurrency = "INR"
        paymentOrder = client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
        paymentId = paymentOrder['id']
        checkout.paymentmode=1
        checkout.save()
        return render(Request,"pay.html",{
            "amount":orderAmount,
            "displayAmount":checkout.total,
            "api_key":settings.RAZORPAY_API_KEY,
            "order_id":paymentId,
            "User":buyer,
            "id":id
        })
    except:
        return HttpResponseRedirect("/profile/")

    
@login_required(login_url="/login/")
def confirmation(Request,id):
    try:
        buyer=Buyer.objects.get(username=Request.user.username)
        checkout=Checkout.objects.get(id=id)
        cart=CheckoutProduct.objects.filter(checkout=checkout)
        subtotal=0
        shipping=0
        total=0
        for item in cart:
            subtotal=subtotal+item.total
        if(subtotal>0 and subtotal<1000):
            shipping=150
        total=shipping+subtotal
        return render(Request,"confirmation.html",{"cart":cart,"subtotal":subtotal,"total":total,"shipping":shipping,"checkout":checkout,"buyer":buyer})
    except:
        return HttpResponseRedirect("/admin/")

def contact(Request):
    if Request.method=="POST":
        name=Request.POST.get("name")
        email=Request.POST.get("email")
        phone=Request.POST.get("phone")
        subject=Request.POST.get("subject")
        message=Request.POST.get("message")
        c=Contact()
        c.name=name
        c.email=email
        c.phone=phone
        c.subject=subject
        c.message=message
        c.save()
        success(Request,"Thanks To Share Your Query With Us!!! Our Team Will Contact you Soon")
    return render(Request,"contact.html")

def shop(Request,mc,sc,br):
    if mc=="All" and sc=="All" and br=="All":
        product=Product.objects.all().order_by("-id")
    elif mc!="All" and sc=="All" and br=="All":
        product=Product.objects.filter(maincategory=Maincategory.objects.get(name=mc)).order_by("-id")
    elif mc=="All" and sc!="All" and br=="All":
        product=Product.objects.filter(subcategory=Subcategory.objects.get(name=sc)).order_by("-id")
    elif mc=="All" and sc=="All" and br!="All":
        product=Product.objects.filter(brand=Brand.objects.get(name=br)).order_by("-id")
    elif mc!="All" and sc!="All" and br=="All":
        product=Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc)).order_by("-id")
    elif mc=="All" and sc!="All" and br!="All":
        product=Product.objects.filter(brand=Brand.objects.get(name=br),subcategory=Subcategory.objects.get(name=sc)).order_by("-id")
    elif mc!="All" and sc=="All" and br!="All":
        product=Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br)).order_by("-id")
    else:
        product=Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc),brand=Brand.objects.get(name=br)).order_by("-id")
    maincategory=Maincategory.objects.all().order_by("-id")
    subcategory=Subcategory.objects.all().order_by("-id")
    brands=Brand.objects.all().order_by("-id")
    paginator = Paginator(product,8)
    page_number = Request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(Request,"shop.html",{"product":page_obj,"maincategory":maincategory,"subcategory":subcategory,"brands":brands,"sc":sc,"mc":mc,"br":br})

def searchPage(Request):
    if(Request.method=="POST"):
        search=Request.POST.get("search").title()
        try:
            maincategory=Maincategory.get(name=search)
        except:
            maincategory=None
        try:
            subcategory=Maincategory.get(name=search)
        except:
            subcategory=None
        try:
            brand=Maincategory.get(name=search)
        except:
            brand=None
        product=Product.objects.filter(Q(name__icontains=search)|Q(maincategory=maincategory)|Q(subcategory=subcategory)|Q(brand=brand)|Q(color=search)|Q(description__icontains=search)).order_by("-id")
        maincategory=Maincategory.objects.all().order_by("-id")
        subcategory=Subcategory.objects.all().order_by("-id")
        brands=Brand.objects.all().order_by("-id")
        paginator = Paginator(product,8)
        page_number = Request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(Request,"shop.html",{"product":page_obj,"maincategory":maincategory,"subcategory":subcategory,"brands":brands,"sc":"All","mc":"All","br":"All"})


def singleproduct(Request,id):
    product=Product.objects.get(id=id)
    return render(Request,"single-product.html",{"product":product})

def about(Request):
    return render(Request,"about.html")

def loginPage(Request):
    if (Request.method=="POST"):
        password=Request.POST.get("password")
        username=Request.POST.get("username")
        user=authenticate(username=username,password=password)
        if(user is not None):
            login(Request,user)
            if(user.is_superuser):
                return HttpResponseRedirect("/admin/")
            else:
                return HttpResponseRedirect("/profile/")
        else:
            error(Request,"Invalid Username or Password!!")   
    return render(Request,"login.html")

@login_required(login_url="/login/")
def logoutPage(Request):
    logout(Request)
    return HttpResponseRedirect("/login/")

def signup(Request):
    if (Request.method=="POST"):
        password=Request.POST.get("password")
        cpassword=Request.POST.get("cpassword")
        if(password==cpassword):
            username=Request.POST.get("username")
            email=Request.POST.get("email")
            try:
                name=Request.POST.get("fullname")
                User.objects.create_user(username=username,password=password,email=email,first_name=name)
                phone=Request.POST.get("phone")
                b=Buyer()
                b.username=username
                b.email=email
                b.phone=phone
                b.name=name
                b.save()
                return HttpResponseRedirect("/login/") 
            except:
                error(Request,"Username is Already Taken!!!")
        else:
            error(Request,"Password and Confirmed Password Does not match")
    return render(Request,"signup.html")

@login_required(login_url="/login/")
def profile(Request):
    if(Request.user.is_superuser):
        return HttpResponseRedirect("/admin/")
    buyer=Buyer.objects.get(username=Request.user.username)
    wishlist=Wishlist.objects.filter(buyer=buyer)
    checkout=Checkout.objects.filter(buyer=buyer)
    orders=[]
    for i in checkout:
        cp=CheckoutProduct.objects.filter(checkout=i)
        orders.append({"checkout":i,"cp":cp})
    return render(Request,"profile.html",{"buyer":buyer,"wishlist":wishlist,"orders":orders})
    
@login_required(login_url="/login/")   
def Updateprofile(Request):
    if(Request.user.is_superuser):
        return HttpResponseRedirect("/admin/")
    buyer=Buyer.objects.get(username=Request.user.username)
    if (Request.method=="POST"):
        buyer.name=Request.POST.get("name")
        buyer.phone=Request.POST.get("phone")
        buyer.email=Request.POST.get("email")
        buyer.address=Request.POST.get("adress")
        pin=Request.POST.get("pin")
        if pin=="":
            pass
        else:
            buyer.pin=Request.POST.get("pin")
        buyer.city=Request.POST.get("city")
        buyer.state=Request.POST.get("state")
        if(Request.FILES.get("pic1")):
            buyer.pic=Request.FILES.get("pic1")
        buyer.save()
        return HttpResponseRedirect("/profile/")

    return render(Request,"update-profile.html",{"buyer":buyer})

@login_required(login_url="/login/")    
def wishlistPage(Request,id):
    buyer=Buyer.objects.get(username=Request.user.username)
    product=Product.objects.get(id=id)
    try:
        w=Wishlist.objects.get(product=product,buyer=buyer)
    except:
        w=Wishlist()
        w.product=product
        w.buyer=buyer
        w.save()
    return HttpResponseRedirect("/profile/")

@login_required(login_url="/login/")
def deletewishlist(Request,id):
    w=Wishlist.objects.get(id=id)
    w.delete()
    return HttpResponseRedirect("/profile/")
def newsLatter(Request):
    if(Request.method=="POST"):
        email=Request.POST.get("email")
        n=NewsLatter()
        n.email=email
        try:
            n.save()
            success(Request,"Thanks To Subscribe Our Newslatter Service!!!")

        except:
            error(Request,"Your Email ID Is Already Subscribed")
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")

def forgetPass1(Request):
    if(Request.method=="POST"):
        username=Request.POST.get("username")
        try:
           buyer=Buyer.objects.get(username=username)
           otp=randint(100000,999999)
           buyer.otp=otp
           buyer.save()
           subject = 'OTP For Password Reset!!! Team Shupershop'
           message ="""Hello """+buyer.name +""",\n"""+"""OTP For Password Reset Is """+str(otp)+""". Please Never Share Your OTP With Anyone."""
           email_from = settings.EMAIL_HOST_USER
           recipient_list = [buyer.email,]
           send_mail( subject, message, email_from, recipient_list )
           Request.session["reset-password-user"]=buyer.username
           Request.session["flag"]=1
           return HttpResponseRedirect("/forget-password2/")
        except:
           error(Request,"Username Not Found Our Data Record")
    return render(Request,"forget1.html")

def forgetPass2(Request):
    user=Request.session.get("reset-password-user",None)
    flag=Request.session.get("flag",None)
    if(Request.method=="POST"):
        otp=Request.POST.get("otp")
        buyer=Buyer.objects.get(username=user)
        if(int(otp)==buyer.otp):
            Request.session["flag"]=2
            return HttpResponseRedirect("/forget-password3/")
        else:
            error(Request,"Invalid OTP")
            return HttpResponseRedirect("/forget-password1/")
    if(user and flag==1):
        return render(Request,"forget2.html")
    else:
        return HttpResponseRedirect("/forget-password1/")
def forgetPass3(Request):
    user=Request.session.get("reset-password-user",None)
    flag=Request.session.get("flag",None)
    if(Request.method=="POST"):
        password=Request.POST.get("password")
        cpassword=Request.POST.get("cpassword")
        if(password==cpassword):
            user=User.objects.get(username=user)
            user.set_password(password)
            user.save()
            del Request.session["reset-password-user"]
            del Request.session["flag"]
            success(Request,"Reset Password Sucessfull")
            return HttpResponseRedirect("/login/")
        else:
            error(Request,"Password And Confirm Password Doesn't Match")
    if(user and flag==2):
        return render(Request,"forget3.html")
    else:
        return HttpResponseRedirect("/forget-password1/")