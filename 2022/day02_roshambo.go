package main

// have to install ioutil
// go get io/ioutil

import (
	"fmt"
	"io/ioutil"
	"log"
	"strings"
)

type rhoShamBoGame struct {
	opponent string
	me       string
}

func readRoShamBoFilePart1(filePath string) []rhoShamBoGame {
	body, err := ioutil.ReadFile(filePath)

	if err != nil {
		log.Fatalf("unable to read file: %v", err)
	}

	allGames := make([]rhoShamBoGame, 0)

	gamesString := strings.Split(strings.Trim(string(body), "\n"), "\n")
	for _, gameString := range gamesString {
		gameDetails := strings.Fields(gameString)

		var opponent string
		switch gameDetails[0] {
		case "A":
			opponent = "rock"
		case "B":
			opponent = "paper"
		case "C":
			opponent = "scissors"
		}

		var me string
		switch gameDetails[1] {
		case "X":
			me = "rock"
		case "Y":
			me = "paper"
		case "Z":
			me = "scissors"
		}

		allGames = append(allGames, rhoShamBoGame{opponent: opponent, me: me})
	}

	return allGames
}

func readRoShamBoFilePart2(filePath string) []rhoShamBoGame {
	body, err := ioutil.ReadFile(filePath)

	if err != nil {
		log.Fatalf("unable to read file: %v", err)
	}

	allGames := make([]rhoShamBoGame, 0)

	var winMap = make(map[string]string)
	winMap["paper"] = "rock"
	winMap["rock"] = "scissors"
	winMap["scissors"] = "paper"

	loseMap := make(map[string]string)
	loseMap["rock"] = "paper"
	loseMap["scissors"] = "rock"
	loseMap["paper"] = "scissors"

	gamesString := strings.Split(strings.Trim(string(body), "\n"), "\n")
	for _, gameString := range gamesString {
		gameDetails := strings.Fields(gameString)

		var opponent string
		switch gameDetails[0] {
		case "A":
			opponent = "rock"
		case "B":
			opponent = "paper"
		case "C":
			opponent = "scissors"
		}

		var me string
		switch gameDetails[1] {
		case "X":
			me = winMap[opponent]
		case "Y":
			me = opponent
		case "Z":
			me = loseMap[opponent]
		}

		allGames = append(allGames, rhoShamBoGame{opponent: opponent, me: me})
	}

	return allGames
}

func scoreRoShamBoGames(games []rhoShamBoGame) int {
	var totalScore int
	for _, game := range games {
		// score shape i selected
		switch game.me {
		case "rock":
			totalScore += 1
		case "paper":
			totalScore += 2
		case "scissors":
			totalScore += 3
		}

		// score outcome
		if game.opponent == game.me {
			totalScore += 3
			continue
		}

		if ((game.me == "paper") && (game.opponent == "rock")) || ((game.me == "scissors") && (game.opponent == "paper")) || ((game.me == "rock") && (game.opponent == "scissors")) {
			totalScore += 6
		}
	}

	return totalScore
}

func day02() {
	// Part 1
	games := readRoShamBoFilePart1("2022/data/day02_sample.txt")
	result := scoreRoShamBoGames(games)

	if result != 15 {
		panic("Part 1 example is failing")
	}

	games = readRoShamBoFilePart1("2022/data/day02_input.txt")
	result = scoreRoShamBoGames(games)
	fmt.Println("Part 1:", result)

	// Part 2
	games = readRoShamBoFilePart2("2022/data/day02_sample.txt")
	result = scoreRoShamBoGames(games)

	if result != 12 {
		panic("Part 2 example is failing")
	}

	games = readRoShamBoFilePart2("2022/data/day02_input.txt")
	result = scoreRoShamBoGames(games)
	fmt.Println("Part 2:", result)
}
