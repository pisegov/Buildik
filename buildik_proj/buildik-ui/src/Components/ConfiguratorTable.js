import React from 'react';
import { Button } from 'react-bootstrap';
import SelectionModal from './Modal/SelectionModal';

const styles = {
  ul: {
    listStyle: 'none',
    margin: 0,
    padding: 0,
  },
};

const configuratorCategory = ['cpu', 'motherboard', 'case', 'gpu', 'cpu_cooler', 'ram', 'storage', 'power_supply_unit'];

function ConfiguratorTable(props) {
  return (
    <>
      <ul style={styles.ul}>
        {configuratorCategory.map(category => {
          // return <SetupComponent category={category} />;
          return <SelectionModal category={category} />;
        })}
      </ul>
      <Button style={{ textAlign: 'right' }}>Save</Button>
    </>
  );
}
export default ConfiguratorTable;
