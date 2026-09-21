import flet as ft
import subprocess
# Предполагаем, что функция называется get_students (исправлена опечатка)
from student_service import ( add_student, get_students, update_student, delete_student ) 
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILE = os.path.join(BASE_DIR, 'test_student.py')



def main(page: ft.Page):
    page.title = 'Студенты'
    page.window.width = 800
    page.window.height = 600

    name = ft.TextField(label='Имя')
    surname = ft.TextField(label='Фамилия')
    age = ft.TextField(label='Возраст')
    score = ft.TextField(label='Баллы')

    # ИСПРАВЛЕНО: columns вместо column
    table = ft.DataTable(
        columns = [ 
            ft.DataColumn(ft.Text('ID')),
            ft.DataColumn(ft.Text('Имя')),
            ft.DataColumn(ft.Text('Фамилия')),
            ft.DataColumn(ft.Text('Возраст')),
            ft.DataColumn(ft.Text('Баллы'))
        ],
        rows=[]
    )

    def refresh_table():
        table.rows.clear()
        # ИСПРАВЛЕНО: get_students() вместо get_studens()
        for student in get_students(): 
            table.rows.append(
                # ИСПРАВЛЕНО: cells вместо call
                ft.DataRow(
                    cells=[ 
                        ft.DataCell(ft.Text(str(student['id']))),
                        ft.DataCell(ft.Text(str(student['name']))),
                        ft.DataCell(ft.Text(str(student['surname']))),
                        ft.DataCell(ft.Text(str(student['age']))),
                        ft.DataCell(ft.Text(str(student['score']))),
                    ]
                )
            )
        page.update()

    def add_click(e):
        try:
            # ИСПРАВЛЕНО: убраны скобки () у .value
            add_student(
                name.value, 
                surname.value, 
                int(age.value), 
                int(score.value)
            )
            subprocess.run(['pytest', TEST_FILE, '-v'])
            
            name.value = ''
            surname.value = ''
            age.value = ''
            score.value = ''
            refresh_table()
        except ValueError as error:
            # ИСПРАВЛЕНО: snack_bar вместо snak_bar
            page.snack_bar = ft.SnackBar(ft.Text(str(error)))
            page.snack_bar.open = True
            page.update()

    # ИСПРАВЛЕНО: добавлена запятая после строки
    page.add(
        ft.Text(
            'Система управления студентами!', 
            size=25 
        ),
        name,
        surname,
        age,
        score,
        ft.ElevatedButton('добавить', on_click=add_click),
        table
    )
    
    # Первоначальная загрузка данных при старте приложения
    refresh_table()

ft.app(target=main)