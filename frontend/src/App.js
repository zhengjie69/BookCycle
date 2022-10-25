import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Container } from 'react-bootstrap';
import { Row, Button, Card } from 'react-bootstrap';
import { SearchBar } from './components/SearchBar';
import { renderMatches, useNavigate } from 'react-router-dom';
import SessionTimeoutModal from './components/SessionTimeoutModal';

function App() {

  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);
  const navigate = useNavigate();
  const userEmail = localStorage.getItem('Email');
  const Authentication = localStorage.getItem('Authentication');

  useEffect(() => {
    fetch('/apis/book/search_book?Email=' + userEmail)
      .then(res => res.json())
      .then(data => {
        setIsLoaded(true);
        setItems(data);

      },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
  }, [])

  function bookByCategories(BookGenre) {
    return (
      <>
        <div className="col d-flex justify-content-start mb-2">
          <Row><h3><b>{BookGenre}</b></h3></Row>
        </div>
        <div className="d-flex justify-content-center">
          <Row xs="auto">
            {items.map(item => (
              <div className="col-sm mb-2" key={item.BookID}>
                {item.Genre === BookGenre ?
                  <Card style={{ width: '15rem', height: '28rem' }}>
                    <Card.Img variant="top" src={item.Image} style={{ height: '15rem' }} />
                    <Card.Body>
                      <Card.Title>{item.Title}</Card.Title>
                      {item.Price === 0 ? <Card.Text>Free</Card.Text> : null}
                      {item.Price > 0 ? <Card.Text>${item.Price}</Card.Text> : null}
                      <Card.Text>{item.BookCondition}</Card.Text>
                      <Button onClick={() => {
                        navigate('/BookListingInformation', {
                          state: {
                            BookID: item.BookID,
                            Condition: item.BookCondition,
                            Title: item.Title,
                            Price: item.Price,
                            Description: item.Description,
                            Image: item.Image,
                            Genre: item.Genre,
                            Location: item.Location,
                            Route: "Home"
                          }
                        });
                      }}>View More</Button>
                    </Card.Body>
                  </Card> : null}
              </div>
            ))}
          </Row>
        </div>
      </>
    )
  }


  return (
    <div className="App">
      <header className="App-header">
        <Container>
          <SearchBar />
          {Authentication === "true" ?
            <SessionTimeoutModal /> : null
          }
          {bookByCategories("Fiction")}
          {bookByCategories("Non-Fiction")}
          {bookByCategories("Mystery")}
        </Container>
      </header>
    </div>
  );
}

export default App;
