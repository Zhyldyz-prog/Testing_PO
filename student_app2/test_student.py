from student_service import (
    add_student, get_students, update_student, delete_student, students
    )

def clear_students():
    students.clear()

def test_add_student():
    clear_students()
    student = add_student('Ivan', 'Ivanov', 20, 85)

    assert student['name'] == 'Ivan'
    assert student['surname'] == 'Ivanov'
    assert student['age'] == 20
    assert student['score'] == 85

    assert len(students) == 1


def test_invalid_age():
    clear_students()

    try: 
        add_student('Ivan', 'Ivanov', 10,85)
        assert False
    except ValueError:
        assert True

def test_invalid_score():
    clear_students()

    try:
        add_student('Ivan', 'Ivanov', 20,150)
        assert False
    except ValueError:
        assert True

def test_update_student():
    clear_students()

    student = add_student('Ivan', 'Ivanov', 20, 85)

    updated = update_student(
        student['id'],
        'Petr',
        'Petrov',
        25,
        95
    )

    assert updated['name'] == 'Petr'
    assert updated['surname'] == 'Petrov'
    assert updated['age'] == 25
    assert updated['score'] == 95


def test_delete_student():
    clear_students()
    student = add_student('Ivan', 'Ivanov', 20, 85)

    result = delete_student(student['id'])

    assert result is True
    assert len(students)==0