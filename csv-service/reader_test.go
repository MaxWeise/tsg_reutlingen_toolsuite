package main

import (
	"log"
	"os"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
	"github.com/stretchr/testify/require"
)

func TestReadCsvFile(t *testing.T) {
	p := "tournament.csv"
	f, err := os.Open(p)
	if err != nil {
		log.Fatalf("Error occured while opening the file %s: %s", p, err)
	}
	c := CsvReader{source: f}

	got, err := c.Read()
	require.Nil(t, err)

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

	require.NotNil(t, got)
	assert.Equal(t, want, got)
}
