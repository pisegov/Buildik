import React, { useState, useEffect } from 'react';
import { Button, Modal } from 'react-bootstrap';
import Cookies from 'universal-cookie';
import axios from 'axios';

import 'bootstrap/dist/css/bootstrap.min.css';
import '../../index.css';

import SetupComponent from '../SetupComponent';
import Component from './Component';

function SelectionModal({ category, setupID, setSetup, itemList }) {
  const [categoryComponents, setCategoryComponents] = useState([]);

  const [initItemList, setInitItemList] = itemList;
  const tempItemList = initItemList;

  // Get category items
  useEffect(() => {
    axios({
      method: 'GET',
      url: `http://127.0.0.1:8000/api/pccomponents/category-${category}/`,
    }).then(response => {
      setCategoryComponents(response.data);
    });
  }, [category]);

  // Flag for showing modal window for saving setup
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  // Getting chosen components and csrf token from cookies
  const cookies = new Cookies();
  const [component, setComponent] = useState(cookies.get(category) || null);
  const csrftoken = cookies.get('csrftoken');

  // If there is component in this category, it adds component to setup initial list
  if (component) {
    tempItemList[category] = { itemID: component.id, number: 1 };
    setInitItemList(tempItemList);
  }

  const [linkID, setLinkID] = useState(null);

  const setItemToSetup = componentID => {
    try {
      // Post the component to current setup
      axios({
        method: 'POST',
        url: 'http://127.0.0.1:8000/api/setups/setup_items/',
        headers: {
          'X-CSRFToken': csrftoken,
        },
        data: {
          setup: setupID,
          item: componentID,
          number: '1',
        },
      }).then(res => {
        if (res) {
          // Get updated setup
          axios({
            method: 'GET',
            url: `http://127.0.0.1:8000/api/setups/${setupID}`,
          }).then(response => {
            setSetup(response.data);
          });

          setLinkID(res.data.id);
        }
      });
    } catch (e) {
      console.log(`Error: ${e}`);
    }
  };

  const chooseComponent = component => {
    setComponent(component);
    cookies.set(category, component);

    if (setupID) setItemToSetup(component.id);
    else {
      tempItemList[category] = { item: component.id, number: 1 };
      setInitItemList(tempItemList);
      console.log(initItemList);
    }
  };

  const deleteComponent = component => {
    if (setupID) {
      console.log(linkID);
      axios({
        method: 'DELETE',
        url: `http://127.0.0.1:8000/api/setups/setup_items/${linkID}`,
        headers: {
          'X-CSRFToken': csrftoken,
        },
      });
    } else {
      delete tempItemList[category];
      setInitItemList(tempItemList);
      console.log(initItemList);
    }

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
          {categoryComponents.map(component => {
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
