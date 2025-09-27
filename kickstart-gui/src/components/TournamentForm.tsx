import React, { useState } from "react";
import { Alert, Button, Form } from "react-bootstrap";
import TournamentTable from "./TournamentTable";
import axios from "axios";
import FileUpload from "./FileUpload";

export interface Tournament {
    first_day: string
    second_day: string
    city: string
    category: string
    age_group: string
}

interface RequestData {
    endpoint: string,
    header: any,
    responseType: any,
    data: Tournament[],
    includeOptional?: boolean,
}

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
        .catch((error) => { console.error(`There has been an error while sending a request: ${error}`) });
}

const TournamentForm = ({ serverUrl }: { serverUrl: string }) => {

    const [first_day, setFirstDay] = useState("");
    const [second_day, setSecondDay] = useState("");
    const [city, setCity] = useState("");
    const [category, setCategory] = useState("");
    const [age_group, setAgeGroup] = useState("");
    const [tournaments, setTournaments] = useState<Tournament[]>([]);

    const [includeOptional, setIncludeOptional] = useState(false);

    const [uploadedFile, setUploadedFile] = useState<File | null>(null)

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

    const handleCreateTournamentOverview = (_: React.FormEvent<HTMLButtonElement>) => {
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

    const handleCreateRefereeOverview = (_: React.FormEvent<HTMLButtonElement>) => {
        // TODO: Handle button click
    };

    const exportDataAsCsv = (_: React.FormEvent<HTMLButtonElement>) => {

        let tournamentsWithNewDateFormat = tournaments.map((tournament: Tournament) => {
            tournament.first_day = `${tournament.first_day}T00:00:00Z`
            tournament.second_day = `${tournament.second_day}T00:00:00Z`
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

    const importDataFromCsv = (_: React.FormEvent<HTMLButtonElement>) => {
        const formData = new FormData();

        if (!uploadedFile) {
            // TODO: Show an alert to the user
            console.error("There is no file uploaded. Please first select a file.")
            return;
        }

        formData.append("file", uploadedFile);
        axios.post(`${serverUrl}:7000/import-csv`,
            formData
        )
            .then((response) => {
                console.info(response)
                // TODO: The response contains the data stored in the CSV file.
            })
            .catch((error) => {
                console.error(error)
            });
    };

    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files) {
            console.error("No File recieved. e.target.files is set to null.");
            return;
        }

        const file = e.target.files[0];
        setUploadedFile(file);
        console.info(`Set uploaded file to ${file}`);
    };

    return (
        <>
            <h1>Input tournament data</h1>
            <div className="container">
                <Form onSubmit={handleAddTournament} className="row">
                    <div className="container" id="input-form-group">
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
                        <Button className="btn-primary my-2" type="submit" >Turnier Hinzufügen</Button>
                    </div>
                </Form>
                <div className="container" id="button-group">
                    <div className="row">
                        <div className="form-check">
                            <input className="form-check-input" type="checkbox" checked={includeOptional} onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
                                console.info(`Checkbox is now ${event.target.checked}`)
                                setIncludeOptional(event.target.checked);
                            }} id="optional-checkbox" />
                            <label className="form-check-label" htmlFor="optional-checkbox">Optionale Turniere einfügen</label>
                        </div>
                        <Button className="btn-primary mx-2 col" onClick={handleCreateTournamentOverview}>Turnierübersicht erstellen</Button>
                        <Button className="btn-primary mx-2 col" onClick={handleCreateRefereeOverview}>Kampfrichterübersicht erstellen</Button>
                    </div>
                </div>
                <div className="container row">
                    <FileUpload
                        handleFileUpload={handleFileUpload}
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
