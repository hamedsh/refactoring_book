from math import floor
from typing import Dict, Any


class Statement:

    def __init__(self) -> None:
        self.plays: Dict[str, Any] = {}
        self.invoice: Dict[str, Any] = {}

    @staticmethod
    def usd(value: float) -> str:
        return f'${value/100:,.2f}'

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

    def volume_credits_for(self, a_performance: Dict[str, Any]) -> int:
        result = 0
        # add volume credits
        result += max(a_performance['audience'] - 30, 0)
        # add extra credits for every ten comedy attendees
        if 'comedy' == self.play_for(a_performance)["type"]:
            result += floor(a_performance["audience"] / 5)
        return result

    def total_volume_credits(self) -> int:
        volume_credits: int = 0
        for perf in self.invoice["performances"]:
            volume_credits += self.volume_credits_for(perf)
        return volume_credits

    def statement(self, invoice: Dict[str, Any], plays: Dict[str, Any]) -> str:
        self.plays = plays
        self.invoice = invoice
        total_amount: int = 0
        result = f'Statement for {invoice["customer"]}\n'

        for perf in invoice["performances"]:
            result += f'    {self.play_for(perf)["name"]}: {Statement.usd(self.amount_for(perf))} ({perf["audience"]} seats)\n'
            total_amount += self.amount_for(perf)
        volume_credits: int = self.total_volume_credits()
        result += f'Amount owed is {Statement.usd(total_amount)}\n'
        result += f'You earned {volume_credits} credits\n'
        return result
