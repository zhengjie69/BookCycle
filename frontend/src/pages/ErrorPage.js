import React from 'react';
import { Row } from 'react-bootstrap';

const ErrorPage = () => {
    return (
        <div className="d-flex align-items-center justify-content-center mb-4 mt-4">
            <Row><h1>Error 404!</h1></Row>
            <Row><h2>Page Not Found</h2></Row>
        </div>
    );
}

export default ErrorPage;