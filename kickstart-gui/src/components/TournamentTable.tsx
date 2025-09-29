import { Table } from "react-bootstrap";
import type { Tournament } from "./TournamentForm";


interface TournamentTableProps {
    tournaments: Tournament[];
}

const TournamentTable = ({ tournaments }: TournamentTableProps) => {
    return (
        <Table striped bordered hover>
            <thead>
                <tr>
                    <th>First Day</th>
                    <th>Second Day</th>
                    <th>City</th>
                    <th>Category</th>
                    <th>Age Group</th>
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
                    </tr>
                ))}
            </tbody>
        </Table>
    );
};

export default TournamentTable;
