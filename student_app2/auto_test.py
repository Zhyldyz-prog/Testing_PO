import subprocess
import time

print("=======")
print("АВТОМАТИЧЕСКОЕ ТЕСТИРОВАНИЕ")
print("=======")


while 1:
    result = subprocess.run(['pytest', 'test_student.py', '-v'],

                            capture_output=True,
                            text=True

                            )

    print("\n----------------") 
    print("РЕЗУЛЬТАТ ТЕСТИРОВАНИЯ")
    print("\n----------------")

    print(result.stdout)

    if result.returncode == 0:
        print('Все тесты пройдены')
    else:
        print('Есть ошибки')

    time.sleep(3)