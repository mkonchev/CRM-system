from django.shortcuts import render, redirect
from apps.car.forms import CarForm


def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            car = form.save()
            return redirect('car_detail', pk=car.pk)
    else:
        form = CarForm()
    return render(request, 'cars/add_car.html', {'form': form})
