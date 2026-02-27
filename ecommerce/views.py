from django.shortcuts import render,redirect
from django.views import View
from .models import Product,Cart,Customer,OrderPlaced,Contact
from django.db.models import Q
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404

class Productview(View):
    def get(self,request):
      electronics = Product.objects.filter(category='E')[:4]
      fashion = Product.objects.filter(category='F')[:4]
      grocery = Product.objects.filter(category='G')[:4]
      vegetable = Product.objects.filter(category='V')[:4]

      return render(request,'home.html',{'electronic':electronics,'fashions':fashion,'grocery':grocery,'vegetables':vegetable})
    

class ProductDetailView(View):
   def get(self,request,pk):
    product = Product.objects.get(pk=pk)
    return render(request,'product_detail.html',{'product':product})
   

def electronics(request,data=None):
   if data == None:
      electronic = Product.objects.filter(category='E')
   elif data == 'Laptop' or data == 'Phone':
      electronic = Product.objects.filter(category='E').filter(brand=data)
   elif data == 'below':
      electronic = Product.objects.filter(category='E').filter(selling_price__lt=10000) 
   elif data == 'above':
      electronic = Product.objects.filter(category='E').filter(selling_price__gt=10000)     
   return render(request,'electronics.html',{'electronic':electronic})


def Fashion(request,data=None):
   if data == None:
      fashion = Product.objects.filter(category='F')
   elif data == 'Jeans' or data == 'shoes' or data == 'shirt':
      fashion = Product.objects.filter(category='F').filter(brand=data)     
   return render(request,'fashion.html',{'fashion':fashion})


def Grocery(request,data=None):
   if data == None:
      grocery = Product.objects.filter(category='G')
   elif data == 'Food' or data == 'Oil' or data == 'Castmetic':
      grocery = Product.objects.filter(category='G').filter(brand=data)     
   return render(request,'grocery.html',{'grocery':grocery})


def Vegetables(request,data=None):
   if data == None:
      vegetable = Product.objects.filter(category='V')
   elif data == 'Root' or data == 'Surface':
      vegetable = Product.objects.filter(category='V').filter(brand=data)     
   return render(request,'Vegetables.html',{'vegetable':vegetable})


def shop(request):
    products = Product.objects.all()

    # 🔹 Category Filter
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)

    # 🔹 Sorting
    sort = request.GET.get('sort')
    if sort == 'low':
        products = products.order_by('discounted_price')
    elif sort == 'high':
        products = products.order_by('-discounted_price')

    context = {
        'products': products
    }
    return render(request, 'shop.html', context)

class CustomerRegistrationView(View):
   def get(self,request):
    form = CustomerRegistrationForm()
    return render(request,'registration.html',{'forms':form})
   def post(self,request):
    form = CustomerRegistrationForm(request.POST)
    if form.is_valid():
       messages.success(request, 'Congratulations!! Registered Successfully')
       form.save()
    return render(request,'registration.html',{'forms':form})   


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
   def get(self,request):
      form = CustomerProfileForm()
      return render(request,'profile.html',{'form':form})
   
   def post(self,request):
      form = CustomerProfileForm(request.POST)
      if form.is_valid():
         usr = request.user
         name = form.cleaned_data['name']
         address = form.cleaned_data['address']
         city = form.cleaned_data['city']
         pincode = form.cleaned_data['pincode']
         state = form.cleaned_data['state']
         reg = Customer(user= usr,name=name, address=address,city=city,pincode=pincode,state=state)
         reg.save()
         messages.success(request,'Congratulations !! Profile Update Successfully')
         return redirect('profile') 
      return render(request,'profile.html',{'form':form,'active':'bg-blue-600'}) 

@login_required
def address(request):
    addresses = Customer.objects.filter(user=request.user)
    return render(request, 'address.html', {'addresses': addresses,'active': 'bg-blue-600'}) 

class ProductDetailView(View):
   def get(self,request,pk):
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    if request.user.is_authenticated:
     item_already_in_cart = Cart.objects.filter(product=product, user=request.user).exists()
    return render(request,'product_detail.html',{'product':product,'item_already_in_cart': item_already_in_cart})


@login_required
def add_to_cart(request):
   user=request.user
   product_id = request.GET.get('prod_id')    
   product = Product.objects.get(id=product_id)
   cart_item, created = Cart.objects.get_or_create(
        user=user,
        product=product
    )

   if not created:
        cart_item.quantity += 1
        cart_item.save()

   #Cart(user=user,product=product).save()
   return redirect('showcart')


@login_required
def show_cart(request):
   if request.user.is_authenticated:
      user = request.user   
      cart = Cart.objects.filter(user=user)

      amount = 0.0
      shipping_amount = 70.0

      for p in cart:
         temamount = (p.quantity * p.product.discounted_price)
         amount += temamount

      total_amount = amount + shipping_amount

      if cart:
         return render(request, 'addcart.html', {
            'carts': cart,
            'total_amount': total_amount,
            'amount': amount
         })
      else:
         return render(request, 'empty.html')


# ➕ Quantity Increase
def plus_quantity(request):
    prod_id = request.GET.get('prod_id')
    cart_item = get_object_or_404(Cart, product_id=prod_id, user=request.user)

    cart_item.quantity += 1
    cart_item.save()

    return redirect('showcart')


# ➖ Quantity Decrease
def minus_quantity(request):
    prod_id = request.GET.get('prod_id')
    cart_item = get_object_or_404(Cart, product_id=prod_id, user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('showcart')

def remove_cart(request):
    prod_id = request.GET.get('prod_id')
    cart_item = get_object_or_404(Cart, product_id=prod_id, user=request.user)
    cart_item.delete()
    return redirect('showcart')

@login_required
def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user

    # Sirf current user ke address
    addresses = Customer.objects.filter(user=user)

    # Sirf current user ke cart items
    cart_items = Cart.objects.filter(user=user)

    amount = 0.0
    shipping_amount = 70.0

    for item in cart_items:
        amount += item.quantity * item.product.discounted_price

    totalamount = amount + shipping_amount

    return render(request, 'checkout.html', {
        'addresses': addresses,
        'cart_items': cart_items,
        'amount': amount,
        'shipping_amount': shipping_amount,
        'totalamount': totalamount
    })

@login_required
def payment_done(request):
    if request.method == "POST":
        user = request.user
        custid = request.POST.get('custid')   # POST use karo
        customer = Customer.objects.get(id=custid)

        cart = Cart.objects.filter(user=user)

        for c in cart:   # cart queryset par loop
            OrderPlaced.objects.create(
                user=user,
                customer=customer,
                product=c.product,
                quantity=c.quantity
            )
            c.delete()

    return redirect("orders")
   
@login_required
def orders(request):
   op =OrderPlaced.objects.filter(user=request.user)
   return render(request,'order.html',{'order_placed': op})



def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        return render(request, 'contact.html', {'success': True})

    return render(request, 'contact.html')


def search(request):
    query = request.GET.get('query')
    products = []

    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    context = {
        'query': query,
        'products': products
    }

    return render(request, 'search_results.html', context)