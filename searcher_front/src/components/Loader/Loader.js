import React from 'react';
import { Spinner, Container } from 'react-bootstrap';

const Loading = () => {
  return (
    <Container className="d-flex justify-content-center align-items-center">
      <Spinner animation="border" variant="primary" role="status">
        <span className="visually-hidden">Loading...</span>
      </Spinner>
    </Container>
  );
};

export default Loading;
