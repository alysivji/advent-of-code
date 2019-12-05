from utils import IntCodeComputer


if __name__ == "__main__":
    with open("2019/data/day05_input.txt") as f:
        intcode_program = f.readline().strip()

    cpu = IntCodeComputer(intcode_program, input_value=1)
    cpu.process()
    print(cpu)
