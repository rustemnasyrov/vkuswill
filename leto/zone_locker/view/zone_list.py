import threading
from django.views.generic import ListView
from ..models import Zone
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

class ZoneListView(ListView):
    model = Zone
    template_name = 'zone_list.html'
    
    context_object_name = 'zones'
    ordering = 'number' # добавленный атрибут

# Создаем объект блокировки
lock = threading.Lock()

@csrf_exempt
def zone_lock(request, pk):
    # Блокируем блокировку
    lock.acquire()

    zone = get_object_or_404(Zone, pk=pk)

    if request.method == 'POST':
        locked = request.POST.get('locked')
        lock_time = request.POST.get('lock_time')
        locked_by = request.POST.get('locked_by')

        if locked == 'true':
            if not zone.locked and not Zone.has_zones_locked_by(locked_by):
                zone.locked = True
                zone.lock_time = lock_time
                zone.owner = locked_by
        else:
            unlock = (zone.owner == locked_by)
            if unlock:
                zone.locked = False
                zone.lock_time = None
                zone.owner = None

        zone.save()

        # Разблокируем блокировку
        lock.release()

        return JsonResponse(zone.response_params().append({'status': 'ok'}))
    else:
        # Разблокируем блокировку
        lock.release()

        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

# Обработчик GET-запроса по адресу '/zone/list/'
@require_http_methods(["GET"])
def zone_list(request):
    # Блокируем блокировку
    lock.acquire()

    # Здесь должна быть логика получения данных о состоянии зон из базы данных или другого источника
    zones = Zone.objects.all()

    # Преобразуем объекты модели в словари
    zones_data = []
    for zone in zones:
        zones_data.append(zone.response_params())

    # Отправляем JSON-объект с данными о зонах в ответе сервера

    # Разблокируем блокировку
    lock.release()

    return JsonResponse({"zones": zones_data})

