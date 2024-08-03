import json

from dateutil import parser
from django.db import transaction
from django.views import View
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views.generic import ListView

from doddy.models import DoddyUser, FarmType, UserFarm
from doddy.utils import get_init_data


# Create your views here.
def home(request):
    # print(request.user.tg_id)
    if request.user.is_authenticated:
        context = {
            'total_berries': request.user.balance,
            'current_energy': request.user.current_energy,
            'max_energy': request.user.max_energy,
            'energy_recover_per_sec': request.user.energy_recover_per_sec,
            'points_per_click': request.user.points_per_click,
            'active_page': 'home'
        }
        return render(request, 'Main.html', context)
    else:
        return render(request, 'auth.html')


@method_decorator(csrf_exempt, name='dispatch')
class IncreaseBalanceView(View):
    def post(self, request):
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)
                clicks_amount = data.get('clicks_amount', 0)
                ts = data.get('timestamp')
                try:
                    user_timestamp = parser.isoparse(ts)
                    if user_timestamp.tzinfo is None:
                        # If naive, make it aware using the current timezone
                        user_timestamp = timezone.make_aware(user_timestamp, timezone.utc)

                    user_timestamp = user_timestamp.astimezone(timezone.get_current_timezone())
                except ValueError as e:
                    print(e)
                    return JsonResponse({'error': 'Invalid timestamp format.'}, status=400)

                with transaction.atomic():
                    user = DoddyUser.objects.select_for_update().get(pk=request.user.pk)
                    res = user.update_energy(user_timestamp, clicks_amount)
                    if not res:
                        return JsonResponse({'status': 'error'}, status=404)
                    user.balance += clicks_amount * user.points_per_click
                    user.save()
                    return JsonResponse({'status': 'success', 'new_balance': request.user.balance, 'new_energy': user.last_energy})
            except:
                return JsonResponse({'status': 'error'}, status=404)
        else:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class AuthView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            initdata = data.get('initdata')

            if not initdata:
                raise PermissionDenied

            tg_data = get_init_data(initdata)
            user = tg_data['user']

            request.user, created = DoddyUser.objects.get_or_create(
                tg_id=user['id'],
                defaults={
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'username': user['username'],
                    'language_code': user['language_code'],
                    'balance': 0
                }
            )
            if created:
                request.user.set_unusable_password()
                request.user.save()

            login(request, request.user)
            return JsonResponse({'status': 'OK'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)


class FarmsView(View):
    def get(self, request, *args, **kwargs):
        user_farms = request.user.farms.all()

        farm_types = FarmType.objects.all()

        farm_type_to_level = {farm.farm_type: farm.level for farm in user_farms}

        for ft in farm_types:
            ft.level = farm_type_to_level.get(ft, None)

        return render(request, 'Main_2.html', context={
            'farms': farm_types,
            'active_page': 'farms'
        })
