import React, { useEffect, useState } from "react";
import { Container, Row, Col } from "react-bootstrap";
import { useLocation, useNavigate } from "react-router-dom";
import SessionTimeoutModal from "../../components/SessionTimeoutModal";
import secureLocalStorage from "react-secure-storage";

function TransactionDetails() {

    const location = useLocation();
    const Authentication = secureLocalStorage.getItem('Authentication');
    const Role = secureLocalStorage.getItem('Role');
    const navigate = useNavigate();

    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);

    const [Transaction, setTransaction] = useState([]);

    useEffect(() => {
        if (Authentication && Role === "User") {
            fetch('/apis/user/get_transaction_details?TransactionID=' + location.state.TransactionID)
                .then(res => res.json())
                .then(data => {
                    setIsLoaded(true);
                    setTransaction(data);
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

    return (
        <Container>
            {Authentication ?
                <SessionTimeoutModal /> : null
            }
            <div className="d-flex align-items-center justify-content-center mb-4 mt-4">
                <h1>Transaction Details</h1>
            </div>
            <div className="d-flex align-items-center justify-content-center mb-4">
                <div className="justify-content-center">
                    <Row className="mb-4">
                        <Col xs={4}><b>Book Title:</b></Col>
                        <Col xs={8}>{Transaction.BookTitle}</Col>
                    </Row>
                    <Row className="mb-4">
                        <Col xs={4}><b>Email:</b></Col>
                        <Col xs={8}>{Transaction.Owner}</Col>
                    </Row>
                    <Row className="mb-4">
                        <Col xs={4}><b>Phone Number:</b></Col>
                        <Col xs={8}>{Transaction.OwnerPhoneNumber}</Col>
                    </Row>
                </div>
            </div>
        </Container >
    );
}

export default TransactionDetails;