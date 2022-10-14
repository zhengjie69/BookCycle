import React, { useEffect, useState } from "react";
import { Col, Row, Container, Button } from "react-bootstrap";
import { useLocation, useNavigate } from "react-router-dom";
import { SearchBar } from "../components/SearchBar";


export default function ViewOffers() {
    const location = useLocation();
    const navigate = useNavigate();

    const userEmail = localStorage.getItem('Email');

    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [bookOffers, setBookOffers] = useState([]);

    useEffect(() => {
        fetch('/apis/user/get_book_offers?BookID=' + location.state.BookID + '&Email=' + userEmail)
            .then(res => res.json())
            .then(data => {
                setIsLoaded(true);
                setBookOffers(data);

            },
                (error) => {
                    setIsLoaded(true);
                    setError(error);
                }
            )
    }, [])

    return (
        <Container>
            <SearchBar />
            <div className="d-flex align-items-center justify-content-center mb-4">
                <img src={location.state.Image} className='img-fluid' alt={location.state.Title} />
            </div>
            <div className="d-flex align-items-center justify-content-center mb-4">
                <Row>
                    <h2>Offers for {location.state.Title}</h2>
                </Row>
            </div>
            <Row>
                <Col><h4>User</h4></Col>
                <Col><h4>Offer Price</h4></Col>
                <Col><h4>Book Offer Status</h4></Col>
                <Col></Col>
                <Col></Col>
            </Row>
            {bookOffers.map(bookOffers => (
                <Row>
                    <Col>
                        <p>{bookOffers.Username}</p>
                    </Col>
                    <Col>
                        <p>{bookOffers.OfferPrice}</p>
                    </Col>
                    <Col>
                        <p>{bookOffers.BookOfferStatus}</p>
                    </Col>
                    <Col>
                        <Button variant="primary">Accept</Button>
                    </Col>
                    <Col>
                        <Button variant="danger">Reject</Button>
                    </Col>
                </Row>
            ))}
        </Container>
    );
}