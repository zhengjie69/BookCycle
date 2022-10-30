import React from 'react'
import { Container } from 'react-bootstrap'
import { Row, Col, Button } from 'react-bootstrap'
import { useLocation, useNavigate } from 'react-router-dom'
import { LoginAlert } from '../components/LoginAlert'
import { SearchBar } from '../components/SearchBar'
import DeleteBookModal from '../components/DeleteBookModal'
import OfferBookModal from '../components/OfferBookModal'
import SessionTimeoutModal from '../components/SessionTimeoutModal'
import AdminDeleteBookModal from '../components/AdminDeleteBookModal'
import secureLocalStorage from "react-secure-storage";

function BookListingInformation() {
    const Authentication = secureLocalStorage.getItem('Authentication');
    const Role = secureLocalStorage.getItem('Role');
    const location = useLocation();
    const navigate = useNavigate();

    return (
        <Container>
            {Authentication ?
                <SessionTimeoutModal /> : null
            }
            {location.state.Route !== "MyListings" && Authentication && Role === "User" ?
                <SearchBar /> : null
            }
            <div className="d-flex align-items-center justify-content-center mb-4 mt-4">
                <img src={location.state.Image} className='img-fluid' alt={location.state.Title} />
            </div>
            <div className="row justify-content-center">
                <table className="ms-3">
                    <Row>
                        <Col className="mb-2 mt-2"><h4><b>{location.state.Title}</b></h4></Col>
                        {/* <Col md={{ span: 3, offset: 5 }} xs={5} className="mb-2 mt-2">Shawn</Col> */}
                    </Row>
                    <Row>
                        <Col md={4} xs={6} className="mb-2 mt-2">
                            {location.state.Price === 0 ? "Free" : null}
                            {location.state.Price > 0 ? "$" + location.state.Price : null}
                        </Col>
                        <Col md={{ span: 3, offset: 5 }} xs={5} className="mb-2 mt-2">
                            {location.state.Route === "MyListings" && Authentication && Role === "User" && location.state.BookStatus === "Available" ?
                                <Button onClick={() => {
                                    navigate('/MyListings/ViewOffers', {
                                        state: {
                                            Title: location.state.Title,
                                            BookID: location.state.BookID,
                                            Image: location.state.Image,
                                        }
                                    });
                                }}>View Offers</Button> : <b>{location.state.BookStatus}</b>}
                            {location.state.Route !== "MyListings" && Authentication && Role === "User" ?
                                <OfferBookModal /> : null
                            }
                            {location.state.Route !== "MyListings" && !Authentication ?
                                <LoginAlert /> : null
                            }
                        </Col>
                    </Row>
                    <Row className="mb-2 mt-2">
                        <Col md={4} xs={6} className="mb-2 mt-2">
                            <p>{location.state.Condition}</p>
                        </Col>
                        <Col md={{ span: 3, offset: 5 }} xs={5} className="mb-2 mt-2">
                            {location.state.Route === "MyListings" && location.state.BookStatus === "Available" && Authentication && Role === "User" ?
                                <Button onClick={() => {
                                    navigate('/MyListings/EditListings', {
                                        state: {
                                            Title: location.state.Title,
                                            BookID: location.state.BookID,
                                            Price: location.state.Price,
                                            Genre: location.state.Genre,
                                            GenreID: location.state.GenreID,
                                            Image: location.state.Image,
                                            Location: location.state.Location,
                                            LocationID: location.state.LocationID,
                                            Description: location.state.Description,
                                            BookStatus: location.state.BookStatus,
                                            Condition: location.state.Condition,
                                            ConditionID: location.state.ConditionID
                                        }
                                    });
                                }}>Edit Listings</Button> : null}
                        </Col>
                    </Row>
                    <Row className="mb-2 mt-2">
                        <Col>
                            <h5>Description</h5>
                        </Col>
                    </Row>
                    <Row>
                        <p>{location.state.Description}</p>
                    </Row>
                    <Row className="mb-2 mt-4">
                        <h5>
                            Location
                        </h5>
                    </Row>
                    <Row className="mb-2 mt-2">
                        <p>
                            <span className="material-symbols-outlined">
                                location_on
                            </span>
                            {location.state.Location}
                        </p>
                    </Row>
                    <Row>
                        <Col md={{ span: 3, offset: 5 }} xs={10} className="mb-2 mt-2">
                            {location.state.Route === "MyListings" && Authentication && Role === "User" ? <DeleteBookModal /> : null}
                        </Col>
                        <Col md={{ span: 3, offset: 5 }} xs={10} className="mb-2 mt-2">
                            {location.state.Route === "ManageBooksResult" && Authentication && Role === "Admin" ? <AdminDeleteBookModal /> : null}
                        </Col>
                    </Row>
                </table>
            </div>
        </Container >
    );
}

export default BookListingInformation;