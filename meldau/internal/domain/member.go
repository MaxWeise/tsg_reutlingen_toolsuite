package domain

// Member represents a Fencer and their information inside the programm.
type Member struct {
	Name     string
	AgeGroup AgeGroup
}

// NewMember provides a way to initialize a new member object
//
// The age group is validated and returns an error, if the value is not allowed.
func (m Member) NewMember(name string, ag string) (Member, error) {
	a, err := AgeGroupFromString(ag)

	if err != nil {
		return Member{}, err
	}

	return Member{Name: name, AgeGroup: a}, nil
}
