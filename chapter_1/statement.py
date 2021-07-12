from functools import reduce
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
        if a_performance["play"]["type"] == "tragedy":
            result = 40000
            if a_performance["audience"] > 30:
                result += 1000 * (a_performance["audience"] - 30)
        elif a_performance["play"]["type"] == "comedy":
            result = 30000
            if a_performance['audience'] > 20:
                result += 10000 + 500 * (a_performance["audience"] - 20)
            result += 300 * a_performance["audience"]
        else:
            raise Exception(f'Unknown type: {a_performance["play"]["type"]}')
        return result

    def play_for(self, a_performance: Dict[str, Any]) -> Dict[str, Any]:
        return self.plays[a_performance["playID"]]

    def volume_credits_for(self, a_performance: Dict[str, Any]) -> int:
        result = 0
        # add volume credits
        result += max(a_performance['audience'] - 30, 0)
        # add extra credits for every ten comedy attendees
        if 'comedy' == a_performance["play"]["type"]:
            result += floor(a_performance["audience"] / 5)
        return result

    def total_volume_credits(self, data: Dict[str, Any]) -> int:
        return sum(item["volume_credits"] for item in data["performances"])

    def total_amount(self, data: Dict[str, Any]) -> int:
        return sum(item["amount"] for item in data["performances"])

    def render_plain_text(self, data: Dict[str, Any]) -> str:
        result = f'Statement for {data["customer"]}\n'

        for perf in data["performances"]:
            result += f'    {perf["play"]["name"]}: {Statement.usd(perf["amount"])} ({perf["audience"]} seats)\n'
        result += f'Amount owed is {Statement.usd(data["total_amount"])}\n'
        result += f'You earned {data["total_volume_credits"]} credits\n'
        return result

    def enrich_performance(self, a_performance: Dict[str, Any]) -> Dict[str, Any]:
        result = a_performance
        result["play"] = self.play_for(a_performance)
        result["amount"] = self.amount_for(result)
        result["volume_credits"] = self.volume_credits_for(result)
        return result

    def create_statement_data(self, invoice: Dict[str, Any]):
        statement_data: Dict[str, Any] = {
            "customer": invoice["customer"],
            "performances": list(map(self.enrich_performance, invoice["performances"])),
        }
        statement_data["total_amount"] = self.total_amount(statement_data)
        statement_data["total_volume_credits"] = self.total_volume_credits(statement_data)
        return statement_data

    def statement(self, invoice: Dict[str, Any], plays: Dict[str, Any]) -> str:
        self.plays = plays
        self.invoice = invoice

        return self.render_plain_text(self.create_statement_data(invoice))
