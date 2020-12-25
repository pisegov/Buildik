import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Link } from 'react-router-dom';
import { func } from 'prop-types';

function Navbar({ isAutorised }) {
  const [userData, setUserData] = useState([]);

  useEffect(() => {
    axios({
      method: 'GET',
      url: 'http://127.0.0.1:8000/api/user/',
    }).then(response => {
      setUserData(response.data);
    });
  }, []);

  function NavbarLinks() {
    return <div></div>;
  }

  return (
    <div className="Navbar">
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            {/* <Link className="nav-link" to={{ pathname: `http://127.0.0.1:8000/`, fromDashboard: false }}>
            </Link> */}
            Buildik
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <div className="navbar-nav">
              {/* {categories.map(c => (
                <Link className="nav-link" to={{ pathname: `/category/${c.id}/`, fromDashboard: false }}>
                  {c.name}
                </Link>
              ))} */}
            </div>
          </div>
        </div>
      </nav>
    </div>
  );
}

export default Navbar;
