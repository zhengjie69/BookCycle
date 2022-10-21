import React, { useState, useEffect } from 'react'
import { Container } from 'react-bootstrap'
import Table from 'react-bootstrap/Table'
import Button from 'react-bootstrap/Button'
import { LinkContainer } from 'react-router-bootstrap'
import { useNavigate } from 'react-router-dom';

function MyProfile() {

    const [error, setError] = useState(null);
    const [isLoaded, setIsLoaded] = useState(false);
    const userEmail = localStorage.getItem('Email');
    const [profileInformation, setProfileInformation] = useState([]);
    const Authentication = localStorage.getItem('Authentication');

    const navigate = useNavigate();

    useEffect(() => {
        if (userEmail !== null && Authentication === "true") {
            fetch('/apis/user/get_user_profile?Email=' + userEmail)
                .then(res => res.json())
                .then(data => {
                    setIsLoaded(true);
                    setProfileInformation(data);
                },
                    (error) => {
                        setIsLoaded(true);
                        setError(error);
                    }
                )
        }
        else {
            return navigate('/');
        }
    }, [])

    return (
        <div className="mt-4">
            <Container>
                <div className="d-flex justify-content-center">
                    <div className="row">
                        {Array.isArray(profileInformation) ?
                            profileInformation.map(profileInformation => (
                                <div className="col-sm">
                                    <h1>My Profile</h1>
                                    <Table borderless>
                                        <tbody>
                                            <tr>
                                                <td className="d-flex justify-content-center">
                                                    <span className="material-symbols-outlined">
                                                        person
                                                    </span>
                                                </td>
                                                <td>{profileInformation.Username}</td>
                                            </tr>
                                            <tr>
                                                <td className="d-flex justify-content-center">
                                                    <span className="material-symbols-outlined">
                                                        mail
                                                    </span>
                                                </td>
                                                <td>{userEmail}</td>
                                            </tr>
                                            <tr>
                                                <td className="d-flex justify-content-center">
                                                    <span className="material-symbols-outlined">
                                                        chat
                                                    </span>
                                                </td>
                                                <td>{profileInformation.ContactNumber}</td>
                                            </tr>
                                        </tbody>
                                    </Table>
                                    <Table borderless>
                                        <tbody>
                                            <tr className="d-flex justify-content-center">
                                                <td>
                                                    <Button onClick={() => {
                                                        navigate('/MyProfile/EditProfile', {
                                                            state: {
                                                                Username: profileInformation.Username,
                                                                ContactNumber: profileInformation.ContactNumber,
                                                            }
                                                        });
                                                    }}>Edit Profile</Button>
                                                </td>
                                            </tr>
                                            <tr className="d-flex justify-content-center">
                                                <td>
                                                    <LinkContainer to="/MyProfile/ChangePassword">
                                                        <Button>Change Password</Button>
                                                    </LinkContainer>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </Table>
                                </div>
                            )) : null
                        }
                    </div>
                </div>
            </Container>
        </div>
    )
};

export default MyProfile;