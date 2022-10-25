import React, { useEffect, useState } from "react";
import { Container, Table, Row, Col } from "react-bootstrap";
import { useLocation, useNavigate } from "react-router-dom";
import DisableUserModal from "../../components/DisableUserModal";
import SessionTimeoutModal from "../../components/SessionTimeoutModal";
import EnableUserModal from "../../components/EnableUserModal";

export default function UsersResult() {
    const location = useLocation();
    const navigate = useNavigate();

    const Authentication = localStorage.getItem("Authentication");
    const Role = localStorage.getItem("Role");

    const [UserEmail, setUserEmail] = useState('');
    const [Username, setUsername] = useState('');
    const [ContactNumber, setContactNumber] = useState('');
    const [AccountStatus, setAccountStatus] = useState('');

    useEffect(() => {
        if (Authentication === "true" && Role === "Admin") {
            setUserEmail(location.state.UserEmail);
            setUsername(location.state.Username);
            setContactNumber(location.state.ContactNumber);
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
                    <h1>Manage User</h1>
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
                                <td>{UserEmail}</td>
                            </tr>
                            <tr>
                                <td>
                                    <span className="material-symbols-outlined">
                                        chat
                                    </span>
                                </td>
                                <td>{ContactNumber}</td>
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
                        {AccountStatus == "Active" ?
                            <DisableUserModal UserEmail={UserEmail} Username={Username} /> : null
                        }
                        {AccountStatus == "Disabled" ?
                            <EnableUserModal UserEmail={UserEmail} Username={Username} /> : null
                        }
                    </div>
                </div>
            </Container>
        </div>
    );
}