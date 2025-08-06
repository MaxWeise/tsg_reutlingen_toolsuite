import { useState } from "react";
import { Button, Form } from "react-bootstrap";
import TournamentTable from "./TournamentTable";

interface Tournament {
    firstDay: string
    secondDay: string
    city: string
    ageGroup: string
    category: string
}

const TournamentForm = () => {

    const [firstDay, setFirstDay] = useState("");
    const [secondDay, setSecondDay] = useState("");
    const [city, setCity] = useState("");
    const [ageGroup, setAgeGroup] = useState("");
    const [category, setCategory] = useState("");
    const [tournaments, setTournaments] = useState<Tournament[]>([]);

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (firstDay && secondDay && city && ageGroup && category) {
            const newTournament: Tournament = {
                firstDay,
                secondDay,
                city,
                ageGroup,
                category
            };
            setTournaments([...tournaments, newTournament]);
            // Clear form fields
            setFirstDay("");
            setSecondDay("");
            setCity("");
            setAgeGroup("");
            setCategory("");
        }
    };

    return (
        <>
            <h1>Input tournament data</h1>
            <Form onSubmit={handleSubmit}>
                <div className="container">
                    <div className="row">
                        <div className="col input-group m-2">
                            <span className="input-group-text">Erster Tag</span>
                            <input type="date" className="form-control" value={firstDay} onChange={(e) => { setFirstDay(e.target.value) }} />
                        </div>
                        <div className="col input-group m-2">
                            <span className="input-group-text">Zweiter Tag</span>
                            <input type="date" className="form-control" value={secondDay} onChange={(e) => { setSecondDay(e.target.value) }} />
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
                            <label className="input-group-text">Altersklasse</label>
                            <select className="form-select" id="inputGroupSelect01" value={ageGroup} onChange={(e) => { setAgeGroup(e.target.value) }}>
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
                    </div>
                    <Button type="submit" className="btn-primary m-2">Submit</Button>
                </div>
            </Form >
            <TournamentTable tournaments={tournaments} />
        </>
    );
};

export default TournamentForm;
