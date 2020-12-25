import React, { useState, useEffect } from 'react';
import { Button } from 'react-bootstrap';
import SelectionModal from './Modal/SelectionModal';
import axios from 'axios';
import { Modal } from 'react-bootstrap';
import NameForm from './NameForm';
import Cookies from 'universal-cookie';

const styles = {
  ul: {
    listStyle: 'none',
    margin: 0,
    padding: 0,
  },
};

const configuratorCategories = [
  'cpu',
  'motherboard',
  'case',
  'gpu',
  'cpu_cooler',
  'ram',
  'storage',
  'power_supply_unit',
];

function ConfiguratorTable(props) {
  const [setup, setSetup] = useState(null);
  const [setupID, setSetupID] = useState(null);
  const [initItemList, setInitItemList] = useState([]);

  useEffect(() => {
    const cookies = new Cookies();
    const tempItemList = initItemList;
    configuratorCategories.map(category => {
      const savedItem = cookies.get(category);

      if (savedItem) {
        tempItemList.push([savedItem.id, 1]);
      }
    });
    setInitItemList(tempItemList);
  }, []);

  const [showSave, setShowSave] = useState(false);
  const handleClose = () => setShowSave(false);
  const handleShow = () => setShowSave(true);

  const setSetupWithID = setup => {
    setSetup(setup);
    setSetupID(setup.id);
  };

  return (
    <>
      <ul style={styles.ul}>
        {configuratorCategories.map(category => {
          // return <SetupComponent category={category} />;
          return (
            <SelectionModal
              category={category}
              setSetup={setSetupWithID}
              setup={setup}
              itemList={[initItemList, setInitItemList]}
            />
          );
        })}
      </ul>
      <Button onClick={handleShow}>Save</Button>

      <Modal show={showSave} onHide={handleClose} size="lg">
        <Modal.Header closeButton>
          <Modal.Title>Назовите сборку</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <NameForm setSetup={setSetupWithID} initList={[initItemList, setInitItemList]} />
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
export default ConfiguratorTable;
