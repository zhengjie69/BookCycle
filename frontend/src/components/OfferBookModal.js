import React, { useState } from 'react';
import { Button, Modal, Form, Row, Col } from 'react-bootstrap';
import { useLocation, useNavigate } from 'react-router-dom';
import secureLocalStorage from "react-secure-storage";

export default function OfferBookModal() {
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const location = useLocation();
    const navigate = useNavigate();

    const TransactionData = new FormData();
    const [Price, setPrice] = useState();

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    let errors = [];

    const postTransaction = async (e) => {

        e.preventDefault();

        const userEmail = secureLocalStorage.getItem('Email');
        const book_id = location.state.BookID;

        const trimmedPriceLength = Price.replace(/ /g, "");
        const PriceLength = trimmedPriceLength ? Price.length : 0;

        if (PriceLength === 0 || +isNaN(Price)) {
            errors.push("Please Enter a Valid Price");
        }
        else {
            TransactionData.append('BookID', book_id);
            TransactionData.append('Email', userEmail);
            TransactionData.append('Offer', Price);
        }

        if (errors.length > 0) {
            setShowErrors({ showErrors: true });
            setErrorMessages(errors);
        }
        else {
            setShowErrors({ showErrors: false });
            setErrorMessages(errors);

            const res = await fetch('/apis/user/send_book_offer', {
                method: "POST",
                body: TransactionData
            });

            const data = await res.json();

            const trimmedResponseMessage = JSON.stringify(data).replace(/[^a-zA-Z ]/g, "");

            if (res.status === 201) {
                if (trimmedResponseMessage == "Successfully Sent Offer") {
                    handleClose();
                    //To look for better solutions
                    alert("Offer requested, Please wait for seller's response")
                    navigate('/');
                }
            }

            if (res.status === 401) {
                errors.push(trimmedResponseMessage);
                setShowErrors({ showErrors: true });
                setErrorMessages(errors);
            }
        }
    }

    return (
        <>
            <Button variant="primary" onClick={handleShow}>
                Offer
            </Button>

            <Modal show={show} onHide={handleClose} centered>
                <Modal.Header closeButton>
                    <Modal.Title>Are you sure you want to offer for this listing?</Modal.Title>
                </Modal.Header>
                <Form onSubmit={postTransaction}>
                    <div className='d-flex align-items-center justify-content-center mb-4'>
                        <Modal.Body>
                            <Form.Group as={Row} className="mb-3" controlId="formPlaintextEmail">
                                <Col xs={1}>
                                    <Form.Label column sm="1" xs lg="2">
                                        <span className="material-symbols-outlined">
                                            attach_money
                                        </span>
                                    </Form.Label>
                                </Col>
                                <Col xs={5}>
                                    <Form.Control required placeholder="Price" type="text" value={Price} onChange={e => setPrice(e.target.value)} />
                                </Col>
                            </Form.Group>
                            <p>Enter 0 if you wish to have the book for free</p>
                            {showErrors ? errorMessages.map((item, index) => {
                                return <b><p key={index}>{item}</p></b>;
                            }) : null}
                        </Modal.Body>
                    </div>
                    <Modal.Footer>
                        <Button variant="success" type="submit">
                            Confirm
                        </Button>
                        <Button variant="secondary" onClick={handleClose}>
                            Close
                        </Button>
                    </Modal.Footer>
                </Form>
            </Modal>

        </>
    );
}