from django.shortcuts import render, get_object_or_404, redirect
from .models import Goat
from .forms import GoatForm
from .forms import DeathRecordForm, SaleRecordForm


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
