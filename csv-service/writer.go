package main

import (
	"encoding/csv"
	"os"
)

type Writer interface {
	write(data []*Tournament) error
}

type CsvWriter struct {
	destination *os.File
}

// treat as constant
var CSV_HEADERS = []string{"Datum", "Ort", "Kategorie", "Altersklasse"}

// / Write [data] to the file specified by CsvWriter
// / Will overwrite existing data in a file with the same name
func (c *CsvWriter) Write(data []*Tournament) error {
	w := csv.NewWriter(c.destination)
	defer w.Flush()

	// Write the header
	w.Write(CSV_HEADERS)

	// Write the data
	for _, t := range data {
		date, err := t.GetDate()

		if err != nil {
			return err
		}

		err = w.Write([]string{date, t.City, t.Category, t.AgeGroup})

		if err != nil {
			return err
		}
	}

	return nil
}
