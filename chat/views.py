from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Xabar
from .forms import XabarForm


@login_required
def sotuvchiga_yozish(request, product_id):
    mahsulot = get_object_or_404(Product, id=product_id)

    sotuvchi = mahsulot.created_by
    if sotuvchi is None:
        return redirect("mahsulot_detail", id=mahsulot.id)

    form = XabarForm(request.POST or None)
    if form.is_valid():
        x = form.save(commit=False)
        x.product = mahsulot
        x.sender = request.user
        x.receiver = sotuvchi
        x.save()
        return redirect("mahsulot_detail", id=mahsulot.id)
    return render(request, "shop/xabarlar.html", {"form":form, "mahsulot":mahsulot})

def xabarlarim(request):

    xabarlar = Xabar.objects.filter(receiver=request.user).order_by("-created_at")
    return render(request, "shop/xabarlar.html", {"xabarlar":xabarlar})















