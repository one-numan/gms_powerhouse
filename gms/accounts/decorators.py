from functools import wraps
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            user = request.user

            # 🚫 Not logged in
            if not user.is_authenticated:
                return redirect('accounts:login')

            # ✅ Superuser always allowed
            if user.is_superuser:
                return view_func(request, *args, **kwargs)

            # 🚫 Role missing or not allowed (SAFE CHECK)
            if not hasattr(user, 'role') or user.role not in allowed_roles:
                return HttpResponseForbidden("403 Forbidden")

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator
