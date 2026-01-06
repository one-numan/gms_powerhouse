from django import forms
from django.utils.timezone import now
from .models import Payment, Plan


class AddPaymentForm(forms.ModelForm):
    """
    Add payment and trigger subscription creation/extension.
    """

    plan = forms.ModelChoiceField(
        queryset=Plan.objects.filter(is_active=True),
        empty_label="Select Plan",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    payment_date = forms.DateField(
        initial=now().date(),
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date'
            }
        )
    )
    class Meta:
        model = Payment
        fields = ['amount', 'payment_mode']

        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount'
            }),
            'payment_mode': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
