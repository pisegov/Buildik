import React, { useState, useEffect } from 'react';
import { Button, Modal } from 'react-bootstrap';
import Cookies from 'universal-cookie';
import axios from 'axios';

import 'bootstrap/dist/css/bootstrap.min.css';
import '../../index.css';

import SetupComponent from '../SetupComponent';
import Component from './Component';

function SelectionModal({ category, setup, setSetup, itemList }) {
  const [categoryComponents, setCategoryComponents] = useState([]);

  const [initItemList, setInitItemList] = itemList;
  const tempItemList = initItemList;

  let urlTail = '';

  if (initItemList.length) {
    urlTail += '?filter-items=[';
    initItemList.map(element => {
      urlTail += `[${element[0]},${element[1]}],`;
    });
    urlTail = urlTail.slice(0, -1);
    urlTail += ']';
  }

  // Get category items
  useEffect(() => {
    axios({
      method: 'GET',
      url: `/api/pccomponents/category-${category}/${urlTail}`,
    }).then(response => {
      setCategoryComponents(response.data);
    });
  }, [urlTail, setup, initItemList]);

  // Flag for showing modal window for saving setup
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  // Getting chosen components and csrf token from cookies
  const cookies = new Cookies();
  const [component, setComponent] = useState(cookies.get(category) || null);
  const csrftoken = cookies.get('csrftoken');

  const setItemToSetup = componentID => {
    try {
      // Post the component to current setup
      axios({
        method: 'POST',
        url: '/api/setups/setup_items/',
        headers: {
          'X-CSRFToken': csrftoken,
        },
        data: {
          setup: setup.id,
          item: componentID,
          number: '1',
        },
      }).then(res => {
        if (res) {
          // Get updated setup
          axios({
            method: 'GET',
            url: `/api/setups/${setup.id}`,
          }).then(response => {
            setSetup(response.data);
          });
        }
      });
    } catch (e) {
      console.log(`Error: ${e}`);
    }
  };

  const chooseComponent = component => {
    setComponent(component);
    cookies.set(category, component);

    if (setup) setItemToSetup(component.id);
    else {
      tempItemList.push([component.id, 1]);

      //   tempItemList[category] = { item: component.id, number: 1 };
      setInitItemList(tempItemList);
    }
  };

  const deleteComponent = component => {
    if (setup) {
      let link = 0;
      setup.parts.map(comp => {
        if (comp.item === component.id) link = comp.relation;
      });

      axios({
        method: 'DELETE',
        url: `/api/setups/setup_items/${link}`,
        headers: {
          'X-CSRFToken': csrftoken,
        },
      }).then(res => {
        if (res) {
          // Get updated setup
          axios({
            method: 'GET',
            url: `/api/setups/${setup.id}`,
          }).then(response => {
            setSetup(response.data);
          });
        }
      });
    } else {
      let counter = 0;

      for (let i = 0; i < tempItemList.length; ++i) {
        if (tempItemList[i][0] === component.id) {
          break;
        }
        ++counter;
      }

      // const index = tempItemList.indexOf([Number(component.id), 1]);
      tempItemList.splice(counter, 1);
      setInitItemList(tempItemList);
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
