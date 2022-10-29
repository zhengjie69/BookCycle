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
        if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email)) {
            return true;
        }
        return false;
    }

    function containsSpecialChars(str) {
        const specialChars = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
        return specialChars.test(str);
    }

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

    const postRegister = async (e) => {

        setErrorMessages([]);

        e.preventDefault();


        const UsernameLength = Username ? Username.length : 0;
        const ContactNumberLength = ContactNumber ? ContactNumber.length : 0;

        console.log(Username);
        console.log(Email);
        console.log(Password);
        console.log(ConfirmPassword);
        console.log(ContactNumber);

        if (UsernameLength <= 12 && UsernameLength > 3) {
            if (containsSpecialChars(Username)) {
                errors.push("Please do not use special characters in your username.");
            }
            else {
                RegisterFormData.append('Username', Username);
            }
        }
        else {
            errors.push("Please enter a valid username with a length of minumum 4 and maximum 12.");
        }

        if (ValidateEmail(Email) === true) {
            RegisterFormData.append('Email', Email)
        }
        else {
            errors.push("Please enter a valid email.");
        }

        if (ValidatePassword(Password) === true) {
            if (Password === ConfirmPassword) {
                RegisterFormData.append('Password', Password);
            }
            else {
                errors.push("Ensure that the password and confirm password is the same");
            }
        }
        else {
            errors.push(ValidatePassword(Password));
        }

        if (!isNaN(+ContactNumber)) {
            if (ContactNumberLength === 8) {
                RegisterFormData.append('ContactNumber', ContactNumber);
            }
            else {
                errors.push("Please enter a valid phone number length");
            }
        }
        else {
            errors.push("Please enter a valid phone number");
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
                localStorage.setItem('Role', data.Role);
                navigate('/');
                window.location.reload(false);
            }

            else {
                const trimmedResponseMessage = JSON.stringify(data).replace(/[^a-zA-Z ]/g, "");
                errors.push(trimmedResponseMessage);
                setShowErrors({ showErrors: true });
                setErrorMessages(errors);
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
                                    Password length to be more than 8 containing 1 uppcase, 1 lowercase and 1 special character
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
                    <div className="d-flex align-items-center justify-content-center mt-4">
                        <Row>
                            {showErrors ? errorMessages.map((item, index) => {
                                return <ul key={index}>{item}</ul>;
                            }) : null}
                        </Row>
                    </div>
                </form>
            </div>
        </Container >
    );
}

export default Register;