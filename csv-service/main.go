package main

import (
	"fmt"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

var testData = []Tournament{
	{
		FirstDay:  time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC),
		SecondDay: time.Date(2000, 1, 2, 0, 0, 0, 0, time.UTC),
		City:      "Reutlingen",
		Category:  "RL",
		AgeGroup:  "U11",
	},
	{
		FirstDay:  time.Date(2000, 1, 31, 0, 0, 0, 0, time.UTC),
		SecondDay: time.Date(2000, 2, 1, 0, 0, 0, 0, time.UTC),
		City:      "Heidenheim",
		Category:  "DM",
		AgeGroup:  "U13",
	},
	{
		FirstDay:  time.Date(2000, 3, 1, 0, 0, 0, 0, time.UTC),
		SecondDay: time.Date(2000, 3, 2, 0, 0, 0, 0, time.UTC),
		City:      "Leverkusen",
		Category:  "QB",
		AgeGroup:  "Senioren",
	},
}

func main() {
	router := gin.Default()

	router.GET("/", healthCheck)
	router.GET("/tournaments", getTournaments)
	router.POST("/tournaments", postTournament)
	router.POST("/export-csv", exportCsv)

	router.Run() // run app on default 8080 and map 7000 to 8080 in Dockerfile
}

func healthCheck(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, "API is live and healthy")
}

func exportCsv(c *gin.Context) {

	// Parse json data to slice of tournament objects
	var tournamentData []Tournament

	if err := c.BindJSON(&tournamentData); err != nil {
		// TODO: Log this
		fmt.Printf("Error while parsing a list of tournaments from CURL-Post request: %s", err)
		c.IndentedJSON(http.StatusBadRequest, err)
		return
	}

	// Create a in-memory csv file
	cw := CsvWriter{c.Writer}

	// Write to the in-memory csv file
	if err := cw.Write(tournamentData); err != nil {
		fmt.Printf("Error while parsing tournament data from CURL-Post request: %s", err)
		return
	}

	// Return a stream/the created csv-file
	c.Header("Content-Disposition", "attachment; filename=tournaments.csv")
	c.Header("Content-Type", "text/csv")
}

func getTournaments(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, testData)
}

// Add a new tournament. This endpoint is just for testing right now
func postTournament(c *gin.Context) {
	var newTournament Tournament

	if err := c.BindJSON(&newTournament); err != nil {
		fmt.Printf("Error while parsing a tournament from CURL-Post request: %s", err)
		return
	}

	testData = append(testData, newTournament)
	c.IndentedJSON(http.StatusCreated, newTournament)
	for _, t := range testData {
		fmt.Println(t)
	}
}
