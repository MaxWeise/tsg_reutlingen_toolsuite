package filewriter

import (
	"path/filepath"
	"testing"
	"tsg_reutlingen_toolsuite/maxweise/meldau/internal/domain"

	"github.com/stretchr/testify/assert"
	"github.com/xuri/excelize/v2"
)

func TestExcelFileWriter_WriteInformationToFile(t *testing.T) {
	// Setup: Create a temporary template file
	tempDir := t.TempDir()
	templatePath := filepath.Join(tempDir, "template.xlsx")
	f := excelize.NewFile()
	if err := f.SaveAs(templatePath); err != nil {
		t.Fatalf("failed to create template file: %v", err)
	}

	fw := ExcelFileWriter{
		templateFile: templatePath,
	}

	members := []domain.Member{
		{Name: "Max Mustermann", AgeGroup: domain.AgeGroupU15},
		{Name: "Erika Mustermann", AgeGroup: domain.AgeGroupU17},
	}
	tournamentInfo := domain.Tournament{
		Title:    "Test Tournament",
		Agegroup: domain.AgeGroupU15,
	}

	outputPath := filepath.Join(tempDir, "output.xlsx")

	t.Run("should replace placeholders and write member list", func(t *testing.T) {
		// Prepare template with placeholders
		fPlaceholder := excelize.NewFile()
		fPlaceholder.SetCellValue("Sheet1", "A1", "{{TournamentTitle}}")
		fPlaceholder.SetCellValue("Sheet1", "B1", "{{TournamentAgeGroup}}")
		fPlaceholder.SetCellValue("Sheet1", "A3", "{{MemberName}}")
		if err := fPlaceholder.SaveAs(templatePath); err != nil {
			t.Fatalf("failed to update template file: %v", err)
		}

		err := fw.WriteInformationToFile(outputPath, members, tournamentInfo)
		assert.NoError(t, err)

		// Verify output file content
		fOutput, err := excelize.OpenFile(outputPath)
		assert.NoError(t, err)
		defer fOutput.Close()

		// Tournament check
		valTitle, _ := fOutput.GetCellValue("Sheet1", "A1")
		assert.Equal(t, tournamentInfo.Title, valTitle)

		// Member list check
		// Member 1 should be at A3 (where the placeholder was)
		valMember1, _ := fOutput.GetCellValue("Sheet1", "A3")
		assert.Equal(t, members[0].Name, valMember1)

		// Member 2 should be at A4 (one row below)
		valMember2, _ := fOutput.GetCellValue("Sheet1", "A4")
		assert.Equal(t, members[1].Name, valMember2)
	})

	t.Run("should return error if template file does not exist", func(t *testing.T) {
		fwInvalid := ExcelFileWriter{
			templateFile: "non-existent.xlsx",
		}
		err := fwInvalid.WriteInformationToFile(outputPath, members, tournamentInfo)
		assert.Error(t, err)
	})
}
