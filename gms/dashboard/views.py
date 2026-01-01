from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from accounts.decorators import role_required
from django.shortcuts import render


@login_required
def dashboard_router(request):
    user = request.user
    
    print(f"Requesting {request}")
    if user.is_superuser:
        return redirect('admin:index')

    role = getattr(user, 'role', None)

    if role == 'organization_manager':
        return redirect('dashboard:org')

    if role == 'gym_manager':
        return redirect('dashboard:branch')

    if role == 'gymown':
        return redirect('dashboard:staff')

    # fallback (logged in but no role)
    return redirect('accounts:login')



@login_required
def dashboard_org(request):
    user = request.user
    data = {
        'name': f'{user.role}',
        'started_in': 2009,
        'city': 'Noida'
    }
    return JsonResponse(data)

def user_data(request):
    user = request.user

    if not user.is_authenticated:
        return {
            'name': 'Guest',
            'role': None,
        }

    return {
        'name': user.get_full_name() or user.username,
        'role': getattr(user, 'role', None),
    }

@role_required(['owner'])
def owner_dashboard(request):
    return render(request, 'dashboard/owner.html')

def fast_logout(request):
    logout(request)
    return redirect('accounts:login')


def blank_page(request):
    return render(request, 'blank.html')


@role_required(['owner','site_manager','gym_manager','staff'])
def sample_page(request):
    print(user_data(request=request))
    return render(request, 'blank.html')