import React, { useState } from 'react';
import { Button, Modal, Form, Row, Col } from 'react-bootstrap';
import { useLocation, useNavigate } from 'react-router-dom';

const AcceptOfferModal = ({ BookOfferID }) => {
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const location = useLocation();
    const navigate = useNavigate();

    const userEmail = localStorage.getItem('Email');
    const AcceptOfferData = new FormData();

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    let errors = [];

    const postOffer = async (e) => {

        e.preventDefault();

        console.log(BookOfferID);
        console.log(userEmail);

        AcceptOfferData.append('BookOfferID', BookOfferID);
        AcceptOfferData.append('Email', userEmail);

        // Error Accepting offer for Book
        const res = await fetch('/apis/user/accept_book_offer', {
            method: "POST",
            body: AcceptOfferData
        });

        const data = await res.json();

        const trimmedResponseMessage = JSON.stringify(data).replace(/[^a-zA-Z ]/g, "");

        if (trimmedResponseMessage == "Successfully Created Transaction") {
            handleClose();
            window.location.reload(false);
        }

        else {
            errors.push(trimmedResponseMessage);
            setShowErrors({ showErrors: true });
            setErrorMessages(errors);
        }
    }

    return (
        <>
            <Button variant="primary" onClick={handleShow}>
                Accept
            </Button>

            <Modal show={show} onHide={handleClose} centered>
                <Modal.Header closeButton>
                    <Modal.Title>Are you sure you accept this listing?</Modal.Title>
                </Modal.Header>
                <Form onSubmit={postOffer}>
                    <div className='d-flex align-items-center justify-content-center mb-4'>
                        <Modal.Body>
                            <p>By pressing on the <b>Confirm</b>, you are <b>accepting</b> the offer given by the user
                                and <b>your contact number will be given to the user</b> to complete the face to face
                                deal with the user</p>
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

export default AcceptOfferModal;