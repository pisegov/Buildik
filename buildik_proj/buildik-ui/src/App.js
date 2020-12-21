import { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from './Components/Navigation/Navbar';
import ConfiguratorTable from './Components/ConfiguratorTable';

function App() {
  return (
    <div className="App">
      <Navbar />
      <div className="wrapper">
        <h1>Configurator</h1>
        <ConfiguratorTable />
      </div>
    </div>
  );
}

export default App;
