import React, { useState, useEffect } from 'react'
import { Container, Row, Col, Button } from 'react-bootstrap'
import OTPInput, { ResendOTP } from "otp-input-react";
import { useNavigate, useLocation } from 'react-router-dom';
import secureLocalStorage from "react-secure-storage";
import { createClient } from '@supabase/supabase-js';

function OTP() {
    const [errorMessages, setErrorMessages] = useState([]);
    const [showErrors, setShowErrors] = useState(false);
    const [isLoaded, setIsLoaded] = useState(false);
    const [contactNum, setContactNum] = useState("");
    const [otp, setOTP] = useState("");
    const location = useLocation();

    const navigate = useNavigate();

    // For OTP Button and Time Design
    const renderButton = (buttonProps) => {
        return (
            <Button id="reSendID" variant="primary" hidden type="submit" {...buttonProps}>
                {buttonProps.remainingTime !== 0 ? `Resend in ${buttonProps.remainingTime} sec` : "Resend"}
            </Button>
        )
    };
    const renderTime = () => React.Fragment;

    // Fetch Contact Number from the User
    useEffect(() => {
        if (location.state.Route !== undefined) {
            fetch('/apis/user/get_user_profile?Email=' + location.state.Email)
                .then(res => res.json())
                .then(data => {
                    setIsLoaded(true);
                    setContactNum("+65" + data[0].ContactNumber);
                },
                    (error) => {
                        setIsLoaded(true);
                        setErrorMessages(error);
                    }
                )
        }
        else {
            return navigate('/');
        }
    }, [])

    // Initialise the Supabase client
    const supabaseUrl = process.env.REACT_APP_OTP_URL
    const supabaseAnonKey = process.env.REACT_APP_OTP_SECRET_KEY
    const supabase = createClient(supabaseUrl, supabaseAnonKey)

    // Send OTP to the User Contact Number
    const SendOTP = async () => {
        let { error } = await supabase.auth.signInWithOtp({
            phone: contactNum
        })
        if (error) {
            setErrorMessages(error)
            return
        }
    }

    // Verify the OTP
    const VerifyCode = async () => {
        let errors = [];
        setErrorMessages([]);
        let { session, error } = await supabase.auth.verifyOtp({
            phone: contactNum,
            token: otp,
            type: "sms"
        })
        if (error) {
            setShowErrors({ showErrors: true });
            setErrorMessages(errors);
            errors.push("Token has Expired or is Invalid.");
            return
        } else {
            secureLocalStorage.setItem("Authentication", location.state.authentication);
            secureLocalStorage.setItem("Email", location.state.Email);
            secureLocalStorage.setItem("Role", location.state.Role);
            navigate("/");
            window.location.reload(false);
        }
    }

    // To toggle the SendOTP Button, Resend Button and Verify Button
    let toggle = () => {
        let sendOTPBtn = document.getElementById("sendFirstOtpID");
        let resendBtn = document.getElementById("reSendID");
        let verifyBtn = document.getElementById("verifyCodeID");
        let space = document.getElementById("space");
        SendOTP();
        resendBtn.removeAttribute("hidden");
        verifyBtn.removeAttribute("hidden");
        space.removeAttribute("hidden");
        sendOTPBtn.style.display = "none";
    }

    return (
        <Container>
            <div className="d-flex justify-content-center mt-4">
                <Row><Col><h1>Two Factor Authentication</h1></Col></Row>
            </div>
            <div className="d-flex justify-content-center mt-1 mb-4">
                <Row><Col><h6>Enter the OTP</h6></Col></Row>
            </div>
            <div className="justify-content-center mt-4 mb-2" id="otpInput">
                <OTPInput className="justify-content-center mt-4 mb-4"
                    value={otp} onChange={setOTP} autoFocus
                    OTPLength={6} otpType="number" disabled={false} secure
                />
            </div>
            <div className="d-flex justify-content-center">
                {showErrors ? errorMessages.map((item, index) => {
                    return <ul style={{ color: "red" }} key={index}>{item}</ul>;
                }) : null}
            </div>
            <div className="d-flex justify-content-center">
                <Row className="mt-2">
                    <Col>
                        <ResendOTP
                            maxTime={30}
                            onTimerComplete={() => console.log("Times up!")}
                            onResendClick={() => SendOTP()}
                            renderButton={renderButton} renderTime={renderTime}
                        />
                    </Col>
                </Row>
                <Row className="mt-2">
                    <Col>
                        <Button variant="primary" type="submit" id="sendFirstOtpID" onClick={toggle}>
                            SendOTP
                        </Button>
                    </Col>
                </Row>
                <Row className="col-sm-1 mt-2" id="space" hidden><span></span></Row>
                <Row className="mt-2">
                    <Col>
                        <Button variant="primary" type="submit" id="verifyCodeID" onClick={VerifyCode} hidden>
                            Verify Code
                        </Button>
                    </Col>
                </Row>
            </div>
        </Container >
    )
}

export default OTP;