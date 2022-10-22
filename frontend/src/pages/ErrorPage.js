import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const ErrorPage = () => {
    return (
        <Container>
            <div className="d-flex align-items-center justify-content-center mb-4 mt-4">
                <Row xs="auto">
                    <Col><h1>Error 404</h1></Col>
                </Row>
            </div>
            <div className="d-flex align-items-center justify-content-center mb-4 mt-4">
                <Row xs="auto">
                    <Col><h2>Page Not Found</h2></Col>
                </Row>
            </div>
        </Container>

    );
}

export default ErrorPage;