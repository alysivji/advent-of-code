package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type RopeMove struct {
	direction string
	units     int
}

func parseRopeMoves(filePath string) []RopeMove {
	input, _ := os.ReadFile(filePath)
	inputLines := strings.Split(strings.TrimSpace(string(input)), "\n")

	var moves []RopeMove
	for _, line := range inputLines {
		lineElements := strings.Fields(line)
		units, _ := strconv.Atoi(lineElements[1])
		move := RopeMove{direction: lineElements[0], units: units}
		moves = append(moves, move)
	}
	return moves
}

var dir_to_vector_map = map[string]Point{
	"R": {x: 0, y: +1},
	"L": {x: 0, y: -1},
	"U": {x: -1, y: 0},
	"D": {x: +1, y: 0},
}

var allDirectionVectors = []Point{
	{x: -1, y: -1},
	{x: 0, y: -1},
	{x: +1, y: -1},
	{x: -1, y: 0},
	{x: 0, y: 0},
	{x: +1, y: 0},
	{x: -1, y: +1},
	{x: 0, y: +1},
	{x: +1, y: +1},
}

func processMovesAndTrackTail(moves []RopeMove) []Point {
	// return list of tail positions after each step

	headPos := Point{x: 0, y: 0}
	tailPos := Point{x: 0, y: 0}

	var tailTracker []Point
	tailTracker = append(tailTracker, tailPos)

	// step through each move, one step at a time
	for _, move := range moves {
		dirVector := dir_to_vector_map[move.direction]

		for i := 0; i < move.units; i++ {
			headPos = headPos.add(dirVector)

			shouldTailMove := true
			for _, dirVector := range allDirectionVectors {
				allowedTailPosition := headPos.add(dirVector)
				if tailPos == allowedTailPosition {
					shouldTailMove = false
				}
			}
			if !shouldTailMove {
				tailTracker = append(tailTracker, tailPos)
				continue
			}

			// normalize distance so we only move 1 space
			var moveTailVector Point
			if headPos.x == tailPos.x {
				moveTailVector = Point{x: 0, y: (headPos.y - tailPos.y) / IntAbs(headPos.y-tailPos.y)}
			} else if headPos.y == tailPos.y {
				moveTailVector = Point{x: (headPos.x - tailPos.x) / IntAbs(headPos.x-tailPos.x), y: 0}
			} else {
				delta_x := (headPos.x - tailPos.x) / IntAbs(headPos.x-tailPos.x)
				delta_y := (headPos.y - tailPos.y) / IntAbs(headPos.y-tailPos.y)
				moveTailVector = Point{x: delta_x, y: delta_y}
			}

			tailPos = tailPos.add(moveTailVector)
			tailTracker = append(tailTracker, tailPos)
		}
	}

	return tailTracker
}

func countNumUniquePositions(positions []Point) int {
	uniquePositions := make(map[Point]void)
	for _, position := range positions {
		uniquePositions[position] = member
	}

	numUniquePositions := 0
	for range uniquePositions {
		numUniquePositions++
	}

	return numUniquePositions
}

func day09() {
	// sample input
	moves := parseRopeMoves("2022/data/day09_sample.txt")
	tailPositions := processMovesAndTrackTail(moves)
	result := countNumUniquePositions(tailPositions)
	fmt.Println(result)
	if result != 13 {
		panic("Part 1 example is failing")
	}

	moves = parseRopeMoves("2022/data/day09_input.txt")
	tailPositions = processMovesAndTrackTail(moves)
	result = countNumUniquePositions(tailPositions)
	fmt.Println("Part 1:", result)
}
