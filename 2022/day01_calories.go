package main

// have to install ioutil
// go get io/ioutil

import (
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"strings"
)

func readFile(filePath string) [][]int {
	body, err := ioutil.ReadFile(filePath)

	if err != nil {
		log.Fatalf("unable to read file: %v", err)
	}

	allElfCalories := make([][]int, 0)

	// run through each elf seprately
	caloriesString := strings.Split(strings.Trim(string(body), "\n"), "\n\n")
	for _, elfCaloriesString := range caloriesString {
		elfCalories := make([]int, 0)

		itemCalories := strings.Split(elfCaloriesString, "\n")
		for _, itemCalorie := range itemCalories {
			i, _ := strconv.Atoi(itemCalorie)
			elfCalories = append(elfCalories, i)
		}

		allElfCalories = append(allElfCalories, elfCalories)
	}

	return allElfCalories
}

func findElfWithMaxCalories(caloriesByElf [][]int) int {
	maxCalories := 0
	for _, elfCalories := range caloriesByElf {
		var currElfTotal = 0
		for _, itemCalorie := range elfCalories {
			currElfTotal += itemCalorie
		}

		if currElfTotal > maxCalories {
			maxCalories = currElfTotal
		}
	}

	return maxCalories
}

func main() {
	var caloriesByElf = readFile("2022/data/day01_sample.txt")
	result := findElfWithMaxCalories(caloriesByElf)
	if result != 24000 {
		panic("Part 1 example is failing")
	}

	caloriesByElf = readFile("2022/data/day01_input.txt")
	result = findElfWithMaxCalories(caloriesByElf)
	fmt.Println("Part 1:", result)
}
