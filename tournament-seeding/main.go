package main

import (
	"fmt"
	"log"
	// "tsg-toolsuite/tournament-seeding/cmd"

	"github.com/xuri/excelize/v2"
)

func main() {

	file, err := excelize.OpenFile("test-rangliste.xlsx")
	if err != nil {
		log.Fatal("Error opening file:", err)
	}

	rows, err := file.GetRows("Tabelle1")
	if err != nil {
		log.Fatal("Error getting rows:", err)
	}

	for _, row := range rows {
		for _, col := range row {
			fmt.Print(col, "\t")
		}
		fmt.Println()
	}
	// cmd.Execute()
}
