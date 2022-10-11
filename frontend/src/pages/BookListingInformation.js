import React from 'react'
import { Container } from 'react-bootstrap'
import { Row, Col, Button, Alert } from 'react-bootstrap'
import { useLocation, useNavigate } from 'react-router-dom'
import { LoginAlert } from '../components/LoginAlert'
import { SearchBar } from '../components/SearchBar'
import DeleteBookModal from '../components/DeleteBookModal'

function BookListingInformation() {
    const Authentication = localStorage.getItem('Authentication');
    const location = useLocation();
    const navigate = useNavigate();

    return (
        <Container>
            <SearchBar />
            <div className="d-flex align-items-center justify-content-center mb-4">
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
                        <Col style={{ justifyContent: 'end' }} md={{ span: 3, offset: 5 }} xs={5} className="mb-2 mt-2">
                            {location.state.Route === "MyListings" ? <Button onClick={() => {
                                navigate('/MyListings/EditListings', {
                                    state: {
                                        Title: location.state.Title,
                                        BookID: location.state.BookID,
                                        Price: location.state.Price,
                                        Genre: location.state.Genre,
                                        Image: location.state.Image,
                                        Location: location.state.Location,
                                        Description: location.state.Description,
                                        BookStatus: location.state.BookStatus,
                                        Condition: location.state.Condition
                                    }
                                });
                            }}>Edit Listings</Button> : null}
                            {location.state.Route !== "MyListings" && Authentication === "true" ? <Button variant='primary'> Offer</Button> : null}
                            {location.state.Route !== "MyListings" && Authentication === null ? <LoginAlert /> : null}
                        </Col>
                    </Row>
                    <Row className="mb-2 mt-2">
                        <Col md={4} xs={6} className="mb-2 mt-2">
                            <p>{location.state.Condition}</p>
                        </Col>
                        <Col style={{ justifyContent: 'end' }} md={{ span: 3, offset: 5 }} xs={5} className="mb-2 mt-2">
                            {location.state.Route === "MyListings" && Authentication === "true" ? <DeleteBookModal /> : null}
                        </Col>
                    </Row>
                    <Row className="mb-2 mt-2">
                        <h5>Description</h5>
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
                </table>
            </div>
        </Container >
    );
}

export default BookListingInformation;