tasks = []
next_id = 1


def add_task(title):
    if not title.strip():
        raise ValueError("Название задачи не может быть пустым")

    global next_id

    task = {
        "id": next_id,
        "title": title,
        "completed": False
    }

    tasks.append(task)
    next_id += 1

    return task


def get_tasks():
    return tasks


def update_task(task_id, new_title):
    if not new_title.strip():
        raise ValueError("Название задачи не может быть пустым")

    for task in tasks:
        if task["id"] == task_id:
            task["title"] = new_title
            return task

    return None


def complete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            return task

    return None


def delete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return True

    return False