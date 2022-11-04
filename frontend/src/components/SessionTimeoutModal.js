import React, { useState, useEffect } from 'react';
import { Modal, ModalHeader, ModalBody, ModalFooter } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import secureLocalStorage from "react-secure-storage";


function SessionTimeoutModal() {
    //Modal
    const [idleModal, setIdleModal] = useState(false);
    const navigate = useNavigate();

    let idleTimeout = 1000 * 60 * 15;  //15 minute
    let idleLogout = 1000 * 60 * 30; //30 Minutes
    let idleEvent;
    let idleLogoutEvent;

    const Email = secureLocalStorage.getItem('Email');
    const LogoutData = new FormData();

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
        clearTimeout(idleEvent);
        clearTimeout(idleLogoutEvent);
        setIdleModal(false);
    }


    /**
     * @method logOut
     * This function will destroy current user session.
     */
    const logOut = async (e) => {
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

        console.log(trimmedResponseMessage);

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
                <button className="btn btn-danger" onClick={(e) => logOut(e)}>Logout</button>
            </ModalFooter>
        </Modal>
    )

}

export default SessionTimeoutModal;