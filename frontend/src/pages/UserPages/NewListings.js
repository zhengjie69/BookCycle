import React, { useState, useEffect } from 'react'
import { Container, Form, Button, Row } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom';
import SessionTimeoutModal from '../../components/SessionTimeoutModal';
import secureLocalStorage from "react-secure-storage";

export default function NewListings() {

    const navigate = useNavigate();
    const Authentication = secureLocalStorage.getItem('Authentication');
    const Role = secureLocalStorage.getItem('Role');
    const userEmail = secureLocalStorage.getItem('Email');

    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [genreDropdown, setGenreDropdown] = useState([]);
    const [locationDropdown, setLocationDropdown] = useState([]);
    const [bookConditionDropdown, setBookConditionDropdown] = useState([]);
    const [bookImage, setBookImage] = useState([]);

    const [BookTitle, setBookTitle] = useState();
    const [Price, setPrice] = useState();
    const [Description, setDescription] = useState();
    const [Condition, setCondition] = useState('');
    const [GenreID, setGenreID] = useState('');
    const [LocationID, setLocationID] = useState('');

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    let errors = [];


    const NewListingsFormData = new FormData();

    useEffect(() => {
        if (Authentication && Role === "User") {

            setGenreID('1');
            setCondition('1');
            setLocationID('1');

            fetch('/apis/book/get_all_genres')
                .then(res => res.json())
                .then(data => {
                    setIsLoaded(true);
                    setGenreDropdown(data);
                },
                    (error) => {
                        setIsLoaded(true);
                        setError(error);
                    }
                )

            fetch('/apis/book/get_all_locations')
                .then(res => res.json())
                .then(data => {
                    setIsLoaded(true);
                    setLocationDropdown(data);
                },
                    (error) => {
                        setIsLoaded(true);
                        setError(error);
                    }
                )

            fetch('/apis/book/get_all_book_conditions')
                .then(res => res.json())
                .then(data => {
                    setIsLoaded(true);
                    setBookConditionDropdown(data);
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

    const postNewListings = async (e) => {

        e.preventDefault();

        NewListingsFormData.append("Price", Price);
        NewListingsFormData.append("Title", BookTitle);
        NewListingsFormData.append("Description", Description);
        NewListingsFormData.append("GenreID", GenreID);
        NewListingsFormData.append("Email", userEmail);
        NewListingsFormData.append("LocationID", LocationID);
        NewListingsFormData.append("BookConditionID", Condition);
        NewListingsFormData.append("Image", bookImage);

        const res = await fetch('/apis/book/create_book', {
            method: "POST",
            body: NewListingsFormData
        });

        for (var pair of NewListingsFormData.entries()) {
            console.log(`${pair[0]}: ${pair[1]}`);
        }

        const data = await res.json();

        const trimmedResponseMessage = JSON.stringify(data).replace(/[^a-zA-Z ]/g, "");

        if (trimmedResponseMessage === "Successfully logged out") {
            navigate('/MyListings');
            window.location.reload(false);
        }
        else {
            errors.push(trimmedResponseMessage);
            setShowErrors({ showErrors: true });
            setErrorMessages(errors);
        }
    }

    return (
        <div className="mt-4">
            <Container>
                {Authentication ?
                    <SessionTimeoutModal /> : null
                }
                <div className="d-flex justify-content-center">
                    <h1>New Listings</h1>
                </div>
                <div className="d-flex justify-content-center">
                    <Form onSubmit={postNewListings}>
                        <Form.Group className="mb-3" controlId="formBookName" value={BookTitle} onChange={e => setBookTitle(e.target.value)}>
                            <Form.Label>Book Title:</Form.Label>
                            <Form.Control required type="text" placeholder="Enter book name" />
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="formGenre" value={GenreID} onChange={e => setGenreID(e.target.value)}>
                            <Form.Label>Genre:</Form.Label>
                            <Form.Select required aria-label="Floating label select condition" >
                                {Array.isArray(genreDropdown) ?
                                    genreDropdown.map(genreDropdown => (
                                        <option value={genreDropdown.GenreID.toString()}>{genreDropdown.GenreName}</option>)) : null
                                }
                            </Form.Select>
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="formBookCondition" value={Condition} onChange={e => setCondition(e.target.value)}>
                            <Form.Label>Book Condition:</Form.Label>
                            <Form.Select aria-label="Floating label select location" >
                                {Array.isArray(bookConditionDropdown) ?
                                    bookConditionDropdown.map(bookConditionDropdown => (
                                        <option value={bookConditionDropdown.BookConditionID.toString()}>{bookConditionDropdown.BookConditionName}</option>)) : null
                                }
                            </Form.Select>
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="formBookPrice" value={Price} onChange={e => setPrice(e.target.value)}>
                            <Form.Label>Book Price:</Form.Label>
                            <Form.Control required type="number" placeholder="Enter book price" />
                            <Form.Text className="text-muted">
                                Enter 0 if you wish to gift the book.
                            </Form.Text>
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="formBookDescription" value={Description} onChange={e => setDescription(e.target.value)}>
                            <Form.Label>Book Description:</Form.Label>
                            <Form.Control required as="textarea" rows={3} />
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="formBookImage">
                            <Form.Label>Book Image: </Form.Label>
                            <Form.Control required type="file" onChange={e => setBookImage(e.target.files[0])} />
                            <Form.Text className="text-muted">Image format must be png, jpg, or jpeg.</Form.Text>
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="formLocation" value={LocationID} onChange={e => setLocationID(e.target.value)}>
                            <Form.Label>Location:</Form.Label>
                            <Form.Select aria-label="Floating label select location" >
                                {Array.isArray(locationDropdown) ?
                                    locationDropdown.map(locationDropdown => (
                                        <option value={locationDropdown.LocationID.toString()}>{locationDropdown.LocationName}</option>)) : null
                                }
                            </Form.Select>
                        </Form.Group>
                        <div className="d-flex justify-content-center mb-3">
                            <Row>
                                {showErrors ? errorMessages.map((item, index) => {
                                    return <ul key={index}>{item}</ul>;
                                }) : null}
                            </Row>
                        </div>
                        <div className="d-flex justify-content-center mb-3">
                            <Button variant="primary" type="submit">
                                Upload
                            </Button>
                        </div>
                    </Form>
                </div>
            </Container>
        </div>
    );
}