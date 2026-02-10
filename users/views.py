
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from  .forms import ProfilForm ,XabarForm
from .models import *
from django.db.models import Q
from django.db import transaction
from .models import Cart
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views import View
from .utls import generate_code
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

@login_required
def order_history(request):
    orders = Order.objects.filter(
        user = request.user
    ).prefetch_related("order_items__product").order_by("-id")

    return render(request, "shop/order_history.html", {
        "orders":orders
    })



@login_required
def messages_view(request, product_id=None, user_id=None):
    User = get_user_model()
    me = request.user

    conversations = Xabar.objects.filter(Q(sender=me) | Q(receiver=me)).order_by("-created_at")

    product = None
    other = None
    chat_messages = Xabar.objects.none()

    if product_id and user_id:
        product = get_object_or_404(Product, id=product_id)
        other = get_object_or_404(User, id=user_id)

        chat_messages = Xabar.objects.filter(product=product).filter(
            Q(sender=me, receiver=other) | Q(sender=other, receiver=me)
        ).order_by("created_at")

    form = XabarForm(request.POST or None)
    if request.method == "POST" and form.is_valid() and product and other:
        x = form.save(commit=False)
        x.product = product
        x.sender = me
        x.receiver = other
        x.save()
        return redirect("messages", product_id=product.id, user_id=other.id)

    return render(request, "shop/messages.html", {
        "conversations": conversations,
        "chat_messages": chat_messages,
        "form": form,
        "product": product,
        "other": other,
    })

@login_required
def profil(request):
    form = ProfilForm(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect("profil")
    return render(request, "shop/profil.html", {"form":form})


class RegisterView(View):
    def get(self, request):
        return render(request, 'auth/register.html')

    def post(self,request):
        username = request.POST['username']
        phone = request.POST['phone']
        email = request.POST['email']
        image = request.FILES['image']
        role = request.POST['role']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'auth/register.html', {
                "error": "Bu username band"
            })
        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'auth/register.html', {
                "error": "Bu email allaqachon ro'yxatdan o'tgan"
            })

        if password !=confirm_password:
            return render(request, 'auth/register.html', {
                "error": "Parollar mos emas "
            })

        user = CustomUser.objects.create_user(
            username = username,
            email = email,
            phone = phone,
            image = image,
            password=password,
            role=role,
            is_active = False
        )

        code = generate_code()


        subject = "Email tasdiqlash kodi"
        from_email = settings.EMAIL_HOST_USER
        to = [email]

        html_content = render_to_string(
            "auth/email_code.html",
            {"code": code, "username": username}
        )

        msg = EmailMultiAlternatives(
            subject=subject,
            body=f"Sizning tasdiqlash kodingiz: {code}",
            from_email=from_email,
            to=to

        )
        EmailCode.objects.create(user=user, code=code)

        request.session['user_id'] = user.id

        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
        except Exception as e:
            # email ketmasa user yaratilib qolmasin desangiz:
            user.delete()
            return render(request, 'auth/register.html', {
                "error": f"Email yuborilmadi. Sabab: {e}"
            })
        return redirect('verify_email')


class Verify_EmailView(View):
    def get(self,request):
        return render(request, 'auth/verify_email.html')

    def post(self,request):
        code = request.POST['code']

        user_id = request.session.get('user_id')
        email_code = EmailCode.objects.filter(user_id=user_id, code=code, is_activated=False).last()

        if email_code is None or email_code.code != code:
            return render(request, 'auth/verify_email.html', {
                "error": "Kiritilgan Code Noto'g'ri"
            })
        time = timezone.now()
        if time > email_code.expires_at:
            return render(request, 'auth/verify_email.html', {
                "error": "Yaroqli muddati o'tgan"
            })

        email_code.is_activated = True
        email_code.save()

        user = CustomUser.objects.get(id=user_id)

        user.is_active = True
        user.save()
        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,  username=username, password=password)

        if user is None:
            return render(request, 'auth/login.html', {
                "error": "Login yoki Parol Noto'g'ri"
            })
        login(request,user)

        if getattr(user, "role", None) == "seller":
            return redirect("seller_dashboard")
        return redirect('home')





def logout1(request):
    logout(request)
    return redirect('home')

@login_required
def add_to_cart(request,  id):
    product = Product.objects.get(id=id)

    quantity = int(request.POST.get("quantity", 1))
    cart_item = Cart.objects.filter(user=request.user, product=product).first()
    if cart_item:
        cart_item.quantity += int(quantity)
        cart_item.save()
    else:
        Cart.objects.create(
            user=request.user,
            product=product,
            quantity=quantity
        )

    return redirect('home')


@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).select_related("product")
    if not cart_items:
        return redirect('home')


    total_price = sum((item.total_price for item in cart_items), 0)


    if request.method == "GET":
        return render(request, "shop/checkout.html", {
            "cart_items": cart_items,
            "total_price": total_price
        })

    with transaction.atomic():
        order = Order.objects.create(
            user=request.user
        )

        for item in cart_items:
            OrderItem.objects.create(
                product=item.product,
                order = order,
                quantity=item.quantity,
                price=item.product.price
            )


        cart_items.delete()
    return redirect('home')





@login_required
def cart_view(request):
    items = Cart.objects.filter(user=request.user).select_related('product')
    total = sum(item.product.price * item.quantity for item in items)
    return render(request,  "shop/cart.html", {"items": items, "total":total})

@login_required
def cart_update(request, id):
    item = Cart.objects.get(id=id, user=request.user)
    item.quantity = int(request.POST["quantity"])
    item.save()
    return redirect("cart")

@login_required
def cart_remove(request, id):
    item = Cart.objects.get(id=id, user=request.user)
    item.delete()
    return redirect("cart")


