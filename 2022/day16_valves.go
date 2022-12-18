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
	step         int
	prevScenario *ValveScenario
	agent        *ValveAgent
	valvesToOpen []string
	flowRate     int
	totalFlow    int
}

type ValveAgent struct {
	currValue     string
	openValveStep int
	flowRateToAdd int
}

func findMaxPressureRelease(valves ValveMap, maxSteps int, startValve string) int {
	distMatrix := createDistanceMatrix(valves)

	var valvesToOpen []string
	for _, valve := range valves {
		if !valve.open {
			valvesToOpen = append(valvesToOpen, valve.name)
		}
	}

	agent := ValveAgent{currValue: startValve, openValveStep: 0, flowRateToAdd: 0}
	initialScenario := ValveScenario{
		step:         0,
		agent:        &agent,
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
		// if counter%10 == 0 {
		// 	break
		// 	// fmt.Println("scenario #", counter)
		// }
		currScenario := scenariosToProcess[0]
		scenariosToProcess = scenariosToProcess[1:]

		// update current flow rate if a valve got oppened
		updatedFlowRate := currScenario.flowRate
		if currScenario.agent.openValveStep == currScenario.step {
			updatedFlowRate += currScenario.agent.flowRateToAdd
		}

		// calculate total flow since previous
		updatedTotalFlow := currScenario.totalFlow
		if currScenario.prevScenario != nil {
			timeElapsed := currScenario.step - currScenario.prevScenario.step
			updatedTotalFlow += currScenario.flowRate * timeElapsed
		}

		// fmt.Println("*******************")
		// fmt.Println(updatedTotalFlow)
		// fmt.Println("Current Scenario")
		// fmt.Println(currScenario)
		// fmt.Println("*******************")

		if currScenario.step == maxSteps {
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
			currValue := currScenario.agent.currValue
			distance := distMatrix[ValvePath{start: currValue, end: valveToOpen}]
			// is there enough time to valve and turn it on?
			timeStepValveWouldReleasePressure := currScenario.step + distance + 1
			movePossible := timeStepValveWouldReleasePressure <= maxSteps
			if movePossible {
				// mark valve as opened
				var updatedValvesToOpen []string
				for _, valve := range currScenario.valvesToOpen {
					if valve != valveToOpen {
						updatedValvesToOpen = append(updatedValvesToOpen, valve)
					}
				}

				// fmt.Println("next", valveToOpen)

				updatedAgent := &ValveAgent{
					currValue:     valveToOpen,
					flowRateToAdd: valves[valveToOpen].flowRate,
					openValveStep: timeStepValveWouldReleasePressure,
				}

				newScenario := ValveScenario{
					step:         timeStepValveWouldReleasePressure,
					prevScenario: &currScenario,
					agent:        updatedAgent,
					valvesToOpen: updatedValvesToOpen,
					flowRate:     updatedFlowRate,
					totalFlow:    updatedTotalFlow,
				}
				// fmt.Println(newScenario, updatedAgent)
				scenariosToProcess = append(scenariosToProcess, newScenario)
				canImprove = true
			}
		}
		// fmt.Println("-------")

		if !canImprove {
			updatedScenario := ValveScenario{
				step:         maxSteps,
				prevScenario: &currScenario,
				agent:        currScenario.agent,
				valvesToOpen: currScenario.valvesToOpen,
				flowRate:     updatedFlowRate,
				totalFlow:    updatedTotalFlow,
			}
			// fmt.Println(updatedScenario)
			// fmt.Println("-------")
			scenariosToProcess = append(scenariosToProcess, updatedScenario)
			continue
		}
	}

	// fmt.Println(counter)
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

	valves = parseValveData("2022/data/day16_input.txt")
	maxRelease = findMaxPressureRelease(valves, 30, "AA")
	fmt.Println("Part 1:", maxRelease)
}
