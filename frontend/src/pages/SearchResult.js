import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Button, Container, Form, Row, Col, Card, FloatingLabel } from "react-bootstrap"
import { SearchBar } from "../components/SearchBar";
import SessionTimeoutModal from "../components/SessionTimeoutModal";

export function SearchResult() {

    const location = useLocation();
    const navigate = useNavigate();

    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);

    const [searchResult, setSearchResult] = useState([]);

    const [genreDropdown, setGenreDropdown] = useState([]);
    const [locationDropdown, setLocationDropdown] = useState([]);

    const [GenreID, setGenreID] = useState("null");
    const [LocationID, setLocationID] = useState("null");
    const [MinPrice, setMinPrice] = useState("null");
    const [MaxPrice, setMaxPrice] = useState("null");
    const userEmail = localStorage.getItem('Email');

    const Authentication = location.getItem('Authentication');

    useEffect(() => {
        console.log(location.state.SearchKey)
        if (location.state.SearchKey !== null && userEmail !== null) {
            fetch('/apis/book/search_book?BookTitle=' + location.state.SearchKey + '&Email=' + userEmail)
                .then(res => res.json())
                .then(data => {
                    setIsLoaded(true);
                    setSearchResult(data);
                },
                    (error) => {
                        setIsLoaded(true);
                        setError(error);
                    }
                )
        }
        else if (location.state.SearchKey !== null && userEmail === null) {
            fetch('/apis/book/search_book?BookTitle=' + location.state.SearchKey)
                .then(res => res.json())
                .then(data => {
                    setIsLoaded(true);
                    setSearchResult(data);
                },
                    (error) => {
                        setIsLoaded(true);
                        setError(error);
                    }
                )
        }

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
    }, [])

    if (!MinPrice) {
        setMinPrice("null");
    }

    if (!MaxPrice) {
        setMaxPrice("null");
    }

    const getFilterResult = async (e) => {

        e.preventDefault();
        console.log(GenreID);
        console.log(LocationID);
        console.log(MinPrice);
        console.log(MaxPrice);

        fetch('/apis/book/search_book?BookTitle=' + location.state.SearchKey +
            '&GenreFilter=' + GenreID + '&LocationFilter=' + LocationID + '&Email=' + userEmail
            + '&MinPriceFilter=' + MinPrice + '&MaxPriceFilter=' + MaxPrice)
            .then(res => res.json())
            .then(data => {
                setIsLoaded(true);
                setSearchResult(data);
            },
                (error) => {
                    setIsLoaded(true);
                    setError(error);
                }
            )

        if (location.state.SearchKey !== null && userEmail !== null && GenreID === null &&
            LocationID === null && MinPrice === null && MaxPrice === null) {
            fetch('/apis/book/search_book?BookTitle=' + location.state.SearchKey + '&Email=' + userEmail)
                .then(res => res.json())
                .then(data => {
                    setIsLoaded(true);
                    setSearchResult(data);
                },
                    (error) => {
                        setIsLoaded(true);
                        setError(error);
                    }
                )
        }

        else if (location.state.SearchKey !== null && userEmail === null && GenreID === null &&
            LocationID === null && MinPrice === null && MaxPrice === null) {
            fetch('/apis/book/search_book?BookTitle=' + location.state.SearchKey)
                .then(res => res.json())
                .then(data => {
                    setIsLoaded(true);
                    setSearchResult(data);
                },
                    (error) => {
                        setIsLoaded(true);
                        setError(error);
                    }
                )
        }
    }

    function getAllBooks() {
        return (
            <>
                <div className="d-flex justify-content-center">
                    {Authentication === "true" ?
                        <SessionTimeoutModal /> : null
                    }
                    <Row xs="auto">
                        {Array.isArray(searchResult) ?
                            searchResult.map(searchResult => (
                                <div className="col-sm mb-2" key={searchResult.BookID}>
                                    {
                                        <Card style={{ width: '15rem', height: '28rem' }}>
                                            <Card.Img variant="top" src={searchResult.Image} style={{ height: '15rem' }} />
                                            <Card.Body>
                                                <Card.Title>{searchResult.Title}</Card.Title>
                                                {searchResult.Price === 0 ? <Card.Text>Free</Card.Text> : null}
                                                {searchResult.Price > 0 ? <Card.Text>${searchResult.Price}</Card.Text> : null}
                                                <Card.Text>{searchResult.BookCondition}</Card.Text>
                                                <Button onClick={() => {
                                                    navigate('/BookListingInformation', {
                                                        state: {
                                                            BookID: searchResult.BookID,
                                                            Condition: searchResult.BookCondition,
                                                            Title: searchResult.Title,
                                                            Price: searchResult.Price,
                                                            Description: searchResult.Description,
                                                            Image: searchResult.Image,
                                                            Genre: searchResult.Genre,
                                                            Location: searchResult.Location,
                                                            Route: "Home"
                                                        }
                                                    });
                                                }}>View More</Button>
                                            </Card.Body>
                                        </Card>}
                                </div>
                            )) : null}
                    </Row>
                </div>
            </>
        )
    }

    return (
        <Container>
            <SearchBar />
            <h3>Search Result for '{location.state.SearchKey}'</h3>
            <Form onSubmit={getFilterResult}>
                <Row xs="auto" className="mt-4">
                    <Col><h5>Filter:</h5></Col>
                    <Col>
                        <Form.Group className="mb-3" controlId="SearchFormGenre" value={GenreID} onChange={e => setGenreID(e.target.value)}>
                            <Form.Select>
                                <option value="null">All</option>
                                {Array.isArray(genreDropdown) ?
                                    genreDropdown.map(genreDropdown => (
                                        <option value={genreDropdown.GenreID}>{genreDropdown.GenreName}</option>)) : null
                                }
                            </Form.Select>
                        </Form.Group>
                    </Col>
                    <Col>
                        <Form.Group className="mb-3" controlId="SearchFormLocation" value={LocationID} onChange={e => setLocationID(e.target.value)}>
                            <Form.Select>
                                <option value="null">All</option>
                                {Array.isArray(locationDropdown) ?
                                    locationDropdown.map(locationDropdown => (
                                        <option value={locationDropdown.LocationID}>{locationDropdown.LocationName}</option>)) : null
                                }
                            </Form.Select>
                        </Form.Group>
                    </Col>
                    <Col>
                        <Form.Group className="mb-3" controlId="SearchFormMinPrice" value={MinPrice} onChange={e => setMinPrice(e.target.value)}>
                            <Form.Control type="number" placeholder="Min Price" />
                        </Form.Group>
                    </Col>
                    <Col>
                        <b> - </b>
                    </Col>
                    <Col>
                        <Form.Group className="mb-3" controlId="SearchFormMaxPrice" value={MaxPrice} onChange={e => setMaxPrice(e.target.value)}>
                            <Form.Control type="number" placeholder="Max Price" />
                        </Form.Group>
                    </Col>
                    <Col>
                        <Button variant="primary" type="submit">
                            Filter
                        </Button>
                    </Col>
                </Row>
            </Form>
            {getAllBooks()}
        </Container>
    )
}