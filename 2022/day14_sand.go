package main

import (
	"fmt"
	"os"
	"strings"
)

type xyMinMax struct {
	xMin int
	xMax int
	yMin int
	yMax int
}

type SandProblem struct {
	grid      map[Point]string
	bounds    xyMinMax
	sandStart Point
}

func parseRockData(filePath string, addFloor bool) *SandProblem {
	// +x is right; +y is down

	input, _ := os.ReadFile(filePath)
	rockPaths := strings.Split(strings.TrimSpace(string(input)), "\n")

	grid := make(map[Point]string)
	for _, rockPath := range rockPaths {
		rockPoints := strings.Split(rockPath, " -> ")

		prev := PointFromString(rockPoints[0])
		for i := 1; i < len(rockPoints); i++ {
			curr := PointFromString(rockPoints[i])

			lineVector := curr.sub(*prev)
			lineLength := IntAbs(lineVector.x) + IntAbs(lineVector.y)
			normalizedLineVector := Point{x: lineVector.x / lineLength, y: lineVector.y / lineLength}
			for j := 0; j <= lineLength; j++ {
				vectorMultipliedByLoopIndex := normalizedLineVector.scalerMult(j)
				newRockPoint := prev.add(vectorMultipliedByLoopIndex)
				grid[newRockPoint] = "#"
			}
			prev = curr
		}
	}

	// get rock boudnaries
	xMin := 500
	xMax := 500
	yMin := 0
	yMax := 0
	for point := range grid {
		if point.x < xMin {
			xMin = point.x
		} else if point.x > xMax {
			xMax = point.x
		}
		if point.y < yMin {
			yMin = point.y
		} else if point.y > yMax {
			yMax = point.y
		}
	}
	bounds := xyMinMax{xMin, xMax, yMin, yMax}

	if addFloor {
		yFloor := yMax + 2
		for x := xMin - 5000; x <= xMax+5000; x++ {
			grid[Point{x: x, y: yFloor}] = "#"
		}
	}

	sandStart := Point{x: 500, y: 0}
	grid[sandStart] = "+"

	return &SandProblem{grid, bounds, sandStart}
}

func simulateSand(problem *SandProblem, part string) int {

	var DIRECTIONS_TO_TRY []Point
	DIRECTIONS_TO_TRY = append(DIRECTIONS_TO_TRY, Point{x: 0, y: 1})
	DIRECTIONS_TO_TRY = append(DIRECTIONS_TO_TRY, Point{x: -1, y: 1})
	DIRECTIONS_TO_TRY = append(DIRECTIONS_TO_TRY, Point{x: +1, y: 1})

	numSandAtRest := 0
	for {
		// drop new piece of sand
		currSandPos := problem.sandStart

		// track sand movement
		for {
			var candidateSandPos Point
			sandMoved := false

			// find out if sand can move
			for _, dirVector := range DIRECTIONS_TO_TRY {
				candidateSandPos = currSandPos.add(dirVector)
				result, exists := problem.grid[candidateSandPos]
				if !exists {
					sandMoved = true
					break
				}
				if result == "#" || result == "o" {
					continue
				}
			}

			if sandMoved {
				currSandPos = candidateSandPos
				if part == "a" && currSandPos.y > problem.bounds.yMax {
					return numSandAtRest
				}
			} else {
				problem.grid[currSandPos] = "o"
				numSandAtRest++
				if part == "b" && currSandPos == problem.sandStart {
					return numSandAtRest
				}
				break
			}
		}
	}
}

func day14() {
	var problem *SandProblem
	var numSandAtRest int

	// sample data
	problem = parseRockData("2022/data/day14_sample.txt", false)
	numSandAtRest = simulateSand(problem, "a")
	if numSandAtRest != 24 {
		panic("Part 1 example is failing")
	}

	problem = parseRockData("2022/data/day14_sample.txt", true)
	numSandAtRest = simulateSand(problem, "b")
	if numSandAtRest != 93 {
		panic("Part 1 example is failing")
	}

	// real data
	problem = parseRockData("2022/data/day14_input.txt", false)
	numSandAtRest = simulateSand(problem, "a")
	fmt.Println("Part 1:", numSandAtRest)

	problem = parseRockData("2022/data/day14_input.txt", true)
	numSandAtRest = simulateSand(problem, "b")
	fmt.Println("Part 2:", numSandAtRest)
}
