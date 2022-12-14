package main

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
