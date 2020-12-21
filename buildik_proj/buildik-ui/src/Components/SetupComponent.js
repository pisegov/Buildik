// import React, { useState, useEffect } from 'react';
import '../index.css';
import './SetupComponent.css';
import { Button } from 'react-bootstrap';

function SetupComponent({ category, component, deleteComponent, modalShow }) {
  const PrintComponent = ({ component, category }) => {
    if (component !== null) {
      return (
        <>
          {/* <p>{`Component id: ${component.id}`}</p> */}
          <div className="category-item-picture" data-role="configurator-product-image" data-icon-name={category}>
            <i />
          </div>
          <div className="category-item-data" data-role="configurator-product-data">
            <div className="not-empty-line">{`${category} ${component.name}`}</div>
            <div className="not-empty-line">
              {component.manufacturer} {component.model}
            </div>
            <div className="not-empty-line">Id: {component.id}</div>
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
          <span data-role="category-name">{category}</span>
        </p>
        <p className="configuration-message" />
      </div>

      <PrintComponent component={component} category={category} />
    </div>
  );
}

export default SetupComponent;
