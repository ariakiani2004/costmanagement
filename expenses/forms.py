from time import time

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Expense


class CaptchaFormMixin:
    captcha_key = ""

    def clean(self):
        # پاسخ پس از هر ارسال مصرف می‌شود.
        expected = self.request.session.pop(self.captcha_key, None)
        if "captcha" not in self.errors and (
            not expected
            or expected["until"] < time()
            or self.cleaned_data.get("captcha") != expected["answer"]
        ):
            self.add_error("captcha", "پاسخ کپچا درست نیست یا منقضی شده است.")
        if self.errors:
            return self.cleaned_data
        return super().clean()


class LoginForm(CaptchaFormMixin, AuthenticationForm):
    captcha_key = "login_captcha"
    captcha = forms.IntegerField(
        label="پاسخ کپچا",
        widget=forms.TextInput(attrs={"inputmode": "numeric", "autocomplete": "off"}),
    )


class SignupForm(CaptchaFormMixin, UserCreationForm):
    captcha_key = "signup_captcha"
    captcha = forms.IntegerField(
        label="پاسخ کپچا",
        widget=forms.TextInput(attrs={"inputmode": "numeric", "autocomplete": "off"}),
    )

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["title", "amount", "category", "spent_on", "note"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "مثلاً خرید میوه"}),
            "amount": forms.TextInput(attrs={"placeholder": "مثلاً ۲۵۰۰۰۰", "inputmode": "numeric"}),
            "spent_on": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "dir": "ltr"}),
            "note": forms.Textarea(attrs={"rows": 3}),
        }
        help_texts = {"spent_on": "تاریخ را به میلادی انتخاب کنید."}


class FilterForm(forms.Form):
    q = forms.CharField(
        label="جست‌وجو", max_length=100, required=False,
        widget=forms.TextInput(attrs={"placeholder": "عنوان هزینه"}),
    )
    category = forms.ChoiceField(
        label="دسته‌بندی", choices=[("", "همهٔ دسته‌ها"), *Expense.Category.choices],
        required=False,
    )
    start = forms.DateField(
        label="از تاریخ", required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "dir": "ltr"}),
    )
    end = forms.DateField(
        label="تا تاریخ", required=False,
        widget=forms.DateInput(format="%Y-%m-%d", attrs={"type": "date", "dir": "ltr"}),
    )

    def clean(self):
        data = super().clean()
        if data.get("start") and data.get("end") and data["start"] > data["end"]:
            self.add_error("end", "تاریخ پایان باید بعد از تاریخ شروع یا برابر با آن باشد.")
        return data
