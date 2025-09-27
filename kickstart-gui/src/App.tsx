import "bootstrap/dist/css/bootstrap.min.css";
import TournamentForm from "./components/TournamentForm";
import axios from "axios";

async function isServerAvailable(serverUrl: string): boolean {
    console.info(`Making health check request to ${serverUrl}:8000/`)
    let isOk = false;
    try {
        const response = await axios.get(`${serverUrl}:8000/`)
        console.log(response);
        isOk = response.status == 200;
    } catch (error) {
        console.error(error)
        return isOk
    }

    console.info(`Now returning ${isOk}`);
    return isOk
};


const App = () => {

  const serverUrl = "http://127.0.0.1"

  return (
    <>
      <TournamentForm serverUrl={serverUrl, isServerAvailable(serverUrl)} />
    </>
  )
}

export default App
