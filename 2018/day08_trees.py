TEST_INPUT = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
TEST_INPUT1 = "2 3 1 1 0 1 99 2 0 3 10 11 12 1 1 2"
integerize = lambda values: [int(val) for val in values.split(" ")]


def process(tree):
    curr_pos = 2
    num_children, num_metadata = tree[:curr_pos]
    # if num_metadata == 0:
    #     raise ValueError

    if num_children > 0:
        metadata = tree[-num_metadata:]
        rest = tree[curr_pos:-num_metadata]
        print(len(tree))
        print(tree)
        print(rest)
        print(len(rest))
        # if len(rest) == 18194:
        #     import pdb; pdb.set_trace()
        return process(rest) + sum(metadata)
    if num_children == 0:
        end_pos = num_metadata + 2
        leaf_sum = sum(tree[2:end_pos])
        rest = tree[end_pos:]
        if rest:
            return leaf_sum + process(rest, tree)
        return leaf_sum

# assert process(integerize(TEST_INPUT)) == 138
print(process(integerize(TEST_INPUT1)))


if __name__ == "__main__":
    with open("day08_input.txt", "r") as f:
        tree = f.read().strip()

    # print(process(integerize(tree)))
