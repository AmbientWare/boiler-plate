import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

// material-ui
import { Toolbar, Box, AppBar, Link } from "@mui/material";
import { useTheme } from "@mui/material/styles";

// project imports
import LandingHeader from "./LandingHeader";
import LoginDialog from "@components/dialog/LoginDialog";
import InquireDialog from "@components/dialog/InquireDialog";
import SubscriptionDialog from "@components/dialog/SubscriptionDialog";
import Banner from "./sections/banner";

// ==============================|| LANDING PAGE ||============================== //

const LandingPage = () => {
  const theme = useTheme();
  const [loginDialogOpen, setLoginDialogOpen] = useState(false);
  const [loginDialogProps, setLoginDialogProps] = useState({});
  const [inquireDialogOpen, setInquireDialogOpen] = useState(false);
  const [subscriptionDialogOpen, setSubscriptionDialogOpen] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    // if on mobile device (for now relying on browser width to determine this, navigate to mobile landing page)
    if (window.innerWidth < 800) {
      navigate("/mobile");
    }
  }, [navigate]);

  useEffect(() => {
    setLoginDialogProps({
      title: "Login",
      confirmButtonName: "Login",
    });
  }, []);

  return (
    <>
      <Box>
        <AppBar
          enableColorOnDark
          position="fixed"
          color="inherit"
          elevation={1}
          sx={{
            bgcolor: theme.palette.background.default,
          }}
        >
          <Toolbar>
            <LandingHeader
              onLogin={() => setLoginDialogOpen(true)}
              onPricing={() => {
                setSubscriptionDialogOpen(true);
              }}
            />
          </Toolbar>
        </AppBar>
        <Box sx={{ height: "100vh", width: "100%" }}>
          <Box sx={{ height: "calc(100vh - 70px)" }}>
            <Banner
              onInquire={() => setInquireDialogOpen(true)}
              onVideoClick={() => {
                setSubscriptionDialogOpen(true);
              }}
            />
          </Box>

          {/* Footer */}
          <Box
            component="footer"
            sx={{
              mt: "auto",
              py: 3,
              bgcolor: "background.paper",
              textAlign: "center",
            }}
          >
            <Link color="textSecondary" href="/terms-and-conditions">
              Terms and Conditions
            </Link>
            <div style={{ display: "inline-block", width: "100px" }} />
            <Link color="textSecondary" href="/privacy-policy">
              Privacy Policy
            </Link>
            <div style={{ display: "inline-block", width: "100px" }} />
            <Link color="textSecondary" href="mailto:info@ambientware.co">
              Contact Us
            </Link>
          </Box>
        </Box>
      </Box>
      <LoginDialog
        show={loginDialogOpen}
        dialogProps={loginDialogProps}
        onClose={() => {
          setLoginDialogOpen(false);
        }}
      />
      <InquireDialog
        isOpen={inquireDialogOpen}
        onClose={() => setInquireDialogOpen(false)}
      />
      <SubscriptionDialog
        show={subscriptionDialogOpen}
        onCancel={() => {
          setSubscriptionDialogOpen(false);
        }}
      />
    </>
  );
};

export default LandingPage;
