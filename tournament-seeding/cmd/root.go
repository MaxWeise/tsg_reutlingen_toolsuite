package cmd

import (
	"errors"
	"fmt"
	"os"
	"strconv"

	"tsg-toolsuite/tournament-seeding/algorithms"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "seeding",
	Short: "Create pools from a list of names.",
	Long:  "Create any number of pools with custom size from a list of names in an excel file.",
	Run: func(cmd *cobra.Command, args []string) {
	},
}

var seedingRoundRobin = &cobra.Command{
	Use:   "round-robin",
	Short: "Seeding like round robin",
	Long:  "Create pools acording to the specified arguments. Supply in this order: number of pools, pool size.",
	Args:  cobra.ExactArgs(2),
	Run: func(cmd *cobra.Command, args []string) {
		// TODO: Read list from excel file
		testList := []string{"Max", "Basti", "Olaf", "Kerim", "Luis", "Jan", "Cornelius", "Alex", "Jussi", "Achim"}

		numberOfPools, poolSize, err := validateSeedingArgs(args[0], args[1], len(testList))
		if err != nil {
			fmt.Println("Error:", err)
			return
		}

		pools := make(map[int][]string)

		// Create for each pool an empty slice with the reserved pool size.
		for index := range numberOfPools {
			pools[index] = make([]string, 0, poolSize)
		}

		algorithms.RoundRobin(numberOfPools, poolSize, &pools, &testList)

		for index, pool := range pools {
			fmt.Printf("Runde %d: %v\n", index, pool)
		}
	},
}

func validateSeedingArgs(numberOfPools string, poolSize string, lenTestList int) (int, int, error) {
	i_numberOfPools, err := strconv.Atoi(numberOfPools)
	if err != nil {
		return 0, 0, err
	}
	i_poolSize, err := strconv.Atoi(poolSize)
	if err != nil {
		return 0, 0, err
	}

	if i_numberOfPools*i_poolSize < lenTestList {
		return 0, 0, errors.New("Not all fencers can be placed in a pool.")
	}

	return i_numberOfPools, i_poolSize, nil
}

func init() {
	rootCmd.AddCommand(seedingRoundRobin)
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintf(os.Stderr, "Oops. An error while executing seeding '%s'\n", err)
		os.Exit(1)
	}
}
