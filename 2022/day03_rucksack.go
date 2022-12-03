package main

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

func readRucksackFile(filePath string) []string {
	input, _ := os.ReadFile(filePath)
	return strings.Split(strings.TrimSpace(string(input)), "\n")
}

func scoreCommonItemInEachRucksack(rucksacks []string) int {
	// parse each rucksack component
	allRucksacks := make([]rucksack, 0)
	for _, line := range rucksacks {
		rucksack := rucksack{comparment1: line[:len(line)/2], comparment2: line[len(line)/2:]}
		allRucksacks = append(allRucksacks, rucksack)
	}

	// score common elements
	totalScore := 0
	for _, rucksack := range allRucksacks {
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

func scoreGroupsUniqueItems(rucksacks []string) int {
	totalScore := 0

	// elves hang out in triples
	for i := 0; i < len(rucksacks)/3; i++ {

		elf1RuckSack := rucksacks[i*3]
		elf1Set := make(map[int]void)
		for _, item := range elf1RuckSack {
			elf1Set[int(item)] = member
		}

		elf2RuckSack := rucksacks[(i*3)+1]
		elf2Set := make(map[int]void)
		for _, item := range elf2RuckSack {
			elf2Set[int(item)] = member
		}

		elf3RuckSack := rucksacks[(i*3)+2]
		elf3Set := make(map[int]void)
		for _, item := range elf3RuckSack {
			elf3Set[int(item)] = member
		}

		for k := range elf1Set {
			if _, ok := elf2Set[k]; ok {
				if _, ok := elf3Set[k]; ok {
					if k > 90 {
						totalScore += (k - 96)
					} else {
						totalScore += (k - 38)
					}
				}
			}
		}
	}

	return totalScore
}

func day03() {
	// Part 1
	rucksacks := readRucksackFile("2022/data/day03_sample.txt")
	result := scoreCommonItemInEachRucksack(rucksacks)
	if result != 157 {
		panic("Part 1 example is failing")
	}

	rucksacks = readRucksackFile("2022/data/day03_input.txt")
	result = scoreCommonItemInEachRucksack(rucksacks)
	fmt.Println("Part 1:", result)

	// Part 2
	rucksacks = readRucksackFile("2022/data/day03_sample.txt")
	result = scoreGroupsUniqueItems(rucksacks)
	if result != 70 {
		panic("Part 2 example is failing")
	}

	rucksacks = readRucksackFile("2022/data/day03_input.txt")
	result = scoreGroupsUniqueItems(rucksacks)
	fmt.Println("Part 2:", result)
}
