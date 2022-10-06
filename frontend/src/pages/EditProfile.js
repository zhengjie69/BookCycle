import React, { useState } from "react"
import { Container, Form, Col, Row, Button } from "react-bootstrap"
import { useLocation, useNavigate } from 'react-router-dom'

const EditProfile = () => {

    const navigate = useNavigate();
    const userEmail = localStorage.getItem('Email');
    const location = useLocation();
    const [Username, setUsername] = useState();
    const [ContactNumber, setContactNumber] = useState();

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    let errors = [];

    const EditProfileData = new FormData();

    const postUpdatedInformation = async (e) => {

        setErrorMessages([]);

        e.preventDefault();

        const UsernameLength = Username ? Username.length : 0;
        EditProfileData.append('Email', userEmail);

        if (isNaN(ContactNumber)) {
            EditProfileData.append('ContactNumber', location.state.ContactNumber);
        }
        else {
            if (!isNaN(+ContactNumber) && ContactNumber.length === 8) {
                EditProfileData.append('ContactNumber', ContactNumber);
            }
            else {
                errors.push("Please enter a valid phone number");
            }
        }

        if (UsernameLength === 0) {
            EditProfileData.append('Username', location.state.Username);
        }
        else {
            EditProfileData.append('Username', Username);
        }

        if (errors.length > 0) {
            setShowErrors({ showErrors: true });
            setErrorMessages(errors);
        }
        else {
            setShowErrors({ showErrors: false });
            const res = await fetch('/apis/user/update_profile', {
                method: "POST",
                body: EditProfileData
            });

            const data = await res.json();

            if (res.status === 200) {
                navigate('/MyProfile');
                window.location.reload(false);
            }
        }

    }

    return (
        <div className='mt-4'>
            <Container>
                <div className="d-flex justify-content-center mb-2">
                    <h1>Edit Profile</h1>
                </div>
                <div className="d-flex justify-content-center">
                    <Form onSubmit={postUpdatedInformation}>
                        <Row>
                            <Form.Group as={Row} className="mb-3" controlId="formName">
                                <Form.Label column sm="1" xs lg="2">
                                    <span className="material-symbols-outlined text-right">
                                        person
                                    </span>
                                </Form.Label>
                                <Col xs={10}>
                                    <Form.Control type="text" placeholder={location.state.Username} value={Username} onChange={e => setUsername(e.target.value)} />
                                </Col>
                            </Form.Group>
                        </Row>
                        <Row>
                            <Form.Group as={Row} className="mb-3" controlId="formPlaintextEmail">
                                <Form.Label column sm="1" xs lg="2">
                                    <span className="material-symbols-outlined">
                                        mail
                                    </span>
                                </Form.Label>
                                <Col xs={10}>
                                    <Form.Control plaintext readOnly defaultValue={userEmail} />
                                </Col>
                            </Form.Group>
                        </Row>
                        <Row>
                            <Form.Group as={Row} className="mb-3" controlId="formName">
                                <Form.Label column sm="1" xs lg="2">
                                    <span className="material-symbols-outlined">
                                        chat
                                    </span>
                                </Form.Label>
                                <Col xs={10}>
                                    <Form.Control type="text" placeholder={location.state.ContactNumber} value={ContactNumber} onChange={e => setContactNumber(e.target.value)} />
                                </Col>
                            </Form.Group>
                        </Row>
                        <Row>
                            <div className="d-flex justify-content-center">
                                <Button variant="primary" type="submit">
                                    Save Changes
                                </Button>
                            </div>
                        </Row>
                        <Row>
                            {showErrors ? errorMessages.map((item, index) => {
                                return <ul key={index}>{item}</ul>;
                            }) : null}
                        </Row>
                    </Form>
                </div>
            </Container>
        </div>
    )
};

export default EditProfile;