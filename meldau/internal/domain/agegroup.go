package domain

import "fmt"

// AgeGroup defines a custom type for tournament age categories.
type AgeGroup string

// Constants for allowed AgeGroup values.
const (
	AgeGroupU11      AgeGroup = "U11"
	AgeGroupU13      AgeGroup = "U13"
	AgeGroupU15      AgeGroup = "U15"
	AgeGroupU17      AgeGroup = "U17"
	AgeGroupU20      AgeGroup = "U20"
	AgeGroupSeniors  AgeGroup = "Senioren"
	AgeGroupVeterans AgeGroup = "Veteranen"
)

// IsValid checks if the value matches one of the defined constants.
func (a AgeGroup) IsValid() bool {
	switch a {
	case AgeGroupU11, AgeGroupU13, AgeGroupU15, AgeGroupU17, AgeGroupU20, AgeGroupSeniors, AgeGroupVeterans:
		return true
	}
	return false
}

// String implements the fmt.Stringer interface.
func (a AgeGroup) String() string {
	return string(a)
}

// AgeGroupFromString validates and parses a string
func AgeGroupFromString(s string) (AgeGroup, error) {
	ag := AgeGroup(s)
	if !ag.IsValid() {
		return "", fmt.Errorf("The value of %s is not a valid member of AgeGroup", s)
	}

	return ag, nil
}
