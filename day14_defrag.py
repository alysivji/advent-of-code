from collections import Counter

from day10_knothash import knot_hash

assert knot_hash("206,63,255,131,65,80,238,157,254,24,133,2,16,0,1,3") == '20b7b54c92bf73cf3e5631458a715149'  # noqa

TEST_INPUT = 'flqrgnkx'

# from https://joernhees.de/blog/2010/09/21/how-to-convert-hex-strings-to-binary-ascii-strings-in-python-incl-8bit-space/
binary = lambda x: "".join(reversed( [i+j for i,j in zip( *[ ["{0:04b}".format(int(c,16)) for c in reversed("0"+x)][n::2] for n in [1,0] ] ) ] ))  # noqa


def calculate_knot_hash_grid(key):
    row_keys = [f'{key}-{i}' for i in range(128)]

    row_keys_hashed = [knot_hash(row).replace(' ', '0') for row in row_keys]
    row_keys_binary = [binary(row) for row in row_keys_hashed]
    counts = [Counter(list(row)) for row in row_keys_binary]
    count1s = [row['1'] for row in counts]
    return sum(count1s)


if __name__ == "__main__":
    assert calculate_knot_hash_grid(TEST_INPUT) == 8108

    print(calculate_knot_hash_grid('jxqlasbh'))
