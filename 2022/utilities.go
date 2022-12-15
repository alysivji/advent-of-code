package main

import (
	"strconv"
	"strings"
)

// need this to hack together sets with maps
type void struct{}

var member void

// used for x, y Point & Vector calculations
type Point struct {
	x int
	y int
}

func (p1 *Point) add(p2 Point) Point {
	return Point{x: p1.x + p2.x, y: p1.y + p2.y}
}

func (p1 *Point) sub(p2 Point) Point {
	return Point{x: p1.x - p2.x, y: p1.y - p2.y}
}

func (p1 *Point) scalerMult(val int) Point {
	return Point{x: val * p1.x, y: val * p1.y}
}

func PointFromString(pointStr string) *Point {
	parts := strings.Split(pointStr, ",")
	x, _ := strconv.Atoi(parts[0])
	y, _ := strconv.Atoi(parts[1])
	return &Point{x, y}
}

var dir_to_vector_map = map[string]Point{
	"R": {x: 0, y: +1},
	"L": {x: 0, y: -1},
	"U": {x: -1, y: 0},
	"D": {x: +1, y: 0},
}

var allDirectionVectors = []Point{
	{x: -1, y: -1},
	{x: 0, y: -1},
	{x: +1, y: -1},
	{x: -1, y: 0},
	{x: 0, y: 0},
	{x: +1, y: 0},
	{x: -1, y: +1},
	{x: 0, y: +1},
	{x: +1, y: +1},
}

var fourDirectionVectors = []Point{
	{x: 0, y: -1},
	{x: -1, y: 0},
	{x: +1, y: 0},
	{x: 0, y: +1},
}

func IntAbs(x int) int {
	if x > 0 {
		return x
	}
	return -1 * x
}
