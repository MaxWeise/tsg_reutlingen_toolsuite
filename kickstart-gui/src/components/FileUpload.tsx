import React, { useEffect, useState } from "react";
import { Button, Form } from "react-bootstrap";

const FileUpload = ({ serviceHealthCheck, setFile, handleCsvExport, handleCsvImport }: any) => {

    const [isServiceAvailable, setIsBackendAvailable] = useState<boolean>(false)

    useEffect(() => {
        const backendIsHealthy = async () => {
            const url: string = "http://127.0.0.1:7000/"
            const healtyh = await serviceHealthCheck("csv-service", url)
            setIsBackendAvailable(healtyh)
        }

        backendIsHealthy();
    }, []);

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
                    <Button disabled={!isServiceAvailable} className="btn-secondary my-2 mx-2 col" onClick={handleCsvExport}>Daten exportieren</Button>
                    <Button disabled={!isServiceAvailable} className="btn-secondary my-2 mx-2 col" onClick={handleCsvImport}>Daten importieren</Button>
                </div>
            </div>
        </>
    );

};

export default FileUpload
