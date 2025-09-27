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
            <div className="container-fluid">
                <Form.Group controlId="formFile" className="row">
                    <Form.Control type="file" onChange={handleFileUpload} />
                </Form.Group>
                <div className="row">
                    <Button className="btn-secondary my-2 mx-2 col" onClick={handleCsvExport}>Daten exportieren</Button>
                    <Button className="btn-secondary my-2 mx-2 col" onClick={handleCsvImport}>Daten importieren</Button>
                </div>
            </div>
        </>
    );

};

export default FileUpload
