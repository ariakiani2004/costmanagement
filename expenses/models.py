from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Expense(models.Model):
    class Category(models.TextChoices):
        FOOD = "food", "خوراک و خرید"
        TRANSPORT = "transport", "رفت‌وآمد"
        HOME = "home", "خانه و قبوض"
        HEALTH = "health", "سلامت"
        LEISURE = "leisure", "تفریح"
        OTHER = "other", "سایر"

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField("عنوان", max_length=100)
    amount = models.PositiveBigIntegerField(
        "مبلغ (تومان)", validators=[MinValueValidator(1), MaxValueValidator(999_999_999_999)]
    )
    category = models.CharField("دسته‌بندی", max_length=12, choices=Category.choices)
    spent_on = models.DateField("تاریخ هزینه", default=timezone.localdate)
    note = models.TextField("یادداشت", blank=True, max_length=500)

    class Meta:
        ordering = ["-spent_on", "-pk"]
        verbose_name = "هزینه"
        verbose_name_plural = "هزینه‌ها"

    def __str__(self):
        return self.title
