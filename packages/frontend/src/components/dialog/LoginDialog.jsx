import { createPortal } from "react-dom";
import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import PropTypes from "prop-types";
import {
  Dialog,
  DialogContent,
  Typography,
  DialogTitle,
  Button,
  ButtonBase,
} from "@mui/material";

// API
import authApi from "@api/auth";
import { baseURL } from "@store/constant";
import { StyledButton } from "@components/button/StyledButton";
import { Input } from "@components/input/Input";
import GoogleImage from "@assets/images/google-assets/light/web_light_sq_ctn@2x.png";

const LoginDialog = ({
  show,
  onClose,
  dialogProps,
  showSignUpDialog = false,
}) => {
  const navigate = useNavigate();
  const showGoogleLogin = true; // set to true to show Google login button
  const useAccessCode = false; // set to true to require access code
  const portalElement = document.getElementById("portal");
  const accessInput = {
    label: "Access Code",
    name: "Access Code",
    type: "string",
  };
  const nameInput = {
    label: "Name",
    name: "name",
    type: "string",
  };
  const emailInput = {
    label: "Email",
    name: "email",
    type: "string",
  };
  const passwordInput = {
    label: "Password",
    name: "password",
    type: "password",
  };

  const [accessCodeVal, setAccessCodeVal] = useState("");
  const [nameVal, setNameVal] = useState("");
  const [emailVal, setEmailVal] = useState("");
  const [passwordVal, setPasswordVal] = useState("");
  const [showSignUp, setShowSignUp] = useState(showSignUpDialog);
  const [signUpMessage, setSignUpMessage] = useState("");
  const [showSignUpMessage, setShowSignUpMessage] = useState(false);

  const onLoginClick = async (name, email, password) => {
    const userInfo = {
      email: email,
      password: password,
    };

    if (showSignUp) {
      userInfo.name = name;
    }

    const api = showSignUp ? authApi.signUp : authApi.loginUser;

    api(userInfo)
      .then((response) => {
        if (response.status === 200) {
          // Handle successful login
          navigate(response.data.redirect_url);
        }
      })
      .catch((error) => {
        if (error.response && error.response.status === 401) {
          // Handle 401 Unauthorized response
          setSignUpMessage(error.response.data.detail);
          setShowSignUpMessage(true);
          setShowSignUp(true);
        } else if (error.response && error.response.status === 409) {
          // Handle 409 Conflict response
          setSignUpMessage(error.response.data.detail);
          setShowSignUpMessage(true);
          setShowSignUp(true);
        } else {
          // Handle other types of errors
          console.error(
            "Login error:",
            error.response ? error.response.data.detail : error.message
          );
        }
      });
  };

  const onGoogleLogin = async () => {
    window.location.href = `${baseURL}/api/v1/login/google`;
  };

  useEffect(() => {
    if (show) {
      setShowSignUp(showSignUpDialog);
    }
  }, [show, showSignUpDialog]);

  const component = show ? (
    <Dialog
      onKeyUp={async (e) => {
        if (e.key === "Enter") {
          await onLoginClick(nameVal, emailVal, passwordVal);
        }
      }}
      open={show}
      onClose={() => {
        onClose && onClose();
        setShowSignUp(false);
        setSignUpMessage("");
        setShowSignUpMessage(false);
      }}
      fullWidth
      maxWidth="xs"
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
    >
      <DialogTitle sx={{ fontSize: "1rem" }} id="alert-dialog-title">
        {showSignUp ? "Sign Up" : dialogProps.title}
      </DialogTitle>
      <DialogContent>
        {useAccessCode && (
          <div>
            <Typography>
              `Boilerplate` is undergoing beta testing. Please reach out for access!
            </Typography>
            <div style={{ marginTop: 20 }}></div>
          </div>
        )}
        {showSignUpMessage && (
          <div>
            <Typography sx={{ color: "red" }}>{signUpMessage}</Typography>
            <div style={{ marginTop: 20 }}></div>
          </div>
        )}
        {showSignUp && (
          <>
            <Typography>Name</Typography>
            <Input
              inputParam={nameInput}
              onChange={(newValue) => setNameVal(newValue)}
              value={setNameVal}
              showDialog={false}
            />
            <div style={{ marginTop: 20 }}></div>
          </>
        )}
        <Typography>Email</Typography>
        <Input
          inputParam={emailInput}
          onChange={(newValue) => setEmailVal(newValue)}
          value={emailVal}
        />
        <div style={{ marginTop: 20 }}></div>
        <Typography>Password</Typography>
        <Input
          inputParam={passwordInput}
          onChange={(newValue) => setPasswordVal(newValue)}
          value={passwordVal}
        />
        <div style={{ marginTop: 20 }}></div>
        {useAccessCode && (
          <div>
            <Typography>Access Code</Typography>
            <Input
              inputParam={accessInput}
              onChange={(newValue) => setAccessCodeVal(newValue)}
              value={accessCodeVal}
            />
            <div style={{ marginTop: 20 }}></div>
          </div>
        )}
        <ButtonBase
          onClick={() => setShowSignUp(!showSignUp)}
          style={{ padding: 0, minWidth: "auto" }}
        >
          <Typography
            component="span"
            sx={{ textDecoration: "underline", cursor: "pointer" }}
          >
            {showSignUp ? "Login" : "Sign Up"}
          </Typography>
        </ButtonBase>
        <div style={{ marginTop: 20 }}></div>
        <StyledButton
          variant="contained"
          fullWidth
          onClick={async () =>
            await onLoginClick(nameVal, emailVal, passwordVal)
          }
        >
          {showSignUp ? "Sign Up" : "Login"}
        </StyledButton>
        {/* Divider Line */}
        <div
          style={{ margin: "20px 0", borderTop: "1px solid #e0e0e0" }}
        ></div>{" "}
        {/* Adjust the margin and color as needed */}
        {/* Google Login Button */}
        {showGoogleLogin && (
          <div
            style={{ width: "100%", display: "flex", justifyContent: "center" }}
          >
            <div style={{ width: "50%" }}>
              <Button
                variant="contained"
                fullWidth
                onClick={onGoogleLogin}
                sx={{
                  padding: 0,
                  background: "none",
                  "&:hover": {
                    background: "none",
                  },
                }}
              >
                <img
                  src={GoogleImage}
                  alt="Login with Google"
                  style={{ width: "100%", height: "auto" }}
                />
              </Button>
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  ) : null;

  return createPortal(component, portalElement);
};

LoginDialog.propTypes = {
  show: PropTypes.bool,
  onClose: PropTypes.func,
  dialogProps: PropTypes.object,
  showSignUpDialog: PropTypes.bool,
};

export default LoginDialog;
