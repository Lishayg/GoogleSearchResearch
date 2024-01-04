from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password

from .models import Languages, Countries, Languageswithcountries
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from django.core.validators import validate_email
from django.utils.safestring import mark_safe


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="First Name: ")
    last_name = forms.CharField(required=True, label="Last Name: ")
    email = forms.EmailField(required=True, label="Email: ")
    age = forms.IntegerField(required=True, label="Age: ", min_value=0)
    language = forms.ModelChoiceField(queryset=Languages.objects.all().order_by('name'),
                                      required=True, empty_label='--select an option--', label="Language: ")
    country = forms.ModelChoiceField(queryset=Countries.objects.all().order_by('name'),
                                     required=True, empty_label='--select an option--', label="Country: ")
    ed_choices = [
        ('', '--select an option--'),
        ("Basic", "Basic"),
        ("High school, without a matriculation certificate", "High school, without a matriculation certificate"),
        ("High school, with a matriculation certificate", "High school, with a matriculation certificate"),
        ("High school without an academic degree", "High school without an academic degree"),
        ("Studying for a bachelor's degree", "Studying for a bachelor's degree"),
        ("Bachelor degree", "Bachelor degree"),
        ("Studying for a Master's or a Ph.D.", "Studying for a Master's or a Ph.D."),
        ("Has a Master's or a Ph.D.", "Has a Master's or a Ph.D.")
    ]
    education = forms.ChoiceField(choices=ed_choices, required=True, label="What is your level of education?")
    science_ed_choices = [
        ('', '--select an option--'),
        ("Elementary school (up to sixth grade)", "Elementary school (up to sixth grade)"),
        ("Middle school or 8-year school", "Middle school or 8-year school"),
        ("High school up to 10th grade", "High school up to 10th grade"),
        ("High school with a scientific or practical major", "High school with a scientific or practical major"),
        ("Scientific / technological / mathematical academic degree",
         "Scientific / technological / mathematical academic degree"),
        ("A non-science academic degree", "A non-science academic degree"),
        ("Professional or military course, training during work",
         "Professional or military course, training during work")
    ]
    science_ed = forms.ChoiceField(
        choices=science_ed_choices,
        required=True,
        label=mark_safe("What is the setting in which you studied science at the highest level?<br>"
                        "('Sciences' includes, for example, biology, chemistry, physics, computer science)")
    )
    proficiency_choices = [
        ('', '--select an option--'),
        ('0', 'No Proficiency'),
        ('1', 'Elementary Proficiency'),
        ('2', 'Limited Working Proficiency'),
        ('3', 'Professional Working Proficiency'),
        ('4', 'Full Professional Proficiency'),
        ('5', 'Mother tongue / Native / Bilingual Proficiency'),
    ]
    language_proficiency = forms.ChoiceField(choices=proficiency_choices, required=True, label="Level of proficiency "
                                                                                               "in the language I "
                                                                                                "chose:")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError('Invalid email address.')

        # Check if email address is already in use
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email address is already in use.')
        return email

    class Meta:
        model = get_user_model()
        fields = (
            "username", "password1", "password2", "first_name", "last_name", "age", "email", "language", "science_ed", "country",
            "education", "language_proficiency")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Column('username', css_class='form-group col-md-6 mb-0'),
            Column('password1', css_class='form-group col-md-6 mb-0'),
            Column('password2', css_class='form-group col-md-6 mb-0'),
            HTML('<h2> Please fill in your personal information:</h2>'),
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('age', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

            Row(
                Column('language', css_class='form-group col-md-6 mb-0'),
                Column('country', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('language_proficiency', css_class='form-group col-md-6 mb-0'),
                Column('education', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),

            'science_ed',


        )

    def save(self, commit=True):
        user = get_user_model()

        email = self.cleaned_data['email']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        age = self.cleaned_data['age']
        language = self.cleaned_data['language']
        science_ed = self.cleaned_data['science_ed']
        country = self.cleaned_data['country']
        education = self.cleaned_data['education']
        language_proficiency = self.cleaned_data['language_proficiency']
        password1 = make_password(self.cleaned_data['password1'])
        username = self.cleaned_data['username']

        try:
            langCountryId = Languageswithcountries.objects.get(languageid=language, countryid=country)
        except Languageswithcountries.DoesNotExist:
            langCountryId = Languageswithcountries.objects.create(languageid=language, countryid=country)

        new_user = user(username=username,
                        usertype='registered',
                        first_name=first_name,
                        last_name=last_name,
                        password=password1,
                        email=email,
                        age=age,
                        langcountryid=langCountryId,
                        proficiencylevel=language_proficiency,
                        academiclevel=education,
                        scienceeducationlevel=science_ed,
                        is_superuser=0,
                        is_staff=0,
                        is_active=1,
                        date_joined=datetime.now(),
                        last_login=datetime.now())

        if commit:
            new_user.save()

        return new_user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'is_active', 'is_staff',
                  'is_superuser']

