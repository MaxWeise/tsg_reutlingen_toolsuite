package main

import (
	"log"
	"os"
	"testing"
	"time"
)

func TestWriteCsvFile(t *testing.T) {
	file, err := os.Create("tournaments.csv")
	if err != nil {
		log.Fatalf("Error occured while creating a file: %s", err)
	}
	c := CsvWriter{file}
	data := []Tournament{
		{
			FirstDay:  time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC),
			SecondDay: time.Date(2000, 1, 2, 0, 0, 0, 0, time.UTC),
			City:      "Reutlingen",
			Category:  "RL",
			AgeGroup:  "U11",
		},
		{
			FirstDay:  time.Date(2000, 1, 31, 0, 0, 0, 0, time.UTC),
			SecondDay: time.Date(2000, 2, 1, 0, 0, 0, 0, time.UTC),
			City:      "Heidenheim",
			Category:  "DM",
			AgeGroup:  "U13",
		},
		{
			FirstDay:  time.Date(2000, 3, 1, 0, 0, 0, 0, time.UTC),
			SecondDay: time.Date(2000, 3, 2, 0, 0, 0, 0, time.UTC),
			City:      "Leverkusen",
			Category:  "QB",
			AgeGroup:  "Senioren",
		},
	}

	c.Write(data)
}
