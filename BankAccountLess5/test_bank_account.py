
import unittest
from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):

    def setUp(self):
        self.account = BankAccount("Айжан", "12345")
        self.account2 = BankAccount("Алина", "67890")

    def tearDown(self):
        del self.account
        del self.account2

    def test_create_account(self):
        self.assertEqual(self.account.owner, "Айжан")
        self.assertEqual(self.account.account_number, "12345")
        self.assertEqual(self.account.get_balance(), 0)

    def test_deposit_success(self):
        self.account.deposit(1000)
        self.assertEqual(self.account.get_balance(), 1000)

    def test_deposit_invalid_amount(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-100)

        self.assertEqual(self.account.get_balance(), 0)

    def test_withdraw_success(self):
        self.account.deposit(1000)
        self.account.withdraw(300)
        self.assertEqual(self.account.get_balance(), 700)

    def test_withdraw_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(500)

        self.assertEqual(self.account.get_balance(), 0)

    def test_withdraw_invalid_amount(self):
        self.account.deposit(1000)

        with self.assertRaises(ValueError):
            self.account.withdraw(-100)

        self.assertEqual(self.account.get_balance(), 1000)

    def test_transfer_success(self):
        self.account.deposit(1000)
        self.account.transfer(self.account2, 400)

        self.assertEqual(self.account.get_balance(), 600)
        self.assertEqual(self.account2.get_balance(), 400)

    def test_transfer_insufficient_funds(self):
        with self.assertRaises(ValueError):
            self.account.transfer(self.account2, 500)

        self.assertEqual(self.account.get_balance(), 0)
        self.assertEqual(self.account2.get_balance(), 0)

    def test_transfer_to_same_account(self):
        self.account.deposit(1000)

        with self.assertRaises(ValueError):
            self.account.transfer(self.account, 300)

        self.assertEqual(self.account.get_balance(), 1000)

    def test_transfer_invalid_amount(self):
        self.account.deposit(1000)

        with self.assertRaises(ValueError):
            self.account.transfer(self.account2, -100)

        self.assertEqual(self.account.get_balance(), 1000)
        self.assertEqual(self.account2.get_balance(), 0)

    def test_get_balance(self):
        self.account.deposit(500)
        self.assertEqual(self.account.get_balance(), 500)

    def test_empty_account(self):
        self.assertTrue(self.account.is_empty())

    def test_non_empty_account(self):
        self.account.deposit(100)
        self.assertFalse(self.account.is_empty())


if __name__ == '__main__':
    unittest.main()