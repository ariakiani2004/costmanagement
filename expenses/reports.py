from datetime import date
from io import BytesIO

from django.conf import settings
from fpdf import FPDF, FontFace
from openpyxl import Workbook
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from .models import Expense
from .templatetags.display import fa_digits, money


REPORT_TITLE = "گزارش هزینه‌های شخصی"
HEADERS = ("عنوان", "دسته‌بندی", "تاریخ میلادی", "مبلغ (تومان)", "یادداشت")


def report_filters(filters, date_label):
    start = filters["start"]
    end = filters["end"]
    dates = "همهٔ تاریخ‌ها"
    if start and end:
        dates = f"از {date_label(start)} تا {date_label(end)}"
    elif start:
        dates = f"از {date_label(start)}"
    elif end:
        dates = f"تا {date_label(end)}"

    details = []
    if filters["category"]:
        category = Expense.Category(filters["category"]).label
        details.append(f"دسته‌بندی {category}")
    if filters["q"]:
        details.append(f"جست‌وجوی «{filters['q']}»")
    return f"تاریخ میلادی {dates}", " | ".join(details)


def export_excel(expenses, filters):
    workbook = Workbook(iso_dates=True)
    sheet = workbook.active
    sheet.title = "هزینه‌ها"
    sheet.sheet_view.rightToLeft = True

    dates, other_filters = report_filters(filters, date.isoformat)
    for row_number, text in enumerate((REPORT_TITLE, dates, other_filters), start=1):
        sheet.merge_cells(start_row=row_number, start_column=1, end_row=row_number, end_column=5)
        cell = sheet.cell(row=row_number, column=1, value=ILLEGAL_CHARACTERS_RE.sub("", text))
        cell.alignment = Alignment(horizontal="right", vertical="center")
    sheet["A1"].font = Font(bold=True, size=16, color="124336")
    sheet.row_dimensions[1].height = 29

    total = sum(expense.amount for expense in expenses)
    sheet.append(["تعداد هزینه‌ها", len(expenses), "جمع (تومان)", total])
    sheet["D4"].number_format = "#,##0"
    for cell in sheet[4]:
        cell.font = Font(bold=True)
    sheet.append([])
    sheet.append(HEADERS)
    for cell in sheet[6]:
        cell.font = Font(color="FFFFFF", bold=True)
        cell.fill = PatternFill("solid", fgColor="124336")
        cell.alignment = Alignment(horizontal="right")

    for expense in expenses:
        sheet.append((
            ILLEGAL_CHARACTERS_RE.sub("", expense.title),
            expense.get_category_display(),
            expense.spent_on,
            expense.amount,
            ILLEGAL_CHARACTERS_RE.sub("", expense.note),
        ))
        title, category, date_cell, amount, note = sheet[sheet.max_row]
        # عنوان و یادداشت واردشده همیشه متن هستند.
        for cell in (title, category, note):
            cell.data_type = "s"
            cell.alignment = Alignment(horizontal="right", vertical="top", wrap_text=True)
        date_cell.number_format = "yyyy-mm-dd"
        amount.number_format = "#,##0"

    if expenses:
        sheet.auto_filter.ref = f"A6:E{sheet.max_row}"
    else:
        sheet.append(["هزینه‌ای برای این گزارش پیدا نشد."])
        sheet.merge_cells("A7:E7")

    for index, width in enumerate((30, 21, 18, 22, 52), start=1):
        sheet.column_dimensions[get_column_letter(index)].width = width
    sheet.freeze_panes = "A7"

    output = BytesIO()
    workbook.save(output)
    return output.getvalue()


class ExpensePDF(FPDF):
    def footer(self):
        self.set_y(-13)
        self.set_font("Noto Arabic", size=9)
        self.set_text_color(82, 99, 108)
        self.cell(text=f"صفحهٔ {fa_digits(self.page_no())}", align="C")


def pdf_date(value):
    return fa_digits(value.isoformat().replace("-", "/"))


def export_pdf(expenses, filters):
    pdf = ExpensePDF(format="A4")
    fonts = settings.BASE_DIR / "static" / "fonts"
    pdf.add_font("Noto Arabic", fname=fonts / "NotoSansArabic-Regular.ttf")
    pdf.add_font("Noto Arabic", style="B", fname=fonts / "NotoSansArabic-Bold.ttf")
    pdf.add_font("Noto Latin", fname=fonts / "NotoSans-Regular.ttf")
    pdf.set_fallback_fonts(["Noto Latin"], exact_match=False)
    pdf.set_text_shaping(True, direction="rtl")
    pdf.set_title(REPORT_TITLE)
    pdf.set_lang("fa")
    pdf.set_margins(13, 15, 13)
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()

    pdf.set_font("Noto Arabic", "B", 18)
    pdf.set_text_color(18, 67, 54)
    pdf.multi_cell(0, 12, REPORT_TITLE, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Noto Arabic", size=10)
    pdf.set_text_color(25, 42, 52)
    total = sum(expense.amount for expense in expenses)
    dates, other_filters = report_filters(filters, pdf_date)
    summary = f"{fa_digits(len(expenses))} هزینه   |   جمع {money(total)} تومان"
    for line in (dates, other_filters, summary):
        if line:
            pdf.multi_cell(0, 7, line, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    if not expenses:
        pdf.multi_cell(0, 7, "هزینه‌ای برای این گزارش پیدا نشد.", align="R")
    else:
        # ستون‌های جدول PDF از چپ ساخته می‌شوند.
        pdf.set_draw_color(220, 228, 232)
        with pdf.table(
            col_widths=(54, 32, 29, 29, 40), text_align="RIGHT",
            line_height=5.5, padding=1.7, borders_layout="HORIZONTAL_LINES",
            headings_style=FontFace(emphasis="BOLD", color=255, fill_color=(18, 67, 54)),
        ) as table:
            table.row(tuple(reversed(HEADERS)))
            for expense in expenses:
                table.row((
                    " ".join(expense.note.split()), money(expense.amount), pdf_date(expense.spent_on),
                    expense.get_category_display(), " ".join(expense.title.split()),
                ))

    return bytes(pdf.output())
