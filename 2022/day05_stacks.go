package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"github.com/gammazero/deque"
)

type StackMove struct {
	startStack     int
	endStack       int
	numBoxesToMove int
}

type towersOfHanoi struct {
	towers []*deque.Deque[string]
	moves  []StackMove
}

func parseTowersOfHanoiInput(filepath string, sample bool) towersOfHanoi {
	input, _ := os.ReadFile(filepath)
	lines := strings.Split(string(input), "\n\n")

	// parse towers
	var numTowers int
	if sample {
		numTowers = 3
	} else {
		numTowers = 9
	}
	// initialize towers
	var towers []*deque.Deque[string]
	for i := 0; i < numTowers; i++ {
		stringDeque := deque.New[string]()
		towers = append(towers, stringDeque)
	}
	// parse towers
	towerLines := strings.Split(lines[0], "\n")
	for _, towerLine := range towerLines[:len(towerLines)-1] {
		for i := 0; i < numTowers; i++ {
			elementLocation := (4 * i) + 1
			if elementLocation > len(towerLine)-1 {
				continue
			}
			stackElement := string(towerLine[elementLocation])

			if stackElement != " " {
				towers[i].PushBack(stackElement)
			}
		}
	}

	// parse moves
	scanner := bufio.NewScanner(strings.NewReader(lines[1]))
	var moves []StackMove
	for scanner.Scan() {
		var startStack, endStack, numBoxesToMove int
		fmt.Sscanf(scanner.Text(), "move %d from %d to %d", &numBoxesToMove, &startStack, &endStack)
		moves = append(moves, StackMove{startStack: startStack - 1, endStack: endStack - 1, numBoxesToMove: numBoxesToMove})
	}

	return towersOfHanoi{moves: moves, towers: towers}
}

func processOneCrateAtATime(towerData towersOfHanoi) string {
	for _, move := range towerData.moves {
		for i := 0; i < move.numBoxesToMove; i++ {
			item := towerData.towers[move.startStack].PopFront()
			towerData.towers[move.endStack].PushFront(item)
		}
	}

	var output string
	for _, tower := range towerData.towers {
		output += tower.Front()
	}
	return output
}

func processMultipleCratesAtATime(towerData towersOfHanoi) string {
	for _, move := range towerData.moves {
		var tempStack deque.Deque[string]
		for i := 0; i < move.numBoxesToMove; i++ {
			item := towerData.towers[move.startStack].PopFront()
			tempStack.PushFront(item)
		}
		for tempStack.Len() > 0 {
			item := tempStack.PopFront()
			towerData.towers[move.endStack].PushFront(item)
		}
	}

	var output string
	for _, tower := range towerData.towers {
		output += tower.Front()
	}
	return output
}

func day05() {
	towerData := parseTowersOfHanoiInput("2022/data/day05_sample.txt", true)
	result := processOneCrateAtATime(towerData)
	if result != "CMZ" {
		panic("Part 1 example is failing")
	}

	towerData = parseTowersOfHanoiInput("2022/data/day05_input.txt", false)
	result = processOneCrateAtATime(towerData)
	fmt.Println("Part 1:", result)

	towerData = parseTowersOfHanoiInput("2022/data/day05_sample.txt", true)
	result = processMultipleCratesAtATime(towerData)
	if result != "MCD" {
		panic("Part 2 example is failing")
	}

	towerData = parseTowersOfHanoiInput("2022/data/day05_input.txt", false)
	result = processMultipleCratesAtATime(towerData)
	fmt.Println("Part 2:", result)
}
