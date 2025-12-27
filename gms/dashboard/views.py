from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def dashboard_router(request):
    """
    Redirect users to role-based dashboards.
    """
    user = request.user
    print(user.role,user            )
    if user.is_superuser:
        print("Super User")
        return redirect('/admin/')

    if user.role == 'organization_manager':

        print("organization_manager")
        return redirect('/dashboard/org/')

    if user.role == 'gym_manager':
        print("gym_manager")
        return redirect('/dashboard/branch/')

    if user.role == 'gymown':
        print("gymown")
        return redirect('/dashboard/staff/')

    return redirect('/accounts/login/')


@login_required
def dashboard_org(request):
    user = request.user
    data = {
        'name': f'{user.role}',
        'started_in': 2009,
        'city': 'Noida'
    }
    return JsonResponse(data)