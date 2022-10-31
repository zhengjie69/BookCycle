import React from 'react'
import Alert from "bootstrap/js/src/alert";
import { Container, Row, Col, Form, Button } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'
import { useNavigate,useParams } from 'react-router-dom';
import {useState, useEffect} from 'react';
import secureLocalStorage from "react-secure-storage";

function ResetPage() {
    const navigate = useNavigate()
    const [Password, setPassword] = useState();
    const { resetCode } = useParams()
    const verifiedresetpasswords = new FormData();

    const changingPassword = async (e) => {

        const res = await fetch('/apis/user/ForgetResetPassword/'+(JSON.stringify(resetCode)).replace(/\"/g, ""), {
            method: "GET",
        });
        if (res.status === 404)
        {

              navigate('/');
              window.location.reload(false);
        }

    }

    useEffect(() => {
        changingPassword()
    }, []);

    const verifiedchangingpassword = async (e) => {
        verifiedresetpasswords.append('Password',Password)
        const res = await fetch('/apis/user/ForgetResetPassword/'+(JSON.stringify(resetCode)).replace(/\"/g, ""), {
            method: "POST",
            body: verifiedresetpasswords
        });
        if (res.status === 201)
        {

            navigate('/');
            window.location.reload(false);

        }
    }
    return (
        <Container>
            <div className="d-flex justify-content-center mt-4">
                <Row><Col><h1>Reset Password</h1></Col></Row>
            </div>
            <form onSubmit={verifiedchangingpassword}>
            <div className="d-flex justify-content-center mt-1 mb-4">
                <Row><Col><h6>Enter the new passowrd</h6></Col></Row>
            </div>
            <div className="justify-content-center mt-4 mb-2">
                <Form>
                    <Row>
                        <Form.Group as={Row} className="mb-3" controlId="formName">
                            <Col md={{ span: 6, offset: 3 }}>
                                <Form.Control type="password" placeholder="Your Password"  value={Password} onChange={e => setPassword(e.target.value)}/>
                            </Col>
                        </Form.Group>
                    </Row>
                </Form>
            </div>
            <div className="d-flex justify-content-center mt-2 mb-4">
                <Row>
                    <Col>
                        <LinkContainer to="/">
                            <Button variant="primary" type="submit" onClick={verifiedchangingpassword} >
                                Submit
                            </Button>
                        </LinkContainer>
                    </Col>
                </Row>
            </div>
        </form>
        </Container >
    )
};

export default ResetPage;