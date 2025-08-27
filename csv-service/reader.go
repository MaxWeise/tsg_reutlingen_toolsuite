package main

type Reader interface {
	read() ([]Tournament, error)
}
