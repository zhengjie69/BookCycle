import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { Button, Container, Form, Row, Col } from "react-bootstrap"
import { SearchBar } from "../components/SearchBar";

export function SearchResult() {

    const location = useLocation();

    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);

    const [searchResult, setSearchResult] = useState([]);

    useEffect(() => {
        console.log(location.state.SearchKey)
        if (location.state.SearchKey !== null) {
            fetch('/apis/book/search_book_by_title?Title=' + location.state.SearchKey)
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
    }, [])

    return (
        <Container>
            <SearchBar />
            <h3>Search Result for '{location.state.SearchKey}'</h3>
            <Row xs="auto" className="mt-4">
                <Col><h5>Filter:</h5></Col>
                <Col><Button>Genre</Button></Col>
                <Col><Button>Location</Button></Col>
                <Col><Button>Price</Button></Col>
            </Row>
        </Container>
    )
}