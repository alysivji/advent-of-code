from collections import defaultdict
from datetime import datetime
import re
from typing import Dict, List, NamedTuple

LOG_PATTERN = r"\[(?P<timestamp>.+)\] (?P<action>.+)"


class Log(NamedTuple):
    timestamp: datetime
    action: str


def load_input(lines: List[str]) -> List[Log]:
    p = re.compile(LOG_PATTERN)

    logs = []
    for line in lines:
        cleaned_line = line.strip()
        m = p.match(cleaned_line)

        log = Log(
            timestamp=datetime.strptime(m.group("timestamp"), "%Y-%m-%d %H:%M"),
            action=m.group("action"),
        )
        logs.append(log)
    return logs


def create_sleep_schedule(logs: List[Log]) -> Dict[int, List[List[int]]]:
    sleep_schedule: Dict[int, List[List[int]]] = defaultdict(list)
    for log in logs:
        if log.action.startswith("Guard #"):
            guard_num = int(re.findall(r"-?\d+", log.action)[0])
        if log.action.startswith("falls asleep"):
            sleep_start = log.timestamp.minute
        if log.action.startswith("wakes up"):
            sleep_end = log.timestamp.minute
            hour: List[int] = [0] * 60
            hour[sleep_start:sleep_end] = [1] * (sleep_end - sleep_start)
            sleep_schedule[guard_num].append(hour)
    return sleep_schedule


def find_most_minutes_slept(sleep_schedule: Dict[int, List[List[int]]]) -> int:
    max_slept = 0
    drowiest = 0
    for key, value in sleep_schedule.items():
        total_slept = sum([sum(single_sleep) for single_sleep in value])
        if total_slept > max_slept:
            max_slept = total_slept
            drowiest = key
    return drowiest


def minute_sleep_the_most(sleep_schedule: Dict[int, List[List[int]]], guard) -> int:
    drowsiest_minute = 0
    minutes_slept = 0
    for idx in range(60):
        times_slept_in_min = 0
        for sleep in sleep_schedule[guard]:
            times_slept_in_min += sleep[idx]
        if times_slept_in_min > minutes_slept:
            drowsiest_minute = idx
            minutes_slept = times_slept_in_min
    return drowsiest_minute


def minute_sleep_the_most_all(sleep_schedule: Dict[int, List[List[int]]]) -> int:
    drowsiest_minute = 0
    minutes_slept = 0
    drowsiest_guard = 0
    for guard in sleep_schedule.keys():
        for idx in range(60):
            times_slept_in_min = 0
            for sleep in sleep_schedule[guard]:
                times_slept_in_min += sleep[idx]
            if times_slept_in_min > minutes_slept:
                drowsiest_minute = idx
                drowsiest_guard = guard
                minutes_slept = times_slept_in_min
    return drowsiest_guard * drowsiest_minute


TEST_INPUT = """[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up""".split(
    "\n"
)
sleep_schedule = create_sleep_schedule(load_input(TEST_INPUT))
drowsiest = find_most_minutes_slept(sleep_schedule)
min_slept_most = minute_sleep_the_most(sleep_schedule, drowsiest)
assert drowsiest == 10
assert min_slept_most == 24
assert drowsiest * min_slept_most == 240
assert minute_sleep_the_most_all(sleep_schedule) == 4455


if __name__ == "__main__":
    with open("day04_input.txt", "r") as f:
        lines = f.readlines()
    logs = sorted(load_input(lines), key=lambda x: x.timestamp)

    sleep_schedule = create_sleep_schedule(logs)
    drowsiest = find_most_minutes_slept(sleep_schedule)
    min_slept_most = minute_sleep_the_most(sleep_schedule, drowsiest)
    print(drowsiest * min_slept_most)
    print(minute_sleep_the_most_all(sleep_schedule))
