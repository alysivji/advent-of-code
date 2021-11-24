from collections import defaultdict
import itertools
import math


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
        self.all_valid_numbers = set().union(*self.rules.values())

    def calculate_error_rate_for_nearby_tickets(self):
        return sum(self.calculate_error_rate(ticket) for ticket in self.nearby_tickets)

    def calculate_error_rate(self, ticket):
        error_rate = 0
        for num in ticket:
            if num not in self.all_valid_numbers:
                error_rate += num

        return error_rate

    def get_valid_tickets(self):
        return [ticket for ticket in self.nearby_tickets if self.is_valid(ticket)]

    def is_valid(self, ticket):
        for num in ticket:
            if num not in self.all_valid_numbers:
                return False

        return True

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

    def deduce_ticket_fields(self):
        valid_tickets = self.get_valid_tickets()
        valid_tickets.append(self.my_ticket)

        possible_positions = {k: set() for k, v in self.rules.items()}

        for field_key in self.rules.keys():
            valid_field = True

            for idx, field_values in enumerate(zip(*valid_tickets)):
                range_to_check = self.rules[field_key]
                for value in field_values:
                    if value not in range_to_check:
                        break
                else:
                    possible_positions[field_key].add(idx)

        fields_by_length = {len(v): k for k, v in possible_positions.items()}
        current_set = set()
        field_mapping = {}

        for idx in range(len(fields_by_length)):
            current_field = fields_by_length[idx + 1]
            inferred_index = possible_positions[current_field].difference(current_set)
            field_mapping[current_field] = inferred_index.pop()
            current_set = possible_positions[current_field]

        return field_mapping


def test_part_1():
    ts = TicketScanner(TEST_INPUT)
    assert ts.calculate_error_rate_for_nearby_tickets() == 71


if __name__ == "__main__":
    with open("2020/data/day16_input.txt") as f:
        ticket_data = f.read().strip()

    ts = TicketScanner(ticket_data)
    result = ts.calculate_error_rate_for_nearby_tickets()
    print(f"Part 1 result is {result}")

    field_mapping = ts.deduce_ticket_fields()
    idx_to_multiply = [v for k, v in field_mapping.items() if k.startswith("departure")]
    values = [ts.my_ticket[idx] for idx in idx_to_multiply]
    result = math.prod(values)
    print(f"Part 2 result is {result}")
