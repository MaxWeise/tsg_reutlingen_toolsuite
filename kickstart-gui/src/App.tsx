import "bootstrap/dist/css/bootstrap.min.css";
import TournamentForm from "./components/TournamentForm";

const App = () => {

  const serverUrl: string = "http://127.0.0.1"

  return (
    <>
      <TournamentForm serverUrl={serverUrl} />
    </>
  )
}

export default App
