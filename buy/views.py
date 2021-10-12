from django.shortcuts import render,redirect
from .forms import OrderForm
from django.utils import timezone
from django.contrib import messages
from .models import Order, Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
@login_required
def order(request):
    if request.method=='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
                ordering = form.save(commit=False)
                ordering.order_time = timezone.now()
                ordering.user = request.user
                ordering.save()
                messages.success(request,"주문을 성공하셨습니다")
                return redirect('root')
    else:
        form = OrderForm()
    
    context = {'form':form}
    return render(request,"buy/order_form.html",context)


@login_required
def order_detail(request):
    order_list = Order.objects.filter(user_id=request.user.id)
    # product = Product.objects.all()
    context = {'order':order_list}
    return render(request,'buy/order_detail.html',context)

# @login_required
# def order_change(request):
#     if request.method =="POST":
#         form = OrderForm(request.POST, instance=request.user)
#         if form.is_valid():
#             ordering = form.save(commit=False)
#             ordering.order_time = timezone.now()
#             # ordering.user = request.user
#             ordering.save()
#     else:
#         form = OrderForm(instance=request.user)

    context = {'form':form}
    return render(request,"buy/order_form.html",context)

@login_required
def order_discard(request):
    order = Order.objects.filter(user_id=request.user.id)
    order.delete()
    messages.success(request,"주문을 취소했습니다.")
    return redirect("root")