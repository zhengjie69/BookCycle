import React, { useState, useEffect } from "react";
import { Container, FloatingLabel, Button, Form, Row } from "react-bootstrap";
import { useLocation, useNavigate } from 'react-router-dom'
import SessionTimeoutModal from "../../components/SessionTimeoutModal";
import secureLocalStorage from "react-secure-storage";


export default function EditListings() {

    const itemLocation = useLocation();
    const navigate = useNavigate();
    const Authentication = secureLocalStorage.getItem('Authentication');
    const Role = secureLocalStorage.getItem('Role');

    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);

    const [GenreDropdown, setGenreDropdown] = useState([]);
    const [LocationDropdown, setLocationDropdown] = useState([]);
    const [ConditionDropdown, setConditionDropdown] = useState([]);

    const [BookID, setBookID] = useState();
    const [BookTitle, setBookTitle] = useState();
    const [Genre, setGenre] = useState();
    const [Location, setLocation] = useState();
    const [Price, setPrice] = useState();
    const [Description, setDescription] = useState();
    const [Condition, setCondition] = useState();
    const [BookImage, setBookImage] = useState();

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    let errors = [];

    const EditListingFormData = new FormData();

    useEffect(() => {
        if (Authentication && Role === "User") {

            setBookID(itemLocation.state.BookID.toString());
            setBookTitle(itemLocation.state.Title);
            setPrice(itemLocation.state.Price.toString());
            setDescription(itemLocation.state.Description);
            setCondition(itemLocation.state.ConditionID.toString());
            setGenre(itemLocation.state.GenreID.toString());
            setLocation(itemLocation.state.LocationID.toString());

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

        }

        else {
            return navigate('/');
        }

    }, [])

    const postEditListings = async (e) => {

        e.preventDefault();

        // console.log(BookID);
        // console.log(BookTitle);
        // console.log(Genre);
        // console.log(Condition);
        // console.log(Price);
        // console.log(Description);
        // console.log(Location);
        // console.log(BookImage);

        EditListingFormData.append("BookID", BookID);
        EditListingFormData.append("Title", BookTitle);
        EditListingFormData.append("GenreID", Genre);
        EditListingFormData.append("BookConditionID", Condition);
        EditListingFormData.append("Price", Price);
        EditListingFormData.append("Description", Description);
        EditListingFormData.append("LocationID", Location);

        if (BookImage === undefined) {
            //EditListingFormData.append("Image", null)
        }
        else {
            EditListingFormData.append("Image", BookImage);
        }

        //To print the details for form data
        // for (var pair of EditListingFormData.entries()) {
        //     console.log(`${pair[0]}: ${pair[1]}`);
        // }

        const res = await fetch('/apis/book/update_book_details', {
            method: "POST",
            body: EditListingFormData
        });

        const data = await res.json();

        const trimmedResponseMessage = JSON.stringify(data).replace(/[^a-zA-Z ]/g, "");

        if (trimmedResponseMessage === "successfully updated") {
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
        <Container>
            {Authentication ?
                <SessionTimeoutModal /> : null
            }
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
                                    .filter(GenreDropdown => GenreDropdown.GenreID === Genre)
                                    .map(FilteredGenreDropdown => (
                                        <option value={FilteredGenreDropdown.GenreID.toString()}>{FilteredGenreDropdown.GenreName}</option>)) : null
                            }
                            {Array.isArray(GenreDropdown) ?
                                GenreDropdown
                                    .filter(GenreDropdown => GenreDropdown.GenreID !== Genre)
                                    .map(FilteredGenreDropdown => (
                                        <option value={FilteredGenreDropdown.GenreID.toString()}>{FilteredGenreDropdown.GenreName}</option>)) : null
                            }
                        </Form.Select>
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formCondition" value={Condition} onChange={(e) => setCondition(e.target.value)}>
                        <Form.Label controlId="floatingSelectCondition" label="Book Condition">Book Condition:</Form.Label>
                        <Form.Select required aria-label="Floating label select condition" >
                            {Array.isArray(ConditionDropdown) ?
                                ConditionDropdown
                                    .filter(ConditionDropdown => ConditionDropdown.BookConditionID === Condition)
                                    .map(FilteredConditionDropdown => (
                                        <option value={FilteredConditionDropdown.BookConditionID.toString()}>{FilteredConditionDropdown.BookConditionName}</option>)) : null
                            }
                            {Array.isArray(ConditionDropdown) ?
                                ConditionDropdown
                                    .filter(ConditionDropdown => ConditionDropdown.BookConditionID !== Condition)
                                    .map(FilteredConditionDropdown => (
                                        <option value={FilteredConditionDropdown.BookConditionID.toString()}>{FilteredConditionDropdown.BookConditionName}</option>)) : null
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
                        <Form.Control type="file" onChange={e => setBookImage(e.target.files[0])} />
                        <Form.Text className="text-muted">Image format must be png, jpg, or jpeg.</Form.Text>
                    </Form.Group>
                    <Form.Group className="mb-3" controlId="formLocation" value={Location} onChange={e => setLocation(e.target.value)}>
                        <FloatingLabel controlId="floatingSelectLocation" label="Location">
                            <Form.Select aria-label="Floating label select location" >
                                {Array.isArray(LocationDropdown) ?
                                    LocationDropdown
                                        .filter(LocationDropdown => LocationDropdown.LocationID === Location)
                                        .map(LocationDropdown => (
                                            <option value={LocationDropdown.LocationID.toString()}>{LocationDropdown.LocationName}</option>)) : null
                                }
                                {Array.isArray(LocationDropdown) ?
                                    LocationDropdown
                                        .filter(LocationDropdown => LocationDropdown.LocationID !== Location)
                                        .map(LocationDropdown => (
                                            <option value={LocationDropdown.LocationID.toString()}>{LocationDropdown.LocationName}</option>)) : null
                                }
                            </Form.Select>
                        </FloatingLabel>
                    </Form.Group>
                    <div className="d-flex justify-content-center mb-3">
                        <Row>
                            {showErrors ? errorMessages.map((item, index) => {
                                return <ul style={{ color: "red" }} key={index}>{item}</ul>;
                            }) : null}
                        </Row>
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