import React, { useState, useEffect } from "react"
import { Container, Form, Col, Row, Button } from "react-bootstrap"
import { useLocation, useNavigate } from 'react-router-dom'
import SessionTimeoutModal from "../../components/SessionTimeoutModal";
import secureLocalStorage from "react-secure-storage";

const EditProfile = () => {

    const Authentication = secureLocalStorage.getItem('Authentication');
    const Role = secureLocalStorage.getItem('Role');
    const navigate = useNavigate();

    const userEmail = secureLocalStorage.getItem('Email');
    const location = useLocation();
    const [Username, setUsername] = useState();
    const [ContactNumber, setContactNumber] = useState();

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    let errors = [];

    const EditProfileData = new FormData();

    useEffect(() => {
        if (Authentication && Role === "User") {
            setUsername(location.state.Username);
            setContactNumber(location.state.ContactNumber);
        }
        else {
            return navigate("/");
        }
    }, []);

    const postUpdatedInformation = async (e) => {

        console.log(ContactNumber);
        console.log(ContactNumber.toString().length);
        console.log(Username);

        setErrorMessages([]);

        e.preventDefault();

        const UsernameLength = Username ? Username.length : 0;
        const ContactNumberLength = ContactNumber ? ContactNumber.toString().length : 0;

        EditProfileData.append('Email', userEmail);

        if (ContactNumberLength === 0) {
            console.log("Entered nil as input");
            EditProfileData.append('ContactNumber', location.state.ContactNumber);
        }
        else if (!isNaN(+ContactNumber)) {
            if (ContactNumberLength === 8) {
                console.log("Entered a valid number");
                EditProfileData.append('ContactNumber', ContactNumber);
            }
            else {
                console.log("Entered a invalid number length");
                errors.push("Please enter a valid phone number length");
            }
        }
        else {
            console.log("Entered a invalid number");
            errors.push("Please enter a valid phone number");
        }

        if (UsernameLength === 0) {
            EditProfileData.append('Username', location.state.Username);
        }
        else if (Username.match(/\W/)) {
            errors.push("Please do not enter special characters to your username");
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

            if (res.status === 201) {
                navigate('/MyProfile');
                window.location.reload(false);
            }
        }

    }

    return (
        <div className='mt-4'>
            <Container>
                {Authentication ?
                    <SessionTimeoutModal /> : null
                }
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
                                    <Form.Control type="text" placeholder={Username} value={Username} onChange={e => setUsername(e.target.value)} />
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
                                    <Form.Control type="text" placeholder={ContactNumber} value={ContactNumber} onChange={e => setContactNumber(e.target.value)} />
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