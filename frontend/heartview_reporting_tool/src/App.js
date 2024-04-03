import './App.css';
import './assets/css/bootstrap.min.css'
import ExcludedClients from './components/ExcludedClients';
// import Login from './components/Login';

function App() {
  return (
    <div className="App bg-dark text-light">
      {/* <Login/> */}
      <ExcludedClients/>
    </div>
  );
}

export default App;
