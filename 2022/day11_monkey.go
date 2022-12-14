package main

import (
	"fmt"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"

	"github.com/gammazero/deque"
	"github.com/maja42/goval"
)

type MonkeyDetails struct {
	items       deque.Deque[int]
	operation   string
	divisibleBy int
	ifTrue      int // monkey to throw to
	ifFalse     int // monkey to throw to
}

func readAndParseMonkeyInformation(filePath string) map[int]MonkeyDetails {
	input, _ := os.ReadFile(filePath)
	inputByMonkey := strings.Split(strings.TrimSpace(string(input)), "\n\n")

	const STARTING_ITEMS = "  Starting items: "
	const OPERATION = "  Operation: new = "
	const TEST = "  Test: divisible by "
	const IF_TRUE = "    If true: throw to monkey "
	const IF_FALSE = "    If false: throw to monkey "

	monkeyData := make(map[int]MonkeyDetails)
	for monkeyNum, monkeyInput := range inputByMonkey {
		var startingItems deque.Deque[int]
		var operation string
		var divisibleBy int
		var ifTrue int
		var ifFalse int
		for _, monkeyLine := range strings.Split(monkeyInput, "\n") {
			if strings.HasPrefix(monkeyLine, STARTING_ITEMS) {
				startingItemsStr := monkeyLine[len(STARTING_ITEMS):]
				for _, item := range strings.Fields(startingItemsStr) {
					if strings.HasSuffix(item, ",") {
						num, _ := strconv.Atoi(item[:len(item)-1])
						startingItems.PushBack(num)
					} else {
						num, _ := strconv.Atoi(item)
						startingItems.PushBack(num)
					}
				}
			} else if strings.HasPrefix(monkeyLine, OPERATION) {
				operation = monkeyLine[len(OPERATION):]
			} else if strings.HasPrefix(monkeyLine, TEST) {
				divisibleBy, _ = strconv.Atoi(monkeyLine[len(TEST):])
			} else if strings.HasPrefix(monkeyLine, IF_TRUE) {
				ifTrue, _ = strconv.Atoi(monkeyLine[len(IF_TRUE):])
			} else if strings.HasPrefix(monkeyLine, IF_FALSE) {
				ifFalse, _ = strconv.Atoi(monkeyLine[len(IF_FALSE):])
			}
		}

		monkeyData[monkeyNum] = MonkeyDetails{
			items:       startingItems,
			operation:   operation,
			divisibleBy: divisibleBy,
			ifTrue:      ifTrue,
			ifFalse:     ifFalse,
		}
	}
	return monkeyData
}

func simulateMonkeyInTheMiddle(monkeyData map[int]MonkeyDetails, numRounds int, feelRelief bool) int {
	var itemsInspected []int
	itemsInspected = make([]int, len(monkeyData))

	for round := 0; round < numRounds; round++ {
		for monkeyNum := 0; monkeyNum < len(monkeyData); monkeyNum++ {
			currMonkeyInfo := monkeyData[monkeyNum]
			for currMonkeyInfo.items.Len() != 0 {
				itemWorryLevel := currMonkeyInfo.items.PopFront()
				itemsInspected[monkeyNum] += 1

				eval := goval.NewEvaluator()
				variables := map[string]interface{}{
					"old": itemWorryLevel,
				}
				result, _ := eval.Evaluate(currMonkeyInfo.operation, variables, nil)
				currentWorryLevel, _ := result.(int)

				if feelRelief {
					currentWorryLevel = int(math.Floor(float64((currentWorryLevel) / 3)))
				}

				var monkeyToThrowTo int
				if currentWorryLevel%currMonkeyInfo.divisibleBy == 0 {
					monkeyToThrowTo = currMonkeyInfo.ifTrue
				} else {
					monkeyToThrowTo = currMonkeyInfo.ifFalse
				}

				monkeyInfo := monkeyData[monkeyToThrowTo]
				monkeyInfo.items.PushBack(currentWorryLevel)
				monkeyData[monkeyToThrowTo] = monkeyInfo
			}
			monkeyData[monkeyNum] = currMonkeyInfo
		}
		// fmt.Println(itemsInspected)
	}

	sort.Ints(itemsInspected)
	return itemsInspected[len(itemsInspected)-1] * itemsInspected[len(itemsInspected)-2]
}

func day11() {
	var monkeyData map[int]MonkeyDetails
	var monkeyBusinessLevel int

	// sample input
	monkeyData = readAndParseMonkeyInformation("2022/data/day11_sample.txt")
	monkeyBusinessLevel = simulateMonkeyInTheMiddle(monkeyData, 20, true)
	if monkeyBusinessLevel != 10605 {
		panic("Part 1 example is failing")
	}
	// monkeyBusinessLevel = simulateMonkeyInTheMiddle(monkeyData, 1000, false)
	// fmt.Println(monkeyBusinessLevel)
	// if monkeyBusinessLevel != 2713310158 {
	// 	panic("Part 2 example is failing")
	// }

	monkeyData = readAndParseMonkeyInformation("2022/data/day11_input.txt")
	monkeyBusinessLevel = simulateMonkeyInTheMiddle(monkeyData, 20, true)
	fmt.Println("Part 1:", monkeyBusinessLevel)
}
