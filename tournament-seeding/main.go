package main

import "fmt"

func main() {
	numberOfPools := 3
	poolSize := 5
	testList := []string{"Max", "Basti", "Olaf", "Kerim", "Luis", "Jan", "Cornelius", "Alex", "Jussi", "Achim"}

	pools := make(map[int][]string)

	// Create for each pool an empty slice with the reserved pool size.
	for index := range numberOfPools {
		pools[index] = make([]string, 0, poolSize)
	}

	// Start at 1 becaues behaviour breaks with a 0-based index
	for index, name := range testList {
		key := index % numberOfPools
		list := pools[key]
		list = append(list, name)
		pools[key] = list
	}

	for index, pool := range pools {
		fmt.Printf("Runde %d: %v\n", index, pool)
	}
}
