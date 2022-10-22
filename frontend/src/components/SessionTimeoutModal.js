import React, { useState, useEffect } from 'react';
import { Modal, ModalHeader, ModalBody, ModalFooter } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';


function SessionTimeoutModal() {
    //Modal
    const [idleModal, setIdleModal] = useState(false);
    const navigate = useNavigate();

    let idleTimeout = 1000 * 60 * 1;  //1 minute
    let idleLogout = 1000 * 60 * 2; //2 Minutes
    let idleEvent;
    let idleLogoutEvent;

    /**
     * Add any other events listeners here
     */
    const events = [
        'mousemove',
        'click',
        'keypress'
    ];


    /**
     * @method sessionTimeout
     * This function is called with each event listener to set a timeout or clear a timeout.
     */
    const sessionTimeout = () => {
        if (!!idleEvent) clearTimeout(idleEvent);
        if (!!idleLogoutEvent) clearTimeout(idleLogoutEvent);

        idleEvent = setTimeout(() => setIdleModal(true), idleTimeout); //show session warning modal.
        idleLogoutEvent = setTimeout(() => logOut(), idleLogout); //Call logged out on session expire.
    };

    /**
     * @method extendSession
     * This function will extend current user session.
     */
    const extendSession = () => {
        setIdleModal(false)
    }


    /**
     * @method logOut
     * This function will destroy current user session.
     */
    const logOut = () => {
        setIdleModal(false);
        localStorage.removeItem('Authentication');
        localStorage.removeItem('Email');
        localStorage.removeItem('Role');
        navigate('/')
        window.location.reload(false);
    }

    useEffect(() => {
        for (let e in events) {
            window.addEventListener(events[e], sessionTimeout);
        }

        return () => {
            for (let e in events) {
                window.removeEventListener(events[e], sessionTimeout);
            }
        }
    }, []);


    return (

        <Modal show={idleModal} toggle={() => setIdleModal(false)}>
            <ModalHeader toggle={() => setIdleModal(false)}>
                <b>Session expire warning</b>
            </ModalHeader>
            <ModalBody>
                Your session will expire in {idleLogout / 60 / 1000} minutes. Do you want to extend the session?
            </ModalBody>
            <ModalFooter>
                <button className="btn btn-primary" onClick={() => extendSession()}>Extend session</button>
                <button className="btn btn-danger" onClick={() => logOut()}>Logout</button>
            </ModalFooter>
        </Modal>
    )

}

export default SessionTimeoutModal;