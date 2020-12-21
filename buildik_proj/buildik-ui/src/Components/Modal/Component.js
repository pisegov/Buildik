import React from 'react';
import { number, string } from 'prop-types';

function Component(props) {
  return (
    <table
      // id="cfg-goods-345187"
      // cfg_id={345187}
      // cfg_group="chassis"
      // className="one-list-tovar cfg-goods"
      onClick={() => {
        props.chooseComponent(props.component);
        props.close();
      }}
      style={{
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '.5rem 1rem',
        border: '2px solid #ccc',
        borderRadius: '4px',
        marginBottom: '.5rem',
        height: '100px',
        width: '100%',
      }}
    >
      <tbody>
        <tr valign="top">
          <td className="x">{props.component.id}</td>
          <td className="goods-thumb">
            <div
              style={{
                width: '40px',
                height: '40px',
                // background: 'url(/cpreview40/shop/345187.jpg) no-repeat 0 0'
              }}
            ></div>
            <span className="mask"></span>
          </td>

          <td className="y">
            <a className="header title">{props.component.name}</a>
            <br />
            <span className="descr">{props.component.shortDescr}</span>
          </td>

          <td className="z">
            <div className="list-price">
              <span>{props.component.price}</span>
              руб.
              <br />
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  );
}

export default Component;
