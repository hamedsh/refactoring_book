from math import floor
from typing import Dict, Any


class Statement:

    def __init__(self) -> None:
        self.plays: Dict[str, Any] = {}

    @staticmethod
    def format_currency(value: float) -> str:
        return f'${value:,.2f}'

    def amount_for(self, a_performance: Dict[str, Any]) -> int:
        result: int = 0
        if self.play_for(a_performance)["type"] == "tragedy":
            result = 40000
            if a_performance["audience"] > 30:
                result += 1000 * (a_performance["audience"] - 30)
        elif self.play_for(a_performance)["type"] == "comedy":
            result = 30000
            if a_performance['audience'] > 20:
                result += 10000 + 500 * (a_performance["audience"] - 20)
            result += 300 * a_performance["audience"]
        else:
            raise Exception(f'Unknown type: {self.play_for(a_performance)["type"]}')
        return result

    def play_for(self, a_performance: Dict[str, Any]) -> Dict[str, Any]:
        return self.plays[a_performance["playID"]]

    def statement(self, invoice: Dict[str, Any], plays: Dict[str, Any]) -> str:
        self.plays = plays
        total_amount: int = 0
        volume_credits: int = 0
        result = f'Statement for {invoice["customer"]}\n'

        for perf in invoice["performances"]:
            this_amount = self.amount_for(perf)
            # add volume credits
            volume_credits += max(perf['audience'] - 30, 0)
            # add extra credits for every ten comedy attendees
            if 'comedy' == self.play_for(perf)["type"]:
                volume_credits += floor(perf["audience"]/5)
            result += f'    {self.play_for(perf)["name"]}: {Statement.format_currency(this_amount/100)} ({perf["audience"]} seats)\n'
            total_amount += this_amount
        result += f'Amount owed is {Statement.format_currency(total_amount/100)}\n'
        result += f'You earned {volume_credits} credits\n'
        return result
