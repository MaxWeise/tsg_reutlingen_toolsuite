package filewriter

import (
	"tsg_reutlingen_toolsuite/maxweise/meldau/internal/domain"

	"github.com/xuri/excelize/v2"
)

type FileWriter interface {
	WriteInformationToFile(fileName string, members []domain.Member, tournamentInfo domain.Tournament) error
}

type ExcelFileWriter struct {
	templateFile string
}

// WriteInformationToFile write names of membes and the tournament data inside a template file.
func (fw ExcelFileWriter) WriteInformationToFile(fileName string, members []domain.Member, tournamentInfo domain.Tournament) error {
	file, err := excelize.OpenFile(fw.templateFile)
	if err != nil {
		return err
	}
	defer file.Close()

	// 1. Replace Tournament Placeholders
	placeholders := map[string]any{
		"{{TournamentTitle}}":    tournamentInfo.Title,
		"{{TournamentAgeGroup}}": tournamentInfo.Agegroup.String(),
		"{{Members}}":            members,
	}

	for _, sheet := range file.GetSheetList() {
		rows, err := file.GetRows(sheet)
		if err != nil {
			return err
		}

		for rowIndex, row := range rows {
			for colIndex, cellValue := range row {
				// 1. Replace Tournament Placeholders
				for placeholder, replacement := range placeholders {
					if cellValue == placeholder {
						cellName, _ := excelize.CoordinatesToCellName(colIndex+1, rowIndex+1)
						file.SetCellValue(sheet, cellName, replacement)
					}
				}

				// 2. Write Member List
				if cellValue == "{{MemberName}}" {
					for i, member := range members {
						// Write names in consecutive rows starting from the placeholder position
						cellName, _ := excelize.CoordinatesToCellName(colIndex+1, rowIndex+1+i)
						file.SetCellValue(sheet, cellName, member.Name)
					}
				}
			}
		}
	}

	// 2. Save the result to the new file
	return file.SaveAs(fileName)
}
