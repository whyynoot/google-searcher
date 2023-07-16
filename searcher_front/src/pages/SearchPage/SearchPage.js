import React, { useState } from 'react';
import { Container } from 'react-bootstrap';
import ResultTable from '../../components/ResultTable/ResulTable';
import SearchForm from '../../components/Searcher/Searcher';
import Loading from '../../components/Loader/Loader';

const SearchPage = () => {
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState([]);
    const [status, setStatus] = useState('');
  
    const handleSearch = async (searchQuery, positiveKeywords, negativeKeywords) => {
        setLoading(true);
        const requestData = {
          query: searchQuery,
          positive: positiveKeywords,
          negative: negativeKeywords,
        };
      
        try {
          const response = await fetch('/api/create_task/', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData),
          });
      
          const { id: taskUUID } = await response.json();
      
          let currentStatus = 'working';
          while (currentStatus !== 'done' || currentStatus !== "failed") {
            await new Promise((resolve) => setTimeout(resolve, 5000));
            const statusResponse = await fetch(`/api/check_for_task/${taskUUID}/`);
            const { status, result } = await statusResponse.json();
            currentStatus = status;
      
            if (currentStatus === 'done') {
              setResults(result);
              setStatus(currentStatus);
              break;
            }
            if (currentStatus === "failed"){
                setResults(result);
                setStatus(currentStatus);
            }
          }
        } catch (error) {
          console.error('Error:', error);
        }
      
        setLoading(false);
    };
  
    return (
      <Container className="my-5">
        <SearchForm handleSearch={handleSearch} />
  
        {loading ? <Loading /> : null}
  
        {status === 'done' && results.length > 0 && <ResultTable results={results} />}
      </Container>
    );
  };
  
export default SearchPage;