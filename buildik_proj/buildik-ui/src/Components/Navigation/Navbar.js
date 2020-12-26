import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Link } from 'react-router-dom';

function Navbar({ sessionId }) {
  function openLogin() {
    if (sessionId) {
      window.location.href = '/logout';
    } else {
      window.location.href = '/login';
    }
  }

  function openAdmin() {
    window.location.href = '/admin';
  }

  function openAPI() {
    window.location.href = '/api/docs';
  }

  function NavbarUserLinks() {
    const [userIsStaff, setUserIsStaff] = useState([]);

    useEffect(() => {
      axios({
        method: 'GET',
        url: 'http://127.0.0.1:8000/api/user/',
      }).then(response => {
        setUserIsStaff(response.data.is_staff);
      });
    }, []);

    if (userIsStaff) {
      return (
        <div>
          <a className="navbar-brand" href="#">
            <div className="nav-link" onClick={openAdmin}>
              Администратор
            </div>
          </a>
          <a className="navbar-brand" href="#">
            <div className="nav-link" onClick={openAdmin}>
              API
            </div>
          </a>
          <a className="navbar-brand" href="#">
            <Link className="nav-link" to={{ pathname: `/setups/`, fromDashboard: false }}>
              Мои сборки
            </Link>
          </a>
          <a className="navbar-brand" href="#">
            <div className="nav-link" onClick={openLogin}>
              Выйти
            </div>
          </a>
        </div>
      );
    } else {
      return (
        <div>
          <a className="navbar-brand" href="#">
            <Link className="nav-link" to={{ pathname: `/setups/`, fromDashboard: false }}>
              Мои сборки
            </Link>
          </a>
          <a className="navbar-brand" href="#">
            <div className="nav-link" onClick={openLogin}>
              Выйти
            </div>
          </a>
        </div>
      );
    }
  }

  function NavbarLinks() {
    if (sessionId) {
      return <NavbarUserLinks />;
    } else {
      return (
        <div>
          <a className="navbar-brand" href="#">
            <div className="nav-link" onClick={openLogin}>
              Войти
            </div>
          </a>
        </div>
      );
    }
  }

  return (
    <div className="Navbar">
      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            <Link className="nav-link" to={{ pathname: `/`, fromDashboard: false }}>
              Buildik
            </Link>
          </a>
          <div className="collapse navbar-collapse" id="navbarNav">
            <div className="navbar-nav" style={{ marginLeft: 'auto', marginRight: '3oem' }}>
              <NavbarLinks />
            </div>
          </div>
        </div>
      </nav>
    </div>
  );
}

export default Navbar;
