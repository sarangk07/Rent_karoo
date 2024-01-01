from typing import Any
from django import forms
import re

from .models import Registerinfo, Profile


class RegisterForm(forms.ModelForm):
    # password & conform password field ,it don't need to add in the database
    password = forms.CharField(
        widget=(
            forms.PasswordInput(
                attrs={"placeholder": "password", "class": "form-control"}
            )
        )
    )
    conf_password = forms.CharField(
        widget=(
            forms.PasswordInput(
                attrs={"placeholder": "re-type", "class": "form-control"}
            )
        )
    )

    class Meta:
        model = Registerinfo  # eath model ann use chyyendath
        fields = "__all__"  # models le ellaaa values um use chyyan

        # fields =['first_name','last_name','email','mobile']

    # for styling input fields
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

    # password and conf_password validation
    def clean(self):
        cleaned_data = super(
            RegisterForm, self
        ).clean()  # super means it accessing the password and conf_password from the RegisterForm.
        password = cleaned_data.get("password")
        conf_password = cleaned_data.get("conf_password")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        license = cleaned_data.get("license")

        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
            print(password, conf_password)
            raise forms.ValidationError(
                "Password must contain at least one letter, one digit, and be at least 8 characters long."
            )
        if not re.match(r"^[A-Za-z][A-Za-z\s]*$", first_name):
            raise forms.ValidationError(
                "First name must only contain characters and no spaces."
            )

        if not re.match(r"^[A-Za-z][A-Za-z\s]*$", last_name):
            raise forms.ValidationError(
                "Last name must only contain characters and no spaces."
            )

        print(password, conf_password)
        if password != conf_password:
            raise forms.ValidationError("Password does not match")

        return cleaned_data


class UserForm(forms.ModelForm):
    class Meta:
        model = Registerinfo
        fields = ("first_name", "last_name")

    def _init_(self, *args, **kwargs):
        super(UserForm, self)._init_(*args, **kwargs)

        self.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control bg-dark text-white"
            self.fields[field].widget.attrs["style"] = "border-color: #A32CC4"


class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "address",
            "mobile",
            "gender",
            "age",
            "education",
            "licencePhoto",
            "state",
            "city",
        )

    def clean_address(self):
        address = self.cleaned_data["address"]
        if not address:
            raise forms.ValidationError("Address is required.")
        return address

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"]
        if not phone_number:
            raise forms.ValidationError("Phone number is required.")
        elif not str(phone_number).isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone_number

    def clean_city(self):
        city = self.cleaned_data["city"]
        if not city:
            raise forms.ValidationError("City is required.")
        return city

    def clean_district(self):
        state = self.cleaned_data["state"]
        if not state:
            raise forms.ValidationError("District is required.")
        return state

    def clean_country(self):
        country = self.cleaned_data["country"]
        if not country:
            raise forms.ValidationError("Country is required.")
        return country

    def __init__(self, *args, **kwargs):
        super(ProfileUpdate, self).__init__(*args, **kwargs)
        self.fields["address"].widget.attrs["placeholder"] = "Address "
        self.fields["mobile"].widget.attrs["placeholder"] = "mobile"
        self.fields["gender"].widget.attrs["placeholder"] = "gender"
        self.fields["age"].widget.attrs["placeholder"] = "age"
        self.fields["education"].widget.attrs["placeholder"] = "education"

        self.fields["licencePhoto"].widget.attrs["style"] = "border-color: #A32CC4"

        self.fields["state"].widget.attrs["placeholder"] = "state"
        self.fields["city"].widget.attrs["placeholder"] = "city"

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control  text-dark"
            self.fields[field].widget.attrs["style"] = "border-color: #A32CC4"
