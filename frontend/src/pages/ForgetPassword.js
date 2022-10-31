import React, {useEffect} from 'react'
import { Container, Row, Col, Form, Button } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'
import { useNavigate } from 'react-router-dom';
import {useState} from 'react';


function ForgetPassword() {
    const navigate = useNavigate()
    const [Email, setEmail] = useState();
    const resetPasswordDetails = new FormData();

    const postForgetPassword = async (e) => {

         resetPasswordDetails.append('Email', Email)
         e.preventDefault();

         const res = await fetch('/apis/user/forget_password_reset', {
            method: "POST",
            body: resetPasswordDetails
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
                <Row><Col><h1>Request Password Reset</h1></Col></Row>
            </div>
            <form onSubmit={postForgetPassword}>
            <div className="d-flex justify-content-center mt-1 mb-4">
                <Row><Col><h6>Enter the email address of your account</h6></Col></Row>
            </div>
            <div className="justify-content-center mt-4 mb-2">
                <Form>
                    <Row>
                        <Form.Group as={Row} className="mb-3" controlId="formName">
                            <Col md={{ span: 6, offset: 3 }}>
                                <Form.Control type="text" placeholder="Your Email"  value={Email} onChange={e => setEmail(e.target.value)}/>
                            </Col>
                        </Form.Group>
                    </Row>
                </Form>
            </div>
            <div className="d-flex justify-content-center mt-2 mb-4">
                <Row>
                    <Col>
                        <LinkContainer to="/">
                            <Button variant="primary" type="submit" onClick={postForgetPassword}>
                                Send a Password Reset Link
                            </Button>
                        </LinkContainer>
                    </Col>
                </Row>
            </div>
            </form>
        </Container >
    )
};

export default ForgetPassword;