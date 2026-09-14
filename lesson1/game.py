import random

round_number = 1
player_score = 0

while round_number <= 10:
    print()
    print('Раунд', round_number)

    player = input('Выбери орёл или решка: ').lower()

    if player != 'орёл' and player != 'решка':
        print('❌ Неверный выбор!')
        continue

    coin = random.choice(['орёл', 'решка'])

    print('🪙 Выпало:', coin)

    if player == coin:
        print('🎉 Ты угадал!')
        player_score += 1
    else:
        print('😔 Ты не угадал!')

    round_number += 1

print()
print('🏁 Игра закончена!')
print(f'👑 Ты угадал - {player_score} раз')