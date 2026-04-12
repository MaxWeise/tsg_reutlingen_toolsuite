package repository

import (
	"fmt"
	"io/fs"
	"log"
	"tsg_reutlingen_toolsuite/maxweise/meldau/internal/domain"

	"github.com/xuri/excelize/v2"
)

// MemberRepository provides an abstraction to read member data
type MemberRepository interface {
	GetAllMembers() ([]domain.Member, error)
}

// ExcelMemberRepository provides read access to a list of
type ExcelMemberRepository struct {
	filesystem fs.FS
	filename   string
}

// GetAllMembers gets the information about all members in an excel db-file.
func (r ExcelMemberRepository) GetAllMembers() ([]domain.Member, error) {
	file, err := r.filesystem.Open(r.filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	workbook, err := excelize.OpenReader(file)
	if err != nil {
		return nil, fmt.Errorf("Invalid or corrupted file: %s. %v", r.filename, err)
	}
	defer workbook.Close()

	sheetName := workbook.GetSheetName(0)
	rows, err := workbook.GetRows(sheetName)
	if err != nil {
		return nil, err
	}

	var members []domain.Member

	for i, row := range rows {
		if i == 0 || len(row) < 2 {
			continue
		}

		name := row[0]
		ageGroupStr := row[1]

		ageGroup, err := domain.AgeGroupFromString(ageGroupStr)
		if err != nil {
			log.Printf("Skipping invalid member %s: %v", name, err)
			continue
		}

		members = append(members, domain.Member{
			Name:     name,
			AgeGroup: ageGroup,
		})
	}

	return members, nil
}
