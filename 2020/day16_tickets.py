from collections import defaultdict
import itertools


TEST_INPUT = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""


class TicketScanner:
    def __init__(self, observed_values):
        rules_raw, my_ticket_raw, nearby_tickets_raw = observed_values.split("\n\n")
        self.rules = self.parse_rules(rules_raw)
        self.my_ticket = [
            self.parse_ticket(ticket) for ticket in my_ticket_raw.split("\n")[1:]
        ][0]
        self.nearby_tickets = [
            self.parse_ticket(ticket) for ticket in nearby_tickets_raw.split("\n")[1:]
        ]

    def calculate_error_rate_for_nearby_tickets(self):
        return sum(self.validate_ticket(ticket) for ticket in self.nearby_tickets)

    def validate_ticket(self, ticket):
        max_valid_fields = 0
        saved_field = None
        for field_list in itertools.permutations(self.rules.keys(), r=len(self.rules)):
            num_valid_fields = 0
            for field, value in zip(field_list, ticket):
                if value in self.rules[field]:
                    num_valid_fields += 1

            if num_valid_fields > max_valid_fields:
                max_valid_fields = num_valid_fields
                saved_field = field_list

        error_rate = 0
        for field, value in zip(saved_field, ticket):
            if value not in self.rules[field]:
                error_rate += value
        return error_rate

    @staticmethod
    def parse_rules(rules_raw):
        rules = defaultdict(set)
        for rule in rules_raw.strip().split("\n"):
            field, ranges = rule.split(": ")

            for rng in ranges.split(" or "):
                lower_bound, upper_bound = rng.split("-")
                for value in range(int(lower_bound), int(upper_bound) + 1):
                    rules[field].add(value)
        return rules

    @staticmethod
    def parse_ticket(raw_ticket):
        return [int(value) for value in raw_ticket.split(",")]


def test_part_1():
    ts = TicketScanner(TEST_INPUT)
    assert ts.calculate_error_rate_for_nearby_tickets() == 71


if __name__ == "__main__":
    with open("2020/data/day16_input.txt") as f:
        ticket_data = f.read().strip()

    ts = TicketScanner(ticket_data)
    result = ts.calculate_error_rate_for_nearby_tickets()
    print(f"Part 1 result is {result}")
