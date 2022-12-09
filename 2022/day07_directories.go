package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type FileSystemNode struct {
	name     string
	size     int
	level    int // used to indent output
	children []*FileSystemNode
	parent   *FileSystemNode
}

func (node *FileSystemNode) String() string {
	// print directory list for debugging purposes
	var sb strings.Builder
	for i := 0; i < node.level; i++ {
		sb.WriteString("  ")
	}
	if node.size == 0 {
		sb.WriteString(fmt.Sprintf("- %s (dir)", node.name))
	} else {
		sb.WriteString(fmt.Sprintf("- %s (file, size=%d)", node.name, node.size))
	}

	for _, child := range node.children {
		sb.WriteString("\n")
		sb.WriteString(child.String())
	}
	return sb.String()
}

func parseCommandsIntoDirectoryTree(filePath string) *FileSystemNode {
	input, _ := os.ReadFile(filePath)
	inputLines := strings.Split(strings.TrimSpace(string(input)), "\n")

	rootDir := &FileSystemNode{name: "/", level: 0}
	currentDir := rootDir

	for _, line := range inputLines {
		fields := strings.Fields(line)

		if fields[1] == "cd" {
			if fields[2] == ".." {
				currentDir = currentDir.parent
			} else {
				for _, child := range currentDir.children {
					if child.name == fields[2] {
						currentDir = child
						break
					}
				}
			}
		} else if fields[1] == "ls" {
			// we dont need to do anything with ls
			continue
		} else {
			// handle directory contents
			size, _ := strconv.Atoi(fields[0])
			newEntry := &FileSystemNode{name: fields[1], size: size, parent: currentDir, level: currentDir.level + 1}
			currentDir.children = append(currentDir.children, newEntry)
		}
	}

	return rootDir
}

func updateWithDirectorySizes(node *FileSystemNode) {
	// update directory nodes with sizes
	var totalSize int
	for _, child := range node.children {
		if len(child.children) > 0 {
			updateWithDirectorySizes(child)
			totalSize += child.size
		} else {
			totalSize += child.size
		}
	}
	node.size = totalSize
}

type Directory struct {
	name string
	size int
}

func pullDirectoryInfo(node *FileSystemNode) []Directory {
	var allDirectories []Directory

	if len(node.children) > 0 {
		allDirectories = append(allDirectories, Directory{name: node.name, size: node.size})
	}

	// go through sub-directories
	for _, child := range node.children {
		if len(child.children) > 0 {
			allDirectories = append(allDirectories, Directory{name: child.name, size: child.size})

			for _, subChild := range child.children {
				allDirectories = append(allDirectories, pullDirectoryInfo(subChild)...)
			}
		}

	}
	return allDirectories
}

func findDirsLessThanThreshold(directories []Directory, threshold int) int {
	totalSize := 0
	for _, dir := range directories {
		if dir.size <= threshold {
			totalSize += dir.size
		}
	}
	return totalSize
}

const TOTAL_DISK_SPACE = 70000000
const UNUSED_SPACE_NEEDED = 30000000

func deletionOptions(directories []Directory) Directory {
	var diskspaceUsed int
	for _, dir := range directories {
		if dir.name == "/" {
			diskspaceUsed = dir.size
		}
	}

	usedSpace := TOTAL_DISK_SPACE - diskspaceUsed
	needToFreeUp := UNUSED_SPACE_NEEDED - usedSpace
	var deletionOptions []Directory
	for _, dir := range directories {
		if dir.size > needToFreeUp {
			deletionOptions = append(deletionOptions, dir)
		}
	}

	min := deletionOptions[0]
	for _, dir := range deletionOptions {
		if dir.size < min.size {
			min = dir
		}
	}

	return min
}

func day07() {
	// sample input
	root := parseCommandsIntoDirectoryTree("2022/data/day07_sample.txt")
	updateWithDirectorySizes(root)
	directories := pullDirectoryInfo(root)
	result := findDirsLessThanThreshold(directories, 100000)
	if result != 95437 {
		panic("Part 1 example is failing")
	}

	toDelete := deletionOptions(directories)
	if toDelete.name != "d" && toDelete.size != 24933642 {
		panic("Part 2 example is failing")
	}

	// real input
	root = parseCommandsIntoDirectoryTree("2022/data/day07_input.txt")
	updateWithDirectorySizes(root)
	directories = pullDirectoryInfo(root)
	result = findDirsLessThanThreshold(directories, 100000)
	fmt.Println("Part 1:", result)

	toDelete = deletionOptions(directories)
	fmt.Println("Part 2:", toDelete)
}
