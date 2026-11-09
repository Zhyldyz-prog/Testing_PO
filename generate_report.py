import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls


def generate_docx_report():
    doc = Document()

    # Настройка шрифта
    style = doc.styles['Normal']
    style.font.name = 'Arial'
    style.font.size = Pt(11)

    # Заголовок документа
    title = doc.add_paragraph()
    title_run = title.add_run("Отчет о результатах автоматического тестирования")
    title_run.bold = True
    title_run.font.size = Pt(16)
    title_run.font.color.rgb = RGBColor(44, 62, 80)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Метаинформация
    meta = doc.add_paragraph()
    meta.add_run("Модуль: ").bold = True
    meta.add_run("tour_app (Horse Tours Startup)\n")
    meta.add_run("Статус системы: ").bold = True
    status_run = meta.add_run("СТАБИЛЕН (5/5 тестов пройдены)\n")
    status_run.font.color.rgb = RGBColor(46, 204, 113)
    status_run.bold = True

    # Создание таблицы
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Table Grid'

    hdr_cells = table.rows[0].cells
    headers = ["ID Теста", "Компонент / Модель", "Описание проверки", "Результат"]

    for i, text in enumerate(headers):
        hdr_cells[i].text = text
        for paragraph in hdr_cells[i].paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
        shading = parse_xml(r'<w:shd {} w:fill="2980B9"/>'.format(nsdecls('w')))
        hdr_cells[i]._tc.get_or_add_tcPr().append(shading)

    # Записи с результатами тестов
    records = [
        ("test_01", "Category & Tour (ManyToMany)", "Проверка связывания тура с несколькими категориями (Конный, Пеший).", "PASSED"),
        ("test_02", "Booking Restriction (Unique)", "Проверка запрета бронирования более 1 тура 1 человеком на одну дату и время.", "PASSED"),
        ("test_03", "TourComment Model (ForeignKey)", "Проверка возможности добавления нескольких отзывов от одного пользователя.", "PASSED"),
        ("test_04", "Booking POST View", "Проверка отправки данных формы бронирования через HTTP POST запрос.", "PASSED"),
        ("test_05", "Comment POST View", "Проверка добавления комментария через HTTP POST запрос.", "PASSED"),
    ]

    for t_id, component, description, result in records:
        row_cells = table.add_row().cells
        row_cells[0].text = t_id
        row_cells[1].text = component
        row_cells[2].text = description
        row_cells[3].text = result
        for p in row_cells[3].paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.color.rgb = RGBColor(46, 204, 113)

    col_widths = [Inches(1.0), Inches(2.2), Inches(3.0), Inches(1.0)]
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = width

    output_filename = 'django_test_report.docx'
    doc.save(output_filename)
    print(f"Отчет успешно создан: {output_filename}")


if __name__ == '__main__':
    generate_docx_report()