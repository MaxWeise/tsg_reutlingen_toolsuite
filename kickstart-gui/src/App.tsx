import "bootstrap/dist/css/bootstrap.min.css";
import TournamentForm from "./components/TournamentForm";
import axios from "axios";


const App = () => {
  const serverUrl: string = "http://127.0.0.1"

  axios.get(`${serverUrl}:8000/`)
    .then(() => {
      console.info("Health check was sucessfull");
    })
    .catch((error) => {
      console.error(`Error occured: ${error}`)
      alert("There has been an error on the server side.")
    });

  return (
    <>
      <TournamentForm serverUrl={serverUrl} />
    </>
  )
}

export default App
