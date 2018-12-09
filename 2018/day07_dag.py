from collections import defaultdict, deque
from queue import PriorityQueue
import re
from typing import Dict, List, Set


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
def process_steps(upstream, downstream) -> str:
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


def time_to_complete(letter: str, step_time) -> int:
    ASCII_DIFF = ord("A") - 1
    return ord(letter) - ASCII_DIFF + step_time


assert time_to_complete("A", 0) == 1
assert time_to_complete("B", 60) == 62


def find_free_worker(workers):
    return min(idx for idx in workers.keys() if workers[idx] is None)


def process_time(steps, upstream, num_workers, step_time_constant) -> int:
    completed_steps: Set[str] = set([])
    queue = deque([step for step in steps])
    processing: PriorityQueue = PriorityQueue()
    elapsed_time = 0

    workers = {idx: None for idx in range(num_workers)}
    free_workers = num_workers

    while len(queue):
        # are the downstream steps complete?
        dependencies_complete = True
        prev_steps = upstream.get(queue[0], None)
        if prev_steps is not None:
            for step in prev_steps:
                if step not in completed_steps:
                    dependencies_complete = False

        # assign to free worker
        if dependencies_complete and free_workers > 0:
            step = queue.popleft()
            step_time = time_to_complete(step, step_time_constant)
            free_workers -= 1

            # assign to free worker
            worker = find_free_worker(workers)
            workers[worker] = step
            processing.put(((elapsed_time + step_time), step))

        # TODO loop thru each free worker
        # TODO what to do when task is done?

    return 0


test_upstream, test_downstream = load_input(TEST_INPUT)
test_steps = process_steps(test_upstream, test_downstream)
assert test_steps == "CABDFE"


if __name__ == "__main__":
    with open("data/day07_input.txt") as f:
        lines = f.readlines()
    upstream, downstream = load_input(lines)
    print(process_steps(upstream, downstream))
