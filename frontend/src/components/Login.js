import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Modal from 'react-bootstrap/Modal';
import { Row, Col } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';
import { useNavigate } from 'react-router-dom';
import secureLocalStorage from "react-secure-storage";

const Login = () => {
    const navigate = useNavigate();
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const [Email, setEmail] = useState();
    const [Password, setPassword] = useState();

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    const LoginFormData = new FormData();

    let errors = [];

    const setData = async (e) => {

        setErrorMessages([]);

        e.preventDefault();

        LoginFormData.append('Email', Email);
        LoginFormData.append('Password', Password);

        const res = await fetch('/apis/user/login', {
            method: "POST",
            body: LoginFormData
        });

        const data = await res.json();

        if (res.status === 201) {
            handleClose();
            // secureLocalStorage.setItem("Authentication", data.authentication);
            // secureLocalStorage.setItem("Email", data.Email);
            // secureLocalStorage.setItem("Role", data.Role);
            // navigate('/');
            navigate('/OTP', {
                state: {
                    Authentication: data.Authentication,
                    Email: data.Email,
                    Role: data.Role,
                    Route: "Login"
                }
            });
            window.location.reload(false);
        }

        else {
            setShowErrors({ showErrors: true });
            setErrorMessages(errors);
            errors.push("Password or Email is entered Wrongly.");
        }


    }
    return (
        <>
            <Button variant="primary" onClick={handleShow}>
                Login
            </Button>

            <Modal show={show} centered onHide={handleClose} size="xl">
                <Modal.Header closeButton>
                    <Modal.Title><h1>Login</h1></Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div className="justify-content-center">
                        <Form className="mb-3" method="POST">
                            <Row className="ms-5">
                                <Form.Group as={Row} className="mb-3" controlId="formEmail">
                                    <Form.Label column sm="1" xs lg="1">
                                        <span className="material-symbols-outlined">
                                            mail
                                        </span>
                                    </Form.Label>
                                    <Col xs={9}>
                                        <Form.Control type="text" placeholder="Email" value={Email} onChange={e => setEmail(e.target.value)} />
                                    </Col>
                                </Form.Group>
                            </Row>
                            <Row className="ms-5">
                                <Form.Group as={Row} className="mb-3" controlId="formPassword">
                                    <Form.Label column sm="1" xs lg="1">
                                        <span class="material-symbols-outlined">
                                            lock
                                        </span>
                                    </Form.Label>
                                    <Col xs={9}>
                                        <Form.Control type="password" placeholder="Password" value={Password} onChange={e => setPassword(e.target.value)} />
                                    </Col>
                                </Form.Group>
                            </Row>
                            <div className="d-flex justify-content-center">
                                {showErrors ? errorMessages.map((item, index) => {
                                    return <ul style={{ color: "red" }} key={index}>{item}</ul>;
                                }) : null}
                            </div>
                            <div className="d-flex justify-content-center">
                                <Button variant="primary" onClick={setData} type="submit">
                                    Login
                                </Button>
                            </div>
                            <div className="d-flex justify-content-center mt-3">
                                <LinkContainer to="/Register">
                                    <Button variant="primary" onClick={handleClose} type="submit">
                                        Register
                                    </Button>
                                </LinkContainer>
                            </div>
                        </Form>
                    </div>
                    <div className="d-flex justify-content-center">
                        <LinkContainer to="/ForgetPassword">
                            <a onClick={handleClose}>Forget Password?</a>
                        </LinkContainer>
                    </div>
                </Modal.Body>
            </Modal>
        </>
    );
};

export default Login;