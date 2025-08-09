package algorithms

type Strategy interface {
	Seeding(numberOfPools int, poolSize int, pools *map[int][]string, nameList *[]string)
}

type RoundRobin struct{}

// Set the first fencer in round 1, the second in round 2, and so on. Loop around when necessary.
func (s RoundRobin) Seeding(numberOfPools int, poolSize int, pools *map[int][]string, nameList *[]string) {
	// Start at 1 becaues behaviour breaks with a 0-based index
	for index, name := range *nameList {
		key := index % numberOfPools
		list := (*pools)[key]
		list = append(list, name)
		(*pools)[key] = list
	}
}

type BlockwiseSeeding struct{}

// Seed the first poolSize members in round 1, the second poolSize members in Round 2 and so on
func (b BlockwiseSeeding) Seeding(numberOfPools int, poolSize int, pools *map[int][]string, nameList *[]string) {
	// Start at 1 becaues behaviour breaks with a 0-based index
	startIndex := 0
	for index := range *pools {
		(*pools)[index] = (*nameList)[startIndex : poolSize+startIndex]
		startIndex += poolSize
	}
}
