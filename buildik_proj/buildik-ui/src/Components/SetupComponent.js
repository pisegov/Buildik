// import React, { useState, useEffect } from 'react';
import '../index.css';
import './SetupComponent.css';
import { Button } from 'react-bootstrap';
import { Strings } from './Strings';
import ShortDescription from './ShortDescription';

function SetupComponent({ category, component, deleteComponent, modalShow }) {
  const PrintComponent = () => {
    if (component !== null) {
      return (
        <>
          {/* <p>{`Component id: ${component.id}`}</p> */}
          <div className="category-item-picture" data-role="configurator-product-image" data-icon-name={category}>
            <i />
          </div>
          <div className="category-item-data" data-role="configurator-product-data">
            <div className="not-empty-line">{`${Strings.get(category)} ${component.manufacturer} ${
              component.model
            }`}</div>
            <div className="not-empty-line">{<ShortDescription component={component} />}</div>
          </div>
          <div className="category-item-price">
            <div className="price">
              <strong>{component.price}</strong>
            </div>
          </div>

          <div className="category-controls" data-role="configurator-controls">
            <Button data-role="show-catalog" variant="primary" onClick={modalShow}>
              Change
            </Button>
            {'  '}
            <Button
              variant="primary"
              onClick={() => {
                deleteComponent(component);
              }}
            >
              Remove
            </Button>
          </div>
        </>
      );
    } else {
      return (
        <>
          <div className="category-item-picture" data-role="configurator-product-image" data-icon-name={category}>
            <i />
          </div>
          <div className="category-item-data" data-role="configurator-product-data">
            <div className="empty-line" />
            <div className="empty-line" />
            <div className="empty-line" />
            <div className="empty-line" />
          </div>

          <div className="category-controls" data-role="configurator-controls">
            <Button className="btn btn-default btn-add" data-role="show-catalog" variant="primary" onClick={modalShow}>
              Add
            </Button>
          </div>
        </>
      );
    }
  };

  return (
    <div className="configurator-category-data">
      <div className="compatibility-status" data-role="compatibility-status-icon"></div>
      <div className="category-name">
        <p>
          <span data-role="category-name">{Strings.get(category)}</span>
        </p>
        <p className="configuration-message" />
      </div>

      <PrintComponent />
    </div>
  );
}

export default SetupComponent;
