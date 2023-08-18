from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Zone

#def zone_list(request):
#    zones = Zone.objects.all()
#    return render(request, 'zone_list.html', {'zones': zones})

def zone_detail(request, pk):
    zone = Zone.objects.get(pk=pk)
    return render(request, 'zone_detail.html', {'zone': zone})
