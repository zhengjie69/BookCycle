import React from 'react'
import Container from 'react-bootstrap/Container'
import { Nav, Navbar, Button } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap'
import Login from './Login'
import { useNavigate } from 'react-router-dom'
import secureLocalStorage from "react-secure-storage";

const NavBarComp = () => {
    const navigate = useNavigate();
    const Authentication = secureLocalStorage.getItem('Authentication');
    const Role = secureLocalStorage.getItem('Role');
    const Email = secureLocalStorage.getItem('Email');

    function LogOut() {
        secureLocalStorage.removeItem('Authentication');
        secureLocalStorage.removeItem('Email');
        secureLocalStorage.removeItem('Role');
        navigate('/')
        window.location.reload(false);
    }

    return (
        <Navbar bg="light" expand="lg" >
            <Container>
                <LinkContainer to="/">
                    <Navbar.Brand>BookCycle</Navbar.Brand>
                </LinkContainer>
                <Navbar.Toggle aria-controls="basic-navbar-nav" />
                <Navbar.Collapse id="basic-navbar-nav" className="justify-content-end">
                    <Nav className="mr-auto">
                        {Authentication && Role === "User" ?
                            <LinkContainer to="/MyOffers">
                                <Nav.Link>My Offers</Nav.Link>
                            </LinkContainer> : null
                        }
                        {Authentication && Role === "User" ?
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
                        {Authentication ?
                            <LinkContainer to="/MyProfile">
                                <Nav.Link>My Profile</Nav.Link>
                            </LinkContainer> : null
                        }
                        {!Authentication ? <Login /> : null}
                        {Authentication ?
                            <Button variant='primary' to='/' onClick={LogOut}> Logout</Button> : null
                        }
                        {/* <NavDropdown title="Dropdown" id="basic-nav-dropdown">
                                    <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                                    <NavDropdown.Item href="#action/3.2">
                                        Another action
                                    </NavDropdown.Item>
                                    <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
                                    <NavDropdown.Divider />
                                    <NavDropdown.Item href="#action/3.4">
                                        Separated link
                                    </NavDropdown.Item>
                                </NavDropdown> */}
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    )
};

export default NavBarComp;