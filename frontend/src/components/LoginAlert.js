import React, { useState, useRef } from 'react';
import Button from 'react-bootstrap/Button';
import Overlay from 'react-bootstrap/Overlay';
import Tooltip from 'react-bootstrap/Tooltip';

export function LoginAlert() {
    const [show, setShow] = useState(false);
    const target = useRef(null);

    return (
        <>
            <Button ref={target} onClick={() => setShow(!show)}>
                Offer
            </Button>
            <Overlay target={target.current} show={show} placement="top">
                {(props) => (
                    <Tooltip id="overlay-example" {...props}>
                        Oh Snap! Have you log in?
                    </Tooltip>
                )}
            </Overlay>
        </>
    );
}