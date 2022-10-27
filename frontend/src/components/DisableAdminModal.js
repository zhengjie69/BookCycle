import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { useLocation, useNavigate } from 'react-router-dom';

export default function DisableAdminModal({ AdminEmail, Username }) {
    const [show, setShow] = useState(false);

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const navigate = useNavigate();

    const DisableAdminData = new FormData();

    const SuperAdminEmail = localStorage.getItem('Email');

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    let errors = [];

    const postDisableAdmin = async (e) => {

        e.preventDefault();

        DisableAdminData.append('superAdminEmail', SuperAdminEmail);
        DisableAdminData.append('AdminEmail', AdminEmail);

        console.log(SuperAdminEmail);

        const res = await fetch('/apis/superadmin/disable_admin_account', {
            method: "POST",
            body: DisableAdminData
        });

        const data = await res.json();

        const trimmedResponseMessage = JSON.stringify(data).replace(/[^a-zA-Z ]/g, "");

        if (trimmedResponseMessage === "Successfully disabled admin account") {
            navigate('/ManageAdmin');
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
                    <Button variant="danger" onClick={postDisableAdmin}>
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