package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type TreeGrid struct {
	rows int
	cols int
	grid map[Point]int
}

func parseTreeHeightInput(filePath string) TreeGrid {
	input, _ := os.ReadFile(filePath)
	inputLines := strings.Split(strings.TrimSpace(string(input)), "\n")

	trees := make(map[Point]int)
	for y, line := range inputLines {
		for x, treeHeight := range line {
			height, _ := strconv.Atoi(string(treeHeight))
			trees[Point{x: x, y: y}] = height
		}
	}
	return TreeGrid{rows: len(inputLines), cols: len(inputLines), grid: trees}
}

func findNumVisibleTrees(treeGrid TreeGrid) int {
	numVisible := 0

	for currTree, height := range treeGrid.grid {

		// edges are always visible
		if currTree.x == 0 || currTree.y == 0 || currTree.x == treeGrid.rows-1 || currTree.y == treeGrid.cols-1 {
			numVisible++
			continue
		}

		// for interior points -- check to the edges
		visible := true
		// check left
		for i := currTree.y - 1; i >= 0; i-- {
			if height <= treeGrid.grid[Point{x: currTree.x, y: i}] {
				visible = false
			}
		}
		if visible {
			numVisible++
			continue
		}

		// check right
		visible = true
		for i := currTree.y + 1; i < treeGrid.cols; i++ {
			if height <= treeGrid.grid[Point{x: currTree.x, y: i}] {
				visible = false
			}
		}
		if visible {
			numVisible++
			continue
		}

		// check up
		visible = true
		for i := currTree.x - 1; i >= 0; i-- {
			if height <= treeGrid.grid[Point{x: i, y: currTree.y}] {
				visible = false
			}
		}
		if visible {
			numVisible++
			continue
		}

		// check down
		visible = true
		for i := currTree.x + 1; i < treeGrid.rows; i++ {
			if height <= treeGrid.grid[Point{x: i, y: currTree.y}] {
				visible = false
			}
		}
		if visible {
			numVisible++
			continue
		}
	}

	return numVisible
}

func findMaxScenicScore(treeGrid TreeGrid) int {
	maxScenicScore := 0

	for currTree, height := range treeGrid.grid {
		// skip all edge trees -- will be multiplying by 0
		if currTree.x == 0 || currTree.y == 0 || currTree.x == treeGrid.rows-1 || currTree.y == treeGrid.cols-1 {
			continue
		}

		// for interior points -- check to the edges
		// check left
		visibleLeft := 0
		for i := currTree.y - 1; i >= 0; i-- {
			visibleLeft++
			if height <= treeGrid.grid[Point{x: currTree.x, y: i}] {
				break
			}
		}

		// check right
		visibleRight := 0
		for i := currTree.y + 1; i < treeGrid.cols; i++ {
			visibleRight++
			if height <= treeGrid.grid[Point{x: currTree.x, y: i}] {
				break
			}
		}

		// check up
		visibleUp := 0
		for i := currTree.x - 1; i >= 0; i-- {
			visibleUp++
			if height <= treeGrid.grid[Point{x: i, y: currTree.y}] {
				break
			}
		}

		// check down
		visibleDown := 0
		for i := currTree.x + 1; i < treeGrid.rows; i++ {
			visibleDown++
			if height <= treeGrid.grid[Point{x: i, y: currTree.y}] {
				break
			}
		}

		scenicScore := visibleLeft * visibleRight * visibleUp * visibleDown

		if scenicScore > maxScenicScore {
			maxScenicScore = scenicScore
		}
	}

	return maxScenicScore
}

func day08() {
	// sample input
	grid := parseTreeHeightInput("2022/data/day08_sample.txt")
	result := findNumVisibleTrees(grid)
	if result != 21 {
		panic("Part 1 example is failing")
	}

	result = findMaxScenicScore(grid)
	if result != 8 {
		panic("Part 2 example is failing")
	}

	grid = parseTreeHeightInput("2022/data/day08_input.txt")
	result = findNumVisibleTrees(grid)
	fmt.Println("Part 1:", result)

	result = findMaxScenicScore(grid)
	fmt.Println("Part 2:", result)
}
