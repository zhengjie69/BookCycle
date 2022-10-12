import React, { useState, useEffect } from "react";
import { Container, FloatingLabel, Button } from "react-bootstrap";
import { useLocation, useNavigate } from 'react-router-dom'
import { Form } from "react-bootstrap";


export default function EditListings() {

    const itemLocation = useLocation();
    const navigate = useNavigate();

    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);

    const [GenreDropdown, setGenreDropdown] = useState([]);
    const [LocationDropdown, setLocationDropdown] = useState([]);
    const [ConditionDropdown, setConditionDropdown] = useState([]);

    const [BookTitle, setBookTitle] = useState(itemLocation.state.Title);
    const [Price, setPrice] = useState(itemLocation.state.Price);
    const [Description, setDescription] = useState(itemLocation.state.Description);
    const [Condition, setCondition] = useState(itemLocation.state.Condition);

    const [Genre, setGenre] = useState(itemLocation.state.Genre);
    const userEmail = localStorage.getItem('Email');
    const [Location, setLocation] = useState(itemLocation.state.Location);

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    let errors = [];

    const EditListingFormData = new FormData();

    const uploadedImage = (e) => {

        console.log(e.target.files[0]);
        EditListingFormData.append('Image', e.target.files[0]);
        console.log(EditListingFormData);
    };

    useEffect(() => {
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
                setConditionDropdown(data);
            },
                (error) => {
                    setIsLoaded(true);
                    setError(error);
                }
            )
    }, [])

    const postEditListings = async (e) => {

        e.preventDefault();

        /* Title: location.state.Title,
            BookID: location.state.BookID,
            Price: location.state.Price,
            Genre: location.state.Genre,
            Image: location.state.Image,
            Location: location.state.Location,
            Description: location.state.Description,
            BookStatus: location.state.BookStatus */

        console.log(BookTitle);
        console.log(Genre);
        console.log(Condition);
        console.log(Price);
        console.log(Description);
        console.log(itemLocation.state.Image);
        console.log(itemLocation.state.BookID);
        console.log(Location);
    }
    return (
        <Container>
            <div className="d-flex justify-content-center">
                <h1>Edit Listing</h1>
            </div>
            <div className="d-flex justify-content-center">
                <Form onSubmit={postEditListings}>
                    <Form.Group className="mb-3" controlId="formBookName" >
                        <Form.Label>Book Title:</Form.Label>
                        <Form.Control required type="text" placeholder="Enter book name" value={BookTitle} onChange={e => setBookTitle(e.target.value)} />
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formGenre" value={Genre} onChange={e => setGenre(e.target.value)}>
                        <Form.Label>Genre:</Form.Label>
                        <Form.Select required aria-label="Floating label select condition">
                            {Array.isArray(GenreDropdown) ?
                                GenreDropdown
                                    .filter(GenreDropdown => GenreDropdown.GenreName === Genre)
                                    .map(FilteredGenreDropdown => (
                                        <option value={FilteredGenreDropdown.GenreID}>{FilteredGenreDropdown.GenreName}</option>)) : null
                            }
                            {Array.isArray(GenreDropdown) ?
                                GenreDropdown
                                    .filter(GenreDropdown => GenreDropdown.GenreName !== Genre)
                                    .map(FilteredGenreDropdown => (
                                        <option value={FilteredGenreDropdown.GenreID}>{FilteredGenreDropdown.GenreName}</option>)) : null
                            }
                        </Form.Select>
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formCondition" value={Condition} onChange={(e) => setCondition(e.target.value)}>
                        <Form.Label controlId="floatingSelectCondition" label="Book Condition">Book Condition:</Form.Label>
                        <Form.Select required aria-label="Floating label select condition" >
                            {Array.isArray(ConditionDropdown) ?
                                ConditionDropdown
                                    .filter(ConditionDropdown => ConditionDropdown.BookConditionName === itemLocation.state.Condition)
                                    .map(FilteredConditionDropdown => (
                                        <option value={FilteredConditionDropdown.BookConditionID}>{FilteredConditionDropdown.BookConditionName}</option>)) : null
                            }
                            {Array.isArray(ConditionDropdown) ?
                                ConditionDropdown
                                    .filter(ConditionDropdown => ConditionDropdown.BookConditionName !== Condition)
                                    .map(FilteredConditionDropdown => (
                                        <option value={FilteredConditionDropdown.BookConditionID}>{FilteredConditionDropdown.BookConditionName}</option>)) : null
                            }
                        </Form.Select>
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formBookPrice" >
                        <Form.Label>Book Price:</Form.Label>
                        <Form.Control required type="number" placeholder="Enter book price" value={Price} onChange={e => setPrice(e.target.value)} />
                        <Form.Text className="text-muted">
                            Enter 0 if you wish to gift the book.
                        </Form.Text>
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formBookDescription">
                        <Form.Label>Book Description:</Form.Label>
                        <Form.Control required as="textarea" rows={3} value={Description} onChange={e => setDescription(e.target.value)} />
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formBookImage">
                        <Form.Label>Book Image: </Form.Label>
                        <Form.Control type="file" onChange={e => uploadedImage(e)} />
                        <Form.Text className="text-muted">Upload Profile Picture (image format must be png, jpg, or jpeg).</Form.Text>
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formLocation" value={Location} onChange={e => setLocation(e.target.value)}>
                        <FloatingLabel controlId="floatingSelectLocation" label="Location">
                            <Form.Select aria-label="Floating label select location" >
                                {Array.isArray(LocationDropdown) ?
                                    LocationDropdown
                                        .filter(LocationDropdown => LocationDropdown.LocationName === Location)
                                        .map(LocationDropdown => (
                                            <option value={LocationDropdown.LocationID}>{LocationDropdown.LocationName}</option>)) : null
                                }
                                {Array.isArray(LocationDropdown) ?
                                    LocationDropdown
                                        .filter(LocationDropdown => LocationDropdown.LocationName !== Location)
                                        .map(LocationDropdown => (
                                            <option value={LocationDropdown.LocationID}>{LocationDropdown.LocationName}</option>)) : null
                                }
                            </Form.Select>
                        </FloatingLabel>
                    </Form.Group>
                    <div className="d-flex justify-content-center mb-3">
                        {showErrors ? errorMessages.map((item, index) => {
                            return <ul key={index}>{item}</ul>;
                        }) : null}
                    </div>
                    <div className="d-flex justify-content-center mb-3">
                        <Button variant="primary" type="submit">
                            Update
                        </Button>
                    </div>
                </Form>
            </div>
        </Container>
    )
}