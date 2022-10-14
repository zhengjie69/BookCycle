import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { useLocation, useNavigate } from 'react-router-dom';

export default function DeleteBookModal() {
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const location = useLocation();
    const navigate = useNavigate();

    const DeleteBookData = new FormData();

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    let errors = [];

    const postDeleteBook = async (e) => {

        e.preventDefault();

        const userEmail = localStorage.getItem('Email');
        const book_id = location.state.BookID;

        console.log(book_id);
        console.log(userEmail);

        DeleteBookData.append('BookID', book_id);
        DeleteBookData.append('Email', userEmail);

        const res = await fetch('/apis/book/delete_book', {
            method: "POST",
            body: DeleteBookData
        });

        const data = await res.json();

        if (res.status === 201) {

            const trimmedResponseMessage = JSON.stringify(data).replace(/[^a-zA-Z ]/g, "");

            if (trimmedResponseMessage === "Error in deleting book") {
                errors.push(trimmedResponseMessage);
                setShowErrors({ showErrors: true });
                setErrorMessages(errors);
            }
            else {
                navigate('/MyListings');
                window.location.reload(false);
            }
        }
    }

    return (
        <>
            <Button variant="danger" onClick={handleShow}>
                Delete this listing
            </Button>

            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Are you sure you want to delete this listing?</Modal.Title>
                </Modal.Header>
                <Modal.Body>{showErrors ? errorMessages.map((item, index) => {
                    return <b><p key={index}>{item}</p></b>;
                }) : null}</Modal.Body>
                <Modal.Footer>
                    <Button variant="danger" onClick={postDeleteBook}>
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