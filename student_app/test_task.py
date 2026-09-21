from task_service import (
    add_task,
    get_tasks,
    update_task,
    complete_task,
    delete_task,
    tasks
)


def clear_tasks():
    tasks.clear()


def test_add_task():

    clear_tasks()

    task = add_task("Сделать лабораторную работу")

    assert task["title"] == "Сделать лабораторную работу"
    assert task["completed"] is False
    assert len(tasks) == 1


def test_empty_task():

    clear_tasks()

    try:
        add_task("")
        assert False
    except ValueError:
        assert True


def test_update_task():

    clear_tasks()

    task = add_task("Старая задача")

    updated = update_task(
        task["id"],
        "Новая задача"
    )

    assert updated["title"] == "Новая задача"


def test_complete_task():

    clear_tasks()

    task = add_task("Выполнить задание")

    completed = complete_task(task["id"])

    assert completed["completed"] is True


def test_delete_task():

    clear_tasks()

    task = add_task("Удалить эту задачу")

    result = delete_task(task["id"])

    assert result is True
    assert len(tasks) == 0