import React, { useState } from "react"
import { Container } from "react-bootstrap"
import Form from "react-bootstrap/Form"
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import Button from 'react-bootstrap/Button'
import { useNavigate } from "react-router-dom"

const ChangePassword = () => {

    const navigate = useNavigate();

    const [CurrentPassword, setCurrentPassword] = useState();
    const [NewPassword, setNewPassword] = useState();
    const [ConfirmNewPassword, setConfirmNewPassword] = useState();
    const userEmail = localStorage.getItem('Email');

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    let errors = [];

    const ChangePasswordData = new FormData();

    const postChangePassword = async (e) => {

        setErrorMessages([]);

        e.preventDefault();

        const NewPasswordLength = NewPassword ? NewPassword.length : 0;

        console.log(CurrentPassword);
        console.log(NewPassword);
        console.log(ConfirmNewPassword);

        ChangePasswordData.append('Email', userEmail);
        ChangePasswordData.append('OldPassword', CurrentPassword);

        if (NewPassword === ConfirmNewPassword) {
            if (NewPasswordLength > 4) {
                ChangePasswordData.append('NewPassword', NewPassword);
            }
            else {
                errors.push("Please adhere to the password criteria");
            }
        }
        else {
            errors.push("New password and Confirm Password is different");
        }

        if (errors.length > 0) {
            setShowErrors({ showErrors: true });
            setErrorMessages(errors);
        }
        else {
            setShowErrors({ showErrors: false });
            const res = await fetch('/apis/user/update_password', {
                method: "POST",
                body: ChangePasswordData
            });

            const data = await res.json();

            if (res.status === 200) {

                const trimmedResponseMessage = JSON.stringify(data).replace(/[^a-zA-Z ]/g, "");

                if (trimmedResponseMessage === "Invalid old password") {
                    console.log("invalid password")
                    errors.push("Current Password is entered wrongly");
                    setShowErrors({ showErrors: true });
                    setErrorMessages(errors);
                }
                else {
                    navigate('/MyProfile');
                    window.location.reload(false);
                }
            }
        }

    }

    return (
        <div className="mt-4">
            <Container>
                <div className="d-flex justify-content-center">
                    <h1>Change Password</h1>
                </div>
                <div className="d-flex justify-content-center">
                    <Form onSubmit={postChangePassword}>
                        <Form.Group as={Row} className="mb-3 mt-4" controlId="formCurrentPassword" value={CurrentPassword} onChange={e => setCurrentPassword(e.target.value)}>
                            <Form.Label column sm="5">
                                Current Password:
                            </Form.Label>
                            <Col>
                                <Form.Control required type="password" />
                            </Col>
                        </Form.Group>
                        <Form.Group as={Row} className="mb-3 mt-4" controlId="formNewPassword" value={NewPassword} onChange={e => setNewPassword(e.target.value)}>
                            <Form.Label column sm="5">
                                New Password:
                            </Form.Label>
                            <Col>
                                <Form.Control required type="password" />
                            </Col>
                        </Form.Group>
                        <Form.Group as={Row} className="mb-3 mt-4" controlId="formConfirmNewPassword" value={ConfirmNewPassword} onChange={e => setConfirmNewPassword(e.target.value)}>
                            <Form.Label column sm="5">
                                Confirm Password:
                            </Form.Label>
                            <Col>
                                <Form.Control required type="password" />
                            </Col>
                        </Form.Group>
                        {showErrors ? errorMessages.map((item, index) => {
                            return <ul key={index}>{item}</ul>;
                        }) : null}
                        <div className="d-flex justify-content-center">
                            <Button variant="primary" type="submit">
                                Save Changes
                            </Button>
                        </div>
                    </Form>
                </div>
            </Container>
        </div>
    )
};

export default ChangePassword;