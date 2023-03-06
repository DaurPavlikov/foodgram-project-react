import io

from django.conf import settings
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

INDENT = 18
X_LIMITER, Y_LIMITER = 50, 800
LIST_SIZE = 14
EMPTY_LIST_SIZE = 18


def pdf_create(data):
    buffer = io.BytesIO()
    page = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('Font', settings.FONT_PATH))
    cursor_x, cursor_y = X_LIMITER, Y_LIMITER
    page.setFont('Font', LIST_SIZE)
    if data:
        page.drawString(cursor_x, cursor_y, 'Cписок покупок:')
        for index, recipe in enumerate(data, start=1):
            page.drawString(
                cursor_x, cursor_y - INDENT,
                f'{index}. {recipe["ingredients__name"]} - '
                f'{recipe["amount"]} '
                f'{recipe["ingredients__measurement_unit"]}.'
            )
            cursor_y -= INDENT
            if cursor_y <= X_LIMITER:
                page.showPage()
                cursor_y = Y_LIMITER
        page.save()
        buffer.seek(0)
        return buffer
    page.setFont('Font', EMPTY_LIST_SIZE)
    page.drawString(
        cursor_x,
        cursor_y,
        'Список покупок пуст.',
    )
    page.save()
    buffer.seek(0)
    return buffer
