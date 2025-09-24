package main

import (
	"strings"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestReadCsvFile(t *testing.T) {
	const mockData = `Datum,Ort,Kategorie,Altersklasse
01./02.01.2000,Reutlingen,RL,U11
31.01./01.02.2000,Heidenheim,DM,U13
01./02.03.2000,Leverkusen,QB,Senioren
`
	mockReader := strings.NewReader(mockData)
	c := CsvReader{source: mockReader}

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
