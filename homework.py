import datetime as dt
from typing import Dict, List, Optional, Tuple, Union


class Record:
    def __init__(self,
                 amount: Union[int, float],
                 comment: str,
                 date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, "%d.%m.%Y").date()


class Calculator:
    def __init__(self, limit: Union[float, int]) -> None:
        self.limit = limit
        self.records: List[Tuple[Union[float, int], str, Optional[None]]] = []

    def add_record(self,
                   record: Tuple[Union[float, int], str,
                                 Optional[None]]) -> None:
        self.records.append(record)

    def get_today_stats(self) -> Union[int, float]:
        present_day = dt.date.today()
        return sum(record.amount for record in self.records if record.date
                   == present_day)

    def get_today_remained(self) -> Union[int, float]:
        return(self.limit - self.get_today_stats())

    def get_week_stats(self) -> Union[int, float]:
        time_interval = dt.timedelta(days=7)
        week = dt.datetime.now() - time_interval
        amount_week: Union[int, float] = 0
        for record in self.records:
            if dt.datetime.now().date() >= record.date > week.date():
                amount_week += record.amount
            else:
                pass
        return amount_week


class CaloriesCalculator(Calculator):
    def get_calories_remained(self) -> str:
        remainder = self.get_today_remained()
        if remainder > 0:
            return ('Сегодня можно съесть что-нибудь ещё,'
                    f' но с общей калорийностью не более {remainder} кКал')
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE: float = 76.54
    EURO_RATE: float = 90.21
    RUB_RATE: float = 1.00

    def get_today_cash_remained(self, currency: str) -> str:
        rates: Dict[str, Tuple[float, str]] = {
            'rub': [self.RUB_RATE, ' руб'],
            'eur': [self.EURO_RATE, ' Euro'],
            'usd': [self.USD_RATE, ' USD']}
        remainder = self.get_today_remained()
        rate = rates[currency][0]
        phrase = rates[currency][1]
        balance_in_currency = abs(round(remainder / rate, 2))
        if remainder == 0:
            return 'Денег нет, держись'
        elif remainder > 0:
            return ('На сегодня осталось '
                    f'{balance_in_currency}'
                    f'{phrase}')
        else:
            return ('Денег нет, держись: твой долг - '
                    f'{balance_in_currency}'
                    f'{phrase}')
