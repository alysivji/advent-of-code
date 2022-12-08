package main

import (
	"fmt"
	"os"
	"strings"
)

func findMarker(buffer string, numDistinctChars int) int {
	for i := numDistinctChars; i < len(buffer)-1; i++ {
		partialPacket := buffer[i-numDistinctChars : i]
		substringSet := make(map[byte]void)
		for j := 0; j < len(partialPacket); j++ {
			substringSet[partialPacket[j]] = member
		}
		if len(substringSet) == numDistinctChars {
			return i
		}
	}

	return -1
}

func day06() {
	if findMarker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4) != 7 {
		panic("Part 1 example is failing")
	}
	if findMarker("bvwbjplbgvbhsrlpgdmjqwftvncz", 4) != 5 {
		panic("Part 1 example is failing")
	}
	if findMarker("nppdvjthqldpwncqszvftbrmjlhg", 4) != 6 {
		panic("Part 1 example is failing")
	}
	if findMarker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4) != 10 {
		panic("Part 1 example is failing")
	}
	if findMarker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4) != 11 {
		panic("Part 1 example is failing")
	}

	input, _ := os.ReadFile("2022/data/day06_input.txt")
	data := strings.TrimSpace(string(input))
	result := findMarker(data, 4)
	fmt.Println("Part 1:", result)

	if findMarker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) != 19 {
		panic("Part 2 example is failing")
	}
	if findMarker("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) != 23 {
		panic("Part 2 example is failing")
	}
	if findMarker("nppdvjthqldpwncqszvftbrmjlhg", 14) != 23 {
		panic("Part 2 example is failing")
	}
	if findMarker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) != 29 {
		panic("Part 2 example is failing")
	}
	if findMarker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) != 26 {
		panic("Part 2 example is failing")
	}

	result = findMarker(data, 14)
	fmt.Println("Part 2:", result)
}
