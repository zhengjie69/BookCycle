import React from 'react'
import { Container, Row, Col, Form, Button } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'

const ForgetPassword = () => {
    return (
        <Container>
            <div className="d-flex justify-content-center mt-4">
                <Row><Col><h1>Reset Password</h1></Col></Row>
            </div>
            <div className="d-flex justify-content-center mt-1 mb-4">
                <Row><Col><h6>Enter the email address of your account</h6></Col></Row>
            </div>
            <div className="justify-content-center mt-4 mb-2">
                <Form>
                    <Row>
                        <Form.Group as={Row} className="mb-3" controlId="formName">
                            <Col md={{ span: 6, offset: 3 }}>
                                <Form.Control type="text" placeholder="Your Email" />
                            </Col>
                        </Form.Group>
                    </Row>
                </Form>
            </div>
            <div className="d-flex justify-content-center mt-2 mb-4">
                <Row>
                    <Col>
                        <LinkContainer to="/">
                            <Button variant="primary" type="submit">
                                Send a Password Reset Link
                            </Button>
                        </LinkContainer>
                    </Col>
                </Row>
            </div>
        </Container >
    )
};

export default ForgetPassword;