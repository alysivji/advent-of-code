package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"time"
)

type SensorData struct {
	loc           Point
	closestBeacon Point
	boundarySet   map[Point]void
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

func parseSensorDataAndReturnBoundaries(filePath string) []SensorData {
	input, _ := os.ReadFile(filePath)
	scanner := bufio.NewScanner(strings.NewReader(string(input)))

	var allSensors []SensorData
	for scanner.Scan() {
		var scannerX, scannerY, beaconX, beaconY int
		fmt.Sscanf(scanner.Text(), "Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d", &scannerX, &scannerY, &beaconX, &beaconY)

		loc := Point{x: scannerX, y: scannerY}
		closestBeacon := Point{x: beaconX, y: beaconY}

		boundarySet := make(map[Point]void)
		maxDistanceAllowed := loc.manhattanDistance(closestBeacon)
		for x := -1 * maxDistanceAllowed; x <= maxDistanceAllowed; x++ {
			yDelta := maxDistanceAllowed - IntAbs(x)

			p1 := loc.add(Point{x: x, y: -yDelta})
			boundarySet[p1] = member
			p2 := loc.add(Point{x: x, y: +yDelta})
			boundarySet[p2] = member
		}

		allSensors = append(allSensors, SensorData{loc, closestBeacon, boundarySet})
	}

	return allSensors
}

func countPositionsBeconsCannotAppearInBoundaryBox(sensors []SensorData, yToCheck int) int {
	beaconGrid := make(map[Point]void)
	for _, sensor := range sensors {
		var boundaryPoints []Point
		for boundaryPoint := range sensor.boundarySet {
			if boundaryPoint.y == yToCheck {
				boundaryPoints = append(boundaryPoints, boundaryPoint)
			}
		}

		if len(boundaryPoints) == 0 {
			continue
		}
		if len(boundaryPoints) == 1 {
			beaconGrid[boundaryPoints[0]] = member
			continue
		}

		directionVector := boundaryPoints[1].sub(boundaryPoints[0])
		vectorLength := boundaryPoints[1].manhattanDistance(boundaryPoints[0])
		normalizedDirectionVector := Point{x: directionVector.x / vectorLength, y: directionVector.y / vectorLength}
		for i := 0; i <= vectorLength; i++ {
			newPoint := boundaryPoints[0].add(normalizedDirectionVector.scalerMult(i))
			beaconGrid[newPoint] = member
		}
	}

	// delete beacons
	for _, sensor := range sensors {
		delete(beaconGrid, sensor.closestBeacon)
	}

	posCount := 0
	for range beaconGrid {
		posCount++
	}

	return posCount
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

	sensors = parseSensorDataAndReturnBoundaries("2022/data/day15_sample.txt")
	result = countPositionsBeconsCannotAppearInBoundaryBox(sensors, 10)
	if result != 26 {
		panic("Part 1 example is failing")
	}

	// real data
	// be smart about how we count
	start = time.Now()
	sensors = parseSensorData("2022/data/day15_input.txt")
	result = countPositionsBeconsCannotAppear(sensors, 2000000)
	fmt.Println("Part 1:", result, "| duration:", duration)

	// boundary box
	start = time.Now()
	sensors = parseSensorDataAndReturnBoundaries("2022/data/day15_input.txt")
	result = countPositionsBeconsCannotAppearInBoundaryBox(sensors, 2000000)
	duration = time.Since(start)
	fmt.Println("Part 1:", result, "| duration:", duration)
}
