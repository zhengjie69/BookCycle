import React, { useState, useEffect } from "react";
import { Container, Row, Form, Col, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import SessionTimeoutModal from "../../components/SessionTimeoutModal";
import secureLocalStorage from "react-secure-storage";

export default function CreateAdmin() {

    const navigate = useNavigate();
    const Authentication = secureLocalStorage.getItem("Authentication");
    const SuperAdminEmail = secureLocalStorage.getItem("Email");
    const Role = secureLocalStorage.getItem("Role");

    const [AdminUsername, setAdminUsername] = useState();
    const [AdminEmail, setAdminEmail] = useState();
    const [AdminPassword, setAdminPassword] = useState();
    const [AdminConfirmPassword, setAdminConfirmPassword] = useState();
    const [AdminContactNumber, setAdminContactNumber] = useState();

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    let errors = [];

    const CreateAdminFormData = new FormData();

    useEffect(() => {
        if (!Authentication || Role !== "SuperAdmin") {
            return navigate('/');
        }
    }, [])

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

    function validatePassword(password) {
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

    const postCreateAdmin = async (e) => {

        setErrorMessages([]);

        e.preventDefault();

        CreateAdminFormData.append('superAdminEmail', SuperAdminEmail);

        const AdminUsernameLength = AdminUsername ? AdminUsername.length : 0;
        const AdminContactNumberLength = AdminContactNumber ? AdminContactNumber.toString().length : 0;

        if (AdminUsernameLength <= 12 && AdminUsernameLength > 3) {
            if (containsSpecialChars(AdminUsername)) {
                errors.push("Please do not use special characters in your username.");
            }
            else {
                CreateAdminFormData.append('Username', AdminUsername);
            }
        }
        else {
            errors.push("Please enter a valid username with a length of minumum 4 and maximum 12.");
        }

        if (ValidateEmail(AdminEmail)) {
            CreateAdminFormData.append('AdminEmail', AdminEmail);
        }
        else {
            errors.push("Please enter a valid email.");
        }

        if (validatePassword(AdminPassword) === true) {
            if (AdminPassword === AdminConfirmPassword) {
                CreateAdminFormData.append('Password', AdminPassword);
            }
            else {
                errors.push("Ensure that the password and confirm password is the same");
            }
        }
        else {
            errors.push(validatePassword(AdminPassword));
        }

        if (!isNaN(+AdminContactNumber)) {
            if (AdminContactNumberLength === 8) {
                CreateAdminFormData.append('ContactNumber', AdminContactNumber);
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

            const res = await fetch('/apis/superadmin/create_admin_account', {
                method: "POST",
                body: CreateAdminFormData
            });

            const data = await res.json();

            const trimmedResponseMessage = JSON.stringify(data).replace(/[^a-zA-Z ]/g, "");

            if (trimmedResponseMessage == "Successfully created user") {
                alert(AdminUsername + " has been created")
                navigate('/');
                window.location.reload(false);
            }
            else {
                errors.push(trimmedResponseMessage);
                setShowErrors({ showErrors: true });
                setErrorMessages(errors);
            }
        }

    }

    return (
        <Container>
            {Authentication ?
                <SessionTimeoutModal /> : null
            }
            <div className="d-flex align-items-center justify-content-center mt-4">
                <Row>
                    <h1>Create Admin</h1>
                </Row>
            </div>
            <div className="d-flex justify-content-center">
                <form onSubmit={postCreateAdmin}>
                    <Row>
                        <Form.Group as={Row} className="mb-3" controlId="formAdminUsername">
                            <Form.Label column sm="1" xs lg="1">
                                <span className="material-symbols-outlined">
                                    person
                                </span>
                            </Form.Label>
                            <Col xs={10}>
                                <Form.Control required type="text" placeholder="Username" value={AdminUsername} onChange={e => setAdminUsername(e.target.value)} />
                            </Col>
                        </Form.Group>
                    </Row>
                    <Row>
                        <Form.Group as={Row} className="mb-3" controlId="formAdminEmail">
                            <Form.Label column sm="1" xs lg="1">
                                <span className="material-symbols-outlined">
                                    mail
                                </span>
                            </Form.Label>
                            <Col xs={10}>
                                <Form.Control required type="email" placeholder="Email" value={AdminEmail} onChange={e => setAdminEmail(e.target.value)} />
                            </Col>
                        </Form.Group>
                    </Row>
                    <Row>
                        <Form.Group as={Row} className="mb-3" controlId="formAdminPassword">
                            <Form.Label column sm="1" xs lg="1">
                                <span className="material-symbols-outlined">
                                    lock
                                </span>
                            </Form.Label>
                            <Col xs={10}>
                                <Form.Control required type="password" placeholder="Password" value={AdminPassword} onChange={e => setAdminPassword(e.target.value)} />
                            </Col>
                            <Col xs={10}>
                                <Form.Text className="text-muted">
                                    Password length to be more than 8 containing 1 uppcase, 1 lowercase and 1 special character
                                </Form.Text>
                            </Col>
                        </Form.Group>
                    </Row>
                    <Row>
                        <Form.Group as={Row} className="mb-3" controlId="formAdminConfirmPassword">
                            <Form.Label column sm="1" xs lg="1">
                                <span className="material-symbols-outlined">
                                    lock
                                </span>
                            </Form.Label>
                            <Col xs={10}>
                                <Form.Control required type="password" placeholder="Confirm Password" value={AdminConfirmPassword} onChange={e => setAdminConfirmPassword(e.target.value)} />
                            </Col>
                        </Form.Group>
                    </Row>
                    <Row>
                        <Form.Group as={Row} className="mb-3" controlId="formAdminContactNumber">
                            <Form.Label column sm="1" xs lg="1">
                                <span className="material-symbols-outlined">
                                    phone
                                </span>
                            </Form.Label>
                            <Col xs={10}>
                                <Form.Control required type="tel" placeholder="Contact Number" value={AdminContactNumber} onChange={e => setAdminContactNumber(e.target.value)} />
                            </Col>
                        </Form.Group>
                    </Row>
                    <div className="d-flex justify-content-center">
                        <Button variant="primary" type="submit">
                            Create
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
        </Container>
    );
}