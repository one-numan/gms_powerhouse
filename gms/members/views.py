from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MemberCreateForm


@login_required
def create_member(request):
    """
    View to create a new gym member.
    """

    if request.method == "POST":
        form = MemberCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('member-list')  # create later
    else:
        form = MemberCreateForm()

    return render(request, 'member_form.html', {'form': form})
