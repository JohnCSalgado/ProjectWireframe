from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, UserManager
from .models import Order, Product
from django.db.models import Sum
import bcrypt

# Create your views here.


def index(request):
    request.session.flush()
    return render(request, 'index.html')


def register(request):  # post redirect
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        # hash the password
        hashed_pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        # create a user
        new_user = User.objects.create(
            first_name=request.POST['first_name'], last_name=request.POST[
                'last_name'], email=request.POST['email'], password=hashed_pw
        )
        # create a session
        request.session['user_id'] = new_user.id
        return redirect('/success')
    return redirect('/')


# render the success page


def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])
    context = {
        'user': this_user[0]
    }

    return render(request, 'success.html', context)


# log in

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/success')
    return redirect('/')
# log out


def logout(request):
    request.session.flush()
    return redirect('/')

def storefront(request):
    allItems = Product.objects.all()
    context = {
        "allItems": Product.objects.all()
    }
    return render(request, "storefront.html", context)

def addItem(request):
    Product.objects.create(
        itemName=request.POST['itemName'],
        description=request.POST['description'],
        price=request.POST['price'],
    )
    return redirect('/storefront')

def deleteItem(request, item_id):
    # NOTE: delete one Item!
    to_delete = Product.objects.get(id=item_id)
    to_delete.delete()
    return redirect('/storefront')

def checkout(request):
    last = Order.objects.last()
    price = last.totalPrice
    fullOrder = Order.objects.aggregate(Sum('quantity_ordered'))['quantity_ordered__sum']
    fullPrice = Order.objects.aggregate(Sum('totalPrice'))['totalPrice__sum']
    context = {
        'orders':fullOrder,
        'total':fullPrice,
        'bill':price,
    }
    return render(request, 'checkout.html', context)

def purchase(request):
    if request.method == 'POST':
        theItem = Product.objects.filter(id=request.POST['id'])
        if not theItem:
            return redirect('/storefront')
        else:
            quantity = int(request.POST['quantity'])
            total = quantity*(float(theItem[0].price))
            Order.objects.create(
                quantity_ordered=quantity, 
                totalPrice=total
            )
            return redirect('/checkout/')
    else:
        return redirect('/storefront')