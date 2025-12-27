from django import forms
from .models import Member


class MemberCreateForm(forms.ModelForm):
    """
    Form to create a Gym Member.
    No update allowed later (as per POC decision).
    """

    class Meta:
        model = Member
        fields = [
            'first_name',
            'last_name',
            'mobile',
            'email',
            'branch',
        ] 

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if len(mobile) != 10 or not mobile.isdigit():
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        return mobile
