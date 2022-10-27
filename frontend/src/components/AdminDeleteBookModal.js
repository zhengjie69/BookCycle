import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { useLocation, useNavigate } from 'react-router-dom';

export default function AdminDeleteBookModal() {
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const location = useLocation();
    const navigate = useNavigate();

    const AdminDeleteBookData = new FormData();

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    let errors = [];

    const postAdminDeleteBook = async (e) => {

        e.preventDefault();

        const adminEmail = localStorage.getItem('Email');
        const userEmail = location.state.UserEmail;
        const book_id = location.state.BookID;
        const username = location.state.Username;

        console.log(book_id);
        console.log(userEmail);
        console.log(adminEmail);

        AdminDeleteBookData.append('BookID', book_id);
        AdminDeleteBookData.append('OwnerEmail', userEmail);
        AdminDeleteBookData.append('Email', adminEmail);

        const res = await fetch('/apis/admin/delete_user_book', {
            method: "POST",
            body: AdminDeleteBookData
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
                navigate('/ManageBooks/ManageBooksResult', {
                    state: {
                        UserEmail: userEmail,
                        Username: username
                    }
                });
                window.location.reload(false);
            }
        }
    }

    return (
        <>
            <Button variant="danger" onClick={handleShow}>
                Delete this book
            </Button>

            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Are you sure you want to delete this listing?</Modal.Title>
                </Modal.Header>
                <Modal.Body>{showErrors ? errorMessages.map((item, index) => {
                    return <b><p key={index}>{item}</p></b>;
                }) : null}</Modal.Body>
                <Modal.Footer>
                    <Button variant="danger" onClick={postAdminDeleteBook}>
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