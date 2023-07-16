import React, { useState } from 'react';
import { Form, Button, Container } from 'react-bootstrap';

const SearchForm = ({ handleSearch }) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [positiveKeywords, setPositiveKeywords] = useState('');
  const [negativeKeywords, setNegativeKeywords] = useState('');

  return (
    <Container className="my-5">
      <Form className="d-grid gap-2">
        <Form.Group className="mb-3">
          <Form.Label>Что ищите?</Form.Label>
          <Form.Control
            type="text"
            placeholder="Введите ваш запрос"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Позитивные кейворды:</Form.Label>
          <Form.Control
            type="text"
            placeholder="Введите позитивные кейворды"
            value={positiveKeywords}
            onChange={(e) => setPositiveKeywords(e.target.value)}
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Негативные кейворды:</Form.Label>
          <Form.Control
            type="text"
            placeholder="Введите негативные кейворды"
            value={negativeKeywords}
            onChange={(e) => setNegativeKeywords(e.target.value)}
          />
        </Form.Group>

        <Button className="mb-3" variant="outline-success" onClick={() => handleSearch(searchQuery, positiveKeywords, negativeKeywords)}>
          Search
        </Button>
      </Form>
    </Container>
  );
};

export default SearchForm;
