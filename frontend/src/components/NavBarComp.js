import React from 'react'
import Container from 'react-bootstrap/Container'
import { Nav, Navbar, Button, Form } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'
import Login from './Login'
import { useNavigate } from 'react-router-dom'
import secureLocalStorage from "react-secure-storage";


const NavBarComp = () => {
    const navigate = useNavigate();
    const Authentication = secureLocalStorage.getItem('Authentication');
    const Role = secureLocalStorage.getItem('Role');
    const Email = secureLocalStorage.getItem('Email');
    const LogoutData = new FormData();
    const OTPpage = window.location.pathname === "/OTP";
    
    const LogOut = async (e) => {

        e.preventDefault();

        LogoutData.append('Email', Email);

        const res = await fetch('/apis/user/logout', {
            method: "POST",
            body: LogoutData
        });

        secureLocalStorage.removeItem('Authentication');
        secureLocalStorage.removeItem('Email');
        secureLocalStorage.removeItem('Role');

        const data = await res.json();

        const trimmedResponseMessage = JSON.stringify(data).replace(/[^a-zA-Z ]/g, "");

        //console.log(trimmedResponseMessage);

        if (trimmedResponseMessage === "Successfully logged out") {
            navigate('/');
            window.location.reload(false);
        }
        else {
            alert("Failed to logout");
        }

        navigate('/');
        window.location.reload(false);
    }

    return (
        <Navbar className="navbar navbar-dark bg-dark" expand="lg">
            <Container>
                {OTPpage ?
                    <Navbar.Brand>BookCycle</Navbar.Brand>: null
                }
                {!OTPpage ?
                    <LinkContainer to="/">
                        <Navbar.Brand>BookCycle</Navbar.Brand>
                    </LinkContainer> : null
                }
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav" className="justify-content-end">
                    <Nav className="mr-auto">
                        {Authentication && Role === "User" && !OTPpage ?
                            <LinkContainer to="/MyOffers">
                                <Nav.Link>My Offers</Nav.Link>
                            </LinkContainer> : null
                        }
                        {Authentication && Role === "User" && !OTPpage ?
                            <LinkContainer to="/MyListings">
                                <Nav.Link>My Listings</Nav.Link>
                            </LinkContainer> : null
                        }
                        {Authentication && Role === "Admin" ?
                            <LinkContainer to="/ManageBooks">
                                <Nav.Link>Manage Books</Nav.Link>
                            </LinkContainer> : null
                        }
                        {Authentication && Role === "Admin" ?
                            <LinkContainer to="/ManageUsers">
                                <Nav.Link>Manage Users</Nav.Link>
                            </LinkContainer> : null
                        }
                        {Authentication && Role === "SuperAdmin" ?
                            <LinkContainer to="/ManageAdmin">
                                <Nav.Link>Manage Administrators</Nav.Link>
                            </LinkContainer> : null
                        }
                        {Authentication && !OTPpage ?
                            <LinkContainer to="/MyProfile">
                                <Nav.Link>My Profile</Nav.Link>
                            </LinkContainer> : null
                        }
                        {!Authentication && !OTPpage ? <Login /> : null}
                        {Authentication && !OTPpage ?
                            <Button variant='primary' onClick={(e) => LogOut(e)}>Logout</Button> : null
                        }
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    )
};

export default NavBarComp;