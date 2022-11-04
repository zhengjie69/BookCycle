import React, { useEffect, useState } from "react";
import { Container, Form, Col, Row, Button } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import { useNavigate } from "react-router-dom";
import SessionTimeoutModal from "../../components/SessionTimeoutModal";
import secureLocalStorage from "react-secure-storage";

export default function ManageAdmin() {

    const Role = secureLocalStorage.getItem('Role');
    const Authentication = secureLocalStorage.getItem('Authentication');
    const SuperAdminEmail = secureLocalStorage.getItem('Email');
    const navigate = useNavigate();

    const [AdminEmail, setAdminEmail] = useState();

    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);

    const AdminResultData = new FormData();

    let errors = [];

    function isValidEmail(email) {
        return /\S+@\S+\.\S+/.test(email);
    }

    useEffect(() => {
        if (!Authentication || Role !== "SuperAdmin") {
            return navigate('/');
        }
    }, [])


    const postAdminSearch = async (e) => {

        e.preventDefault();

        setErrorMessages([]);

        const AdminEmailLength = AdminEmail ? AdminEmail.length : 0;

        if (AdminEmailLength !== 0 && isValidEmail(AdminEmail)) {
            AdminResultData.append('AdminEmail', AdminEmail);
            AdminResultData.append('SuperAdminEmail', SuperAdminEmail);

            const res = await fetch('/apis/superadmin/search_admin', {
                method: "POST",
                body: AdminResultData
            });

            const data = await res.json();

            if (data[0].ContactNumber !== undefined && data[0].AccountStatus !== undefined && data[0].Username !== undefined) {
                navigate('/ManageAdmin/ManageAdminResult', {
                    state: {
                        AdminEmail: AdminEmail,
                        Username: data[0].Username,
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
                        <h1>Manage Administrators</h1>
                    </Row>
                </div>
                <div className="row h-100 justify-content-center align-items-center">
                    <Form className="mt-4 me-3" onSubmit={postAdminSearch}>
                        <Row>
                            <Form.Group as={Row} className="mb-3">
                                <Col xs={11}>
                                    <Form.Control type="text" placeholder="Search For Administrator (Using Email)" value={AdminEmail} onChange={e => setAdminEmail(e.target.value)} />
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
                                return <ul style={{ color: "red" }} key={index}>{item}</ul>;
                            }) : null}
                        </Row>
                    </Form>
                </div>
                <div className="d-flex align-items-center justify-content-center mt-4">
                    <LinkContainer to="/CreateAdmin">
                        <Button>Create Administrator</Button>
                    </LinkContainer>
                </div>
            </Container>
        </div>
    );
}