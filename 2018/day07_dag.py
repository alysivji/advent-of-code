from collections import defaultdict
from queue import PriorityQueue
import re
from typing import Any, Dict, List, NamedTuple, Set


STEP_PATTERN = r"Step (?P<curr>[A-Z]).*step (?P<next>[A-Z]).*."

TEST_INPUT = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""".split(
    "\n"
)


def load_input(lines: List[str]):
    downstream: Dict[str, List[str]] = defaultdict(list)
    upstream: Dict[str, List[str]] = defaultdict(list)

    p = re.compile(STEP_PATTERN)
    for line in lines:
        m = p.match(line.strip())
        downstream[m.group("curr")].append(m.group("next"))
        upstream[m.group("next")].append(m.group("curr"))
    return upstream, downstream


# @_print("part1")
def process_steps_synchronous(upstream, downstream) -> str:
    # find the one that isn't in any of the descendents
    no_upstream = set(downstream.keys()) - set(upstream.keys())

    # make a priority queue
    queue: PriorityQueue = PriorityQueue()
    for move in no_upstream:
        queue.put((ord(move), move))

    result = ""
    visited: Set[str] = set()
    to_visit: Set[str] = set()
    while not queue.empty():
        curr_item = queue.get()[1]
        visited.add(curr_item)
        result += curr_item

        for next_step in downstream[curr_item]:
            # are its upstream tasks done?
            all_visisted = True
            for prev_step in upstream[next_step]:
                if prev_step not in visited:
                    all_visisted = False

            if all_visisted and next_step not in to_visit:
                to_visit.add(next_step)
                queue.put((ord(next_step), next_step))
    return result


def time_to_complete(letter: str, task_constant) -> int:
    ASCII_DIFF = ord("A") - 1
    return ord(letter) - ASCII_DIFF + task_constant


assert time_to_complete("A", task_constant=0) == 1
assert time_to_complete("B", task_constant=60) == 62


class Task(NamedTuple):
    end_time: int
    item: Any


def peek(queue: PriorityQueue) -> Task:
    item = queue.queue[0]
    return Task(item[0], item[1])


def process_time_concurrent(upstream, downstream, num_workers, const) -> int:
    job_queue: PriorityQueue = PriorityQueue()
    workers: PriorityQueue = PriorityQueue(maxsize=num_workers)

    # run initial set of tasks (-1 b/c we start at 0)
    kickoff_tasks = set(downstream.keys()) - set(upstream.keys())
    for task in kickoff_tasks:
        task_time = time_to_complete(task, const)
        workers.put((task_time - 1, task))
    curr_time = peek(workers).end_time

    completed_tasks = set()
    queued_tasks = set()
    all_tasks = set(list(downstream) + list(upstream))
    while completed_tasks != all_tasks:
        # process completed tasks
        while not workers.empty():
            if peek(workers).end_time != curr_time:
                break

            finished_task = workers.get()[1]
            completed_tasks.add(finished_task)

            # find tasks we can add to queue
            for next_task in downstream[finished_task]:
                upstream_complete = True
                for dependency in upstream[next_task]:
                    if dependency not in completed_tasks:
                        upstream_complete = False
                        break

                if upstream_complete and next_task not in queued_tasks:
                    job_queue.put((ord(next_task), next_task))
                    queued_tasks.add(next_task)

        # assign the workers tasks
        while not job_queue.empty() and not workers.full():
            next_task = job_queue.get()[1]
            task_time = time_to_complete(next_task, const)
            workers.put((curr_time + task_time, next_task))

        # advance to time that next event is done
        if not workers.empty():
            curr_time = peek(workers).end_time
    return curr_time + 1


test_up, test_down = load_input(TEST_INPUT)
assert process_steps_synchronous(test_up, test_down) == "CABDFE"
assert process_time_concurrent(test_up, test_down, num_workers=2, const=0) == 15


if __name__ == "__main__":
    with open("data/day07_input.txt") as f:
        lines = f.readlines()
    upstream, downstream = load_input(lines)
    print(process_steps_synchronous(upstream, downstream))
    print(process_time_concurrent(upstream, downstream, num_workers=5, const=60))
