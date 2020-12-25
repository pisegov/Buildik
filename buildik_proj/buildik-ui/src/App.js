import { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from './Components/Navigation/Navbar';
import ConfiguratorTable from './Components/ConfiguratorTable';
import Cookies from 'universal-cookie';

function App() {
  const cookies = new Cookies();

  const [isAutorised, setIsAutorised] = useState(false);

  useEffect(() => {
    setIsAutorised(Boolean(cookies.get('sessionid')));
  }, []);

  return (
    <div className="App">
      <Navbar isAutorised={isAutorised} />
      <div className="wrapper">
        <h1>Configurator</h1>
        <ConfiguratorTable />
      </div>
    </div>
  );
}

export default App;
