import { Button, Form } from "react-bootstrap";

const FileUpload = ({ handleFileUpload, handleCsvExport, handleCsvImport }: any) => {

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
