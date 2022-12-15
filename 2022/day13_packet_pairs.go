package main

import (
	"fmt"
	"os"
	"strings"
)

type packetPair struct {
	left  string
	right string
}

func readPacketData(filePath string) []packetPair {
	input, _ := os.ReadFile(filePath)
	packetPairs := strings.Split(strings.TrimSpace(string(input)), "\n\n")

	var allPairs []packetPair
	for _, pair := range packetPairs {
		parts := strings.Split(pair, "\n")
		allPairs = append(allPairs, packetPair{left: parts[0], right: parts[1]})
	}
	return allPairs
}

func day13() {
	var packets []packetPair

	// sample data
	packets = readPacketData("2022/data/day13_sample.txt")
	fmt.Println(packets)
}
