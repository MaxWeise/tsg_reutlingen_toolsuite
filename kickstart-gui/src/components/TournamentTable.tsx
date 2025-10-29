import { Button, Table } from "react-bootstrap";
import type { Tournament } from "./TournamentForm";


interface TournamentTableProps {
    tournaments: Tournament[];
    onDelete: (index: number) => void;
}

const TournamentTable = ({ tournaments, onDelete }: TournamentTableProps) => {

    return (
        <Table striped bordered hover>
            <thead>
                <tr>
                    <th>Erster Tag</th>
                    <th>Zweiter Tag</th>
                    <th>Stadt</th>
                    <th>Kategorie</th>
                    <th>Altersklasse</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {tournaments.map((tournament, index) => (
                    <tr key={index}>
                        <td>{tournament.first_day}</td>
                        <td>{tournament.second_day}</td>
                        <td>{tournament.city}</td>
                        <td>{tournament.category}</td>
                        <td>{tournament.age_group}</td>
                        <td>
                            <Button className="btn btn-danger" onClick={() => onDelete(index)}>Delete Tournament</Button>
                        </td>
                    </tr>
                ))}
            </tbody>
        </Table>
    );
};

export default TournamentTable;
