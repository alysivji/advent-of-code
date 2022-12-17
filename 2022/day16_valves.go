package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

type ValveData struct {
	name       string
	flowRate   int
	neighbours []string
	open       bool
}

type ValveMap map[string]*ValveData
type ValveMatrix map[string][]*ValveData

func (m ValveMatrix) String() {
	for valveName, neighbours := range m {
		fmt.Println("Valve", valveName)
		for _, neighbour := range neighbours {
			fmt.Println(*neighbour)
		}
	}
}

func parseValveData(filePath string) ValveMap {
	input, _ := os.ReadFile(filePath)
	scanner := bufio.NewScanner(strings.NewReader(string(input)))

	regEx := `Valve (?P<valve>\w+) has flow rate=(?P<flowRate>\d+); tunnel(s)* lead(s)* to valve(s)* (?P<neighbhours>([A-Z]+(,\s)*)+)`

	valveMap := make(map[string]*ValveData)
	for scanner.Scan() {
		extractedField := processRegularExpression(regEx, scanner.Text())

		var neighbours []string
		for _, neighbour := range strings.Split(extractedField["neighbhours"], ", ") {
			neighbours = append(neighbours, neighbour)
		}

		open := false
		flowRate, _ := strconv.Atoi(extractedField["flowRate"])
		if flowRate == 0 {
			open = true
		}

		valve := &ValveData{
			name:       extractedField["valve"],
			flowRate:   flowRate,
			neighbours: neighbours,
			open:       open,
		}
		valveMap[valve.name] = valve
	}

	return valveMap
}

func createAdjacencyMatrix(valveMap ValveMap) ValveMatrix {
	adjMatrix := make(ValveMatrix)

	for valveName, valveInfo := range valveMap {
		for _, neighbour := range valveInfo.neighbours {
			adjMatrix[valveName] = append(adjMatrix[valveName], valveMap[neighbour])
		}
	}

	return adjMatrix
}

type ValvePath struct {
	start string
	end   string
}

type ValveDistance map[ValvePath]int

func createDistanceMatrix(valves ValveMap) ValveDistance {
	adjMatrix := createAdjacencyMatrix(valves)

	var allValves []string
	for valveName := range adjMatrix {
		allValves = append(allValves, valveName)
	}

	distanceMatrix := make(ValveDistance)
	for i := 0; i < len(allValves); i++ {
		distances := getMinDistanceFromSingleTunnel(valves, adjMatrix, allValves[i])
		for end, distance := range distances {
			distanceMatrix[ValvePath{start: allValves[i], end: end}] = distance
		}
	}

	return distanceMatrix
}

type ValveCheckData struct {
	name string
	dist int
}

func getMinDistanceFromSingleTunnel(valves ValveMap, adjMatrix ValveMatrix, start string) map[string]int {
	var checkQ []ValveCheckData
	checkQ = append(checkQ, ValveCheckData{name: start, dist: 0})

	minDistance := make(map[string]int)
	for valve := range valves {
		minDistance[valve] = math.MaxInt
	}
	for len(checkQ) > 0 {
		currValve := checkQ[0]
		checkQ = checkQ[1:]

		// is distance to current valve less than what we have?
		if currValve.dist < minDistance[currValve.name] {
			minDistance[currValve.name] = currValve.dist
		}

		for _, neighbour := range adjMatrix[currValve.name] {
			if currValve.dist+1 < minDistance[neighbour.name] {
				nextValveToCheck := ValveCheckData{name: neighbour.name, dist: currValve.dist + 1}
				checkQ = append(checkQ, nextValveToCheck)
			}
		}
	}

	return minDistance
}

type ValveScenario struct {
	time         int
	currValve    string
	valvesToOpen []string
	flowRate     int
	totalFlow    int
}

func findMaxPressureRelease(valves ValveMap, maxSteps int, startValve string) int {
	distMatrix := createDistanceMatrix(valves)

	var valvesToOpen []string
	for _, valve := range valves {
		if !valve.open {
			valvesToOpen = append(valvesToOpen, valve.name)
		}
	}

	initialScenario := ValveScenario{
		time:         0,
		currValve:    startValve,
		valvesToOpen: valvesToOpen,
		flowRate:     0,
		totalFlow:    0,
	}

	var scenariosToProcess []ValveScenario
	scenariosToProcess = append(scenariosToProcess, initialScenario)
	maxFlow := 0
	// maxCounter := 10
	counter := 0
	// len(scenariosToProcess) > 0 ||
	// counter <= maxCounter
	for len(scenariosToProcess) > 0 {
		counter++
		if counter%1000000 == 0 {
			fmt.Println("scenario #", counter)
		}
		// fmt.Println("*******************")
		// fmt.Println("Current Scenario")
		currScenario := scenariosToProcess[0]
		// fmt.Println(currScenario)
		// fmt.Println("*******************")

		scenariosToProcess = scenariosToProcess[1:]

		// update flow rate and exit if we are at the limit
		updatedTotalFlow := currScenario.totalFlow + currScenario.flowRate
		if currScenario.time+1 == maxSteps {
			// fmt.Println(currScenario)
			if updatedTotalFlow > maxFlow {
				maxFlow = updatedTotalFlow
			}
			continue
		}

		canImprove := false
		for _, valveToOpen := range currScenario.valvesToOpen {
			// how far is valve?
			// fmt.Println("valve to open", valveToOpen)
			// do we have enough time to get there and turn it on?
			// if so, add it
			distance := distMatrix[ValvePath{start: currScenario.currValve, end: valveToOpen}]
			// is there enough time to valve and turn it on?
			timeStepValveWouldReleasePressure := currScenario.time + distance + 1
			movePossible := timeStepValveWouldReleasePressure <= maxSteps
			if movePossible {
				// mark valve as opened
				var updatedValvesToOpen []string
				for _, valve := range currScenario.valvesToOpen {
					if valve != valveToOpen {
						updatedValvesToOpen = append(updatedValvesToOpen, valve)
					}
				}

				updatedFlowRate := currScenario.flowRate + valves[valveToOpen].flowRate
				// update flow rate for fast travel
				fastTravelTotalFlow := updatedTotalFlow + (timeStepValveWouldReleasePressure-currScenario.time-1)*currScenario.flowRate
				newScenario := ValveScenario{
					time:         timeStepValveWouldReleasePressure,
					currValve:    valveToOpen,
					valvesToOpen: updatedValvesToOpen,
					flowRate:     updatedFlowRate,
					totalFlow:    fastTravelTotalFlow,
				}
				// fmt.Println(newScenario)
				// fmt.Println("-------")
				scenariosToProcess = append(scenariosToProcess, newScenario)
				canImprove = true
			}
		}

		if !canImprove {
			nextStep := currScenario.time + 1
			updatedScenario := ValveScenario{
				time:         nextStep,
				currValve:    currScenario.currValve,
				valvesToOpen: currScenario.valvesToOpen,
				flowRate:     currScenario.flowRate,
				totalFlow:    updatedTotalFlow,
			}
			// fmt.Println(updatedScenario)
			// fmt.Println("-------")
			scenariosToProcess = append(scenariosToProcess, updatedScenario)
			continue
		}
	}

	return maxFlow
}

func day16() {
	var valves ValveMap
	var maxRelease int

	valves = parseValveData("2022/data/day16_sample.txt")
	maxRelease = findMaxPressureRelease(valves, 30, "AA")
	if maxRelease != 1651 {
		panic("Part 1 example is failing")
	}

	// valves = parseValveData("2022/data/day16_input.txt")
	// maxRelease = findMaxPressureRelease(valves, 30, "AA")
	// fmt.Println("Part 1:", maxRelease)
}
