package filewriter

import (
	"bytes"
	"log/slog"
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
		{Name: "John Doe", AgeGroup: domain.AgeGroupU15},
	}
	tournamentInfo := domain.Tournament{
		Title:    "Test Tournament",
		Agegroup: domain.AgeGroupU15,
	}

	outputPath := filepath.Join(tempDir, "output.xlsx")

	t.Run("should replace placeholders and generate dynamic columns for members", func(t *testing.T) {
		// Prepare template with placeholders
		fPlaceholder := excelize.NewFile()
		fPlaceholder.SetCellValue("Sheet1", "A1", "{{TournamentTitle}}")
		fPlaceholder.SetCellValue("Sheet1", "B2", "{{Members}}")
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

		// Member columns check
		// U15 should be at B2 (Header)
		valHeaderU15, _ := fOutput.GetCellValue("Sheet1", "B2")
		assert.Equal(t, domain.AgeGroupU15.String(), valHeaderU15)

		// U15 Members at B3, B4
		valU15_1, _ := fOutput.GetCellValue("Sheet1", "B3")
		valU15_2, _ := fOutput.GetCellValue("Sheet1", "B4")
		assert.Contains(t, []string{"Max Mustermann", "John Doe"}, valU15_1)
		assert.Contains(t, []string{"Max Mustermann", "John Doe"}, valU15_2)

		// U17 should be at C2 (Next column)
		valHeaderU17, _ := fOutput.GetCellValue("Sheet1", "C2")
		assert.Equal(t, domain.AgeGroupU17.String(), valHeaderU17)

		// U17 Member at C3
		valU17_1, _ := fOutput.GetCellValue("Sheet1", "C3")
		assert.Equal(t, "Erika Mustermann", valU17_1)
	})

	t.Run("should return error if template file does not exist", func(t *testing.T) {
		fwInvalid := ExcelFileWriter{
			templateFile: "non-existent.xlsx",
		}
		err := fwInvalid.WriteInformationToFile(outputPath, members, tournamentInfo)
		assert.Error(t, err)
	})
}

// Given an empty member list,
// When calling the function,
// Then it should not replace the placeholder for the members.
// And a log statement should be created.
func TestExcelFileWriter_WriteInformationToFile_NoMembers(t *testing.T) {
	// Setup: Create a temporary template file
	tempDir := t.TempDir()
	templatePath := filepath.Join(tempDir, "template.xlsx")
	f := excelize.NewFile()
	if err := f.SaveAs(templatePath); err != nil {
		t.Fatalf("failed to create template file: %v", err)
	}

	var buff bytes.Buffer
	h := slog.NewTextHandler(&buff, nil)
	testLogger := slog.New(h)
	fw := ExcelFileWriter{
		templateFile: templatePath,
		logger:       testLogger,
	}

	// Empty Members
	members := []domain.Member{}
	tournamentInfo := domain.Tournament{
		Title:    "Test Tournament",
		Agegroup: domain.AgeGroupU15,
	}

	outputPath := filepath.Join(tempDir, "output.xlsx")

	t.Run("Should not replace the members placeholder and emit a log statement.", func(t *testing.T) {
		// Prepare template with placeholders
		fPlaceholder := excelize.NewFile()
		fPlaceholder.SetCellValue("Sheet1", "A1", "{{TournamentTitle}}")
		fPlaceholder.SetCellValue("Sheet1", "B2", "{{Members}}")
		if err := fPlaceholder.SaveAs(templatePath); err != nil {
			t.Fatalf("failed to update template file: %v", err)
		}

		// Run the tested method
		err := fw.WriteInformationToFile(outputPath, members, tournamentInfo)
		assert.NoError(t, err)

		// Verify output file content
		fOutput, err := excelize.OpenFile(outputPath)
		assert.NoError(t, err)
		defer fOutput.Close()

		// Tournament check
		valTitle, _ := fOutput.GetCellValue("Sheet1", "A1")
		assert.Equal(t, tournamentInfo.Title, valTitle)

		// Check invariant placeholder
		ph, _ := fOutput.GetCellValue("Sheet1", "B2")
		// assert.Equal(t, "{{Members}}", ph)
		assert.Equal(t, "{{Members}}", ph)

		// Check Logger message with level WARN or higher
		assert.Contains(t, buff.String(), "level=WARN")
	})

}
