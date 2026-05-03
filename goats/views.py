from django.shortcuts import render, get_object_or_404, redirect
from .models import Goat, DeathRecord, SaleRecord
from .forms import GoatForm
from .forms import DeathRecordForm, SaleRecordForm
from django.db.models import Sum, Count, Avg
from django.db import IntegrityError
from django.shortcuts import redirect

def home(request):
    return redirect('/goats/')

def dashboard(request):

    total_goats = Goat.objects.count()

    alive_goats = Goat.objects.filter(status='alive').count()
    sold_goats = Goat.objects.filter(status='sold').count()
    dead_goats = Goat.objects.filter(status='dead').count()

    total_purchase = Goat.objects.aggregate(
        Sum('purchase_price')
    )['purchase_price__sum'] or 0

    total_sales = SaleRecord.objects.aggregate(
        Sum('sale_price')
    )['sale_price__sum'] or 0

    profit = total_sales - total_purchase

    avg_profit_per_goat = profit / sold_goats if sold_goats > 0 else 0

    # -------------------------
    # CHART DATA (FIXED + SAFE ORDER)
    # -------------------------
    data = Goat.objects.values('status').annotate(count=Count('id'))

    status_order = ['alive', 'sold', 'dead']

    data_dict = {item['status']: item['count'] for item in data}

    labels = [status.capitalize() for status in status_order]
    counts = [data_dict.get(status, 0) for status in status_order]

    context = {
        "total_goats": total_goats,
        "alive_goats": alive_goats,
        "sold_goats": sold_goats,
        "dead_goats": dead_goats,
        "total_purchase": total_purchase,
        "total_sales": total_sales,
        "profit": profit,
        "avg_profit_per_goat": avg_profit_per_goat,
        "labels": labels,
        "counts": counts,
    }
    
    return render(request, "goats/dashboard.html", context)

# =========================
# GOAT LIST (FIXED FILTER LOGIC)
# =========================
def goat_list(request):

    query = request.GET.get('q')
    status = request.GET.get('status')

    goats = Goat.objects.all()

    if query:
        goats = goats.filter(tag_number__icontains=query)

    if status:
        goats = goats.filter(status=status)

    return render(request, 'goats/goat_list.html', {'goats': goats})


# =========================
# ADD GOAT
# =========================
def add_goat(request):

    if request.method == 'POST':
        form = GoatForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('goat_list')

    else:
        form = GoatForm()

    return render(request, 'goats/add_goat.html', {'form': form})


# =========================
# GOAT DETAIL
# =========================
def goat_detail(request, pk):

    goat = get_object_or_404(Goat, pk=pk)
    kids = goat.kids.all()

    return render(request, 'goats/goat_detail.html', {
        'goat': goat,
        'kids': kids
    })


# =========================
# RECORD DEATH
# =========================
def record_death(request, pk):

    goat = get_object_or_404(Goat, pk=pk)

    if request.method == "POST":
        form = DeathRecordForm(request.POST)

        if form.is_valid():
            death = form.save(commit=False)
            death.goat = goat
            death.save()

            goat.status = 'dead'
            goat.save()

            return redirect('goat_list')

    else:
        form = DeathRecordForm()

    return render(request, 'goats/record_death.html', {
        'form': form,
        'goat': goat
    })


# =========================
# RECORD SALE
# =========================
def record_sale(request, pk):

    goat = get_object_or_404(Goat, pk=pk)

    if goat.status in ['dead', 'sold']:
        return redirect('goat_detail', pk=goat.pk)

    if request.method == "POST":
        form = SaleRecordForm(request.POST)

        if form.is_valid():
            sale = form.save(commit=False)
            sale.goat = goat
            sale.save()

            goat.status = 'sold'
            goat.save()

            return redirect('goat_list')

    else:
        form = SaleRecordForm()

    return render(request, 'goats/record_sale.html', {
        'form': form,
        'goat': goat
    })