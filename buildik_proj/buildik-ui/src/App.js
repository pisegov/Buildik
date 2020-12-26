import { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from './Components/Navigation/Navbar';
import ConfiguratorTable from './Components/ConfiguratorTable';
import Cookies from 'universal-cookie';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import SetupsPage from './Components/SetupsPage';
import Login from './Components/Login';

function App() {
  const cookies = new Cookies();
  const [sessionId, setSessionId] = useState(cookies.get('sessionid'));

  // useEffect(() => {
  //   setSessionId();
  //   console.log('From app.js - ' + sessionId);
  // }, []);

  return (
    <div className="App">
      <Router>
        <Navbar sessionId={sessionId} />
        <Switch>
          <Route path="/setups/" exact={SetupsPage}>
            <SetupsPage sessionId={sessionId} />
          </Route>
          <Route path="/" exact={ConfiguratorTable}>
            <div className="wrapper">
              <h1>Buildik</h1>
              <ConfiguratorTable />
            </div>
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
