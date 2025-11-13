package cmd

import (
	"errors"
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
	Long:  "Create pools acording to the specified arguments. Supply in this order: ranking-file, number of pools, pool size.",
	Args:  cobra.ExactArgs(3),
	Run: func(cmd *cobra.Command, args []string) {
		r := algorithms.RoundRobin{}
		err := runCommand(args[0], args[1], args[2], r)
		if err != nil {
			fmt.Print("Error: ", err)
			return
		}
	},
}

var seedingBlockwise = &cobra.Command{
	Use:   "blockwise",
	Short: "Seeding in blocks.",
	Long:  "Create pools acording to the specified arguments. Supply in this order: ranking-file, number of pools, pool size.",
	Args:  cobra.ExactArgs(3),
	Run: func(cmd *cobra.Command, args []string) {
		r := algorithms.BlockwiseSeeding{}
		err := runCommand(args[0], args[1], args[2], r)
		if err != nil {
			fmt.Print("Error: ", err)
			return
		}
	},
}

// Define the flow of seeding. Provide an abstraction to handle different seeding algorithms in the same sequence of steps
func runCommand(filePath string, numberOfPools string, size string, seedingAlgorithm algorithms.Strategy) error {
	file, err := excelize.OpenFile(filePath)
	if err != nil {
		return err
	}

	sheetName, err := selectSheetName(file)
	if err != nil {
		return err
	}

	nameList, err := getNamesFromExcel(file, sheetName)
	fmt.Println(nameList)
	if err != nil {
		return err
	}

	pools, err := runSeedingLogic(numberOfPools, size, nameList, seedingAlgorithm)
	if err != nil {
		return err
	}

	for index, pool := range pools {
		fmt.Printf("Runde %d: %v\n", index, pool)
	}

	return nil
}

func runSeedingLogic(numOfPools string, size string, nameList []string, strategy algorithms.Strategy) (map[int][]string, error) {
	numberOfPools, poolSize, err := validateSeedingArgs(numOfPools, size, len(nameList))
	if err != nil {
		return nil, err
	}

	pools := make(map[int][]string)

	// Create for each pool an empty slice with the reserved pool size.
	for index := range numberOfPools {
		pools[index] = make([]string, 0, poolSize)
	}

	strategy.Seeding(numberOfPools, poolSize, &pools, &nameList)

	return pools, err
}

func getNamesFromExcel(file *excelize.File, sheetName string) ([]string, error) {

	rows, err := file.GetRows(sheetName)
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

// Prompts the user to select a sheet from the workbook
// If only one sheet is available, the function will automatically select this sheet.
func selectSheetName(file *excelize.File) (string, error) {

	sheetNames := file.GetSheetList()

	// If only one element exists then return this single element
	if len(sheetNames) == 1 {
		return sheetNames[0], nil
	}

	for index, n := range sheetNames {
		fmt.Println(index, "---", n)

	}
	var i int
	fmt.Println("Please select a worksheet")
	fmt.Scan(&i)

	if i >= len(sheetNames) {
		return "", errors.New("Entered a number that is too large.")
	}

	return sheetNames[i], nil

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
