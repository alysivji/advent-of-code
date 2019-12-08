from collections import Counter
from typing import List, NamedTuple


class Image(NamedTuple):
    h: int
    w: int


def separate_layers(img_str: str, img: Image) -> dict:
    num = len(img_str) / (img.h * img.w)

    layers = []
    for idx in range(int(num)):
        start_idx = idx * (img.h * img.w)
        end_idx = (idx + 1) * (img.h * img.w)
        image = img_str[start_idx:end_idx]
        layers.append(image)

    return layers


def find_layer_with_fewest_digit(layers: List, digit: str):
    counters = []

    for layer in layers:
        counter = Counter(layer)
        counters.append(counter)

    digit_count = [counter[digit] for counter in counters]
    idx = digit_count.index(min(digit_count))
    return layers[idx]


def calculate_result(layer: str) -> int:
    counter = Counter(layer)
    return counter['1'] * counter['2']


def test_calculate_result():
    img = Image(w=3, h=2)
    TEST_INPUT = "123456789012"
    layers = separate_layers(TEST_INPUT, img)
    assert len(layers) == 2

    layer = find_layer_with_fewest_digit(layers, '0')
    result = calculate_result(layer)

    assert result == 1


def min_image(layers: List[str]) -> str:
    min_image = []
    for idx in range(len(layers[0])):
        vertical_pixels = []
        for layer in layers:
            vertical_pixels.append(int(layer[idx]))

        # find_first_non_two
        max_val = 2
        for val in vertical_pixels:
            if val < max_val:
                min_image.append(val)
                break

    return min_image


def test_min_image():
    TEST_INPUT = "0222112222120000"
    img = Image(w=2, h=2)
    layers = separate_layers(TEST_INPUT, img)

    result = min_image(layers)

    assert result == [0, 1, 1, 0]


if __name__ == "__main__":
    with open("2019/data/day08_input.txt", "r") as f:
        img_str = f.readline().strip()

    img = Image(w=25, h=6)
    layers = separate_layers(img_str, img)
    layer = find_layer_with_fewest_digit(layers, '0')
    result = calculate_result(layer)

    print(f"Result is {result}")

    result = min_image(layers)
    result_scrubbed = [' ' if item == 0 else str(item) for item in result]

    for line in range(img.h):
        start_idx = line * img.w
        end_idx = (line + 1) * img.w
        print(result_scrubbed[start_idx:end_idx])
