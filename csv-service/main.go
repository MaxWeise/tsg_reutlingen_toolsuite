package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()
	router.Use(cors.Default()) // allow all origins TODO: only allow a select range of origins.

	log.SetFlags(log.LstdFlags | log.Lshortfile)

	router.GET("/", healthCheck)
	router.POST("/export-csv", exportCsv)
	router.POST("/import-csv", importCsv)

	router.Run() // run app on default 8080 and map 7000 to 8080 in Dockerfile
}

func healthCheck(c *gin.Context) {
	c.IndentedJSON(http.StatusOK, "API is live and healthy")
}

func importCsv(c *gin.Context) {
	log.Println("Importing csv file.")
	file, err := c.FormFile("file")
	if err != nil {
		errFormat := fmt.Sprintf("get form err: %s", err.Error())
		c.String(http.StatusBadRequest, errFormat)
		log.Println(errFormat)
		return
	}

	f, err := file.Open()
	if err != nil {
		errFormat := fmt.Sprintf("open file err: %s", err.Error())
		c.String(http.StatusBadRequest, errFormat)
		log.Println(errFormat)
		return
	}
	defer f.Close()

	log.Println("Sucessfully parsed csv file. Now reading file.")
	csvReader := CsvReader{f}
	records, err := csvReader.Read()
	if err != nil {
		errFormat := fmt.Sprintf("read all err: %s", err.Error())
		c.String(http.StatusInternalServerError, errFormat)
		log.Println(errFormat)
		return
	}

	c.JSON(http.StatusOK, records)
}

func exportCsv(c *gin.Context) {
	log.Println("Receiving data from the client, now parsing")
	var tournamentData []Tournament

	if err := c.BindJSON(&tournamentData); err != nil {
		errFormat := fmt.Sprintf("Error while parsing a list of tournaments from CURL-Post request: %s", err)
		c.IndentedJSON(http.StatusBadRequest, errFormat)
		log.Println(errFormat)
		return
	}

	log.Println("Now writing to csv file.")
	cw := CsvWriter{c.Writer}

	if err := cw.Write(tournamentData); err != nil {
		errFormat := fmt.Sprintf("Error while parsing tournament data from CURL-Post request: %s", err)
		c.IndentedJSON(http.StatusInternalServerError, errFormat)
		log.Println(errFormat)
		return
	}

	log.Println("Sucessfully written to file. Serving to client.")
	c.Header("Content-Disposition", "attachment; filename=tournaments.csv")
	c.Header("Content-Type", "text/csv")
}
