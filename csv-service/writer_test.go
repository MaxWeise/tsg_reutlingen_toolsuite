package main

import (
	"log"
	"os"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

func TestWriteCsvFile(t *testing.T) {
	name := "tournaments.csv"
	file, err := os.Create(name)
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
	assert.FileExists(t, name, "The file that should be created does not exits.")

	err = os.Remove(name)
	if err != nil {
		if os.IsNotExist(err) {
			log.Printf("Could not remove file, it does not exist.")
		} else {
			log.Fatalf("There has been an error removing the file %s: %s", name, err)
		}
	}
}
