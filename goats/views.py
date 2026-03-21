from django.shortcuts import render, get_object_or_404, redirect
from .models import Goat, DeathRecord, SaleRecord
from .forms import GoatForm
from .forms import DeathRecordForm, SaleRecordForm
from django.db.models import Sum

def dashboard(request):

    total_goats = Goat.objects.count()

    alive_goats = Goat.objects.filter(is_alive=True, is_sold=False).count()

    sold_goats = Goat.objects.filter(is_sold=True).count()

    dead_goats = Goat.objects.filter(is_alive=False, is_sold=False).count()

    total_purchase = Goat.objects.aggregate(
        Sum('purchase_price')
    )['purchase_price__sum'] or 0

    total_sales = SaleRecord.objects.aggregate(
        Sum('sale_price')
    )['sale_price__sum'] or 0

    profit = total_sales - total_purchase

    if sold_goats > 0:
        avg_profit_per_goat = profit / sold_goats
    else:
        avg_profit_per_goat = 0

    context = {
        "total_goats": total_goats,
        "alive_goats": alive_goats,
        "sold_goats": sold_goats,
        "dead_goats": dead_goats,
        "total_purchase": total_purchase,
        "total_sales": total_sales,
        "profit": profit,
        "avg_profit_per_goat": avg_profit_per_goat
    }

    return render(request, "goats/dashboard.html", context)
def goat_list(request):
    goats = Goat.objects.all()
    return render(request, 'goats/goat_list.html', {'goats': goats})

def add_goat(request):

    if request.method == 'POST':
        form = GoatForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('goat_list')

    else:
        form = GoatForm()

    return render(request, 'goats/add_goat.html', {'form': form})

def goat_detail(request, pk):
    goat = get_object_or_404(Goat, pk=pk)
    kids = goat.kids.all()  # goats where this goat is the mother

    context = {
        'goat': goat,
        'kids': kids
    }

    return render(request, 'goats/goat_detail.html', context)

def record_death(request, pk):

    goat = get_object_or_404(Goat, pk=pk)

    if request.method == "POST":

        form = DeathRecordForm(request.POST)

        if form.is_valid():

            death = form.save(commit=False)
            death.goat = goat
            death.save()

            goat.is_alive = False
            goat.save()

            return redirect('goat_detail', pk=goat.id)

    else:
        form = DeathRecordForm()

    return render(request, 'goats/record_death.html', {
        'form': form,
        'goat': goat
    })

def record_sale(request, pk):

    goat = get_object_or_404(Goat, pk=pk)

    if goat.is_sold:
        return redirect('goat_detail', pk=goat.id)

    if request.method == "POST":

        form = SaleRecordForm(request.POST)

        if form.is_valid():

            sale = form.save(commit=False)

            sale.goat = goat

            sale.save()

            goat.is_sold = True
            goat.is_alive = False
            goat.save()

            return redirect('goat_detail', pk=goat.id)

    else:
        form = SaleRecordForm()

    return render(request, 'goats/record_sale.html', {
        'form': form,
        'goat': goat
    })
