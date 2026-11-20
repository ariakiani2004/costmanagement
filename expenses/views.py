from secrets import randbelow
from time import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from .forms import ExpenseForm, FilterForm, LoginForm, SignupForm
from .models import Expense
from .reports import export_excel, export_pdf


EXPORT_FORMATS = {
    "xlsx": (export_excel, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
    "pdf": (export_pdf, "application/pdf"),
}


def new_captcha(request, key):
    first = randbelow(8) + 2
    second = randbelow(8) + 2
    previous = request.session.get(key)
    while previous and first + second == previous["answer"]:
        second = randbelow(8) + 2
    request.session[key] = {"answer": first + second, "until": time() + 300}
    return f"{first} + {second}"


class SignInView(LoginView):
    template_name = "login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["captcha_question"] = new_captcha(self.request, LoginForm.captcha_key)
        return context


@never_cache
@csrf_protect
@require_http_methods(["GET", "POST"])
def signup(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = SignupForm(request, request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "حساب شما ساخته شد. حالا می‌توانید وارد شوید.")
        return redirect("login")

    return render(request, "signup.html", {
        "form": form,
        "captcha_question": new_captcha(request, SignupForm.captcha_key),
    })


@login_required
def dashboard(request):
    expenses = Expense.objects.filter(owner=request.user)
    results = expenses
    filters = FilterForm(request.GET)
    if filters.is_valid():
        data = filters.cleaned_data
        if data["q"]:
            results = results.filter(title__icontains=data["q"])
        if data["category"]:
            results = results.filter(category=data["category"])
        if data["start"]:
            results = results.filter(spent_on__gte=data["start"])
        if data["end"]:
            results = results.filter(spent_on__lte=data["end"])

        export_format = request.GET.get("export")
        if export_format in EXPORT_FORMATS:
            export, content_type = EXPORT_FORMATS[export_format]
            date_suffix = f"-through-{data['end'].isoformat()}" if data["end"] else ""
            return HttpResponse(
                export(list(results), data),
                content_type=content_type,
                headers={
                    "Content-Disposition": f'attachment; filename="expenses{date_suffix}.{export_format}"',
                    "Cache-Control": "private, no-store",
                },
            )

    today = timezone.localdate()
    month = expenses.filter(spent_on__year=today.year, spent_on__month=today.month)
    totals = expenses.aggregate(total=Sum("amount", default=0))
    page = Paginator(results, 10).get_page(request.GET.get("page"))
    query = request.GET.copy()
    query.pop("page", None)
    query.pop("export", None)
    return render(request, "dashboard.html", {
        "total": totals["total"],
        "month_total": month.aggregate(total=Sum("amount", default=0))["total"],
        "expense_count": expenses.count(),
        "filters": filters,
        "page": page,
        "filter_query": query.urlencode(),
    })


@login_required
@require_http_methods(["GET", "POST"])
def expense_form(request, pk=None):
    expense = None
    if pk is not None:
        expense = get_object_or_404(Expense, pk=pk, owner=request.user)

    form = ExpenseForm(request.POST if request.method == "POST" else None, instance=expense)
    if request.method == "POST" and form.is_valid():
        entry = form.save(commit=False)
        entry.owner = request.user
        entry.save()
        message = "هزینه ثبت شد." if expense is None else "تغییرات ذخیره شد."
        messages.success(request, message)
        return redirect("dashboard")

    return render(request, "expense_form.html", {"form": form, "expense": expense})


@login_required
@require_http_methods(["GET", "POST"])
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, owner=request.user)
    if request.method == "POST":
        expense.delete()
        messages.success(request, "هزینه حذف شد.")
        return redirect("dashboard")
    return render(request, "expense_delete.html", {"expense": expense})
