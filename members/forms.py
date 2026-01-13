from django import forms
from .models import Member


# class MemberCreateForm(forms.ModelForm):
#     """
#     Form used to create Gym Members.

#     Important:
#     - organization & branch are NOT exposed in the form
#     - they are injected from request.user in the view
#     """

#     class Meta:
#         model = Member
#         fields = [
#             'first_name',
#             'last_name',
#             'mobile',
#             'email',
#             'is_active',
#         ]

#         widgets = {
#             'first_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'First Name'
#             }),
#             'last_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Last Name'
#             }),
#             'mobile': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Mobile Number'
#             }),
#             'email': forms.EmailInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Email'
#             }),
#             'is_active': forms.CheckboxInput(attrs={
#                 'class': 'form-check-input'
#             }),
#         }



# class MemberUpdateForm(forms.ModelForm):
#     """
#     Restricted update form for Member.

#     Editable:
#     - email
#     - is_active

#     Non-editable:
#     - first_name
#     - last_name
#     - mobile
#     """

#     class Meta:
#         model = Member
#         fields = ['email', 'is_active']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         # UX improvements
#         self.fields['email'].widget.attrs.update({
#             'class': 'form-control',
#             'placeholder': 'Email (optional)'
#         })

#         self.fields['is_active'].widget.attrs.update({
#             'class': 'form-check-input'
#         })




class MemberCreateForm(forms.ModelForm):
    """
    Form used to create Gym Members.

    Important:
    - organization & branch are NOT exposed
    - injected from request.user in the view
    - optimized for fast front-desk entry
    """

    class Meta:
        model = Member
        fields = [
            # --- Core (Required / Primary) ---
            'first_name',
            'last_name',
            'mobile',
            'gender',

            # --- Contact (Optional) ---
            'email',

            # --- Address (India-friendly) ---
            'address_line',
            'area',
            'city',
            'state',
            'pincode',

            # --- Status ---
            'is_active',
        ]

        widgets = {
            # -----------------------------
            # Core fields
            # -----------------------------
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name (optional)',
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mobile Number',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
            }),

            # -----------------------------
            # Contact
            # -----------------------------
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email (optional)',
            }),

            # -----------------------------
            # Address
            # -----------------------------
            'address_line': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'House no, street, landmark',
                'rows': 2,
            }),
            'area': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Area / Locality',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City',
            }),
            'state': forms.Select(attrs={
                'class': 'form-select',
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'PIN Code',
            }),

            # -----------------------------
            # Status
            # -----------------------------
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_mobile(self):
        """
        Basic mobile validation (India-friendly).
        """
        mobile = self.cleaned_data.get('mobile')

        if mobile and len(mobile) < 10:
            raise forms.ValidationError("Enter a valid mobile number.")

        return mobile


class MemberUpdateForm(forms.ModelForm):
    """
    Update form for Member profile.

    Editable:
    - email
    - gender
    - address fields
    - is_active

    Locked (identity fields):
    - first_name
    - last_name
    - mobile
    """

    class Meta:
        model = Member
        fields = [
            'email',
            'gender',
            'address_line',
            'area',
            'city',
            'state',
            'pincode',
            'is_active',
        ]

        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email (optional)',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
            }),
            'address_line': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'House no, street, landmark',
            }),
            'area': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Area / Locality',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City',
            }),
            'state': forms.Select(attrs={
                'class': 'form-select',
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'PIN Code',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
