package main

import (
	"log"
	"os"
	"testing"
	"time"
)

func TestReadCsvFile(t *testing.T) {
	p := "tournament.csv"
	f, err := os.Open(p)
	if err != nil {
		log.Fatalf("Error occured while opening the file %s: %s", p, err)
	}
	c := CsvReader{source: f}

	got, err := c.Read()
	if err != nil {
		log.Fatalf("Error occured while reading the file %s: %s", p, err)
	}

	want := []Tournament{
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

	if got == nil {
		t.Error("Return value is nil.")
	}

	for i, g := range got {
		w := want[i]
		if g != w {
			t.Errorf("Difference at index %d\nExcpected: %s\nGot: %s", i, w, g)
		}
	}

}
