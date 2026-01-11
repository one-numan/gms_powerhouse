from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from organizations.models import Organization, Branch
from members.models import Member
from subscriptions.models import Plan, Subscription, Payment

User = get_user_model()


class Command(BaseCommand):
    help = "Seed dummy data for GMS POC testing"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Seeding dummy data..."))

        # -------------------------
        # Organization
        # -------------------------
        org, _ = Organization.objects.get_or_create(
            name="Powerhouse Gym",
            defaults={"is_active": True}
        )

        # -------------------------
        # Branches
        # -------------------------
        branch1, _ = Branch.objects.get_or_create(
            organization=org,
            name="Andheri Branch"
        )

        branch2, _ = Branch.objects.get_or_create(
            organization=org,
            name="Bandra Branch"
        )

        # -------------------------
        # Users
        # -------------------------
        org_manager, _ = User.objects.get_or_create(
            username="org_manager",
            defaults={
                "role": "organization_manager",
                "organization": org,
                "branch": branch1,
                "is_staff": True
            }
        )
        org_manager.set_password("password123")
        org_manager.save()

        branch_manager, _ = User.objects.get_or_create(
            username="branch_manager",
            defaults={
                "role": "branch_manager",
                "organization": org,
                "branch": branch1,
                "is_staff": True
            }
        )
        branch_manager.set_password("password123")
        branch_manager.save()

        staff_user, _ = User.objects.get_or_create(
            username="staff_user",
            defaults={
                "role": "staff",
                "organization": org,
                "branch": branch1,
                "is_staff": True
            }
        )
        staff_user.set_password("password123")
        staff_user.save()

        # -------------------------
        # Plans
        # -------------------------
        plan_1m, _ = Plan.objects.get_or_create(
            organization=org,
            name="1 Month",
            duration_days=30,
            amount=1500
        )

        plan_3m, _ = Plan.objects.get_or_create(
            organization=org,
            name="3 Months",
            duration_days=90,
            amount=4000
        )

        # -------------------------
        # Members
        # -------------------------
        members = []
        for i in range(1, 6):
            member, _ = Member.objects.get_or_create(
                organization=org,
                branch=branch1,
                mobile=f"99900000{i}",
                defaults={
                    "first_name": f"Member{i}",
                    "email": f"member{i}@test.com",
                    "is_active": True
                }
            )
            members.append(member)

        # -------------------------
        # Subscriptions & Payments
        # -------------------------
        for member in members:
            start_date = timezone.now().date()
            end_date = start_date + timedelta(days=plan_1m.duration_days)

            subscription = Subscription.objects.create(
                organization=org,
                member=member,
                plan=plan_1m,
                start_date=start_date,
                end_date=end_date,
                status="active",
                created_by=branch_manager
            )

            Payment.objects.create(
                organization=org,
                subscription=subscription,
                member=member,
                amount=plan_1m.amount,
                payment_mode="cash",
                payment_date=start_date,
                received_by=staff_user
            )

        self.stdout.write(self.style.SUCCESS("Dummy data seeded successfully!"))
