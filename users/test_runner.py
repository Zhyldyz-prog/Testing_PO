import unittest
from django.test.runner import DiscoverRunner
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls


class DocxTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_records = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.test_records.append((test._testMethodName, str(test), "PASSED"))

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.test_records.append((test._testMethodName, str(test), "FAILED"))

    def addError(self, test, err):
        super().addError(test, err)
        self.test_records.append((test._testMethodName, str(test), "ERROR"))


class DocxTestRunner(DiscoverRunner):
    def get_resultclass(self):
        return DocxTestResult

    def run_suite(self, suite, **kwargs):
        result = super().run_suite(suite, **kwargs)
        self.generate_word_report(result.test_records)
        return result

    def generate_word_report(self, records):
        doc = Document()
        style = doc.styles['Normal']
        style.font.name = 'Arial'
        style.font.size = Pt(11)

        title = doc.add_paragraph()
        title_run = title.add_run("Отчет о результатах автоматического тестирования (Users & Captcha)")
        title_run.bold = True
        title_run.font.size = Pt(15)
        title_run.font.color.rgb = RGBColor(44, 62, 80)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER

        all_passed = all(r[2] == "PASSED" for r in records)
        meta = doc.add_paragraph()
        meta.add_run("Модуль: ").bold = True
        meta.add_run("users (Регистрация, Авторизация с капчей, Личный кабинет)\n")
        meta.add_run("Статус: ").bold = True
        status_run = meta.add_run("ВСЕ ТЕСТЫ ПРОЙДЕНЫ\n" if all_passed else "ЕСТЬ ОШИБКИ\n")
        status_run.font.color.rgb = RGBColor(46, 204, 113) if all_passed else RGBColor(231, 76, 60)
        status_run.bold = True

        table = doc.add_table(rows=1, cols=3)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        headers = ["Метод теста", "Тестовый сценарий", "Результат"]

        for i, text in enumerate(headers):
            hdr_cells[i].text = text
            for p in hdr_cells[i].paragraphs:
                for run in p.runs:
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)
            shading = parse_xml(r'<w:shd {} w:fill="2980B9"/>'.format(nsdecls('w')))
            hdr_cells[i]._tc.get_or_add_tcPr().append(shading)

        for method_name, full_name, status in records:
            row_cells = table.add_row().cells
            row_cells[0].text = method_name
            row_cells[1].text = full_name
            row_cells[2].text = status
            for p in row_cells[2].paragraphs:
                for r in p.runs:
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(46, 204, 113) if status == "PASSED" else RGBColor(231, 76, 60)

        col_widths = [Inches(2.5), Inches(3.2), Inches(1.3)]
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width

        output_file = 'users_test_report.docx'
        doc.save(output_file)
        print(f"\n[OK] Отчет успешно сохранен в Word: {output_file}")