with open("2017/day01_input.txt") as f:
    captcha = f.read().strip()

total = 0

for i, _ in enumerate(captcha[:-1]):
    if captcha[i] == captcha[i + 1]:
        total += int(captcha[i])

if captcha[0] == captcha[-1]:
    total += int(captcha[0])

print(total)

def part2(captcha):
    steps_fwd = int(len(captcha) / 2)

    total = 0
    for i in range(steps_fwd):
        if captcha[i] == captcha[i + steps_fwd]:
            total += int(captcha[i]) * 2

    return total

print(part2(captcha))
