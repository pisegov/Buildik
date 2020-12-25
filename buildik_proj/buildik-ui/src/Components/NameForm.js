import { useState } from 'react';
import axios from 'axios';
import Cookies from 'universal-cookie';

export default function NameForm({ setSetup, initList }) {
  const [name, setName] = useState('');

  const [initItemList, setInitItemList] = initList;

  const cookies = new Cookies();
  const csrftoken = cookies.get('csrftoken');

  const handleSubmit = e => {
    e.preventDefault();

    try {
      axios({
        method: 'POST',
        url: 'http://127.0.0.1:8000/api/setups/',
        headers: {
          'X-CSRFToken': csrftoken,
        },
        data: { name },
      }).then(res => {
        // Object.entries(initItemList).map(([key, value]) => {
        initItemList.map(pair => {
          axios({
            method: 'POST',
            url: 'http://127.0.0.1:8000/api/setups/setup_items/',
            headers: {
              'X-CSRFToken': csrftoken,
            },
            data: {
              setup: res.data.id,
              item: pair[0],
              number: pair[1],
            },
          }).then();
        });

        setInitItemList({});

        axios({
          method: 'GET',
          url: `http://127.0.0.1:8000/api/setups/${res.data.id}`,
        }).then(response => {
          setSetup(response.data);
        });
      });
    } catch (e) {
      console.log(`Error: ${e}`);
    }
  };

  return (
    <form onSubmit={e => handleSubmit(e)}>
      <label>
        Имя:
        <input type="text" value={name} onChange={e => setName(e.target.value)} />
      </label>
      <input type="submit" value="Отправить" />
    </form>
  );
}
