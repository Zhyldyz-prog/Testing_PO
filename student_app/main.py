import flet as ft
import subprocess
import os

from task_service import (
    add_task,
    get_tasks,
    update_task,
    complete_task,
    delete_task
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_FILE = os.path.join(BASE_DIR, "test_task.py")


def main(page: ft.Page):

    page.title = "Менеджер задач"
    page.padding = 20

    title = ft.TextField(
        label="Название задачи",
        hint_text="Введите задачу",
        width=400
    )

    tasks_list = ft.Column(
        spacing=10
    )

    result_text = ft.Text(
        "",
        size=16
    )

    selected_task_id = [None]

    def refresh_tasks():

        tasks_list.controls.clear()

        for task in get_tasks():

            if task["completed"]:
                task_text = ft.Text(
                    "✓ " + task["title"],
                    size=18
                )
            else:
                task_text = ft.Text(
                    task["title"],
                    size=18
                )

            task_id = task["id"]

            def edit_click(e, task_id=task_id):

                for current_task in get_tasks():

                    if current_task["id"] == task_id:

                        title.value = current_task["title"]

                        selected_task_id[0] = task_id

                        page.update()

                        break

            def complete_click(e, task_id=task_id):

                complete_task(task_id)

                result_text.value = "Задача выполнена"

                refresh_tasks()

            def delete_click(e, task_id=task_id):

                delete_task(task_id)

                result_text.value = "Задача удалена"

                refresh_tasks()

            row = ft.Row(
                controls=[
                    task_text,

                    ft.ElevatedButton(
                        "Изменить",
                        on_click=edit_click
                    ),

                    ft.ElevatedButton(
                        "Выполнить",
                        on_click=complete_click
                    ),

                    ft.ElevatedButton(
                        "Удалить",
                        on_click=delete_click
                    )
                ]
            )

            tasks_list.controls.append(row)

        page.update()

    def add_or_update_click(e):

        if not title.value.strip():

            result_text.value = "Введите название задачи"

            page.update()

            return

        try:

            if selected_task_id[0] is None:

                add_task(title.value)

                result_text.value = "Задача добавлена"

            else:

                update_task(
                    selected_task_id[0],
                    title.value
                )

                result_text.value = "Задача изменена"

                selected_task_id[0] = None

            title.value = ""

            refresh_tasks()

        except ValueError as error:

            result_text.value = str(error)

            page.update()

    def run_tests_click(e):

        result = subprocess.run(
            [
                "python",
                "-m",
                "pytest",
                TEST_FILE,
                "-v"
            ],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:

            result_text.value = (
                "Все тесты пройдены!\n\n"
                + result.stdout
            )

        else:

            result_text.value = (
                "Есть ошибки в тестах!\n\n"
                + result.stdout
                + "\n"
                + result.stderr
            )

        page.update()

    add_button = ft.ElevatedButton(
        "Добавить / изменить",
        on_click=add_or_update_click
    )

    test_button = ft.ElevatedButton(
        "Запустить тесты",
        on_click=run_tests_click
    )

    page.add(

        ft.Text(
            "Менеджер задач",
            size=30,
            weight=ft.FontWeight.BOLD
        ),

        ft.Divider(),

        ft.Row(
            controls=[
                title,
                add_button
            ]
        ),

        ft.Text(
            "Список задач:",
            size=22,
            weight=ft.FontWeight.BOLD
        ),

        tasks_list,

        ft.Divider(),

        test_button,

        ft.Text(
            "Результат:",
            size=18,
            weight=ft.FontWeight.BOLD
        ),

        result_text
    )

    refresh_tasks()


ft.app(target=main)