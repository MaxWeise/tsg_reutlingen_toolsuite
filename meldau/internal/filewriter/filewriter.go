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

// WriteInformationToFile write names of members and the tournament data inside a template file.
func (fw ExcelFileWriter) WriteInformationToFile(fileName string, members []domain.Member, tournamentInfo domain.Tournament) error {
	file, err := excelize.OpenFile(fw.templateFile)
	if err != nil {
		return err
	}
	defer file.Close()

	membersByGroup := make(map[domain.AgeGroup][]domain.Member)
	for _, m := range members {
		membersByGroup[m.AgeGroup] = append(membersByGroup[m.AgeGroup], m)
	}

	orderedGroups := []domain.AgeGroup{
		domain.AgeGroupU11,
		domain.AgeGroupU13,
		domain.AgeGroupU15,
		domain.AgeGroupU17,
		domain.AgeGroupU20,
		domain.AgeGroupSeniors,
		domain.AgeGroupVeterans,
	}

	type handler func(f *excelize.File, sheet string, col, row int)

	handlers := map[string]handler{
		"{{TournamentTitle}}": func(f *excelize.File, sheet string, col, row int) {
			cell, _ := excelize.CoordinatesToCellName(col, row)
			f.SetCellValue(sheet, cell, tournamentInfo.Title)
		},
		"{{TournamentAgeGroup}}": func(f *excelize.File, sheet string, col, row int) {
			cell, _ := excelize.CoordinatesToCellName(col, row)
			f.SetCellValue(sheet, cell, tournamentInfo.Agegroup.String())
		},
		"{{Members}}": func(f *excelize.File, sheet string, col, row int) {
			currentCol := col
			for _, group := range orderedGroups {
				mList, exists := membersByGroup[group]
				if !exists || len(mList) == 0 {
					continue
				}

				// Write AgeGroup Header
				headerCell, _ := excelize.CoordinatesToCellName(currentCol, row)
				f.SetCellValue(sheet, headerCell, group.String())

				// Write Members under the header
				for i, m := range mList {
					memberCell, _ := excelize.CoordinatesToCellName(currentCol, row+1+i)
					f.SetCellValue(sheet, memberCell, m.Name)
				}

				currentCol++
			}
		},
	}

	for _, sheet := range file.GetSheetList() {
		rows, err := file.GetRows(sheet)
		if err != nil {
			return err
		}

		for rowIndex, row := range rows {
			for colIndex, cellValue := range row {
				if h, ok := handlers[cellValue]; ok {
					h(file, sheet, colIndex+1, rowIndex+1)
				}
			}
		}
	}

	return file.SaveAs(fileName)
}
