import json

from django.views import View
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login, authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from doddy.models import DoddyUser
from doddy.utils import get_init_data


# Create your views here.
def home(request):
    # print(request.user.tg_id)
    if request.user.is_authenticated:
        return render(request, 'Main.html')
    else:
        return render(request, 'auth.html')


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

