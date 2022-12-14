package main

import (
	"fmt"
	"os"
	"strings"
)

type HillClimbingProblem struct {
	start     Point
	dest      Point
	heightMap map[Point]int
}

func parseHillData(filePath string) HillClimbingProblem {
	input, _ := os.ReadFile(filePath)
	rows := strings.Split(strings.TrimSpace(string(input)), "\n")

	var start, dest Point
	heightMap := make(map[Point]int)
	for y, row := range rows {
		for x, height := range row {
			if height == 'S' {
				height = 'a'
				start = Point{x, y}
			} else if height == 'E' {
				height = 'z'
				dest = Point{x, y}
			}
			heightMap[Point{x, y}] = int(height - 'a')
		}
	}

	return HillClimbingProblem{start, dest, heightMap}
}

type hillCheckData struct {
	point    Point
	numSteps int
}

func hillClimbBacktrack(problem HillClimbingProblem, part string) int {
	var checkQ []hillCheckData
	checkQ = append(checkQ, hillCheckData{point: problem.dest, numSteps: 0})
	visitedInMinSteps := make(map[Point]int)

	for len(checkQ) > 0 {
		currClimb := checkQ[len(checkQ)-1]
		checkQ = checkQ[:len(checkQ)-1]

		visitedInMinSteps[currClimb.point] = currClimb.numSteps

		for _, directionVector := range fourDirectionVectors {
			candidatePoint := currClimb.point.add(directionVector)
			candidateHeight, ok := problem.heightMap[candidatePoint]
			if !ok {
				continue
			}

			if problem.heightMap[currClimb.point]-candidateHeight <= 1 {
				minStepsToPoint, ok := visitedInMinSteps[candidatePoint]
				if ok {
					if currClimb.numSteps+1 >= minStepsToPoint {
						continue
					}
				}

				checkQ = append(checkQ, hillCheckData{point: candidatePoint, numSteps: currClimb.numSteps + 1})
			}
		}
	}

	if part == "a" {
		for point := range problem.heightMap {
			if point == problem.start {
				return visitedInMinSteps[point]
			}
		}
	} else if part == "b" {
		minSteps := 1000000
		for point, height := range problem.heightMap {
			if height != 0 {
				continue
			}
			if visitedInMinSteps[point] != 0 && visitedInMinSteps[point] < minSteps {
				minSteps = visitedInMinSteps[point]
			}
		}
		return minSteps
	}

	return -1
}

func day12() {
	var problem HillClimbingProblem
	var result int

	// sample data
	problem = parseHillData("2022/data/day12_sample.txt")
	result = hillClimbBacktrack(problem, "a")
	if result != 31 {
		panic("Part 1 example is failing")
	}

	result = hillClimbBacktrack(problem, "b")
	if result != 29 {
		panic("Part 2 example is failing")
	}

	// real data
	problem = parseHillData("2022/data/day12_input.txt")
	result = hillClimbBacktrack(problem, "a")
	fmt.Println("Part 1:", result)

	result = hillClimbBacktrack(problem, "b")
	fmt.Println("Part 2:", result)
}
