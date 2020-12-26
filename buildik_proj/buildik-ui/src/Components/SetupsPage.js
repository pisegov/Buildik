import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button } from 'react-bootstrap';
import Cookies from 'universal-cookie';

function SetupsPage({ sessionId }) {
  const cookies = new Cookies();
  const csrftoken = cookies.get('csrftoken');

  const [user, setUser] = useState({});

  useEffect(() => {
    axios({
      method: 'GET',
      url: `http://127.0.0.1:8000/api/user/`,
    }).then(response => {
      setUser(response.data);
    });
  }, []);

  function GetSetups() {
    const [setups, setSetups] = useState([]);

    useEffect(() => {
      axios({
        method: 'GET',
        url: `http://127.0.0.1:8000/api/setups/`,
      }).then(response => {
        setSetups(response.data);
      });
    }, []);

    function deleteSetup(setup) {
      axios({
        method: 'DELETE',
        url: `http://127.0.0.1:8000/api/setups/${setup.id}`,
        headers: {
          'X-CSRFToken': csrftoken,
        },
      }).then(res => {
        if (res) {
          // Get updated setup
          axios({
            method: 'GET',
            url: `http://127.0.0.1:8000/api/setups/`,
          }).then(response => {
            setSetups(response.data);
          });
        }
      });
    }
    return (
      <div className="wrapper">
        <h1>
          Сборки {user.first_name} {user.last_name}{' '}
        </h1>
        <div style={{ paddingTop: '1rem' }}>
          {setups.map(setup => {
            return (
              <div>
                <ul>
                  <h3 style={{ color: 'navy' }}>Название сборки: {setup.name}</h3>
                  {setup.parts.map(component => {
                    return (
                      <h4>
                        {component.manufacturer} {component.model}
                      </h4>
                    );
                  })}
                </ul>
                <div style={{ marginLeft: 'auto', marginRight: '.5oem', width: '120px', color: 'red' }}>
                  <div style={{ marginLeft: 'auto', marginRight: '.5oem', width: '120px' }}>
                    <style type="text/css">
                      {`
                        .btn-flat {
                          background-color: red;
                          color: white;
                        }

                      `}
                    </style>
                    <Button
                      variant="flat"
                      onClick={() => {
                        deleteSetup(setup);
                      }}
                    >
                      Удалить
                    </Button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  if (sessionId) {
    return <GetSetups />;
  } else {
    return (
      <div>
        <p>You are not autorised</p>
        <p>Please login</p>
      </div>
    );
  }
}

export default SetupsPage;
