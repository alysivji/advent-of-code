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

func processMovesAndTrackTail(moves []RopeMove, numKnots int) []Point {
	// return list of tail positions after each step
	var tailTracker []Point

	var knots []Point
	for i := 0; i < numKnots; i++ {
		knots = append(knots, Point{x: 0, y: 0})
	}
	tailTracker = append(tailTracker, knots[len(knots)-1])

	// step through each move, one step at a time
	for _, move := range moves {
		dirVector := dir_to_vector_map[move.direction]

		for i := 0; i < move.units; i++ {
			knots[0] = knots[0].add(dirVector)

			for j := 1; j < len(knots); j++ {
				prevKnot := knots[j-1]
				currKnot := knots[j]

				shouldCurrKnotMove := true
				for _, dirVector := range allDirectionVectors {
					allowedPosition := prevKnot.add(dirVector)
					if currKnot == allowedPosition {
						shouldCurrKnotMove = false
					}
				}
				if !shouldCurrKnotMove {
					break
				}

				// normalize distance so we only move 1 space
				var moveTailVector Point
				if prevKnot.x == currKnot.x {
					moveTailVector = Point{x: 0, y: (prevKnot.y - currKnot.y) / IntAbs(prevKnot.y-currKnot.y)}
				} else if prevKnot.y == currKnot.y {
					moveTailVector = Point{x: (prevKnot.x - currKnot.x) / IntAbs(prevKnot.x-currKnot.x), y: 0}
				} else {
					delta_x := (prevKnot.x - currKnot.x) / IntAbs(prevKnot.x-currKnot.x)
					delta_y := (prevKnot.y - currKnot.y) / IntAbs(prevKnot.y-currKnot.y)
					moveTailVector = Point{x: delta_x, y: delta_y}
				}

				knots[j] = currKnot.add(moveTailVector)
			}

			tailTracker = append(tailTracker, knots[len(knots)-1])
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
	tailPositions := processMovesAndTrackTail(moves, 2)
	result := countNumUniquePositions(tailPositions)
	if result != 13 {
		panic("Part 1 example is failing")
	}

	tailPositions = processMovesAndTrackTail(moves, 10)
	result = countNumUniquePositions(tailPositions)
	if result != 1 {
		panic("Part 1 example is failing")
	}

	moves = parseRopeMoves("2022/data/day09_sample2.txt")
	tailPositions = processMovesAndTrackTail(moves, 10)
	result = countNumUniquePositions(tailPositions)
	if result != 36 {
		panic("Part 1 example is failing")
	}

	moves = parseRopeMoves("2022/data/day09_input.txt")
	tailPositions = processMovesAndTrackTail(moves, 2)
	result = countNumUniquePositions(tailPositions)
	fmt.Println("Part 1:", result)

	tailPositions = processMovesAndTrackTail(moves, 10)
	result = countNumUniquePositions(tailPositions)
	fmt.Println("Part 2:", result)
}
