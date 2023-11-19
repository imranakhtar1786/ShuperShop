from django import template
register=template.Library()

@register.filter(name="paymentMode")
def paymentMode(Request,num):
    if num==0:
        return "COD"
    else:
        return "NetBanking"
    
@register.filter(name="paymentStatus")
def paymentStatus(Request,num):
    if num==0:
        return "Pending"
    else:
        return "Done"
    
@register.filter(name="orderStatus")
def orderStatus(Request,num):
    if num==0:
        return "Order is Placed"
    elif num==1:
        return "Order is Packed"
    elif num==2:
        return "Ready To Dispatch"
    elif num==3:
        return "Dispached"
    elif num==4:
        return "Out For Delivery"
    else:
        return "Delivered"
@register.filter(name="paymentTrack")
def paymentTrack(mode,status):
    if(mode==0 and status==0):
        return True
    elif(mode==1 and status==0):
        return True
    else:
        return False

@register.filter(name="status")
def status(mode,status):
    if(mode==1 and status==0):
        return True
    else:
        return False