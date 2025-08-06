import { Table } from "react-bootstrap";

interface Tournament {
    firstDay: string;
    secondDay: string;
    city: string;
    ageGroup: string;
    category: string;
}

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
                    <th>Age Group</th>
                    <th>Category</th>
                </tr>
            </thead>
            <tbody>
                {tournaments.map((tournament, index) => (
                    <tr key={index}>
                        <td>{tournament.firstDay}</td>
                        <td>{tournament.secondDay}</td>
                        <td>{tournament.city}</td>
                        <td>{tournament.ageGroup}</td>
                        <td>{tournament.category}</td>
                    </tr>
                ))}
            </tbody>
        </Table>
    );
};

export default TournamentTable;
