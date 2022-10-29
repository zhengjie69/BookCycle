import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { useNavigate } from 'react-router-dom';
import secureLocalStorage from "react-secure-storage";

export default function EnableUserModal({ UserEmail, Username }) {
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const navigate = useNavigate();

    const EnableUserData = new FormData();

    const AdminEmail = secureLocalStorage.getItem('Email');

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    let errors = [];

    const postEnableUser = async (e) => {

        e.preventDefault();

        EnableUserData.append('Email', AdminEmail);
        EnableUserData.append('UserEmail', UserEmail);

        const res = await fetch('/apis/admin/enable_user_account', {
            method: "POST",
            body: EnableUserData
        });

        const data = await res.json();

        const trimmedResponseMessage = JSON.stringify(data).replace(/[^a-zA-Z ]/g, "");

        if (trimmedResponseMessage === "successfully enabled account") {
            navigate('/ManageUsers');
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
            <Button variant="success" onClick={handleShow}>
                Enable
            </Button>

            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Are you sure you want to enable {Username}?</Modal.Title>
                </Modal.Header>
                <Modal.Body>{showErrors ? errorMessages.map((item, index) => {
                    return <b><p key={index}>{item}</p></b>;
                }) : null}</Modal.Body>
                <Modal.Footer>
                    <Button variant="success" onClick={postEnableUser}>
                        Enable
                    </Button>
                    <Button variant="secondary" onClick={handleClose}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    );
}