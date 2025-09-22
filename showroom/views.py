from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, Bike, CartItem

# Home Page
def home(request):
    companies = Company.objects.all()
    return render(request, "showroom/home.html", {"companies": companies})


# Bike List for a Company
def bike_list(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    bikes = company.bikes.all()
    return render(request, "showroom/bike_list.html", {"company": company, "bikes": bikes})


# Add to Cart
def add_to_cart(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)
    if bike.stock > 0:
        cart_item, created = CartItem.objects.get_or_create(bike=bike)
        cart_item.quantity += 1
        cart_item.save()

        bike.stock -= 1
        bike.save()
    return redirect("cart")


# Buy Now (direct purchase)
def buy_now(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)
    if bike.stock > 0:
        bike.stock -= 1
        bike.save()
        items = [(bike, 1, bike.price)]  # (bike, qty, subtotal)
        return render(request, "showroom/bill.html", {"items": items, "total": bike.price})
    return redirect("bike_list", company_id=bike.company.id)


# View Cart
def view_cart(request):
    items = CartItem.objects.all()
    total = sum([item.get_total() for item in items])
    return render(request, "showroom/cart.html", {"items": items, "total": total})


# Remove from Cart
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.bike.stock += item.quantity
    item.bike.save()
    item.delete()
    return redirect("cart")


# Generate Bill
def generate_bill(request):
    items = CartItem.objects.all()
    bill_data = [(item.bike, item.quantity, item.get_total()) for item in items]
    total = sum([item.get_total() for item in items])
    CartItem.objects.all().delete()  # clear cart
    return render(request, "showroom/bill.html", {"items": bill_data, "total": total})
