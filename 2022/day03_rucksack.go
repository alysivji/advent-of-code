package main

// have to install ioutil
// go get io/ioutil

import (
	"fmt"
	"os"
	"strings"
)

type rucksack struct {
	comparment1 string
	comparment2 string
}
type void struct{}

var member void

func readRucksackFile(filePath string) []rucksack {
	input, _ := os.ReadFile(filePath)
	lines := strings.Split(strings.TrimSpace(string(input)), "\n")

	allRucksacks := make([]rucksack, 0)

	for _, line := range lines {
		rucksack := rucksack{comparment1: line[:len(line)/2], comparment2: line[len(line)/2:]}
		allRucksacks = append(allRucksacks, rucksack)
	}

	return allRucksacks
}

func scoreCommonItem(rucksacks []rucksack) int {
	totalScore := 0

	for _, rucksack := range rucksacks {
		comparment1Set := make(map[int]void)
		for _, item := range rucksack.comparment1 {
			comparment1Set[int(item)] = member
		}

		comparment2Set := make(map[int]void)
		for _, item := range rucksack.comparment2 {
			comparment2Set[int(item)] = member
		}

		for k := range comparment1Set {
			if _, ok := comparment2Set[k]; ok {
				if k > 90 {
					totalScore += (k - 96)
				} else {
					totalScore += (k - 38)
				}
			}
		}
	}

	return totalScore
}

func day03() {
	// Part 1
	rucksacks := readRucksackFile("2022/data/day03_sample.txt")
	result := scoreCommonItem(rucksacks)

	if result != 157 {
		panic("Part 1 example is failing")
	}

	rucksacks = readRucksackFile("2022/data/day03_input.txt")
	result = scoreCommonItem(rucksacks)
	fmt.Println("Part 1:", result)

	// // Part 2
	// games = readRoShamBoFilePart2("2022/data/day02_sample.txt")
	// result = scoreRoShamBoGames(games)

	// if result != 12 {
	// 	panic("Part 2 example is failing")
	// }

	// games = readRoShamBoFilePart2("2022/data/day02_input.txt")
	// result = scoreRoShamBoGames(games)
	// fmt.Println("Part 2:", result)
}
