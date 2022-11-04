import React, { useEffect, useState } from "react";
import { Container, Form, Col, Row, Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import SessionTimeoutModal from "../../components/SessionTimeoutModal";
import secureLocalStorage from "react-secure-storage";

export default function ManageUsers() {

    const Role = secureLocalStorage.getItem('Role');
    const Authentication = secureLocalStorage.getItem('Authentication');
    const AdminEmail = secureLocalStorage.getItem('Email');
    const navigate = useNavigate();

    const [UserEmail, setUserEmail] = useState();

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    const UserResultData = new FormData();

    let errors = [];

    function isValidEmail(email) {
        return /\S+@\S+\.\S+/.test(email);
    }

    useEffect(() => {
        if (!Authentication && Role !== "Admin") {
            return navigate('/');
        }
    }, [])


    const postUserSearch = async (e) => {

        e.preventDefault();

        setErrorMessages([]);

        const UserEmailLength = UserEmail ? UserEmail.length : 0;

        if (UserEmailLength !== 0 && isValidEmail(UserEmail)) {
            UserResultData.append('UserEmail', UserEmail);
            UserResultData.append('AdminEmail', AdminEmail);

            const res = await fetch('/apis/admin/search_user', {
                method: "POST",
                body: UserResultData
            });

            const data = await res.json();

            //console.log(data[0].ContactNumber);

            if (data[0].ContactNumber !== undefined && data[0].AccountStatus !== undefined && data[0].Username !== undefined) {
                navigate('/ManageUsers/ManageUsersResult', {
                    state: {
                        UserEmail: UserEmail,
                        ContactNumber: data[0].ContactNumber,
                        AccountStatus: data[0].AccountStatus,
                        Username: data[0].Username
                    }
                });
                window.location.reload(false);
            }

            else {
                errors.push("The email of the user entered is not found");
                setShowErrors({ showErrors: true });
                setErrorMessages(errors);
            }
        }
        else {
            errors.push("Please enter a valid email");
            setShowErrors({ showErrors: true });
            setErrorMessages(errors);
        }
    }

    return (
        <div className="mt-5 pt-5">
            <Container>
                {Authentication ?
                    <SessionTimeoutModal /> : null
                }
                <div className="d-flex align-items-center justify-content-center mb-4">
                    <Row>
                        <h1>Manage Users</h1>
                    </Row>
                </div>
                <div className="row h-100 justify-content-center align-items-center">
                    <Form className="mt-4 me-3" onSubmit={postUserSearch}>
                        <Row>
                            <Form.Group as={Row} className="mb-3">
                                <Col xs={11}>
                                    <Form.Control type="text" placeholder="Search For User (Using Email)" value={UserEmail} onChange={e => setUserEmail(e.target.value)} />
                                </Col>
                                <Col xs={1}>
                                    <Button variant="primary" type="submit">
                                        <span className="material-symbols-outlined">
                                            search
                                        </span>
                                    </Button>
                                </Col>
                            </Form.Group>
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
    );
}