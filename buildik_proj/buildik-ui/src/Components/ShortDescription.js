import React from 'react';
import { shortStrings, Strings } from './Strings';

export default function ShortDescription({ component }) {
  return (
    <span className="shortDescr">
      <span>[</span>
      <span>
        {Object.entries(component).map(([key, value]) => {
          if (
            key !== 'image_url' &&
            key !== 'number' &&
            key !== 'id' &&
            key !== 'price' &&
            key !== 'manufacturer' &&
            key !== 'model' &&
            key !== 'category' &&
            key !== 'interfaces'
          )
            return <span>{`${Strings.get(key)}: ${value}, `}</span>;
        })}
      </span>
      <span>]</span>
    </span>
  );
}
