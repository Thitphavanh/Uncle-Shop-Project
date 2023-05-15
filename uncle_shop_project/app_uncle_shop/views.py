from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.core.paginator import Paginator


def home(request):
    product = AllProduct.objects.all().order_by('id').reverse()[:3]
    preorder = AllProduct.objects.filter(quantity__lte=0)
    context = {'product': product, 'preorder': preorder}
    return render(request, 'app_uncle_shop/home.html', context)


def about(request):
    return render(request, 'app_uncle_shop/about.html')


def contact(request):
    return render(request, 'app_uncle_shop/contact.html')


def add_product(request):
    if request.user.profile.usertype != 'admin':
        return redirect('home-page')

    if request.method == 'POST' and request.FILES['imageupload']:
        data = request.POST.copy()
        name = data.get('name')
        price = data.get('price')
        detail = data.get('detail')
        imageurl = data.get('imageurl')
        quantity = data.get('quantity')
        unit = data.get('unit')

        new = AllProduct()
        new.name = name
        new.price = price
        new.detail = detail
        new.imageurl = imageurl
        new.quantity = quantity
        new.unit = unit

        file_image = request.FILES['imageupload']
        file_image_name = request.FILES['imageupload'].name.replace(' ', '')
        # print('File Images:', file_image)
        # print('File Images:', file_image_name)
        file_system_storage = FileSystemStorage()
        file_name = file_system_storage.save(file_image_name, file_image)
        upload_file_url = file_system_storage.url(file_name)
        new.images = upload_file_url[6:]

        new.save()

    return render(request, 'app_uncle_shop/add-product.html')


def all_products(request):
    # product = AllProduct.objects.all()
    product = AllProduct.objects.all().order_by('id').reverse()
    paginator = Paginator(product, 6)
    page = request.GET.get('page')
    product = paginator.get_page(page)
    context = {'product': product}
    return render(request, 'app_uncle_shop/all-product.html', context)


def register(request):
    if request.method == 'POST':
        data = request.POST.copy()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')

        new_user = User()
        new_user.username = email
        new_user.email = email
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.set_password(password)
        new_user.save()

        profile = Profile()
        profile.user = User.objects.get(username=email)
        profile.save()

        user = authenticate(username=email, password=password)
        login(request, user)
        return redirect('home-page')

    return render(request, 'app_uncle_shop/register.html')


def add_to_cart(request, pid):
    username = request.user.username
    user = User.objects.get(username=username)
    check = AllProduct.objects.get(id=pid)
    try:
        new_cart = Cart.objects.get(user=user, productid=str(pid))
        new_quan = new_cart.quantity + 1
        new_cart.quantity = new_quan
        calculate = new_cart.price * new_quan
        new_cart.total = calculate
        new_cart.save()

        # update ຈຳນວນຂອງກະຕ່າສິນຄ້າ ໃນຕອນນີ້
        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        update_quan = Profile.objects.get(user=user)
        update_quan.cartquan = count
        update_quan.save()
        return redirect('all-product-page')

    except:
        new_cart = Cart()
        new_cart.user = user
        new_cart.productid = pid
        new_cart.productname = check.name
        new_cart.price = int(check.price)
        new_cart.quantity = 1
        calculate = int(check.price) * 1
        new_cart.total = calculate
        new_cart.save()

        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        update_quan = Profile.objects.get(user=user)
        update_quan.cartquan = count
        update_quan.save()

        return redirect('all-product-page')


def my_cart(request):
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}
    if request.method == 'POST':
        data = request.POST.copy()
        productid = data.get('productid')
        # print('PID', productid)
        item = Cart.objects.get(user=user, productid=productid)
        item.delete()
        context['status'] = 'delete'

        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        update_quan = Profile.objects.get(user=user)
        update_quan.cartquan = count
        update_quan.save()

    mycart = Cart.objects.filter(user=user)
    count = sum([c.quantity for c in mycart])
    total = sum([c.total for c in mycart])

    context['mycart'] = mycart
    context['count'] = count
    context['total'] = total

    return render(request, 'app_uncle_shop/my-cart.html', context)


def my_cart_edit(request):
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        # print(data)
        if data.get('clear') == 'clear':
            print(data.get('clear'))
            Cart.objects.filter(user=user).delete()
            update_quan = Profile.objects.get(user=user)
            update_quan.cartquan = 0
            update_quan.save()
            return redirect('my-cart-page')

        edit_list = []
        for k, v in data.items():
            # print([k, v])
            if k[:2] == 'pd':
                pid = int(k.split('_')[1])
                dt = [pid, int(v)]
                edit_list.append(dt)
        # print('Edit list:', edit_list)
        for ed in edit_list:
            edit = Cart.objects.get(productid=ed[0], user=user)
            edit.quantity = ed[1]
            calculate = edit.price * ed[1]
            edit.total = calculate
            edit.save()

        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        update_quan = Profile.objects.get(user=user)
        update_quan.cartquan = count
        update_quan.save()
        return redirect('my-cart-page')

    mycart = Cart.objects.filter(user=user)
    context['mycart'] = mycart
    return render(request, 'app_uncle_shop/my-cart-edit.html', context)


def check_out(request):
    username = request.user.username
    user = User.objects.get(username=username)
    if request.method == 'POST':
        data = request.POST.copy()
        name = data.get('name')
        tel = data.get('tel')
        address = data.get('address')
        shipping = data.get('shipping')
        payment = data.get('payment')
        other = data.get('other')
        page = data.get('page')
        if page == 'information':
            context = {}
            context['name'] = name
            context['tel'] = tel
            context['address'] = address
            context['shipping'] = shipping
            context['payment'] = payment
            context['other'] = other

            mycart = Cart.objects.filter(user=user)
            count = sum([c.quantity for c in mycart])
            total = sum([c.total for c in mycart])

            context['mycart'] = mycart
            context['count'] = count
            context['total'] = total

            return render(request, 'app_uncle_shop/checkout-2.html', context)

        if page == 'confirm':
            print('Confirm')
            print(data)
            mycart = Cart.objects.filter(user=user)
            member_id = str(user.id).zfill(4)
            date_time = datetime.now().strftime("%Y%m%d%H%M%S")
            order_id = 'OD' + member_id + date_time
            for mc in mycart:
                order_product = OrderProduct()
                order_product.orderid = order_id
                order_product.productid = mc.productid
                order_product.productname = mc.productname
                order_product.price = mc.price
                order_product.quantity = mc.quantity
                order_product.total = mc.total
                order_product.save()

            order_pending = OrderPending()
            order_pending.orderid = order_id
            order_pending.user = user
            order_pending.name = name
            order_pending.tel = tel
            order_pending.address = address
            order_pending.shipping = shipping
            order_pending.payment = payment
            order_pending.other = other
            order_pending.save()

            Cart.objects.filter(user=user).delete()
            update_quan = Profile.objects.get(user=user)
            update_quan.cartquan = 0
            update_quan.save()
            return redirect('my-cart-page')

    return render(request, 'app_uncle_shop/checkout-1.html')


def order_prodcut(request):
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}

    order_pending = OrderPending.objects.filter(user=user)

    for od in order_pending:
        orderid = od.orderid
        order_product = OrderProduct.objects.filter(orderid=orderid)
        total = sum([o.total for o in order_product])
        od.total = total
        count = sum([o.quantity for o in order_product])

        if od.shipping == 'flash':
            shipping_cost = sum(
                [20 if i == 0 else 10 for i in range(count)])
        elif od.shipping == 'kerry':
            shipping_cost = sum(
                [20 if i == 0 else 8 for i in range(count)])
        elif od.shipping == '่j&t':
            shipping_cost = sum(
                [20 if i == 0 else 9 for i in range(count)])
        elif od.shipping == '่thailandpost':
            shipping_cost = sum(
                [20 if i == 0 else 12 for i in range(count)])
        else:
            shipping_cost = sum(
                [20 if i == 0 else 11 for i in range(count)])

        if od.payment == 'cod':
            shipping_cost += 10
        od.shipping_cost = shipping_cost

    context['allorder'] = order_pending

    return render(request, 'app_uncle_shop/order-product.html', context)


def all_order_prodcut(request):
    context = {}
    order_pending = OrderPending.objects.all()

    for od in order_pending:
        orderid = od.orderid
        order_product = OrderProduct.objects.filter(orderid=orderid)
        total = sum([o.total for o in order_product])
        od.total = total
        count = sum([o.quantity for o in order_product])

        if od.shipping == 'flash':
            shipping_cost = sum(
                [20 if i == 0 else 10 for i in range(count)])
        elif od.shipping == 'kerry':
            shipping_cost = sum(
                [20 if i == 0 else 8 for i in range(count)])
        elif od.shipping == '่j&t':
            shipping_cost = sum(
                [20 if i == 0 else 9 for i in range(count)])
        elif od.shipping == '่thailandpost':
            shipping_cost = sum(
                [20 if i == 0 else 12 for i in range(count)])
        else:
            shipping_cost = sum(
                [20 if i == 0 else 11 for i in range(count)])

        if od.payment == 'cod':
            shipping_cost += 10
        od.shipping_cost = shipping_cost

    context['allorder'] = order_pending

    return render(request, 'app_uncle_shop/all-order-product.html', context)


def upload_slip(request, orderid):
    if request.method == 'POST' and request.FILES['upload_slip']:
        data = request.POST.copy()
        slip_time = data.get('slip_time')
        bank_account = data.get('bank_account')

        update = OrderPending.objects.get(orderid=orderid)
        update.slip_time = slip_time
        update.bank_account = bank_account

        file_image_slip = request.FILES['upload_slip']
        file_image_name = request.FILES['upload_slip'].name.replace(' ', '')
        file_system_storage = FileSystemStorage()
        file_name = file_system_storage.save(file_image_name, file_image_slip)
        upload_file_url = file_system_storage.url(file_name)
        update.slip = upload_file_url[6:]

        update.save()

    order_product = OrderProduct.objects.filter(orderid=orderid)
    total = sum([o.total for o in order_product])
    order_pending_detail = OrderPending.objects.get(orderid=orderid)
    count = sum([o.quantity for o in order_product])

    if order_pending_detail.shipping == 'flash':
        shipping_cost = sum([20 if i == 0 else 10 for i in range(count)])
    elif order_pending_detail.shipping == 'kerry':
        shipping_cost = sum([20 if i == 0 else 8 for i in range(count)])
    elif order_pending_detail.shipping == 'j&t':
        shipping_cost = sum([20 if i == 0 else 9 for i in range(count)])
    elif order_pending_detail.shipping == '่thailandpost':
        shipping_cost = sum([20 if i == 0 else 12 for i in range(count)])
    else:
        shipping_cost = sum([20 if i == 0 else 11 for i in range(count)])

    if order_pending_detail.payment == 'cod':
        shipping_cost += 10

    context = {'orderid': orderid,
               'total': total,
               'shipping_cost': shipping_cost,
               'grandtotal': total + shipping_cost,
               'order_pending_detail': order_pending_detail,
               'count': count}

    return render(request, 'app_uncle_shop/upload-slip.html', context)


def update_paid(request, orderid, status):
    if request.user.profile.usertype != 'admin':
        return redirect('home-page')
    order_pending = OrderPending.objects.get(orderid=orderid)
    if status == 'confirm':
        order_pending.paid = True
    elif status == 'cancel':
        order_pending.paid = False
    order_pending.save()
    return redirect('all-order-product-page')


def update_tracking(request, orderid):
    if request.user.profile.usertype != 'admin':
        return redirect('home-page')

    if request.method == 'POST':
        order_pending = OrderPending.objects.get(orderid=orderid)
        data = request.POST.copy()
        tracking_number = data.get('tracking_number')
        order_pending.tracking_number = tracking_number
        order_pending.save()
        return redirect('all-order-product-page')

    order_pending = OrderPending.objects.get(orderid=orderid)
    order_product = OrderProduct.objects.filter(orderid=orderid)

    total = sum([o.total for o in order_product])
    order_pending.total = total
    count = sum([o.quantity for o in order_product])

    if order_pending.shipping == 'flash':
        shipping_cost = sum(
            [20 if i == 0 else 10 for i in range(count)])
    elif order_pending.shipping == 'kerry':
        shipping_cost = sum(
            [20 if i == 0 else 8 for i in range(count)])
    elif order_pending.shipping == '่j&t':
        shipping_cost = sum(
            [20 if i == 0 else 9 for i in range(count)])
    elif order_pending.shipping == '่thailandpost':
        shipping_cost = sum(
            [20 if i == 0 else 12 for i in range(count)])
    else:
        shipping_cost = sum(
            [20 if i == 0 else 11 for i in range(count)])

    if order_pending.payment == 'cod':
        shipping_cost += 10
    order_pending.shipping_cost = shipping_cost

    context = {"order_pending": order_pending,
               "order_product": order_product,
               "total": total, "count": count}

    return render(request, 'app_uncle_shop/update-tracking.html', context)


def my_order(request, orderid):
    username = request.user.username
    user = User.objects.get(username=username)

    order_pending = OrderPending.objects.get(orderid=orderid)
    if user != order_pending.user:
        return redirect('all-product-page')

    order_product = OrderProduct.objects.filter(orderid=orderid)

    total = sum([o.total for o in order_product])
    order_pending.total = total
    count = sum([o.quantity for o in order_product])

    if order_pending.shipping == 'flash':
        shipping_cost = sum(
            [20 if i == 0 else 10 for i in range(count)])
    elif order_pending.shipping == 'kerry':
        shipping_cost = sum(
            [20 if i == 0 else 8 for i in range(count)])
    elif order_pending.shipping == '่j&t':
        shipping_cost = sum(
            [20 if i == 0 else 9 for i in range(count)])
    elif order_pending.shipping == '่thailandpost':
        shipping_cost = sum(
            [20 if i == 0 else 12 for i in range(count)])
    else:
        shipping_cost = sum(
            [20 if i == 0 else 11 for i in range(count)])

    if order_pending.payment == 'cod':
        shipping_cost += 10
    order_pending.shipping_cost = shipping_cost

    context = {"order_pending": order_pending,
               "order_product": order_product,
               "total": total, "count": count}

    return render(request, 'app_uncle_shop/my-order.html', context)
