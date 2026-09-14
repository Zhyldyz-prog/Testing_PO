def check_choice(choice):
    if choice == 'орёл':
        return 'heads'
    elif choice == 'решка':
        return 'tails'
    else:
        raise ValueError('Выбор должен быть орёл или решка')


def add_score(score):
    return score + 1


def is_game_finished(round_number):
    return round_number > 10