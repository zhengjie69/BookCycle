import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Container, Row, Col, Button } from "react-bootstrap";
import EditOfferModal from "../components/EditOfferModal";
import DeleteOfferModal from "../components/DeleteOfferModal";

export default function MyOffers() {

    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [userOffers, setuserOffers] = useState([]);
    const navigate = useNavigate();
    const Authentication = localStorage.getItem('Authentication');
    var PendingList = [];
    var AcceptedList = [];
    var RejectedList = [];

    const userEmail = localStorage.getItem('Email');

    useEffect(() => {
        if (userEmail !== null && Authentication === "true") {
            fetch('/apis/user/get_all_user_book_offers?Email=' + userEmail)
                .then(res => res.json())
                .then(data => {
                    setIsLoaded(true);
                    setuserOffers(data);

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

    if (Array.isArray(userOffers)) {
        PendingList = userOffers.filter(userOffers => userOffers.BookOfferStatus === "Pending")
        AcceptedList = userOffers.filter(userOffers => userOffers.BookOfferStatus === "Accepted")
        RejectedList = userOffers.filter(userOffers => userOffers.BookOfferStatus === "Rejected")
    }

    return (
        <Container>
            <div className="d-flex align-items-center justify-content-center mb-4">
                <Row>
                    <h1>My Offers</h1>
                </Row>
            </div>
            <Row>
                <Col>
                    <p><b>Book Name</b></p>
                </Col>
                <Col>
                    <p><b>Price Offered</b></p>
                </Col>
                <Col>
                    <p><b>Book Offer Status</b></p>
                </Col>
                <Col></Col>
            </Row>
            {AcceptedList.length > 0 ?
                AcceptedList
                    .map(AcceptedOffers => (
                        <Row>
                            <Col>
                                <p>{AcceptedOffers.BookTitle}</p>
                            </Col>
                            <Col>
                                <p>{AcceptedOffers.OfferPrice !== 0 ? "$" + AcceptedOffers.OfferPrice : "Free"}</p>
                            </Col>
                            <Col>
                                <p>{AcceptedOffers.BookOfferStatus}</p>
                            </Col>
                            <Col>
                                <Button onClick={() => {
                                    navigate('/MyOffers/TransactionDetails', {
                                        state: {
                                            TransactionID: AcceptedOffers.TransactionID,
                                        }
                                    });
                                }}>Details</Button>
                            </Col>
                        </Row>
                    )) : null
                // <div className="d-flex align-items-center justify-content-center mb-4">
                //     <Row>
                //         <h3>No Offers</h3>
                //     </Row>
                // </div>
            }
            {PendingList.length > 0 ?
                PendingList
                    .map(PendingOffers => (
                        <Row>
                            <Col>
                                <p>{PendingOffers.BookTitle}</p>
                            </Col>
                            <Col>
                                <p>{PendingOffers.OfferPrice !== 0 ? "$" + PendingOffers.OfferPrice : "Free"}</p>
                            </Col>
                            <Col>
                                <p>{PendingOffers.BookOfferStatus}</p>
                            </Col>
                            <Col>
                                <EditOfferModal BookOfferID={PendingOffers.BookOfferID} BookOfferPrice={PendingOffers.OfferPrice} />
                                <DeleteOfferModal BookOfferID={PendingOffers.BookOfferID} />
                            </Col>
                        </Row>
                    )) : null
                // <div className="d-flex align-items-center justify-content-center mb-4">
                //     <Row>
                //         <h3>No Offers</h3>
                //     </Row>
                // </div>
            }
        </Container>
    );
}