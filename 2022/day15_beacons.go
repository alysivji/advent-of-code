package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type SensorData struct {
	loc           Point
	closestBeacon Point
}

func parseSensorData(filePath string) []SensorData {
	input, _ := os.ReadFile(filePath)
	scanner := bufio.NewScanner(strings.NewReader(string(input)))

	var allSensors []SensorData
	for scanner.Scan() {
		var scannerX, scannerY, beaconX, beaconY int
		fmt.Sscanf(scanner.Text(), "Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d", &scannerX, &scannerY, &beaconX, &beaconY)
		newSensor := SensorData{
			loc:           Point{x: scannerX, y: scannerY},
			closestBeacon: Point{x: beaconX, y: beaconY},
		}
		allSensors = append(allSensors, newSensor)
	}

	return allSensors
}

func countPositionsBeconsCannotAppear(sensors []SensorData, yToCheck int) int {
	beaconGrid := make(map[Point]string)

	// find where beacons cannot be
	for _, sensor := range sensors {
		sensorPos := sensor.loc
		maxDistanceAllowed := sensorPos.manhattanDistance(sensor.closestBeacon)
		// fmt.Println(sensorPos, sensor.closestBeacon, maxDistanceAllowed)

		xRange := maxDistanceAllowed - IntAbs(sensorPos.y-yToCheck)
		for x := -1 * xRange; x <= xRange; x++ {
			candidatePosition := sensorPos.add(Point{x: x, y: yToCheck - sensorPos.y})
			beaconGrid[candidatePosition] = "#"
			// fmt.Println(candidatePosition)
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

func day15() {
	var sensors []SensorData
	var result int

	// sample data
	sensors = parseSensorData("2022/data/day15_sample.txt")
	result = countPositionsBeconsCannotAppear(sensors, 10)
	if result != 26 {
		panic("Part 1 example is failing")
	}

	// real data
	sensors = parseSensorData("2022/data/day15_input.txt")
	result = countPositionsBeconsCannotAppear(sensors, 2000000)
	fmt.Println("Part 1:", result)
}
