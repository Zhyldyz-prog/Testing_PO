
class BankAccount:
    def __init__(self, owner, account_number):
        self.owner = owner
        self.account_number = account_number
        self.balance = 0

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть больше нуля")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть больше нуля")
        if amount > self.balance:
            raise ValueError("Недостаточно средств на счете")
        self.balance -= amount

    def transfer(self, other_account, amount):
        if amount <= 0:
            raise ValueError("Сумма перевода должна быть больше нуля")
        if amount > self.balance:
            raise ValueError("Недостаточно средств для перевода")
        if other_account is self:
            raise ValueError("Нельзя переводить деньги на свой счет")

        self.balance -= amount
        other_account.balance += amount

    def get_balance(self):
        return self.balance

    def is_empty(self):
        return self.balance == 0