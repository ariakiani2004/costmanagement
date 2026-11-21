<h1 align="center" dir="rtl">مدیریت هزینه‌های شخصی</h1>
<p align="center"><strong>costmanagement</strong></p>
<p align="center" dir="rtl">یک وب‌اپلیکیشن آموزشی برای ثبت خرج‌های روزانه، مرور هزینه‌های ماه و گرفتن گزارش از یک بازهٔ دلخواه.</p>

<p align="center" dir="ltr">
  <img src="https://img.shields.io/badge/Python-3-3776AB?style=flat-square&amp;logo=python&amp;logoColor=white" alt="Python 3">
  <img src="https://img.shields.io/badge/Django-5.2-126451?style=flat-square&amp;logo=django&amp;logoColor=white" alt="Django 5.2">
  <img src="https://img.shields.io/badge/SQLite-3-245876?style=flat-square&amp;logo=sqlite&amp;logoColor=white" alt="SQLite 3">
  <img src="https://img.shields.io/badge/Export-Excel_%C2%B7_PDF-52636C?style=flat-square" alt="خروجی Excel و PDF">
</p>

<div dir="rtl">

## امکانات

رابط فارسی و راست‌چین پروژه با HTML، CSS و JavaScript ساخته شده است. مبلغ‌ها به **تومان** و تاریخ‌ها بر اساس **تقویم میلادی** ثبت می‌شوند.

| بخش | امکانات |
| --- | --- |
| حساب کاربری | ثبت‌نام و ورود با کپچای جمع ساده، تغییر رمز عبور و خروج. هر کاربر به هزینه‌های حساب خودش دسترسی دارد. |
| مدیریت هزینه‌ها | ثبت، ویرایش و حذف هزینه با عنوان، مبلغ، دسته‌بندی، تاریخ و یادداشت اختیاری. |
| داشبورد | نمایش مجموع هزینه‌ها، مجموع ماه جاری و تعداد هزینه‌های ثبت‌شده. |
| جست‌وجو و فیلتر | جست‌وجو در عنوان هزینه و محدود کردن فهرست بر اساس دسته‌بندی و بازهٔ تاریخ. |
| گزارش | دریافت جزئیات هزینه‌های مطابق فیلتر در قالب Excel یا PDF، همراه با تعداد و جمع مبلغ. |
| ظاهر | انتخاب حالت روشن یا تیره در صفحه‌های ورود، ثبت‌نام و داخل حساب. انتخاب در همان مرورگر ذخیره می‌شود. |

## نصب و اجرا در Windows PowerShell

برای دریافت کد از GitHub، در PowerShell این دو دستور را اجرا کنید.

<div dir="ltr">

```powershell
git clone https://github.com/ariakiani2004/costmanagement.git
Set-Location .\costmanagement
```

</div>

اگر پروژه را از فایل ZIP استخراج کرده‌اید، PowerShell را در پوشهٔ حاوی `manage.py` و `requirements.txt` باز کنید. پس از نصب Python 3.12، دستورهای زیر را به‌ترتیب اجرا کنید.

<div dir="ltr">

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

</div>

دستور `migrate` در اولین اجرا پایگاه دادهٔ `db.sqlite3` را می‌سازد. پس از اجرای سرور، صفحهٔ ورود را باز کنید و برای ساخت حساب روی «ثبت‌نام» بزنید. [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## دریافت گزارش

1. در داشبورد، آخرین روز گزارش را در کادر **«تا تاریخ»** انتخاب کنید. مثلاً با انتخاب `2026-06-30`، هزینه‌های خودِ ۳۰ ژوئن هم در گزارش می‌آیند.
2. برای محدود کردن گزارش، تاریخ شروع و دسته‌بندی را انتخاب کنید یا در کادر «جست‌وجو» بخشی از عنوان هزینه را بنویسید. با خالی گذاشتن تاریخ پایان، گزارش همهٔ تاریخ‌های مطابق سایر فیلترها را پوشش می‌دهد.
3. روی **«دانلود اکسل»** برای دریافت فایل `.xlsx` یا **«دانلود PDF»** برای دریافت نسخهٔ قابل چاپ بزنید.

هر دو فایل همهٔ ردیف‌های مطابق فیلتر را در بر می‌گیرند، حتی وقتی فهرست داشبورد چند صفحه دارد. بالای گزارش، تعداد هزینه‌ها و جمع مبلغ همین ردیف‌ها به تومان درج می‌شود.

## ساختار پروژه

| مسیر | نقش |
| --- | --- |
| `costmanagement/` | تنظیمات Django، اتصال به SQLite و مسیرهای اصلی سایت |
| `expenses/` | مدل هزینه، فرم‌ها و منطق ورود، داشبورد و مدیریت هزینه‌ها |
| `expenses/reports.py` | ساخت فایل Excel با `openpyxl` و گزارش PDF فارسی با `fpdf2` |
| `templates/` | قالب‌های HTML ورود، ثبت‌نام، داشبورد و فرم‌های هزینه |
| `static/` | فایل‌های CSS و JavaScript، تنظیم حالت تیره و فونت‌های فارسی |

## نویسندگان

**Aria Kaini** و **Mohammad Arami**

</div>
