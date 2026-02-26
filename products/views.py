from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Like, Comment, Category
from .forms import ProductForm, QidiruvForm, CommitForm, CategoryForm
from django.db.models import Q
from users.models import OrderItem


@login_required
def seller_sotgan_maxs(request):
    sold_items = OrderItem.objects.filter(
        product__created_by=request.user
    ).select_related("product", "order", "order__user").order_by("-order__created_at")

    return render(request, "seller/sold_items.html", {
        "sold_items":sold_items
    })


@login_required
def seller_comments(request):
    comments = Comment.objects.filter(
        product__created_by=request.user
    ).select_related("user", "product").order_by("-created_at")

    return render(request, "seller/comments_list.html", {
        "comments": comments
    })

@login_required
def category_list(request):
    categories = Category.objects.all().order_by("name")
    return render(request, "seller/category_list.html", {
        "categories": categories
    })

@login_required
def category_create(request):
    if request.method== "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("category_list")
    else:
        form =  CategoryForm()


        return render(request, "seller/category_form.html",{
            "form": form,
            "title": "Category qo'shish",
            "btn-text": "Saqlash"
        })


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk = pk)

    if request.method== "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect("category_list")
    else:
        form =  CategoryForm(instance=category)


        return render(request, "seller/category_form.html",{
            "form": form,
            "title": "Category tahrirlash",
            "btn-text": "Yangilash"
        })

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect("category_list")


def home(request):
    if request.user.is_authenticated and getattr(request.user, "role", None) == "seller":
        return redirect("seller_dashboard")
    products = Product.objects.all().order_by("-created_at")[:20]
    category = Category.objects.all().order_by("name")

    return render(request, "index.html", {"products":products, "category": category})

def sotuvchi_tek(user):
    return user.is_authenticated and getattr(user, "role", None) == "seller"

@login_required
def seller_dashboard(request):
    if not sotuvchi_tek(request.user):
        return redirect("home")
    return render(request, "seller/dashboard.html")

@login_required
def mahsular(request):
    if not sotuvchi_tek(request.user):
        return redirect("/")

    mahsulotlar = Product.objects.filter(created_by = request.user)
    return render(request, "seller/royxat.html", {"mahsulotlar":mahsulotlar})

@login_required
def mahsulot_add(request):
    if not sotuvchi_tek(request.user):
        return redirect("home")

    form = ProductForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        yangi = form.save(commit=False)
        yangi.created_by = request.user
        yangi.save()
        return redirect("mahsulotlarim")

    return render(request, "seller/form.html", {"form": form, "is_edit":False})


@login_required
def mahsulot_edit(request, id):
    if not sotuvchi_tek(request.user):
        return redirect("/")

    mahsulot = get_object_or_404(Product, id=id, created_by=request.user)

    form = ProductForm(request.POST or None, request.FILES or None, instance=mahsulot)

    if form.is_valid():
        form.save()
        return redirect("mahsulotlarim")

    return render(request, "seller/form.html", {"form": form})


@login_required
def mahsulot_delete(request,id):
    if not sotuvchi_tek(request.user):
        return redirect("/")

    mahsulot = get_object_or_404(Product, id=id, created_by=request.user)

    if request.method == "POST":
        mahsulot.delete()
        return redirect("seller_dashboard")

    return render(request, "seller/Ochirish.html", {"mahsulot": mahsulot})

def maxsulotlar(request):
    category = Category.objects.all().order_by("name")

    form = QidiruvForm(request.GET)
    q = ""
    if form.is_valid():
        q = form.cleaned_data.get("q") or ""

    cat = request.GET.get("cat") or ""

    queryset = Product.objects.all().order_by("-created_at")

    if q:
        queryset = queryset.filter(Q(title__icontains=q) | Q(desc__icontains=q))

    if cat:
        queryset = queryset.filter(category_id=cat)

    return render(request, "maxsulotlar.html", {
        "maxsulotlar": queryset,
        "category": category,
        "form": form,
        "q": q,
        "cat": cat,
    })

def maxsulot_detail(request, id):
    maxsulot = get_object_or_404(Product,  id=id)

    liked = False

    if request.user.is_authenticated:
        liked = Like.objects.filter(user = request.user, product= maxsulot).exists()

    comment_form = CommitForm()

    return render(request, "shop/detail.html", {
        "maxsulot": maxsulot,
        "liked": liked,
        "comment_form": comment_form,
    })

@login_required
def like_toggle(request,id):
    product = get_object_or_404(Product, id=id)

    like = Like.objects.filter(user=request.user, product=product).first()
    if like:
        like.delete()
    else:
        Like.objects.create(user=request.user, product=product)

    return redirect("mahsulot_detail", id=product.id)


@login_required
def sevimlilar(request):

    mahsulotlar = Product.objects.filter(likes__user=request.user).order_by("-created_at")
    return render(request, "shop/sevimlilar.html", {"mahsulotlar":mahsulotlar})


@login_required
def comment_qoshish(request, id):
    mahsulot = get_object_or_404(Product, id=id)

    form = CommitForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.product = mahsulot
        comment.save()
    return redirect("mahsulot_detail", id=mahsulot.id)


@login_required
def comment_tahrir(request, id):
    comment = get_object_or_404(Comment, id=id)
    if comment.user != request.user and not request.user.is_staff:
        return redirect("mahsulot_detail", id=comment.product.id)

    form = CommitForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect("mahsulot_detail", id=comment.product.id)
    return render(request, "shop/comment_form.html", {"form": form, "comment": comment})


@login_required
def comment_ochir(request, id):
    comment = get_object_or_404(Comment, id=id)
    if comment.user != request.user and not request.user.is_staff:
        return redirect("mahsulot_detail", id=comment.product.id)

    if request.method == "POST":
        pid = comment.product.id
        comment.delete()
        return redirect("mahsulot_detail", id=pid)
    return render(request, "shop/comment_form.html", {"comment": comment})



















