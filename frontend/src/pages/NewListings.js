import React, { useState, useEffect } from 'react'
import { Container, Form, Button, FloatingLabel, InputGroup } from 'react-bootstrap'
import { useNavigate } from 'react-router-dom';

export default function NewListings() {

    const navigate = useNavigate();
    const Authentication = localStorage.getItem('Authentication');
    const Role = localStorage.getItem('Role');

    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const [genreDropdown, setGenreDropdown] = useState([]);
    const [locationDropdown, setLocationDropdown] = useState([]);
    const [bookConditionDropdown, setBookConditionDropdown] = useState([]);

    const [BookTitle, setBookTitle] = useState();
    const [Price, setPrice] = useState();
    const [Description, setDescription] = useState();
    const [Condition, setCondition] = useState('1');
    const [GenreID, setGenreID] = useState('1');
    const userEmail = localStorage.getItem('Email');
    const [LocationID, setLocationID] = useState('1');

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    let errors = [];


    const NewListingsFormData = new FormData();

    useEffect(() => {
        if (Authentication === "true" && Role === "User") {
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

    const uploadedImage = (e) => {
        console.log(e.target.files[0]);
        NewListingsFormData.append('Image', e.target.files[0]);
        console.log(NewListingsFormData);
    };

    const postNewListings = async (e) => {

        e.preventDefault();

        console.log(Price);
        console.log(BookTitle);
        console.log(Description);
        console.log(GenreID);
        console.log(LocationID);
        console.log(Condition);

        NewListingsFormData.append("Price", Price);
        NewListingsFormData.append("Title", BookTitle);
        NewListingsFormData.append("Description", Description);
        NewListingsFormData.append("GenreID", GenreID);
        NewListingsFormData.append("Email", userEmail);
        NewListingsFormData.append("LocationID", LocationID);
        NewListingsFormData.append("BookConditionID", Condition);

        const res = await fetch('/apis/book/create_book', {
            method: "POST",
            body: NewListingsFormData
        });

        const data = await res.json();

        const trimmedResponseMessage = JSON.stringify(data).replace(/[^a-zA-Z ]/g, "");

        if (res.status === 201) {
            console.log(trimmedResponseMessage);
            navigate('/');
            window.location.reload(false);
        }
        else {
            console.log(trimmedResponseMessage);
            errors.push(trimmedResponseMessage);
            setShowErrors({ showErrors: true });
            setErrorMessages(errors);
        }
    }

    return (
        <div className="mt-4">
            <Container>
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
                                        <option value={genreDropdown.GenreID}>{genreDropdown.GenreName}</option>)) : null
                                }
                            </Form.Select>
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="formBookCondition" value={Condition} onChange={e => setCondition(e.target.value)}>
                            <Form.Label>Book Condition:</Form.Label>
                            <Form.Select aria-label="Floating label select location" >
                                {Array.isArray(bookConditionDropdown) ?
                                    bookConditionDropdown.map(bookConditionDropdown => (
                                        <option value={bookConditionDropdown.BookConditionID}>{bookConditionDropdown.BookConditionName}</option>)) : null
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
                            <Form.Control required type="file" onChange={e => uploadedImage(e)} />
                            <Form.Text className="text-muted">Upload Profile Picture (image format must be png, jpg, or jpeg).</Form.Text>
                        </Form.Group>
                        <Form.Group className="mb-3" controlId="formLocation" value={LocationID} onChange={e => setLocationID(e.target.value)}>
                            <FloatingLabel controlId="floatingSelectLocation" label="Location">
                                <Form.Select aria-label="Floating label select location" >
                                    {Array.isArray(locationDropdown) ?
                                        locationDropdown.map(locationDropdown => (
                                            <option value={locationDropdown.LocationID}>{locationDropdown.LocationName}</option>)) : null
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
                                Upload
                            </Button>
                        </div>
                    </Form>
                </div>
            </Container>
        </div>
    );
}