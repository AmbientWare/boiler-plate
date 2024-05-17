import { createPortal } from "react-dom";
import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import {
  Dialog,
  DialogContent,
  DialogTitle,
  Typography,
  Box,
} from "@mui/material";
import axios from "axios";

// project imports
import { baseURL } from "@store/constant";
import { StyledButton } from "@components/button/StyledButton";

const UpdateSubscriptionDialog = ({ show, updateShow }) => {
  const portalElement = document.getElementById("portal");

  const [data, setData] = useState({});
  const [message, setMessage] = useState("");

  const manageSubscriptionClick = async () => {
    const subscriptionDetails = await axios.get(
      `${baseURL}/api/v1/subscriptions/portal`
    );
    // redirect to subscription management portal
    window.location.href = subscriptionDetails.data;
  };

  useEffect(() => {
    const subscriptionDetails = axios.get(
      `${baseURL}/api/v1/subscriptions/user`
    );

    Promise.all([subscriptionDetails])
      .then(([subscriptionDetails]) => {
        setMessage(
          `Your subscription status is ${subscriptionDetails.data.status}. Please update your subscription.`
        );
        setData(subscriptionDetails.data);
        if (subscriptionDetails.data.status !== "active") {
          updateShow(true);
        }
      })
      .catch((error) => {
        console.error("Error fetching customer subscription data:", error);
      });

    // eslint-disable-next-line
  }, []);

  const component = show ? (
    <Dialog
      onClose={() => updateShow(false)}
      open={show}
      fullWidth
      maxWidth="sm"
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
    >
      <DialogTitle sx={{ fontSize: "2rem" }} id="alert-dialog-title">
        Update Your Subscription!
      </DialogTitle>
      <DialogContent>
        <Typography variant="body1" sx={{ pb: 2 }}>
          {message}
        </Typography>
        <Box sx={{ display: "flex", gap: 2 }}>
          <StyledButton
            type="submit"
            variant="contained"
            sx={{ color: "white" }}
            onClick={() => manageSubscriptionClick()}
          >
            {data.status === "trialing" ? "Manage Subscription" : "Subscribe"}
          </StyledButton>
          {data.status === "trialing" ? (
            <StyledButton
              type="submit"
              variant="contained"
              sx={{ color: "white" }}
              onClick={() => updateShow(false)}
            >
              Later
            </StyledButton>
          ) : null}
        </Box>
      </DialogContent>
    </Dialog>
  ) : null;

  return createPortal(component, portalElement);
};

UpdateSubscriptionDialog.propTypes = {
  show: PropTypes.bool,
  onCancel: PropTypes.func,
  showSubs: PropTypes.func,
};

export default UpdateSubscriptionDialog;
