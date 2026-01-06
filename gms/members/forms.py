from django import forms
from .models import Member


class MemberCreateForm(forms.ModelForm):
    """
    Form used to create Gym Members.

    Important:
    - organization & branch are NOT exposed in the form
    - they are injected from request.user in the view
    """

    class Meta:
        model = Member
        fields = [
            'first_name',
            'last_name',
            'mobile',
            'email',
            'is_active',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mobile Number'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }



class MemberUpdateForm(forms.ModelForm):
    """
    Restricted update form for Member.

    Editable:
    - email
    - is_active

    Non-editable:
    - first_name
    - last_name
    - mobile
    """

    class Meta:
        model = Member
        fields = ['email', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # UX improvements
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Email (optional)'
        })

        self.fields['is_active'].widget.attrs.update({
            'class': 'form-check-input'
        })