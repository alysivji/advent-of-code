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

func IntAbs(x int) int {
	if x > 0 {
		return x
	}
	return -1 * x
}
