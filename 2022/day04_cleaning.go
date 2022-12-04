package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func findCompletePairsOverlap(filePath string) int {
	input, _ := os.ReadFile(filePath)
	lines := strings.Split(strings.TrimSpace(string(input)), "\n")

	totalOverlaps := 0

	for _, line := range lines {
		sections := strings.Split(line, ",")

		elf1Range := sections[0]
		inclusiveRange := strings.Split(elf1Range, "-")
		elf1Lo, _ := strconv.Atoi(inclusiveRange[0])
		elf1Hi, _ := strconv.Atoi(inclusiveRange[1])

		elf2Range := sections[1]
		inclusiveRange = strings.Split(elf2Range, "-")
		elf2Lo, _ := strconv.Atoi(inclusiveRange[0])
		elf2Hi, _ := strconv.Atoi(inclusiveRange[1])

		sectionsToClean := make(map[int]void)
		var longestHi, longestLo, shortestHi, shortestLo int
		if (elf2Hi - elf2Lo) > (elf1Hi - elf1Lo) {
			longestHi = elf2Hi
			longestLo = elf2Lo

			shortestHi = elf1Hi
			shortestLo = elf1Lo
		} else {
			longestHi = elf1Hi
			longestLo = elf1Lo

			shortestHi = elf2Hi
			shortestLo = elf2Lo
		}

		for i := longestLo; i <= longestHi; i++ {
			sectionsToClean[i] = member
		}
		numSectionsForLongestHi := len(sectionsToClean)

		for i := shortestLo; i <= shortestHi; i++ {
			sectionsToClean[i] = member
		}
		if len(sectionsToClean) == numSectionsForLongestHi {
			totalOverlaps++
		}
	}

	return totalOverlaps
}

func findPartialPairsOverlap(filePath string) int {
	input, _ := os.ReadFile(filePath)
	lines := strings.Split(strings.TrimSpace(string(input)), "\n")

	totalOverlaps := 0

	for _, line := range lines {
		sections := strings.Split(line, ",")

		elf1Range := sections[0]
		inclusiveRange := strings.Split(elf1Range, "-")
		elf1Lo, _ := strconv.Atoi(inclusiveRange[0])
		elf1Hi, _ := strconv.Atoi(inclusiveRange[1])

		elf2Range := sections[1]
		inclusiveRange = strings.Split(elf2Range, "-")
		elf2Lo, _ := strconv.Atoi(inclusiveRange[0])
		elf2Hi, _ := strconv.Atoi(inclusiveRange[1])

		sectionsToClean := make(map[int]void)
		var longestHi, longestLo, shortestHi, shortestLo int
		if (elf2Hi - elf2Lo) > (elf1Hi - elf1Lo) {
			longestHi = elf2Hi
			longestLo = elf2Lo

			shortestHi = elf1Hi
			shortestLo = elf1Lo
		} else {
			longestHi = elf1Hi
			longestLo = elf1Lo

			shortestHi = elf2Hi
			shortestLo = elf2Lo
		}

		for i := longestLo; i <= longestHi; i++ {
			sectionsToClean[i] = member
		}

		numSectionsForLongestHi := len(sectionsToClean)
		for i := shortestLo; i <= shortestHi; i++ {
			sectionsToClean[i] = member

			if len(sectionsToClean) == numSectionsForLongestHi {
				totalOverlaps++
				break
			} else {
				numSectionsForLongestHi++
			}
		}
	}

	return totalOverlaps
}

func day04() {
	// Part 1
	result := findCompletePairsOverlap("2022/data/day04_sample.txt")
	if result != 2 {
		panic("Part 1 example is failing")
	}

	result = findCompletePairsOverlap("2022/data/day04_input.txt")
	fmt.Println("Part 1:", result)

	// Part 2
	// result = findPartialPairsOverlap("2022/data/day04_sample.txt")
	// if result != 4 {
	// 	panic("Part 2 example is failing")
	// }

	result = findPartialPairsOverlap("2022/data/day04_input.txt")
	fmt.Println("Part 2:", result)
}
