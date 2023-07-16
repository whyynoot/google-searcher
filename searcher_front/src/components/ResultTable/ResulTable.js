import React from 'react';
import { Table, Image } from 'react-bootstrap';

const ResultTable = ({ results }) => {
  return (
    <Table striped bordered hover responsive>
      <colgroup>
        <col style={{ width: '20%' }} /> 
        <col style={{ width: '20%' }} /> 
        <col style={{ width: '20%' }} /> 
        <col style={{ width: '20%' }} /> 
        <col style={{ width: '20%' }} />
      </colgroup>
      <thead>
        <tr>
          <th className="text-center">
              URL
          </th>
          <th className="text-center">Photo</th>
          <th className="text-center">Region</th>
          <th className="text-center">Relevance</th>
          <th className="text-center">Content Analysis</th>
        </tr>
      </thead>
      <tbody>
        {results.map((result, index) => (
          <tr key={index}>
            <td style={{ maxWidth: '100px' }}>
              <a href={result.url} target="_blank" rel="noopener noreferrer" style={{ wordWrap: 'break-word' }}>
                {result.url}
              </a>
            </td>
            <td>
              {result.photo && (
                <Image src={result.photo} alt="error loading or getting photo" style={{ maxWidth: '100px' }} />
              )}
            </td>
            <td>{result.region}</td>
            <td>{result.relevance}</td>
            <td>{result.content_analysis}</td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

export default ResultTable;