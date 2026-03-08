from django.shortcuts import render, get_object_or_404
from .models import Goat


def goat_list(request):
    goats = Goat.objects.all()
    return render(request, 'goats/goat_list.html', {'goats': goats})


def goat_detail(request, pk):
    goat = get_object_or_404(Goat, pk=pk)
    kids = goat.kids.all()  # goats where this goat is the mother

    context = {
        'goat': goat,
        'kids': kids
    }

    return render(request, 'goats/goat_detail.html', context)
