from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_member_created_email(member):
    """
    Sends welcome email to newly added gym member.
    """

    subject = f"Welcome to {member.organization.name}"
    to_email = [member.email]

    context = {
        "gym_name": member.organization.name,
        "member_name": member.first_name,
        "member_mobile": member.mobile,
        "branch_name": member.branch.name,
    }

    html_content = render_to_string(
        "emails/email_member_added_member.html",
        context
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body="Welcome to our gym!",  # fallback text
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to_email,
    )

    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)

def send_staff_member_added_notification(member, created_by):
    """
    Notifies staff / branch manager when a new member is added.
    """

    subject = "New Member Added"
    # to_email = [
    #     member.branch.manager.email
    # ] if member.branch.manager else []

    to_email = ['numantesting@gmail.com']
    context = {
        # "gym_name": member.organization.name,
        # "member_name": member.first_name,
        # "branch_name": member.branch.name,
        # "staff_name": created_by.get_full_name(),
    }

    html_content = render_to_string(
        "emails/email_member_added_staff.html",
        context
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body="New member added",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to_email,
    )

    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)

def send_staff_member_payment_notification():
    """
    Notifies staff / branch manager when a new member is added.
    """

    subject = "New Member Payment Received"
    # to_email = [
    #     member.branch.manager.email
    # ] if member.branch.manager else []

    to_email = ['numantesting@gmail.com']
    context = {
        # "gym_name": member.organization.name,
        # "member_name": member.first_name,
        # "branch_name": member.branch.name,
        # "staff_name": created_by.get_full_name(),
    }

    html_content = render_to_string(
        "emails/email_membership_increment_staff.html",
        context
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body="New member added",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to_email,
    )

    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)


def send_member_payment_notification():
    """
    Notifies staff / branch manager when a new member is added.
    """

    subject = "Membership Activated Successfully!"
    # to_email = [
    #     member.branch.manager.email
    # ] if member.branch.manager else []

    to_email = ['numantesting@gmail.com']
    context = {
        # "gym_name": member.organization.name,
        # "member_name": member.first_name,
        # "branch_name": member.branch.name,
        # "staff_name": created_by.get_full_name(),
    }

    html_content = render_to_string(
        "emails/email_membership_increment.html",
        context
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body="New member added",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to_email,
    )

    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)


