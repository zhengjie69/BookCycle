import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { useLocation, useNavigate } from 'react-router-dom';
import secureLocalStorage from "react-secure-storage";

export default function DisableUserModal({ UserEmail, Username }) {
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const navigate = useNavigate();

    const DisableUserData = new FormData();

    const AdminEmail = secureLocalStorage.getItem('Email');

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    let errors = [];

    const postDisableUser = async (e) => {

        e.preventDefault();

        DisableUserData.append('Email', AdminEmail);
        DisableUserData.append('UserEmail', UserEmail);

        const res = await fetch('/apis/admin/disable_user_account', {
            method: "POST",
            body: DisableUserData
        });

        const data = await res.json();

        const trimmedResponseMessage = JSON.stringify(data).replace(/[^a-zA-Z ]/g, "");

        if (trimmedResponseMessage === "successfully disabled account") {
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
            <Button variant="danger" onClick={handleShow}>
                Disable
            </Button>

            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Are you sure you want to disable {Username}?</Modal.Title>
                </Modal.Header>
                <Modal.Body>{showErrors ? errorMessages.map((item, index) => {
                    return <b><p key={index}>{item}</p></b>;
                }) : null}</Modal.Body>
                <Modal.Footer>
                    <Button variant="danger" onClick={postDisableUser}>
                        Disable
                    </Button>
                    <Button variant="secondary" onClick={handleClose}>
                        Close
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    );
}