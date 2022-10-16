import React, { useState } from 'react';
import { Button, Modal, Form, Row, Col } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

export default function EditOfferModal({ BookOfferID, BookOfferPrice }) {
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const navigate = useNavigate();

    const EditTransactionData = new FormData();
    const [Price, setPrice] = useState();

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    const userEmail = localStorage.getItem('Email');

    let errors = [];

    const postEditTransaction = async (e) => {

        e.preventDefault();

        console.log(BookOfferID);
        console.log(userEmail);
        console.log(BookOfferPrice);

        const trimmedPriceLength = Price.replace(/ /g, "");
        const PriceLength = trimmedPriceLength ? Price.length : 0;

        if (PriceLength === 0 || +isNaN(Price)) {
            errors.push("Please Enter a Valid Price");
        }
        else {
            EditTransactionData.append('BookOfferID', BookOfferID);
            EditTransactionData.append('Email', userEmail);
            EditTransactionData.append('Offer', Price);
        }

        if (errors.length > 0) {
            setShowErrors({ showErrors: true });
            setErrorMessages(errors);
        }
        else {
            setShowErrors({ showErrors: false });
            setErrorMessages(errors);

            const res = await fetch('/apis/user/edit_book_offer', {
                method: "POST",
                body: EditTransactionData
            });

            const data = await res.json();

            const trimmedResponseMessage = JSON.stringify(data).replace(/[^a-zA-Z ]/g, "");

            if (trimmedResponseMessage === "Successfully edited book offer") {
                handleClose();
                //To look for better solutions
                alert("Offer Edited, Please wait for seller's response")
                navigate('/MyOffers');
                window.location.reload(false);
            }
            else {
                errors.push(trimmedResponseMessage);
                setShowErrors({ showErrors: true });
                setErrorMessages(errors);
            }
        }
    }

    return (
        <>
            <Button variant="primary" onClick={handleShow}>
                Edit
            </Button>

            <Modal show={show} onHide={handleClose} centered>
                <Modal.Header closeButton>
                    <Modal.Title>Please re-enter the amount you wish to offer</Modal.Title>
                </Modal.Header>
                <Form onSubmit={postEditTransaction}>
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