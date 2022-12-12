package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func readAndParseCpuInstructionSet(filePath string) []string {
	input, _ := os.ReadFile(filePath)
	return strings.Split(strings.TrimSpace(string(input)), "\n")
}

func executeProgramAndTrackXValue(instructions []string) []int {
	var xValues []int

	// x starts at 1
	xValues = append(xValues, 1)
	for _, instruction := range instructions {
		x := xValues[len(xValues)-1]

		xValues = append(xValues, x)
		if strings.HasPrefix(instruction, "noop") {
			continue
		}

		parts := strings.Fields(instruction)
		addValue, _ := strconv.Atoi(parts[1])
		xValues = append(xValues, x+addValue)
	}

	return xValues
}

func calculateSignalStrength(xs []int) int {
	signalStrength := 0
	for i, x := range xs {
		cycleNum := i + 1

		if cycleNum == 20 || (cycleNum%40 == 20) {
			signalStrength += x * cycleNum
		}
	}

	return signalStrength
}

func drawCrtImage(xs []int) {
	for height := 0; height < 6; height++ {
		for pos := 0; pos <= 39; pos++ {
			spriteMiddlePos := xs[(height*40)+pos]

			if (spriteMiddlePos-1 <= pos) && (pos <= spriteMiddlePos+1) {
				fmt.Print("#")
			} else {
				fmt.Print(" ")
			}
		}
		fmt.Print("\n")
	}
}

func day10() {
	var instructions []string
	var xs []int
	var signalStrength int

	// sample input
	instructions = readAndParseCpuInstructionSet("2022/data/day10_sample.txt")
	xs = executeProgramAndTrackXValue(instructions)
	signalStrength = calculateSignalStrength(xs)
	if signalStrength != 13140 {
		panic("Part 1 example is failing")
	}

	// real input
	instructions = readAndParseCpuInstructionSet("2022/data/day10_input.txt")
	xs = executeProgramAndTrackXValue(instructions)
	signalStrength = calculateSignalStrength(xs)
	fmt.Println("Part 1:", signalStrength)

	fmt.Println("Part 2:")
	drawCrtImage(xs)
}
