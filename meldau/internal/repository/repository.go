package repository

import (
	"io/fs"
	"tsg_reutlingen_toolsuite/maxweise/meldau/internal/domain"
)

// MemberRepository provides an abstraction to read member data
type MemberRepository interface {
	GetAllMembers() []domain.Member
}

// ExcelMemberRepository provides read access to a list of
type ExcelMemberRepository struct {
	Filepath fs.FS
}

// GetAllMembers provides access to all members present in the excel file.
func (r ExcelMemberRepository) GetAllMembers() []domain.Member {

}
