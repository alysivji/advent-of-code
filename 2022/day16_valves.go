package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"

	"golang.org/x/exp/slices"
	"gonum.org/v1/gonum/stat/combin"
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
	step          int
	prevScenario  *ValveScenario
	agents        []ValveAgent
	valvesToOpen  []string
	startFlowRate int
	// endFlowRate   int
	totalFlow int
}

type ValveAgent struct {
	currValue         string
	nextStepAvailable int
	flowRateToAdd     int
}

func findMaxPressureRelease(valves ValveMap, maxSteps int, startValve string, numAgents int) int {
	distMatrix := createDistanceMatrix(valves)

	var valvesToOpen []string
	for _, valve := range valves {
		if !valve.open {
			valvesToOpen = append(valvesToOpen, valve.name)
		}
	}

	var agents []ValveAgent
	for i := 0; i < numAgents; i++ {
		agent := ValveAgent{currValue: startValve, nextStepAvailable: 0, flowRateToAdd: 0}
		agents = append(agents, agent)
	}

	initialScenario := ValveScenario{
		step:          0,
		agents:        agents,
		valvesToOpen:  valvesToOpen,
		startFlowRate: 0,
		// endFlowRate:   0,
		totalFlow: 0,
	}

	var scenariosToProcess []ValveScenario
	scenariosToProcess = append(scenariosToProcess, initialScenario)
	maxFlow := 0
	counter := 0
	var bestScenarioEnd *ValveScenario
	for len(scenariosToProcess) > 0 {
		counter++
		// if counter%10 == 0 {
		// break
		// fmt.Println("scenario #", counter)
		// }
		currScenario := scenariosToProcess[0]
		scenariosToProcess = scenariosToProcess[1:]

		// update current flow rate if a valve got opened
		// figure out which agents are free
		updatedFlowRate := currScenario.startFlowRate
		var availableAgents []*ValveAgent
		var availableAgentPositions []int
		for idx, agent := range currScenario.agents {
			if agent.nextStepAvailable == currScenario.step {
				updatedFlowRate += agent.flowRateToAdd
				agent.flowRateToAdd = 0
				agent.nextStepAvailable = 0
				// fmt.Println("rate", updatedFlowRate)
				availableAgents = append(availableAgents, &agent)
				availableAgentPositions = append(availableAgentPositions, idx)
			}
		}

		// fmt.Println("*******************")
		// fmt.Println(updatedTotalFlow)
		// fmt.Println("Current Scenario")
		// fmt.Println(currScenario)
		// fmt.Println("*******************")

		if currScenario.step == maxSteps {
			if currScenario.totalFlow > maxFlow {
				maxFlow = currScenario.totalFlow
				bestScenarioEnd = &currScenario
			}
			continue
		}

		possibleValves := currScenario.valvesToOpen
		if len(availableAgents) > 1 {
			possibleValves = append(possibleValves, "")
		}

		var valveCombinations [][]int
		n := len(possibleValves)
		k := len(availableAgents)
		if n == 0 {
		} else if n >= k {
			valveCombinations = combin.Permutations(len(possibleValves), len(availableAgents))
		} else {
			arr := make([]int, 1)
			arr[0] = 0
			valveCombinations = append(valveCombinations, arr)
		}

		canImprove := false
		for _, valvePositions := range valveCombinations {
			var updatedAgents []ValveAgent
			var valvesBeingOpened []string
			movePossible := true
			for idx, valvePosition := range valvePositions {
				agentToProcess := availableAgents[idx]
				valveToOpen := possibleValves[valvePosition]
				// fmt.Println("valve to open", valveToOpen)

				var updatedAgent ValveAgent
				if valveToOpen == "" {
					updatedAgent = ValveAgent{
						currValue:         agentToProcess.currValue,
						flowRateToAdd:     0,
						nextStepAvailable: maxSteps,
					}
				} else {
					// how far is valve?
					// do we have enough time to get there and turn it on?
					currValue := agentToProcess.currValue
					distance := distMatrix[ValvePath{start: currValue, end: valveToOpen}]
					// is there enough time to valve and turn it on?
					timeStepValveWouldReleasePressure := currScenario.step + distance + 1
					movePossible = movePossible && timeStepValveWouldReleasePressure <= maxSteps

					updatedAgent = ValveAgent{
						currValue:         valveToOpen,
						flowRateToAdd:     valves[valveToOpen].flowRate,
						nextStepAvailable: timeStepValveWouldReleasePressure,
					}

					valvesBeingOpened = append(valvesBeingOpened, valveToOpen)
				}
				updatedAgents = append(updatedAgents, updatedAgent)
			}

			if movePossible {
				// add missing agent
				for idx, agent := range currScenario.agents {
					if !slices.Contains(availableAgentPositions, idx) {
						updatedAgents = append(updatedAgents, agent)
					}
				}

				var updatedValvesToOpen []string
				for _, valve := range currScenario.valvesToOpen {
					if !slices.Contains(valvesBeingOpened, valve) {
						updatedValvesToOpen = append(updatedValvesToOpen, valve)
					}
				}

				nextStep := math.MaxInt
				for _, agent := range updatedAgents {
					if agent.nextStepAvailable < nextStep {
						nextStep = agent.nextStepAvailable
					}
				}

				// endFlowRate := updatedFlowRate
				// for _, agent := range updatedAgents {
				// 	if agent.nextStepAvailable == nextStep {
				// 		endFlowRate += agent.flowRateToAdd
				// 	}
				// }

				// calculate total flow since previous
				updatedTotalFlow := currScenario.totalFlow
				timeElapsed := nextStep - currScenario.step
				updatedTotalFlow += updatedFlowRate * timeElapsed
				newScenario := ValveScenario{
					step:          nextStep,
					prevScenario:  &currScenario,
					agents:        updatedAgents,
					valvesToOpen:  updatedValvesToOpen,
					startFlowRate: updatedFlowRate,
					// endFlowRate:   endFlowRate,
					totalFlow: updatedTotalFlow,
				}
				// fmt.Println(newScenario, updatedAgents)
				scenariosToProcess = append(scenariosToProcess, newScenario)
				canImprove = true
			}
		}
		// fmt.Println("-------")

		if !canImprove {
			// fmt.Println("reached")
			updatedTotalFlow := currScenario.totalFlow
			timeElapsed := maxSteps - currScenario.step
			updatedTotalFlow += updatedFlowRate * timeElapsed

			updatedScenario := ValveScenario{
				step:          maxSteps,
				prevScenario:  &currScenario,
				agents:        currScenario.agents,
				valvesToOpen:  currScenario.valvesToOpen,
				startFlowRate: updatedFlowRate,
				// endFlowRate:   endFlowRate,
				totalFlow: updatedTotalFlow,
			}
			// fmt.Println(updatedScenario)
			// fmt.Println("-------")
			scenariosToProcess = append(scenariosToProcess, updatedScenario)
			continue
		}
	}

	// fmt.Println(counter)
	currScenario := bestScenarioEnd
	for currScenario.prevScenario != nil {
		fmt.Println(currScenario)
		currScenario = currScenario.prevScenario
	}
	fmt.Println(currScenario)
	return maxFlow
}

func day16() {
	var valves ValveMap
	var maxRelease int

	// sample data
	// valves = parseValveData("2022/data/day16_sample.txt")
	// maxRelease = findMaxPressureRelease(valves, 30, "AA", 1)
	// if maxRelease != 1651 {
	// 	panic("Part 1 example is failing")
	// }

	valves = parseValveData("2022/data/day16_sample.txt")
	maxRelease = findMaxPressureRelease(valves, 26, "AA", 2)
	fmt.Println(maxRelease)

	// real data
	// valves = parseValveData("2022/data/day16_input.txt")
	// maxRelease = findMaxPressureRelease(valves, 30, "AA", 1)
	// fmt.Println("Part 1:", maxRelease)

	valves = parseValveData("2022/data/day16_input.txt")
	maxRelease = findMaxPressureRelease(valves, 30, "AA", 2)
	fmt.Println(maxRelease)
}
