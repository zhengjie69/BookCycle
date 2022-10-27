import React, { useEffect, useState } from "react";
import { Container, Card, Button, Row } from "react-bootstrap";
import { useLocation, useNavigate } from "react-router-dom";
import SessionTimeoutModal from "../../components/SessionTimeoutModal";

export default function ManageBooksResult() {
    const location = useLocation();
    const navigate = useNavigate();

    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [userBooks, setUserBooks] = useState([]);

    const adminEmail = localStorage.getItem('Email');
    const Authentication = localStorage.getItem('Authentication');
    const Role = localStorage.getItem('Role');

    const [Username, setUsername] = useState();


    useEffect(() => {
        if (adminEmail !== null && Authentication === "true" && Role === "Admin") {

            setUsername(location.state.Username);

            fetch('/apis/book/get_all_user_books?Email=' + location.state.UserEmail)
                .then(res => res.json())
                .then(data => {
                    setIsLoaded(true);
                    setUserBooks(data);
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
            {Authentication === "true" ?
                <SessionTimeoutModal /> : null
            }
            <Container>
                <div className='d-flex justify-content-center mb-4'>
                    <h1>{Username}'s Books</h1>
                </div>
                <div className="d-flex justify-content-center">
                    <Row>
                        {Array.isArray(userBooks) ?
                            userBooks.map(item => (
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
                                                        Username: location.state.Username,
                                                        UserEmail: location.state.UserEmail,
                                                        BookID: item.BookID,
                                                        Condition: item.BookCondition,
                                                        Title: item.Title,
                                                        Price: item.Price,
                                                        Description: item.Description,
                                                        Image: item.Image,
                                                        Genre: item.Genre,
                                                        Location: item.Location,
                                                        BookStatus: item.BookStatus,
                                                        Route: "ManageBooksResult"
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
}