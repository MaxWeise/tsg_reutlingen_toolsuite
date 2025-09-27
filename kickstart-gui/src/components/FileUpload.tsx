import { Button, Form } from "react-bootstrap";

const FileUpload = ({ setFile, handleCsvExport, handleCsvImport }: any) => {

    const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (!e.target.files) {
            console.error("No File recieved. e.target.files is set to null.");
            return;
        }

        const file = e.target.files[0];
        setFile(file);
        console.info(`Set uploaded file to ${file}`);
    };

    return (
        <>
            <Form.Group controlId="formFile">
                <Form.Control type="file" onChange={handleFileUpload} />
            </Form.Group>
            <Button className="btn-primary mx-2" onClick={handleCsvExport}>Daten exportieren</Button>
            <Button className="btn-primary mx-2" onClick={handleCsvImport}>Daten importieren</Button>
        </>
    );

};

export default FileUpload
