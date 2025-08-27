package main

import (
	"errors"
	"fmt"
	"time"
)

const (
	DATE_FORMAT = "02.01.2006"
)

type Tournament struct {
	FirstDay  time.Time
	SecondDay time.Time
	City      string
	Category  string // TODO: Add validation in constructor
	AgeGroup  string // TODO: Add validation in constructor
}

// / Create a tournament object from a parameter list of strings and return the adress of the said object.
func NewTournament(firstDay string, secondDay string, city string, category string, ageGroup string) (*Tournament, error) {
	fd, err := time.Parse(DATE_FORMAT, firstDay)
	if err != nil {
		return nil, err
	}

	sd, err := time.Parse(DATE_FORMAT, secondDay)
	if err != nil {
		return nil, err
	}
	t := &Tournament{
		FirstDay:  fd,
		SecondDay: sd,
		City:      city,
		Category:  category,
		AgeGroup:  ageGroup,
	}

	return t, nil
}

// / Return the date saved in the object in the representation
// / dd./DD.mm.yyyy or dd.mm./DD.MM.yyyy
// / where D and M are the following day/month of d and m respectively.
func (t *Tournament) GetDate() (string, error) {
	if t == nil {
		return "", errors.New("Received nil-pointer")
	}

	// Get parts of the date object
	y, m1, d1 := t.FirstDay.Date()
	_, m2, d2 := t.SecondDay.Date()

	if t.FirstDay.Month() == t.SecondDay.Month() {
		return fmt.Sprintf("%02d./%02d.%02d.%d",
			d1,
			d2,
			m1,
			y,
		), nil
	} else {
		return fmt.Sprintf("%02d.%02d./%02d.%02d.%d",
			d1,
			m1,
			d2,
			m2,
			y,
		), nil

	}
}
