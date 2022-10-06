import { Form, Row, Col, Button } from "react-bootstrap"

export function SearchBar() {
    return (
        <div className="row h-100 justify-content-center align-items-center">
            <Form className="mt-4 me-3">
                <Row>
                    <Form.Group as={Row} className="mb-3">
                        <Col xs={11}>
                            <Form.Control type="text" placeholder="Search For Books" />
                        </Col>
                        <Col xs={1}>
                            <Button type="submit">
                                <span className="material-symbols-outlined">
                                    search
                                </span>
                            </Button>
                        </Col>
                    </Form.Group>
                </Row>
            </Form>
        </div>
    )
}