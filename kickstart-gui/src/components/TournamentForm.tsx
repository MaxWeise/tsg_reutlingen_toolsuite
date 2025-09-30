import React, { useEffect, useState } from "react";
import { Button, Form } from "react-bootstrap";
import TournamentTable from "./TournamentTable";
import axios from "axios";
import FileUpload from "./FileUpload";

/**
 * Represents a single tournament event.
 *
 * @param {string} first_day - The start date of the tournament in YYYY-MM-DD format.
 * @param {string} second_day - The end date of the tournament in YYYY-MM-DD format. Can be the same as the first day.
 * @param {string} city - The city where the tournament takes place.
 * @param {string} category - The category of the tournament (e.g., RL for 'Rangliste', DM for 'Deutsche Meisterschaft').
 * @param {string} age_group - The age group for which the tournament is held (e.g., U13, U17, Senioren).
 */
export interface Tournament {
    first_day: string
    second_day: string
    city: string
    category: string
    age_group: string
}

/**
 * Bundle data used to make a request in an object. This is primarily used for logging.
 *
 * @param {string} endpoint - The endpoint to send the request to.
 * @param {any} header - The header to send with the request.
 * @param {any} responseType - The type of the response.
 * @param {Tournament[]} data - The data contained in the request.
 * @param {boolean | void} includeOptional - Wheather to include optional tournaments in the overview. Only used for Tournament Overview.
 */
interface RequestData {
    endpoint: string,
    header: any,
    responseType: any,
    data: Tournament[],
    includeOptional?: boolean,
}


const TournamentForm = ({ serverUrl }: { serverUrl: string }) => {

    const [first_day, setFirstDay] = useState("");
    const [second_day, setSecondDay] = useState("");
    const [city, setCity] = useState("");
    const [category, setCategory] = useState("");
    const [age_group, setAgeGroup] = useState("");
    const [tournaments, setTournaments] = useState<Tournament[]>([]);

    const [uploadedFile, setUploadedFile] = useState<File | null>(null)

    const [isBackendAvailable, setIsBackendAvailable] = useState<boolean>(false)

    /* Check the health of saison-kickstarter backend */
    useEffect(() => {
        const backendIsHealthy = async () => {
            const url: string = "http://127.0.0.1:8000/"
            const healtyh = await checkServiceHealth("saison-kickstarter-backend", url)
            setIsBackendAvailable(healtyh)
        }

        backendIsHealthy();
    }, []);

    const handleAddTournament = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (first_day && second_day && city && age_group && category) {
            const newTournament: Tournament = {
                first_day,
                second_day,
                city,
                category,
                age_group,
            };
            setTournaments([...tournaments, newTournament]);
            // Clear form fields
            setFirstDay("");
            setSecondDay("");
            setCity("");
            setCategory("");
            setAgeGroup("");
        }
    };

    /* make a request to the backend to create a tournament overview */
    const handleCreateTournamentOverview = (includeOptional: boolean) => {
        const endpoint = includeOptional
            ? `${serverUrl}:8000/overview/tournament?include_optional=true`
            : `${serverUrl}:8000/overview/tournament`;
        const header = { 'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }
        const responseType = "blob"

        // Used for logging
        const request: RequestData = {
            endpoint: endpoint,
            header: header,
            responseType: responseType,
            data: tournaments,
            includeOptional: includeOptional,
        };
        makeFileDownloadRequest(request, "tournament_overview_file.xlsx");
    };

    /* make a request to the backend to create a referee overview */
    const handleCreateRefereeOverview = () => {
        const endpoint = `${serverUrl}:8000/overview/referee`;
        const header = { 'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }
        const responseType = "blob"

        const request: RequestData = {
            endpoint: endpoint,
            header: header,
            responseType: responseType,
            data: tournaments,
        };
        makeFileDownloadRequest(request, "referee_overview_file.xlsx");
    };

    /* Take the tournament data from the table and export it into a csv file */
    const exportDataAsCsv = () => {

        let tournamentsWithNewDateFormat = tournaments.map((tournament: Tournament) => {
            tournament.first_day = `${tournament.first_day}T00:00:00Z`
            tournament.second_day = `${tournament.second_day}T00:00:00Z`
            tournament.city = tournament.city.trim()
            tournament.age_group = tournament.age_group.trim()
            tournament.category = tournament.category.trim()
            return tournament
        });

        const endpoint = `${serverUrl}:7000/export-csv`;
        const header = { 'Accept': 'text/csv' }
        const responseType = "blob"

        // Used for logging
        const request: RequestData = {
            endpoint: endpoint,
            header: header,
            responseType: responseType,
            data: tournamentsWithNewDateFormat,
        };
        makeFileDownloadRequest(request, "tournaments.csv");
    };

    /* Take the tournament data from a csv file and import them into the programm */
    const importDataFromCsv = (_: React.FormEvent<HTMLButtonElement>) => {
        const formData = new FormData();

        if (!uploadedFile) {
            const msg = "There is no file uploaded. Please first select a file."
            console.error(msg)
            alert(msg)
            return;
        }

        formData.append("file", uploadedFile);
        axios.post(`${serverUrl}:7000/import-csv`,
            formData
        )
            .then((response) => {
                console.info(response.data)
                const tournaments: Tournament[] = response.data.map(function(item: any) {
                    return ({
                        first_day: parseDate(item.first_day),
                        second_day: parseDate(item.second_day),
                        city: item.city.trim(),
                        category: item.category.trim(),
                        age_group: item.age_group.trim(),
                    });
                });
                setTournaments(tournaments)
            })
            .catch((error) => {
                console.error(error)
                alert(error)
            });
    };

    return (
        <>
            <h1>Input tournament data</h1>
            <div className="container-fluid">
                <Form onSubmit={handleAddTournament} className="row">
                    <div className="container-fluid" id="input-form-group">
                        <div className="row my-2">
                            <div className="col input-group">
                                <span className="input-group-text">Erster Tag</span>
                                <input type="date" className="form-control" value={first_day} onChange={(e) => { setFirstDay(e.target.value) }} />
                            </div>
                            <div className="col input-group">
                                <span className="input-group-text">Zweiter Tag</span>
                                <input type="date" className="form-control" value={second_day} onChange={(e) => { setSecondDay(e.target.value) }} />
                            </div>
                        </div>
                        <div className="row my-2">
                            <div className="col input-group">
                                <span className="input-group-text">Stadt</span>
                                <input type="text" className="form-control" value={city} onChange={(e) => { setCity(e.target.value) }} />
                            </div>
                        </div>
                        <div className="row my-2">
                            <div className="col input-group">
                                <label className="input-group-text">Kategorie</label>
                                <select className="form-select" id="inputGroupSelect01" value={category} onChange={(e) => { setCategory(e.target.value) }}>
                                    <option selected>Kategorie</option>
                                    <option>RL</option>
                                    <option>QB</option>
                                    <option>BNWM</option>
                                    <option>DM</option>
                                </select>
                            </div>
                            <div className="col input-group">
                                <label className="input-group-text">Altersklasse</label>
                                <select className="form-select" id="inputGroupSelect01" value={age_group} onChange={(e) => { setAgeGroup(e.target.value) }}>
                                    <option selected>Altersklasse</option>
                                    <option>U11</option>
                                    <option>U13</option>
                                    <option>U15</option>
                                    <option>U17</option>
                                    <option>U20</option>
                                    <option>Senioren</option>
                                    <option>Veteranen</option>
                                </select>
                            </div>
                        </div>
                        <div className="container-fluid row">
                            <Button className="btn-primary my-2 mx-2 col" type="submit" >Turnier Hinzufügen</Button>
                        </div>
                    </div>
                </Form>
                <div className="container-fluid row my-2">
                    <Button disabled={!isBackendAvailable} className="btn-primary mx-2 col" onClick={() => handleCreateTournamentOverview(true)}>Turnierübersicht erstellen</Button>
                    <Button disabled={!isBackendAvailable} className="btn-primary mx-2 col" onClick={() => handleCreateTournamentOverview(false)}>Turnierübersicht erstellen (optionale turniere)</Button>
                </div>
                <div className="container-fluid row my-2">
                    <Button disabled={!isBackendAvailable} className="btn-primary mx-2 col" onClick={handleCreateRefereeOverview}>Kampfrichterübersicht erstellen</Button>
                </div>
                <div className="container-fluid row my-2">
                    <FileUpload
                        serviceHealthCheck={checkServiceHealth}
                        setFile={setUploadedFile}
                        handleCsvExport={exportDataAsCsv}
                        handleCsvImport={importDataFromCsv} />
                </div>
                <div id="tournament-table">
                    <TournamentTable tournaments={tournaments} />
                </div>
            </div>
        </>
    );
};

export default TournamentForm;

/** 
 * Make a request to the specified server to determines it's availability.
 * 
 * @param {string} serviceName - The name of the service. Primarily used for logging.
 * @param {string} serviceUrl - The url which is used to contact the service. Expects that the root endpoint is used for health checking.
 * @returns {boolean} True if the server returns a response code in the 2xx range. False otherwise
 * */
const checkServiceHealth = async (serviceName: string, serviceUrl: string): Promise<boolean> => {
    try {
        console.info(`Checking health for ${serviceName}`)
        const response = await fetch(serviceUrl)

        console.info("Service is healthy. Eneabling buttons.")
        return response.ok
    } catch (error) {
        console.error(`Health check failed for ${serviceName}. Backend is not available at ${serviceUrl}`)
        return false
    }
};

/** 
 * Make a post request to the backend api.
 * When status code is 2xx a hidden link is created and clicked which will download the excel file with the given name.
 *
 * @param {RequestData} requestData - An object that holds the data to make the request.
 * @param {string} fileName - The name of the file that get's downloaded.
 */
function makeFileDownloadRequest(requestData: RequestData, fileName: string): void {
    console.info(`Making the following request ${JSON.stringify(requestData)}`)

    axios.post(
        requestData.endpoint,
        requestData.data,
        {
            headers: requestData.header,
            responseType: requestData.responseType
        },
    )
        .then((response) => {
            console.log(response)
            const blob = new Blob([response.data], { type: response.headers['content-type'] });
            const url = window.URL.createObjectURL(blob);

            // Construct a hidden link object and click it automatically
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', fileName);
            document.body.appendChild(link);
            link.click();

            // Clean up
            link.parentNode?.removeChild(link);
            window.URL.revokeObjectURL(url);
        })
        .catch((error) => { console.error(`There has been an error while sending a request: ${error} `) });
};

/**
 * Parse a data from the go format (RF3339 with timestamp) to YYYY-MM-DD format
 *
 * @param {string} date - The date given from the api in RF3339 format. 
 * @returns {string} - The date in YYYY-MM-DD format.
 */
function parseDate(date: string): string {
    const parts = date.split("T");
    return parts[0];
};
