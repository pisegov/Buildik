import React from 'react';
import ShortDescription from '../ShortDescription';

function Component({ component, chooseComponent, close }) {
  return (
    <table
      onClick={() => {
        chooseComponent(component);
        close();
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
          <td className="x">{component.id}</td>
          <td className="goods-thumb">
            <div
              style={{
                width: '80px',
                height: '80px',
                backgroundImage: `url("${component.image_url}")`,
                backgroundPosition: 'center',
                backgroundSize: '100% auto',
                backgroundRepeat: 'no-repeat',
                color: 'white',
              }}
            >
              <i />
            </div>
            <span className="mask"></span>
          </td>

          <td className="y">
            <a className="header title">
              {component.manufacturer} {component.model}
            </a>
            <br />
            <ShortDescription component={component} />
          </td>

          <td className="z">
            <div className="list-price">
              <span>{component.price}</span>
              <br />
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  );
}

export default Component;
