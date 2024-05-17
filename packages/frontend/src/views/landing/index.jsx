import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

// material-ui
import { Toolbar, Box, AppBar } from "@mui/material";
import { useTheme } from "@mui/material/styles";

// project imports
import LandingHeader from "./LandingHeader";
import { LandingStyles } from "./sections/styles";
import LoginDialog from "@components/dialog/LoginDialog";
import InquireDialog from "@components/dialog/InquireDialog";
import SubscriptionDialog from "@components/dialog/SubscriptionDialog";
import Banner from "./sections/banner";
import Features from "./sections/features";
import Footer from "./sections/footer";
import Reviews from "./sections/reviews";
import { PixelGrid } from "@components/pixelGrid/pixelGrid";

// ==============================|| LANDING PAGE ||============================== //

const LandingPage = () => {
  const theme = useTheme();
  const [loginDialogOpen, setLoginDialogOpen] = useState(false);
  const [loginDialogProps, setLoginDialogProps] = useState({});
  const [showSignUp, setShowSignUp] = useState(false);
  const [inquireDialogOpen, setInquireDialogOpen] = useState(false);
  const [subscriptionDialogOpen, setSubscriptionDialogOpen] = useState(false);

  const navigate = useNavigate();

  // useEffect(() => {
  //   // if on mobile device (for now relying on browser width to determine this, navigate to mobile landing page)
  //   if (window.innerWidth < 800) {
  //     navigate("/mobile");
  //   }
  // }, [navigate]);

  useEffect(() => {
    setLoginDialogProps({
      title: "Login",
      confirmButtonName: "Login",
    });
  }, []);

  return (
    <Box
      display={"flex"}
      flexDirection={"row"}
      alignContent={"center"}
      justifyContent={"center"}
      position={"relative"}
    >
      <Box sx={LandingStyles.pixelGridContainer}>
        <PixelGrid />
      </Box>
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
      <Box
        display={"flex"}
        flexDirection={"column"}
        width={"80%"}
        justifyContent={"center"}
        mt={{ xs: 15, sm: 15, md: 20 }}
        zIndex={1}
        sx={{ pointerEvents: "none" }}
      >
        {/* Banner */}
        <Banner
          onInquire={() => setInquireDialogOpen(true)}
          onSignUp={() => {
            setShowSignUp(true);
            setLoginDialogOpen(true);
          }}
        />

        {/* Features */}
        <Features />

        {/* Reviews */}
        <Reviews />

        {/* Footer */}
        <Footer />
      </Box>
      <LoginDialog
        show={loginDialogOpen}
        dialogProps={loginDialogProps}
        onClose={() => {
          setShowSignUp(false);
          setLoginDialogOpen(false);
        }}
        showSignUpDialog={showSignUp}
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
    </Box>
  );
};

export default LandingPage;
