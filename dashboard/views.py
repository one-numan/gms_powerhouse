from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse
from accounts.decorators import role_required
from django.shortcuts import render
from members.forms import MemberCreateForm, MemberUpdateForm
from members.models import Member
from django.utils.timezone import now
from django.db.models import Q, Sum
from django.utils.timezone import localdate
from accounts.models import User
from subscriptions.models import Subscription, Payment
from subscriptions.forms import AddPaymentForm
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.db import transaction


from core.emails.member_emails import (
    send_member_created_email,
    send_staff_member_added_notification,
    send_member_payment_notification,
    send_staff_member_payment_notification
)
# from datetime import timedelta
# from django.shortcuts import render, redirect, get_object_or_404
# from django.utils.timezone import now

# from accounts.decorators import role_required
# from members.models import Member
# from subscriptions.models import Subscription
# from subscriptions.forms import AddPaymentForm


@login_required
def dashboard_router(request):
    user = request.user
    
    print(f"Requesting {request}")
    if user.is_superuser:
        return redirect('admin:index')

    print(user.role)
    role = getattr(user, 'role', None)

    if role == 'site_manager':
        return redirect('dashboard:org')

    if role == 'gym_manager':
        return redirect('dashboard:branch')

    if role == 'staff':
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


# def add_member(request):
#     return render(request, 'add_member.html')

@role_required(['owner','site_manager','gym_manager','staff'])
def sample_page(request):
    print(user_data(request=request))
    return render(request, 'blank.html')

@role_required(['owner','site_manager','gym_manager','staff'])
def add_member(request):
    """
    Create a gym member.

    Organization & Branch are injected from logged-in user.
    This avoids integrity errors and RBAC violations.
    """

    if request.method == 'POST':
        form = MemberCreateForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)

            # 🔐 RBAC enforcement
            member.organization = request.user.organization
            member.branch = request.user.branch
            member.save()

            send_member_created_email(member) 
            send_staff_member_added_notification(member=member,created_by=request.user)

            return redirect('dashboard:member_list')  # adjust later
    else:
        form = MemberCreateForm()

    return render(request, 'add_member.html', {
        'form': form
    })


@role_required(['owner', 'site_manager', 'gym_manager', 'staff'])
def member_list(request):

    members = Member.objects.filter(
        organization=request.user.organization,
        deleted_at__isnull=True
    )

    if request.user.role == 'staff':
        members = members.filter(branch=request.user.branch)

    # attach derived membership status
    member_data = []
    for member in members:
        member.membership_status = get_membership_status(member)
        member_data.append(member)

    return render(
        request,
        'member_list.html',
        {'members': member_data}
    )



def get_membership_status(member):
    """
    Returns membership status string for a member
    based on latest subscription.
    """
    today = now().date()

    latest_subscription = (
        Subscription.objects
        .filter(member=member)
        .order_by('-end_date')
        .first()
    )

    if not latest_subscription:
        return "No Membership"

    end_date = latest_subscription.end_date
    days_left = (end_date - today).days

    if days_left > 0:
        return f"Active ({days_left} days left)"
    elif days_left == 0:
        return "Expires Today"
    else:
        return f"Expired ({abs(days_left)} days ago)"






# @role_required(['owner', 'site_manager', 'gym_manager', 'staff'])
# @transaction.atomic
# def add_payment(request, member_id):
#     """
#     Add a payment for a member and create a subscription.

#     Business Rules:
#     - A member can have ONLY ONE active subscription at a time
#     - Old active subscription must be expired before creating a new one
#     - Payment is always linked to exactly ONE subscription

#     Flow:
#     Member → Subscription → Payment
#     """

#     # -------------------------
#     # Fetch member with RBAC
#     # -------------------------
#     member = get_object_or_404(
#         Member,
#         id=member_id,
#         organization=request.user.organization,
#         deleted_at__isnull=True
#     )

#     if request.method == 'POST':
#         form = AddPaymentForm(request.POST)

#         if form.is_valid():
#             # -------------------------
#             # Extract cleaned data
#             # -------------------------
#             plan = form.cleaned_data['plan']
#             payment_date = form.cleaned_data['payment_date']

#             # -------------------------
#             # Expire existing active subscription (CRITICAL FIX)
#             # -------------------------
#             active_subscription = (
#                 Subscription.objects
#                 .filter(
#                     member=member,
#                     status='active',
#                     deleted_at__isnull=True
#                 )
#                 .first()
#             )

#             if active_subscription:
#                 active_subscription.status = 'expired'
#                 active_subscription.save(update_fields=['status'])

#             # -------------------------
#             # Create new subscription
#             # -------------------------
#             start_date = payment_date
#             end_date = start_date + timedelta(days=plan.duration_days)

#             subscription = Subscription.objects.create(
#                 organization=request.user.organization,
#                 member=member,
#                 plan=plan,
#                 start_date=start_date,
#                 end_date=end_date,
#                 status='active',
#                 created_by=request.user
#             )

#             # -------------------------
#             # Create payment
#             # -------------------------
#             payment = form.save(commit=False)
#             payment.organization = request.user.organization
#             payment.member = member
#             payment.subscription = subscription
#             payment.received_by = request.user
#             payment.payment_date = payment_date
#             payment.save()

#             return redirect('dashboard:member_list')

#     else:
#         form = AddPaymentForm()

#     return render(
#         request,
#         'add_payment.html',
#         {
#             'form': form,
#             'member': member
#         }
#     )



@login_required
@role_required(['owner', 'site_manager', 'gym_manager', 'staff'])
@transaction.atomic
def add_payment(request, member_id):
    """
    Add a payment for a member and create/extend a subscription.

    Business Rules:
    - A member can have ONLY ONE active subscription at a time
    - If a member buys again before expiry → extend from end_date
    - If no active subscription → start from payment_date
    - Payment is ALWAYS linked to exactly ONE subscription
    - NO overlapping subscriptions (guaranteed)

    Flow:
    Member → Subscription → Payment
    """

    # --------------------------------------------------
    # Fetch member with RBAC & safety checks
    # --------------------------------------------------
    member = get_object_or_404(
        Member,
        id=member_id,
        organization=request.user.organization,
        deleted_at__isnull=True
    )

    if request.method == 'POST':
        form = AddPaymentForm(request.POST)

        if form.is_valid():
            # --------------------------------------------------
            # Extract cleaned data
            # --------------------------------------------------
            plan = form.cleaned_data['plan']
            payment_date = form.cleaned_data['payment_date']

            # --------------------------------------------------
            # Fetch active subscription (if exists)
            # --------------------------------------------------
            active_subscription = (
                Subscription.objects
                .filter(
                    member=member,
                    status='active',
                    deleted_at__isnull=True
                )
                .first()
            )

            # --------------------------------------------------
            # Calculate subscription start & end (NO OVERLAP)
            # --------------------------------------------------
            if active_subscription and active_subscription.end_date >= payment_date:
                # Extend from existing subscription end date
                start_date = active_subscription.end_date + timedelta(days=1)
            else:
                # Start fresh
                start_date = payment_date

            end_date = start_date + timedelta(days=plan.duration_days)

            # --------------------------------------------------
            # Expire previous active subscription
            # --------------------------------------------------
            if active_subscription:
                active_subscription.status = 'expired'
                active_subscription.updated_at = now()
                active_subscription.save(update_fields=['status', 'updated_at'])

            # --------------------------------------------------
            # Create NEW subscription
            # --------------------------------------------------
            subscription = Subscription.objects.create(
                organization=request.user.organization,
                member=member,
                plan=plan,
                start_date=start_date,
                end_date=end_date,
                status='active',
                created_by=request.user
            )

            # --------------------------------------------------
            # Create payment (linked to subscription)
            # --------------------------------------------------
            payment = form.save(commit=False)
            payment.organization = request.user.organization
            payment.member = member
            payment.subscription = subscription
            payment.received_by = request.user
            payment.payment_date = payment_date
            payment.save()
            send_staff_member_payment_notification()
            send_member_payment_notification()
            return redirect('dashboard:member_list')

    else:
        form = AddPaymentForm()

    return render(
        request,
        'add_payment.html',
        {
            'form': form,
            'member': member
        }
    )


@role_required(['owner', 'site_manager', 'gym_manager', 'staff'])
def member_subscriptions(request, member_id):
    """
    Show full subscription history for a member.
    """

    member = get_object_or_404(
        Member,
        id=member_id,
        organization=request.user.organization,
        deleted_at__isnull=True
    )

    subscriptions = (
        Subscription.objects
        .filter(
            member=member,
            deleted_at__isnull=True
        )
        .select_related('plan')
        .order_by('-start_date')
    )

    return render(
        request,
        'subscription_list.html',
        {
            'member': member,
            'subscriptions': subscriptions
        }
    )


# dashboard/views.py
@login_required
@role_required(['owner', 'site_manager', 'gym_manager','staff'])
def edit_member(request, pk):
    member = get_object_or_404(
        Member,
        pk=pk,
        organization=request.user.organization,
        deleted_at__isnull=True
    )

    form = MemberUpdateForm(request.POST or None, instance=member)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard:member_list')

    return render(request, 'edit_member.html', {
        'form': form,
        'member': member
    })

@login_required
@role_required(['owner', 'site_manager', 'gym_manager', 'staff'])
def member_payment_list(request, member_id):
    member = get_object_or_404(
        Member,
        id=member_id,
        organization=request.user.organization,
        deleted_at__isnull=True
    )

    payments = (
        Payment.objects
        .filter(member=member)
        .select_related('subscription__plan', 'received_by')
        .order_by('-payment_date')
    )

    return render(
        request,
        'member_payments.html',
        {
            'member': member,
            'payments': payments
        }
    )


@login_required
@role_required(['owner', 'site_manager', 'gym_manager', 'staff'])
def today_payment(request):
    """
    Show today's payments for the logged-in user's branch.
    Staff can only see their branch payments.
    """

    today = now().date()

    payments = (
        Payment.objects
        .filter(
            payment_date=today,
            member__branch=request.user.branch,
            member__organization=request.user.organization
        )
        .select_related(
            'member',
            'subscription__plan',
            'received_by'
        )
        .order_by('-created_at')
    )

    total_amount = sum(p.amount for p in payments)

    return render(
        request,
        'today_payments.html',
        {
            'payments': payments,
            'total_amount': total_amount,
            'today': today
        }
    )

@login_required
@role_required(['owner', 'site_manager', 'gym_manager', 'staff'])
def all_payments2(request):
    """
    Show all payments for the logged-in user's branch.
    """

    payments = (
        Payment.objects
        .filter(
            member__branch=request.user.branch,
            member__organization=request.user.organization
        )
        .select_related(
            'member',
            'subscription__plan',
            'received_by'
        )
        .order_by('-payment_date', '-created_at')
    )

    total_amount = sum(p.amount for p in payments)

    return render(
        request,
        'all_payments.html',
        {
            'payments': payments,
            'total_amount': total_amount
        }
    )

@role_required(['staff'])
def staff_today_payments(request):
    today = now().date()

    payments = Payment.objects.filter(
        payment_date=today,
        member__branch=request.user.branch
    ).select_related('member')

    return render(
        request,
        'staff/today_payments.html',
        {'payments': payments}
    )

@role_required(['staff'])
def staff_expired_members(request):
    today = now().date()

    members = Member.objects.filter(
        branch=request.user.branch,
        deleted_at__isnull=True
    ).exclude(
        subscriptions__status='active',
        subscriptions__end_date__gte=today
    )

    return render(
        request,
        'staff/expired_members.html',
        {'members': members}
    )


@login_required
def profile_page(request):
    # Safely fetch the Member linked to the logged-in user
    profile = get_object_or_404(Member, id=request.user.id)
    return render(
        request,
        'profile.html',
        {
            'pro': profile,
            'role':request.user.role
        }
    )

@login_required
def faq(request):
    return render(request,'faq.html')



def base_payment_queryset(request):
    """
    Base queryset for payment pages.
    Keeps logic DRY and safe.
    """
    return (
        Payment.objects
        .filter(
            member__branch=request.user.branch,
            member__organization=request.user.organization,
            is_void=False
        )
        .select_related(
            'member',
            'subscription__plan',
            'received_by'
        )
        .order_by('-payment_date', '-created_at')
    )


# @login_required
# @role_required(['owner', 'site_manager', 'gym_manager', 'staff'])
# def all_payment2(request):
#     """
#     All Payments page with:
#     - Search (Member + Payment Ref + Gym User)
#     - Filters
#     - Mobile-first support
#     """

#     payments = base_payment_queryset(request)

#     # -------------------------
#     # GET params
#     # -------------------------
#     search_query = request.GET.get('q', '').strip()
#     payment_mode = request.GET.get('mode', '').strip()
#     received_by = request.GET.get('by', '').strip()
#     start_date = request.GET.get('start', '').strip()
#     end_date = request.GET.get('end', '').strip()

#     # -------------------------
#     # SEARCH (SAFE + COMPLETE)
#     # -------------------------
#     if search_query:
#         payments = payments.filter(
#             Q(member__first_name__icontains=search_query) |
#             Q(member__last_name__icontains=search_query) |
#             Q(payment_ref__icontains=search_query) |

#             # 🔍 Gym User (received_by)
#             Q(received_by__username__icontains=search_query) |
#             Q(received_by__first_name__icontains=search_query) |
#             Q(received_by__last_name__icontains=search_query) |
#             Q(received_by__mobile__icontains=search_query)
#         )

#     # -------------------------
#     # Filters
#     # -------------------------
#     if payment_mode:
#         payments = payments.filter(payment_mode=payment_mode)

#     if received_by:
#         payments = payments.filter(received_by_id=received_by)

#     if start_date and end_date:
#         payments = payments.filter(
#             payment_date__range=[start_date, end_date]
#         )

#     # -------------------------
#     # Total Amount
#     # -------------------------
#     total_amount = payments.aggregate(
#         total=Sum('amount')
#     )['total'] or 0

#     # -------------------------
#     # Gym Users for filter dropdown
#     # -------------------------
#     staff_users = User.objects.filter(
#         organization=request.user.organization,
#         branch=request.user.branch,
#         role__in=['owner', 'site_manager', 'gym_manager', 'staff'],
#         is_active=True
#     ).order_by('username')

#     # -------------------------
#     # Context
#     # -------------------------
#     context = {
#         'payments': payments,
#         'total_amount': total_amount,
#         'page_title': 'All Payments',
#         'active_page': 'payments',

#         # Filters
#         'payment_modes': Payment.PAYMENT_MODE_CHOICES,
#         'staff_users': staff_users,
#     }

#     return render(request, 'all_payment2.html', context)

@login_required
@role_required(['owner', 'site_manager', 'gym_manager', 'staff'])
def all_payments(request):

    payments_qs = base_payment_queryset(request)

    # -------------------------
    # GET params
    # -------------------------
    search_query = request.GET.get('q', '').strip()
    payment_mode = request.GET.get('mode', '').strip()
    received_by = request.GET.get('by', '').strip()
    start_date = request.GET.get('start', '').strip()
    end_date = request.GET.get('end', '').strip()

    # -------------------------
    # Search
    # -------------------------
    if search_query:
        payments_qs = payments_qs.filter(
            Q(member__first_name__icontains=search_query) |
            Q(member__last_name__icontains=search_query) |
            Q(payment_ref__icontains=search_query) |
            Q(received_by__username__icontains=search_query) |
            Q(received_by__first_name__icontains=search_query) |
            Q(received_by__last_name__icontains=search_query) |
            Q(received_by__mobile__icontains=search_query)
        )

    # -------------------------
    # Filters
    # -------------------------
    if payment_mode:
        payments_qs = payments_qs.filter(payment_mode=payment_mode)

    if received_by:
        payments_qs = payments_qs.filter(received_by_id=received_by)

    if start_date and end_date:
        payments_qs = payments_qs.filter(
            payment_date__range=[start_date, end_date]
        )

    # -------------------------
    # Pagination (20 per page)
    # -------------------------
    paginator = Paginator(payments_qs, 15)
    page_number = request.GET.get('page')

    try:
        payments = paginator.page(page_number)
    except PageNotAnInteger:
        payments = paginator.page(1)
    except EmptyPage:
        payments = paginator.page(paginator.num_pages)

    # -------------------------
    # Total Amount (filtered)
    # -------------------------
    total_amount = payments_qs.aggregate(
        total=Sum('amount')
    )['total'] or 0

    # -------------------------
    # Staff list
    # -------------------------
    staff_users = User.objects.filter(
        organization=request.user.organization,
        branch=request.user.branch,
        role__in=['owner', 'site_manager', 'gym_manager', 'staff'],
        is_active=True
    ).order_by('username')

    context = {
        'payments': payments,        # 👈 paginated object
        'total_amount': total_amount,
        'page_title': 'All Payments',
        'active_page': 'payments',

        # Filters
        'payment_modes': Payment.PAYMENT_MODE_CHOICES,
        'staff_users': staff_users,
    }

    return render(request, 'all_payment2.html', context)


@login_required
@role_required(['owner', 'site_manager', 'gym_manager', 'staff'])
def today_payment(request):
    """
    Today Payments page
    - Search
    - Filters
    - Pagination (20 per page)
    """

    today = localdate()

    payments_qs = base_payment_queryset(request).filter(
        payment_date=today
    )

    # -------------------------
    # GET params
    # -------------------------
    search_query = request.GET.get('q', '').strip()
    payment_mode = request.GET.get('mode', '').strip()
    received_by = request.GET.get('by', '').strip()
    start_date = request.GET.get('start', '').strip()
    end_date = request.GET.get('end', '').strip()

    # -------------------------
    # Search (SAFE FIELDS ONLY)
    # -------------------------
    if search_query:
        payments_qs = payments_qs.filter(
            Q(member__first_name__icontains=search_query) |
            Q(member__last_name__icontains=search_query) |
            Q(payment_ref__icontains=search_query) |
            Q(received_by__username__icontains=search_query) |
            Q(received_by__first_name__icontains=search_query) |
            Q(received_by__last_name__icontains=search_query) |
            Q(received_by__mobile__icontains=search_query)
        )

    # -------------------------
    # Filters
    # -------------------------
    if payment_mode:
        payments_qs = payments_qs.filter(payment_mode=payment_mode)

    if received_by:
        payments_qs = payments_qs.filter(received_by_id=received_by)

    # (Date range optional, still allowed for consistency)
    if start_date and end_date:
        payments_qs = payments_qs.filter(
            payment_date__range=[start_date, end_date]
        )

    # -------------------------
    # Pagination (20 per page)
    # -------------------------
    paginator = Paginator(payments_qs, 20)
    page_number = request.GET.get('page')

    try:
        payments = paginator.page(page_number)
    except PageNotAnInteger:
        payments = paginator.page(1)
    except EmptyPage:
        payments = paginator.page(paginator.num_pages)

    # -------------------------
    # Total Amount (filtered)
    # -------------------------
    total_amount = payments_qs.aggregate(
        total=Sum('amount')
    )['total'] or 0

    # -------------------------
    # Staff users for filter
    # -------------------------
    staff_users = User.objects.filter(
        organization=request.user.organization,
        branch=request.user.branch,
        role__in=['owner', 'site_manager', 'gym_manager', 'staff'],
        is_active=True
    ).order_by('username')

    # -------------------------
    # Context
    # -------------------------
    context = {
        'payments': payments,
        'total_amount': total_amount,
        'page_title': 'Today Payments',
        'active_page': 'payments',

        # Filters
        'payment_modes': Payment.PAYMENT_MODE_CHOICES,
        'staff_users': staff_users,
    }

    return render(request, 'today_payments.html', context)



def base_payment_queryset(request):
    return (
        Payment.objects
        .filter(
            member__branch=request.user.branch,
            member__organization=request.user.organization,
            is_void=False
        )
        .select_related(
            'member',
            'subscription__plan',
            'received_by'
        )
        .order_by('-payment_date', '-created_at')
    )


@login_required
@role_required(['owner', 'site_manager', 'gym_manager', 'staff'])
def payments_view(request, period="all"):
    """
    Unified payments view:
    period = all | today | last_7_days | this_month
    """

    today = localdate()
    payments_qs = base_payment_queryset(request)

    # -------------------------
    # Period filters
    # -------------------------
    if period == "today":
        payments_qs = payments_qs.filter(payment_date=today)
        page_title = "Today Payments"

    elif period == "last_7_days":
        start_date = today - timedelta(days=6)
        payments_qs = payments_qs.filter(
            payment_date__range=[start_date, today]
        )
        page_title = "Last 7 Days Payments"

    elif period == "this_month":
        payments_qs = payments_qs.filter(
            payment_date__year=today.year,
            payment_date__month=today.month
        )
        page_title = "This Month Payments"

    else:
        page_title = "All Payments"

    # -------------------------
    # GET params
    # -------------------------
    q = request.GET.get('q', '').strip()
    mode = request.GET.get('mode', '').strip()
    by = request.GET.get('by', '').strip()
    start = request.GET.get('start', '').strip()
    end = request.GET.get('end', '').strip()

    # -------------------------
    # Search
    # -------------------------
    if q:
        payments_qs = payments_qs.filter(
            Q(member__first_name__icontains=q) |
            Q(member__last_name__icontains=q) |
            Q(payment_ref__icontains=q) |
            Q(received_by__username__icontains=q) |
            Q(received_by__first_name__icontains=q) |
            Q(received_by__last_name__icontains=q) |
            Q(received_by__mobile__icontains=q)
        )

    # -------------------------
    # Filters
    # -------------------------
    if mode:
        payments_qs = payments_qs.filter(payment_mode=mode)

    if by:
        payments_qs = payments_qs.filter(received_by_id=by)

    # Optional override date range
    if start and end:
        payments_qs = payments_qs.filter(
            payment_date__range=[start, end]
        )

    # -------------------------
    # Pagination (20)
    # -------------------------
    paginator = Paginator(payments_qs, 20)
    page_number = request.GET.get('page')

    try:
        payments = paginator.page(page_number)
    except PageNotAnInteger:
        payments = paginator.page(1)
    except EmptyPage:
        payments = paginator.page(paginator.num_pages)

    # -------------------------
    # Total
    # -------------------------
    total_amount = payments_qs.aggregate(
        total=Sum('amount')
    )['total'] or 0

    # -------------------------
    # Staff list
    # -------------------------
    staff_users = User.objects.filter(
        organization=request.user.organization,
        branch=request.user.branch,
        role__in=['owner', 'site_manager', 'gym_manager', 'staff'],
        is_active=True
    ).order_by('username')

    context = {
        'payments': payments,
        'total_amount': total_amount,
        'page_title': page_title,
        'active_page': 'payments',

        'payment_modes': Payment.PAYMENT_MODE_CHOICES,
        'staff_users': staff_users,
        'period': period,
    }

    return render(request, 'payments.html', context)



@login_required
@role_required(['owner', 'site_manager', 'gym_manager', 'staff'])
def subscription_expiry_view(request, period="all"):
    """
    Unified subscription expiry view:
    period = all | today | tomorrow | last_7_days
    """

    today = localdate()
    tomorrow = today + timedelta(days=1)
    seven_days_ago = today - timedelta(days=6)

    subscriptions_qs = Subscription.objects.filter(
        organization=request.user.organization,
        deleted_at__isnull=True
    ).select_related('member', 'plan')

    # -------------------------
    # Period filters
    # -------------------------
    if period == "today":
        subscriptions_qs = subscriptions_qs.filter(
            status='active',
            end_date=today
        )
        page_title = "Subscriptions Expiring Today"

    elif period == "tomorrow":
        subscriptions_qs = subscriptions_qs.filter(
            status='active',
            end_date=tomorrow
        )
        page_title = "Subscriptions Expiring Tomorrow"

    elif period == "last_7_days":
        subscriptions_qs = subscriptions_qs.filter(
            end_date__range=[seven_days_ago, today]
        )
        page_title = "Subscriptions Expired in Last 7 Days"

    else:
        page_title = "All Subscriptions"

    # -------------------------
    # GET params
    # -------------------------
    q = request.GET.get('q', '').strip()
    start = request.GET.get('start', '').strip()
    end = request.GET.get('end', '').strip()
    status = request.GET.get('status', '').strip()

    # -------------------------
    # Search
    # -------------------------
    if q:
        subscriptions_qs = subscriptions_qs.filter(
            Q(member__first_name__icontains=q) |
            Q(member__last_name__icontains=q) |
            Q(member__mobile__icontains=q) |
            Q(plan__name__icontains=q)
        )

    # -------------------------
    # Filters
    # -------------------------
    if status:
        subscriptions_qs = subscriptions_qs.filter(status=status)

    if start and end:
        subscriptions_qs = subscriptions_qs.filter(
            end_date__range=[start, end]
        )

    # -------------------------
    # Pagination (20)
    # -------------------------
    paginator = Paginator(subscriptions_qs.order_by('end_date'), 20)
    page_number = request.GET.get('page')

    try:
        subscriptions = paginator.page(page_number)
    except PageNotAnInteger:
        subscriptions = paginator.page(1)
    except EmptyPage:
        subscriptions = paginator.page(paginator.num_pages)

    context = {
        'subscriptions': subscriptions,
        'page_title': page_title,
        'active_page': 'subscriptions',
        'period': period,
        'status_choices': Subscription.STATUS_CHOICES,
    }

    return render(request, 'subscriptions_expiry.html', context)
