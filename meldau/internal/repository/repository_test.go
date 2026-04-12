package repository

import (
	"bytes"
	"io/fs"
	"testing"
	"testing/fstest"
	"tsg_reutlingen_toolsuite/maxweise/meldau/internal/domain"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"github.com/xuri/excelize/v2"
)

func TestExcelMemberRepository_GetAllMembers(t *testing.T) {
	// 1. Wir erstellen eine echte (temporäre) Excel-Datei im Speicher mit excelize
	f := excelize.NewFile()
	defer f.Close()

	sheetName := "Sheet1"
	f.SetCellValue(sheetName, "A1", "Name")
	f.SetCellValue(sheetName, "B1", "AgeGroup")
	f.SetCellValue(sheetName, "C1", "Email")

	f.SetCellValue(sheetName, "A2", "Max Mustermann")
	f.SetCellValue(sheetName, "B2", "U17")
	f.SetCellValue(sheetName, "C2", "max@example.com")

	f.SetCellValue(sheetName, "A3", "Erika Musterfrau")
	f.SetCellValue(sheetName, "B3", "Senioren")
	f.SetCellValue(sheetName, "C3", "erika@example.com")

	// Excel-Datei in einen Buffer schreiben
	var buf bytes.Buffer
	err := f.Write(&buf)
	assert.NoError(t, err)

	// 2. Wir nutzen fstest.MapFS, um die Excel-Datei im Speicher zu "mounten"
	mockFS := fstest.MapFS{
		"test_members.xlsx": &fstest.MapFile{
			Data: buf.Bytes(),
		},
	}

	repo := ExcelMemberRepository{
		filesystem: mockFS,
		filename:   "test_members.xlsx",
	}

	// 3. Ausführung
	members, err := repo.GetAllMembers()

	// 4. Prüfungen
	assert.NoError(t, err)
	assert.Len(t, members, 2)

	// Prüfen, ob die Daten korrekt gemappt wurden
	assert.Equal(t, "Max Mustermann", members[0].Name)
	assert.Equal(t, domain.AgeGroupU17, members[0].AgeGroup)

	assert.Equal(t, "Erika Musterfrau", members[1].Name)
	assert.Equal(t, domain.AgeGroupSeniors, members[1].AgeGroup)
}

func TestExcelMemberRepository_GetAllMembers_FileNotFound(t *testing.T) {
	mockFS := fstest.MapFS{}
	repo := ExcelMemberRepository{
		filesystem: mockFS,
		filename:   "file_does_not_exist.xlsx",
	}

	_, err := repo.GetAllMembers()
	require.Error(t, err)
	assert.ErrorIs(t, err, fs.ErrNotExist)
}

func TestExcelMemberRepository_GetAllMembers_NotAnExcelFile(t *testing.T) {
	var buf bytes.Buffer
	mockFS := fstest.MapFS{
		"test_members.csv": &fstest.MapFile{
			Data: buf.Bytes(),
		},
	}
	repo := ExcelMemberRepository{
		filesystem: mockFS,
		filename:   "test_members.csv",
	}

	_, err := repo.GetAllMembers()
	require.Error(t, err)
}
