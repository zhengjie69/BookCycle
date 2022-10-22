import React, { useEffect, useState } from "react";
import { Col, Row, Container } from "react-bootstrap";
import { useLocation, useNavigate } from "react-router-dom";
import AcceptOfferModal from "../components/AcceptOfferModal";

export default function ViewOffers() {
    const location = useLocation();
    const navigate = useNavigate();
    const Authentication = localStorage.getItem('Authentication');
    const Role = localStorage.getItem('Role');

    const userEmail = localStorage.getItem('Email');

    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [bookOffers, setBookOffers] = useState([]);
    var ListOfPending = [];
    var ListOfAccepted = [];

    useEffect(() => {
        if (Authentication === 'true' && Role === "User") {
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
        }

        else {
            return navigate('/');
        }
    }, [])

    if (Array.isArray(bookOffers)) {
        ListOfPending = bookOffers.filter(bookOffers => bookOffers.BookOfferStatus === "Pending")
        ListOfAccepted = bookOffers.filter(bookOffers => bookOffers.BookOfferStatus === "Accepted")
    }

    return (
        <Container>
            {bookOffers.length !== 0 ?
                <>
                    <div className="d-flex align-items-center justify-content-center mb-4 mt-4">
                        <Row>
                            <h2>Offers for "{location.state.Title}"</h2>
                        </Row>
                    </div>
                    <div className="d-flex align-items-center justify-content-center mb-4">
                        <img src={location.state.Image} className='img-fluid' alt={location.state.Title} />
                    </div>
                </> : null}
            <Row>
                <Col><h4>User</h4></Col>
                <Col><h4>Offer Price</h4></Col>
                <Col><h4>Book Offer Status</h4></Col>
                <Col></Col>
            </Row>
            {/* if there is accepted offer */}
            {ListOfAccepted.length > 0 ?
                ListOfAccepted
                    .map(AcceptedBookOffers => (
                        <Row>
                            <Col>
                                <p>{AcceptedBookOffers.Username}</p>
                            </Col>
                            <Col>
                                <p>{AcceptedBookOffers.OfferPrice}</p>
                            </Col>
                            <Col>
                                <p>{AcceptedBookOffers.BookOfferStatus}</p>
                            </Col>
                            <Col>
                            </Col>
                        </Row>
                    )) : null}
            {ListOfAccepted.length === 0 && ListOfPending.length === 0 ?
                <div className="d-flex align-items-center justify-content-center mt-4">
                    <h4>No Offers</h4>
                </div> : null
            }
            {/* if there is no accepted offers */}
            {ListOfAccepted.length === 0 ?
                ListOfPending
                    .map(bookOffers => (
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
                                {bookOffers.BookOfferStatus === "Pending" ?
                                    <AcceptOfferModal BookOfferID={bookOffers.BookOfferID} /> : null
                                }
                            </Col>
                        </Row>
                    )) : null}
        </Container>
    );
}