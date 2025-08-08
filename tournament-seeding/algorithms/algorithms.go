package algorithms

func RoundRobin(numberOfPools int, poolSize int, pools *map[int][]string, testList *[]string) {
	// Start at 1 becaues behaviour breaks with a 0-based index
	for index, name := range *testList {
		key := index % numberOfPools
		list := (*pools)[key]
		list = append(list, name)
		(*pools)[key] = list
	}
}
