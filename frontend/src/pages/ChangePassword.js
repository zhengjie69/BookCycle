import React, { useState, useEffect } from "react"
import { Container } from "react-bootstrap"
import Form from "react-bootstrap/Form"
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import Button from 'react-bootstrap/Button'
import { useNavigate } from "react-router-dom"
import SessionTimeoutModal from "../components/SessionTimeoutModal"
import secureLocalStorage from "react-secure-storage";

const ChangePassword = () => {

    const Authentication = secureLocalStorage.getItem('Authentication');
    const navigate = useNavigate();

    useEffect(() => {
        if (!Authentication) {
            return navigate("/");
        }
    }, []);

    const [CurrentPassword, setCurrentPassword] = useState();
    const [NewPassword, setNewPassword] = useState();
    const [ConfirmNewPassword, setConfirmNewPassword] = useState();
    const userEmail = secureLocalStorage.getItem('Email');

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    let errors = [];

    function ValidatePassword(password) {
        var pattern = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[-+_!@#$%^&*.,?]).+$");

        if (!password || password.length === 0 || password.length < 8 || password.length > 25) {
            return ("Please give a valid length of password.");
        }

        if (pattern.test(password)) {
            return true
        } else {
            return ("Please adhere to the password criteria.");
        }
    }

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

        if (ValidatePassword(NewPassword) === true) {
            if (NewPassword === ConfirmNewPassword) {
                ChangePasswordData.append('NewPassword', NewPassword);
            }
            else {
                errors.push("New password and Confirm Password is different");
            }
        }
        else {
            errors.push(ValidatePassword(NewPassword));
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

            if (res.status === 201) {

                const trimmedResponseMessage = JSON.stringify(data).replace(/[^a-zA-Z ]/g, "");

                if (trimmedResponseMessage === "Password Successfully Changed") {
                    navigate('/MyProfile');
                    window.location.reload(false);
                }
                else {
                    errors.push(trimmedResponseMessage);
                    setShowErrors({ showErrors: true });
                    setErrorMessages(errors);
                }
            }
        }

    }

    return (
        <div className="mt-4">
            <Container>
                {Authentication ?
                    <SessionTimeoutModal /> : null
                }
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
                                <Form.Text className="text-muted">
                                    Password length to be more than 8 containing 1 uppcase, 1 lowercase and 1 special character
                                </Form.Text>
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
                        <div className="d-flex align-items-center justify-content-center mt-4">
                            <Row>
                                {showErrors ? errorMessages.map((item, index) => {
                                    return <ul style={{ color: "red" }} key={index}>{item}</ul>;
                                }) : null}
                            </Row>
                        </div>
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