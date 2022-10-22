import React, { useState } from 'react';
import { Container, Form, Col, Row, Button } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

function Register() {

    const navigate = useNavigate();
    const [Username, setUsername] = useState();
    const [Email, setEmail] = useState();
    const [Password, setPassword] = useState();
    const [ConfirmPassword, setConfirmPassword] = useState();
    const [ContactNumber, setContactNumber] = useState();

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    let errors = [];

    const RegisterFormData = new FormData();

    function ValidateEmail(email) {
        if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email)) { return true; }
        return false;
    }

    const postRegister = async (e) => {

        setErrorMessages([]);

        e.preventDefault();

        RegisterFormData.append('Username', Username);
        const PasswordLength = Password ? Password.length : 0;
        const ContactNumberLength = ContactNumber ? ContactNumber.length : 0;

        if (ValidateEmail(Email) === true) {
            RegisterFormData.append('Email', Email)
        }
        else {
            errors.push("Please enter a valid email.");
        }

        if (Password === ConfirmPassword && PasswordLength > 4) {
            RegisterFormData.append('Password', Password)
        }
        else if (PasswordLength < 4) {
            errors.push("Please follow password criteria.");
        }
        else if (Password !== ConfirmPassword) {
            errors.push("Please enter the same password and confirm password.");
        }

        if (!isNaN(+ContactNumber) && ContactNumberLength === 8) {
            RegisterFormData.append('ContactNumber', ContactNumber)
        }
        else {
            errors.push("Please enter a valid phone number")
        }

        if (errors.length > 0) {
            setShowErrors({ showErrors: true });
            setErrorMessages(errors);
        }
        else {
            setShowErrors({ showErrors: false });
            const res = await fetch('/apis/user/create_user', {
                method: "POST",
                body: RegisterFormData
            });

            const data = await res.json();
            if (res.status === 201) {
                localStorage.setItem('Authentication', data.authentication);
                localStorage.setItem('Email', data.Email);
                navigate('/');
                window.location.reload(false);
            }

        }
    }

    return (
        <Container>
            <div className="d-flex justify-content-center mb-2">
                <h1>Register</h1>
            </div>
            <div className="d-flex justify-content-center">
                <form onSubmit={postRegister}>
                    <Row>
                        <Form.Group as={Row} className="mb-3" controlId="formUsername">
                            <Form.Label column sm="1" xs lg="1">
                                <span className="material-symbols-outlined">
                                    person
                                </span>
                            </Form.Label>
                            <Col xs={10}>
                                <Form.Control required type="text" placeholder="Username" value={Username} onChange={e => setUsername(e.target.value)} />
                            </Col>
                        </Form.Group>
                    </Row>
                    <Row>
                        <Form.Group as={Row} className="mb-3" controlId="formEmail">
                            <Form.Label column sm="1" xs lg="1">
                                <span className="material-symbols-outlined">
                                    mail
                                </span>
                            </Form.Label>
                            <Col xs={10}>
                                <Form.Control required type="email" placeholder="Email" value={Email} onChange={e => setEmail(e.target.value)} />
                            </Col>
                        </Form.Group>
                    </Row>
                    <Row>
                        <Form.Group as={Row} className="mb-3" controlId="formPassword">
                            <Form.Label column sm="1" xs lg="1">
                                <span className="material-symbols-outlined">
                                    lock
                                </span>
                            </Form.Label>
                            <Col xs={10}>
                                <Form.Control required type="password" placeholder="Password" value={Password} onChange={e => setPassword(e.target.value)} />
                            </Col>
                            <Col xs={10}>
                                <Form.Text className="text-muted">
                                    Password Length is to be more than 4.
                                </Form.Text>
                            </Col>
                        </Form.Group>
                    </Row>
                    <Row>
                        <Form.Group as={Row} className="mb-3" controlId="formConfirmPassword">
                            <Form.Label column sm="1" xs lg="1">
                                <span className="material-symbols-outlined">
                                    lock
                                </span>
                            </Form.Label>
                            <Col xs={10}>
                                <Form.Control required type="password" placeholder="Confirm Password" value={ConfirmPassword} onChange={e => setConfirmPassword(e.target.value)} />
                            </Col>
                        </Form.Group>
                    </Row>
                    <Row>
                        <Form.Group as={Row} className="mb-3" controlId="formContactNumber">
                            <Form.Label column sm="1" xs lg="1">
                                <span className="material-symbols-outlined">
                                    phone
                                </span>
                            </Form.Label>
                            <Col xs={10}>
                                <Form.Control required type="tel" placeholder="Contact Number" value={ContactNumber} onChange={e => setContactNumber(e.target.value)} />
                            </Col>
                        </Form.Group>
                    </Row>
                    <div className="d-flex justify-content-center">
                        <Button variant="primary" type="submit">
                            Register
                        </Button>
                    </div>
                    {showErrors ? errorMessages.map((item, index) => {
                        return <ul key={index}>{item}</ul>;
                    }) : null}
                </form>
            </div>
        </Container >
    );
}

export default Register;