package main

import (
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()

	router.GET("/", healthCheck)
	router.POST("/export-csv", exportCsv)
	router.POST("/import-csv", importCsv)

	router.Run() // run app on default 8080 and map 7000 to 8080 in Dockerfile
}

func healthCheck(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, "API is live and healthy")
}

func importCsv(c *gin.Context) {
	file, err := c.FormFile("file")
	if err != nil {
		c.String(http.StatusBadRequest, fmt.Sprintf("get form err: %s", err.Error()))
		return
	}

	f, err := file.Open()
	if err != nil {
		c.String(http.StatusBadRequest, fmt.Sprintf("open file err: %s", err.Error()))
		return
	}
	defer f.Close()

	csvReader := CsvReader{f}
	records, err := csvReader.Read()
	if err != nil {
		c.String(http.StatusInternalServerError, fmt.Sprintf("read all err: %s", err.Error()))
		return
	}

	c.JSON(http.StatusOK, records)
}

func exportCsv(c *gin.Context) {
	var tournamentData []Tournament

	if err := c.BindJSON(&tournamentData); err != nil {
		// TODO: Log this
		fmt.Printf("Error while parsing a list of tournaments from CURL-Post request: %s", err)
		c.IndentedJSON(http.StatusBadRequest, err)
		return
	}

	cw := CsvWriter{c.Writer}

	if err := cw.Write(tournamentData); err != nil {
		fmt.Printf("Error while parsing tournament data from CURL-Post request: %s", err)
		return
	}

	c.Header("Content-Disposition", "attachment; filename=tournaments.csv")
	c.Header("Content-Type", "text/csv")
}
