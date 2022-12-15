package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"time"
)

type SensorData struct {
	loc               Point
	closestBeacon     Point
	manhattanDistance int
}

func parseSensorData(filePath string) []SensorData {
	input, _ := os.ReadFile(filePath)
	scanner := bufio.NewScanner(strings.NewReader(string(input)))

	var allSensors []SensorData
	for scanner.Scan() {
		var scannerX, scannerY, beaconX, beaconY int
		fmt.Sscanf(scanner.Text(), "Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d", &scannerX, &scannerY, &beaconX, &beaconY)
		loc := Point{x: scannerX, y: scannerY}
		closestBeacon := Point{x: beaconX, y: beaconY}
		manhattanDistance := loc.manhattanDistance(closestBeacon)
		sensor := SensorData{loc, closestBeacon, manhattanDistance}
		allSensors = append(allSensors, sensor)
	}

	return allSensors
}

func countPositionsBeconsCannotAppear(sensors []SensorData, yToCheck int) int {
	beaconGrid := make(map[Point]string)

	// find where beacons cannot be
	for _, sensor := range sensors {
		sensorPos := sensor.loc

		xRange := sensor.manhattanDistance - IntAbs(sensorPos.y-yToCheck)
		for x := -1 * xRange; x <= xRange; x++ {
			candidatePosition := sensorPos.add(Point{x: x, y: yToCheck - sensorPos.y})
			beaconGrid[candidatePosition] = "#"
		}
	}

	// place beacons
	for _, sensor := range sensors {
		beaconGrid[sensor.closestBeacon] = "B"
	}

	posCount := 0
	for point, value := range beaconGrid {
		if point.y == yToCheck && value == "#" {
			posCount += 1
		}
	}

	return posCount
}

func findBeaconTuningFrequency(sensors []SensorData, xMin int, xMax int, yMin int, yMax int) int {
	// get the the complete boundary points for manhattan distance + 1
	boundaryPlus1Set := make(map[Point]void)
	for _, sensor := range sensors {

		maxDistanceAllowed := sensor.manhattanDistance + 1
		for x := -1 * maxDistanceAllowed; x <= maxDistanceAllowed; x++ {
			yDelta := maxDistanceAllowed - IntAbs(x)

			// filter out locations outside of box
			p1 := sensor.loc.add(Point{x: x, y: -yDelta})
			if p1.x >= xMin && p1.x <= xMax && p1.y >= yMin && p1.y <= yMax {
				boundaryPlus1Set[p1] = member
			}
			p2 := sensor.loc.add(Point{x: x, y: +yDelta})
			if p2.x >= xMin && p2.x <= xMax && p2.y >= yMin && p2.y <= yMax {
				boundaryPlus1Set[p2] = member
			}
		}
	}

	// loop through all sensors and ensure point is further than manhattan distance
	for _, sensor := range sensors {

		for boundaryPlus1Point := range boundaryPlus1Set {
			if sensor.loc.manhattanDistance(boundaryPlus1Point) <= sensor.manhattanDistance {
				delete(boundaryPlus1Set, boundaryPlus1Point)
			}
		}
	}

	// we should only have one point left
	for point := range boundaryPlus1Set {
		return point.x*4000000 + point.y
	}

	return -1
}

func day15() {
	var sensors []SensorData
	var result int
	var start time.Time
	var duration time.Duration

	// sample data
	sensors = parseSensorData("2022/data/day15_sample.txt")
	result = countPositionsBeconsCannotAppear(sensors, 10)
	if result != 26 {
		panic("Part 1 example is failing")
	}

	sensors = parseSensorData("2022/data/day15_sample.txt")
	result = findBeaconTuningFrequency(sensors, 0, 20, 0, 20)
	if result != 56000011 {
		panic("Part 2 example is failing")
	}

	// real data
	start = time.Now()
	sensors = parseSensorData("2022/data/day15_input.txt")
	result = countPositionsBeconsCannotAppear(sensors, 2000000)
	duration = time.Since(start)
	fmt.Println("Part 1:", result, "| duration:", duration)

	start = time.Now()
	sensors = parseSensorData("2022/data/day15_input.txt")
	result = findBeaconTuningFrequency(sensors, 0, 4000000, 0, 4000000)
	duration = time.Since(start)
	fmt.Println("Part 2:", result, "| duration:", duration)
}
