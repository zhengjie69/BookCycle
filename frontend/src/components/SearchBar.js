import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Form, Row, Col, Button } from "react-bootstrap"

export function SearchBar() {

    const navigate = useNavigate();

    const [Search, setSearch] = useState();

    const postSearch = async (e) => {

        e.preventDefault();

        const SearchLength = Search ? Search.length : 0;

        if (SearchLength !== 0) {
            navigate('/SearchResult', {
                state: {
                    SearchKey: Search
                }
            });
            window.location.reload(false);
        }
    }

    return (
        <div className="row h-100 justify-content-center align-items-center">
            <Form className="mt-4 me-3" onSubmit={postSearch}>
                <Row>
                    <Form.Group as={Row} className="mb-3">
                        <Col xs={11}>
                            <Form.Control type="text" placeholder="Search For Books" value={Search} onChange={e => setSearch(e.target.value)} />
                        </Col>
                        <Col xs={1}>
                            <Button variant="primary" type="submit">
                                <span className="material-symbols-outlined">
                                    search
                                </span>
                            </Button>
                        </Col>
                    </Form.Group>
                </Row>
            </Form>
        </div>
    )
}