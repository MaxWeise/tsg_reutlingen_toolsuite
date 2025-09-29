package cmd

import (
	"fmt"
	"os"
	"strconv"

	"tsg-toolsuite/tournament-seeding/algorithms"

	"github.com/spf13/cobra"
	"github.com/xuri/excelize/v2"
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
		nameList, err := getNamesFromExcel("test-rangliste.xlsx")
		if err != nil {
			fmt.Println("Error:", err)
			return
		}

		r := algorithms.RoundRobin{}
		runSeedingLogic(args[0], args[1], nameList, r)
	},
}

var seedingBlockwise = &cobra.Command{
	Use:   "blockwise",
	Short: "Seeding in blocks.",
	Long:  "Create pools acording to the specified arguments. Supply in this order: number of pools, pool size.",
	Args:  cobra.ExactArgs(2),
	Run: func(cmd *cobra.Command, args []string) {
		nameList, err := getNamesFromExcel("test-rangliste.xlsx")
		if err != nil {
			fmt.Println("Error:", err)
			return
		}

		r := algorithms.BlockwiseSeeding{}
		runSeedingLogic(args[0], args[1], nameList, r)
	},
}

func runSeedingLogic(numOfPools string, size string, nameList []string, strategy algorithms.Strategy) error {
	numberOfPools, poolSize, err := validateSeedingArgs(numOfPools, size, len(nameList))
	if err != nil {
		return err
	}

	pools := make(map[int][]string)

	// Create for each pool an empty slice with the reserved pool size.
	for index := range numberOfPools {
		pools[index] = make([]string, 0, poolSize)
	}

	strategy.Seeding(numberOfPools, poolSize, &pools, &nameList)

	for index, pool := range pools {
		fmt.Printf("Runde %d: %v\n", index, pool)
	}

	return nil
}

func getNamesFromExcel(fileName string) ([]string, error) {
	file, err := excelize.OpenFile(fileName)
	if err != nil {
		return nil, err
	}

	rows, err := file.GetRows("Tabelle1")
	if err != nil {
		return nil, err
	}

	names := []string{}

	for _, row := range rows {
		if len(row) == 0 {
			continue
		}
		names = append(names, row[2])
	}

	// Remove header from list
	names = names[1:]
	return names, nil
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
		return 0, 0, fmt.Errorf("Not all fencers can be placed in a pool. You have %d fencers.", lenTestList)
	}

	return i_numberOfPools, i_poolSize, nil
}

func init() {
	rootCmd.AddCommand(seedingRoundRobin)
	rootCmd.AddCommand(seedingBlockwise)
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintf(os.Stderr, "Oops. An error while executing seeding '%s'\n", err)
		os.Exit(1)
	}
}
