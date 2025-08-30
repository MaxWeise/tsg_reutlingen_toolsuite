package main

import (
	"encoding/csv"
	"fmt"
	"os"
	"strings"
)

type Reader interface {
	Read() ([]Tournament, error)
}

type CsvReader struct {
	source *os.File
}

func (c *CsvReader) Read() ([]Tournament, error) {
	// Read csv file and get the raw data
	r := csv.NewReader(c.source)
	data, err := r.ReadAll()

	if err != nil {
		return []Tournament{}, err
	}

	// Remove the header
	data = data[1:]

	ret := []Tournament{}

	for _, d := range data {
		date, city, category, ageGroup := d[0], d[1], d[2], d[3]
		firstDay, secondDay, err := parseDate(date)

		if err != nil {
			return nil, err
		}

		// construct tournament objects
		t, err := NewTournament(firstDay, secondDay, city, category, ageGroup)
		ret = append(ret, *t)

	}

	// return the data or an error
	return ret, nil
}

// TODO: parse dd./DD.mm.yyyy to dd.mm.yyyy and DD.mm.yyyy
//
//	and parse dd.mm./DD.MM.yyyy to dd.mm.yyyy and DD.MM.yyyy formats
func parseDate(date string) (string, string, error) {
	if len(date) < 14 {
		return "", "", fmt.Errorf("wrong date-format recieved: %s.\nDate should follow either dd./dd.mm.yyyy or dd.mm./dd.mm.yyyy format", date)
	}

	partsUncleaned := strings.Split(date, ".")
	var parts []string
	for _, part := range partsUncleaned {
		parts = append(parts, strings.ReplaceAll(part, "/", ""))
	}

	if len(date) == 14 {
		// Handle Weekend in same month
		firstDay := parts[0]
		secondDay := parts[1]
		month := parts[2]
		year := parts[3]

		return fmt.Sprintf("%s.%s.%s", firstDay, month, year), fmt.Sprintf("%s.%s.%s", secondDay, month, year), nil
	}

	firstDay := parts[0]
	firstMonth := parts[1]
	secondDay := parts[2]
	secondMonth := parts[3]
	year := parts[4]

	return fmt.Sprintf("%s.%s.%s", firstDay, firstMonth, year), fmt.Sprintf("%s.%s.%s", secondDay, secondMonth, year), nil
}
