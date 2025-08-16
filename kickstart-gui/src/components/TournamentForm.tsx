import { useState } from "react";
import { Button, Form } from "react-bootstrap";
import TournamentTable from "./TournamentTable";
import axios from "axios";

const SERVER: string = "http://127.0.0.1:8000"

export interface Tournament {
    first_day: string
    second_day: string
    city: string
    category: string
    age_group: string
}

const TournamentForm = () => {

    const [first_day, setFirstDay] = useState("");
    const [second_day, setSecondDay] = useState("");
    const [city, setCity] = useState("");
    const [category, setCategory] = useState("");
    const [age_group, setAgeGroup] = useState("");
    const [tournaments, setTournaments] = useState<Tournament[]>([]);

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

    const handleSubmit = (_: React.FormEvent<HTMLButtonElement>) => {
        console.log(tournaments);
        axios.post(
            `${SERVER}/overview/tournament`,
            tournaments,
            {
                headers: { 'Accept': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' },
                responseType: "blob",
            },
        )
            .then((response) => {
                console.log(response)
                const blob = new Blob([response.data], { type: response.headers['content-type'] });
                const url = window.URL.createObjectURL(blob);

                // Construct a hidden link object and click it automatically
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', "tournament_overview_file.xlsx");
                document.body.appendChild(link);
                link.click();

                // Clean up
                link.parentNode?.removeChild(link);
                window.URL.revokeObjectURL(url);
            })
            .catch((error) => { alert(`There has been an error while sending a request: ${error}`) });
    };


    // TODO: Add checkbox to include optional tournaments
    return (
        <>
            <h1>Input tournament data</h1>
            <Form onSubmit={handleAddTournament}>
                <div className="container">
                    <div className="row">
                        <div className="col input-group m-2">
                            <span className="input-group-text">Erster Tag</span>
                            <input type="date" className="form-control" value={first_day} onChange={(e) => { setFirstDay(e.target.value) }} />
                        </div>
                        <div className="col input-group m-2">
                            <span className="input-group-text">Zweiter Tag</span>
                            <input type="date" className="form-control" value={second_day} onChange={(e) => { setSecondDay(e.target.value) }} />
                        </div>
                    </div>
                    <div className="row">
                        <div className="col input-group m-2">
                            <span className="input-group-text">Stadt</span>
                            <input type="text" className="form-control" value={city} onChange={(e) => { setCity(e.target.value) }} />
                        </div>
                    </div>
                    <div className="row">
                        <div className="col input-group m-2">
                            <label className="input-group-text">Kategorie</label>
                            <select className="form-select" id="inputGroupSelect01" value={category} onChange={(e) => { setCategory(e.target.value) }}>
                                <option selected>Kategorie</option>
                                <option>RL</option>
                                <option>QB</option>
                                <option>BNWM</option>
                                <option>DM</option>
                            </select>
                        </div>
                        <div className="col input-group m-2">
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
                    <Button type="submit" className="btn-primary m-2">Add</Button>
                    <Button className="btn-primary m-2" onClick={handleSubmit}>Submit</Button>
                </div>
            </Form >
            <TournamentTable tournaments={tournaments} />
        </>
    );
};

export default TournamentForm;
