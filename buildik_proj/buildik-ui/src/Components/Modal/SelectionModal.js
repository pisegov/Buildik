import React, { useState, useEffect } from 'react';
import { Button, Modal } from 'react-bootstrap';
import { number, string } from 'prop-types';
import { useCookies } from 'react-cookie';
import Cookies from 'universal-cookie';
import axios from 'axios';

import 'bootstrap/dist/css/bootstrap.min.css';
import '../../index.css';

import SetupComponent from '../SetupComponent';
import Component from './Component';

function SelectionModal({ category }) {
  const [exampleData, setExampleData] = useState([
    {
      id: 1,
      name: 'Some item 1',
      manufacturer: 'Intel',
      model: 'Core I3',
      category,
      price: '300$',
      shortDescr: 'Short description of item 1',
    },
    {
      id: 2,
      name: 'Some item 2',
      manufacturer: 'AMD',
      model: 'Rizen 5',
      category,
      price: '300$',
      shortDescr: 'Short description of item 2',
    },
    {
      id: 3,
      name: 'Some item 3',
      manufacturer: 'Intel',
      model: 'Core I9',
      category,
      price: '300$',
      shortDescr: 'Short description of item 3',
    },
  ]);

  useEffect(() => {
    axios({
      method: 'GET',
      url: `http://127.0.0.1:8000/api/pccomponents/category-${category}/`,
    }).then(response => {
      setExampleData(response.data);
    });
  }, [category]);

  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);
  const cookies = new Cookies();

  const [component, setComponent] = useState(cookies.get(category) || null);

  // const [cookies, setCookie, removeCookie] = useCookies([]);

  const chooseComponent = comp => {
    setComponent(comp);
    cookies.set(category, comp);
  };

  const deleteComponent = () => {
    setComponent(null);
    cookies.remove(category);
  };

  return (
    <>
      <SetupComponent
        category={category}
        component={component}
        deleteComponent={deleteComponent}
        modalShow={handleShow}
      />

      <Modal show={show} onHide={handleClose} size="xl">
        <Modal.Header closeButton>
          <Modal.Title>Select {category}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {exampleData.map(component => {
            return <Component close={handleClose} chooseComponent={chooseComponent} component={component} />;
          })}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" onClick={handleClose}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default SelectionModal;
