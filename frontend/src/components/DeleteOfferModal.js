import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { useNavigate } from 'react-router-dom';
import secureLocalStorage from "react-secure-storage";

export default function DeleteOfferModal({ BookOfferID }) {
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const navigate = useNavigate();

    const DeleteOfferData = new FormData();

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    const userEmail = secureLocalStorage.getItem('Email');

    let errors = [];

    const postDeleteOffer = async (e) => {

        e.preventDefault();

        DeleteOfferData.append('BookOfferID', BookOfferID);
        DeleteOfferData.append('Email', userEmail);

        const res = await fetch('/apis/user/delete_book_offer', {
            method: "POST",
            body: DeleteOfferData
        });

        const data = await res.json();

        if (res.status === 201) {

            const trimmedResponseMessage = JSON.stringify(data).replace(/[^a-zA-Z ]/g, "");

            if (trimmedResponseMessage === "Successfully deleted book offer") {
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
            <Button variant="danger" onClick={handleShow}>
                Delete
            </Button>

            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Are you sure you want to delete this offer?</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <b>There will be no reversal if the offer is deleted</b>
                    {showErrors ?
                        errorMessages.map((item, index) => {
                            return <b><p key={index}>{item}</p></b>;
                        }) : null
                    }
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="danger" onClick={postDeleteOffer}>
                        Delete
                    </Button>
                    <Button variant="secondary" onClick={handleClose}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    );
}