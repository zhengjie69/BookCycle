import React, { useState, useEffect } from 'react'
import { Container, Row } from 'react-bootstrap'
import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import 'bootstrap/dist/css/bootstrap.min.css';
import { LinkContainer } from 'react-router-bootstrap'
import { useNavigate } from 'react-router-dom';
import SessionTimeoutModal from '../../components/SessionTimeoutModal';
import secureLocalStorage from "react-secure-storage";

function MyListings() {

    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [items, setItems] = useState([]);
    const navigate = useNavigate();
    const userEmail = secureLocalStorage.getItem('Email');
    const Authentication = secureLocalStorage.getItem('Authentication');
    const Role = secureLocalStorage.getItem('Role');


    useEffect(() => {
        if (userEmail !== null && Authentication && Role === "User") {
            fetch('/apis/book/get_all_user_books?Email=' + userEmail)
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
        }
        else {
            return navigate('/');
        }
    }, [])

    return (
        <div className='mt-4 d-flex justify-content-center'>
            {Authentication ?
                <SessionTimeoutModal /> : null
            }
            <Container>
                <div className="d-flex justify-content-center">
                    <LinkContainer to="/MyListings/NewListings">
                        <Button> Create New Listings</Button>
                    </LinkContainer>
                </div>
                <div className='mb-4'>
                    <h3><b>My Listings</b></h3>
                </div>
                <div className="d-flex justify-content-center">
                    <Row>
                        {Array.isArray(items) ?
                            items.map(item => (
                                <div className="col-sm mb-2" key={item.BookID}>
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
                                                        ConditionID: item.BookConditionID,
                                                        Title: item.Title,
                                                        Price: item.Price,
                                                        Description: item.Description,
                                                        Image: item.Image,
                                                        Genre: item.Genre,
                                                        GenreID: item.GenreID,
                                                        Location: item.Location,
                                                        LocationID: item.LocationID,
                                                        BookStatus: item.BookStatus,
                                                        Route: "MyListings"
                                                    }
                                                });
                                            }}>View More</Button>
                                        </Card.Body>
                                    </Card>
                                </div>
                            )) : null
                        }
                    </Row>
                </div>
            </Container>
        </div>
    )
};

export default MyListings;