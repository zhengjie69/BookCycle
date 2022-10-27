import React, { useEffect, useState } from "react";
import { Container, Table, Row, Col } from "react-bootstrap";
import { useLocation, useNavigate } from "react-router-dom";
import SessionTimeoutModal from "../../components/SessionTimeoutModal";
import DeleteAdminModal from "../../components/DeleteAdminModal";
import DisableAdminModal from "../../components/DisableAdminModal"

export default function ManageAdminResult() {
    const location = useLocation();
    const navigate = useNavigate();

    const Authentication = localStorage.getItem("Authentication");
    const Role = localStorage.getItem("Role");

    const [AdminEmail, setAdminEmail] = useState('');
    const [Username, setUsername] = useState('');
    const [AccountStatus, setAccountStatus] = useState('');

    useEffect(() => {
        if (Authentication === "true" && Role === "SuperAdmin") {
            setAdminEmail(location.state.AdminEmail);
            setUsername(location.state.Username);
            setAccountStatus(location.state.AccountStatus);
        }
        else {
            navigate('/');
        }
    }, [])

    return (
        <div className="mt-4">
            <Container>
                {Authentication === "true" ?
                    <SessionTimeoutModal /> : null
                }
                <div className="d-flex justify-content-center align-items-center">
                    <h1>Manage Administrator</h1>
                </div>
                <div className="d-flex justify-content-center align-items-center">
                    <div className="row">
                        <Table>
                            <tr>
                                <td>
                                    <span className="material-symbols-outlined">
                                        person
                                    </span>
                                </td>
                                <td>{Username}</td>
                            </tr>
                            <tr>
                                <td>
                                    <span className="material-symbols-outlined">
                                        mail
                                    </span>
                                </td>
                                <td>{AdminEmail}</td>
                            </tr>
                            <tr>
                                <td>
                                    <span className="material-symbols-outlined">
                                        Autorenew
                                    </span>
                                </td>
                                <td>{AccountStatus}</td>
                            </tr>
                        </Table>
                        <Row>
                            {AccountStatus === "Active" ?
                                <DisableAdminModal AdminEmail={AdminEmail} Username={Username} /> : null
                            }
                        </Row>
                        <Row>
                            <DeleteAdminModal AdminEmail={AdminEmail} Username={Username} />
                        </Row>
                    </div>
                </div>
            </Container>
        </div>
    );
}