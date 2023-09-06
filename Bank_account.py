import datetime
import pytz


class Confirmation:
    def __init__(self, account_number, transaction_code, transaction_id, time, time_utc):
        self.account_number = account_number
        self.transaction_code = transaction_code
        self.transaction_id = transaction_id
        self.time = time
        self.time_utc = time_utc

    def __str__(self):
        return (f'account_number: {self.account_number}\n'
                f'transaction_code: {self.transaction_code}\n'
                f'transaction_id: {self.transaction_id}\n'
                f'time: {self.time}\n'
                f'time_utc: {self.time_utc}\n')


class Account:
    acc_number = 100000
    monthly_interest_rate = 50
    transaction_id = 100

    def __init__(self, first_name: str, last_name: str, time_zone: int, balance: int) -> None:
        if isinstance(first_name, str) and isinstance(last_name, str):
            self.__first_name = first_name.strip()
            self.__last_name = last_name.strip()
            self.__full_name = self.__first_name + ' ' + self.__last_name

        if isinstance(time_zone, int):
            self.__time_zone = time_zone
        else:
            raise ValueError("Time zone must be integer")

        if isinstance(balance, int) and balance >= 0:
            self.__balance = balance
        else:
            raise ValueError("Balances must be integer")
        self.__number = Account.acc_number
        Account.acc_number += 1
        Account.transaction_id += 1

    @property
    def number(self):
        return self.__number

    @property
    def first_name(self) -> str:
        return self.__first_name

    @first_name.setter
    def first_name(self, name: str) -> None:
        if isinstance(name, str):
            self.first_name = name
        else:
            raise ValueError("First name must be string")

    @property
    def last_name(self) -> str:
        return self.__last_name

    @last_name.setter
    def last_name(self, name: str) -> None:
        if isinstance(name, str):
            self.last_name = name
        else:
            raise ValueError("Last name must be string")

    @property
    def full_name(self) -> str:
        return self.__full_name

    @property
    def balance(self) -> int:
        return self.__balance

    def deposit(self, funds: int) -> str:
        if isinstance(funds, int) and funds >= 0:
            self.__balance += funds
        else:
            raise ValueError("Funds must be a positive integer")
        Account.transaction_id += 1
        return self.generate_confirmation_number('deposit')

    def withdrawal(self, funds: int) -> str:
        if isinstance(funds, int) and 0 <= funds <= self.balance:
            self.__balance -= funds
        else:
            raise ValueError("Funds must be a positive integer or there isn't enough balance")
        Account.transaction_id += 1
        return self.generate_confirmation_number('withdrawal')

    def add_interest(self) -> str:
        self.__balance += self.__balance * Account.monthly_interest_rate // 100
        Account.transaction_id += 1
        return self.generate_confirmation_number('interest')

    def generate_confirmation_number(self, transaction: str):
        conf_number = ''
        if transaction == 'deposit':
            transaction_code = 'D'
        elif transaction == 'withdrawal':
            transaction_code = 'W'
        elif transaction == 'interest':
            transaction_code = 'I'
        elif transaction == 'declined':
            transaction_code = 'X'
        else:
            return ValueError("Invalid transaction type")
        conf_number += transaction_code + '-' + str(self.number) + '-'

        user_timezone = pytz.FixedOffset(self.__time_zone * 60)
        current_utc_time = datetime.datetime.utcnow()
        current_time_user_timezone = current_utc_time.astimezone(user_timezone)
        conf_number += current_time_user_timezone.strftime("%Y%m%d%H%M%S%Z")
        conf_number += '-' + str(Account.transaction_id)
        return conf_number

    @staticmethod
    def from_confirmation_number(conf_number: str):
        lst = conf_number.split('-')
        transaction_code = lst[0]
        acc_number = lst[1]
        current_time_user_timezone = lst[2]
        current_time_user_timezone = (current_time_user_timezone[:4] + '-' + current_time_user_timezone[4:6] + '-' +
                                      current_time_user_timezone[6:8] + ' ' + current_time_user_timezone[8:10] + ':' +
                                      current_time_user_timezone[10:12] + ':' + current_time_user_timezone[12:14])
        transaction_id = lst[3]
        current_utc_time = datetime.datetime.utcnow()
        return Confirmation(acc_number, transaction_code, transaction_id,
                            current_time_user_timezone,
                            current_utc_time.strftime("%Y-%m-%d %H:%M:%S"))


if not str(Account.transaction_id).startswith('1'):
    raise ValueError("Invalid transaction ID. It must start with 1.")
try:
    acc = Account('James', 'Nelson', 8, 1000)
    acc1 = Account('James', 'Nelson', 2, 200)
    acc.deposit(100)
    acc.withdrawal(200)
    acc.add_interest()
    print(acc.balance)
except ValueError as ve:
    print(str(ve))
