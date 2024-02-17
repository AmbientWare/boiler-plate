import PropTypes from "prop-types";

// material-ui
import { Box } from "@mui/material";

// icons
import { IconLogin } from "@tabler/icons-react";

// project imports
import LogoSection from "@layout/MainLayout/LogoSection";
import { StyledButton } from "@components/button/StyledButton";

// ==============================|| CANVAS HEADER ||============================== //

const LandingHeader = ({ onLogin, onPricing }) => {
  return (
    <>
      <Box
        component="span"
        sx={{ display: { xs: "none", md: "block" }, flexGrow: 1 }}
      >
        <LogoSection />
      </Box>
      <Box sx={{ flexGrow: 1 }}>{/* additional elements here */}</Box>
      <Box>
        <StyledButton
          variant="contained"
          color="secondary"
          sx={{ mr: "10px", color: "white" }}
          onClick={onPricing}
        >
          Pricing
        </StyledButton>
        <StyledButton
          variant="contained"
          color="secondary"
          onClick={onLogin}
          startIcon={<IconLogin />}
        >
          Login / Signup
        </StyledButton>
      </Box>
    </>
  );
};

LandingHeader.propTypes = {
  onLogin: PropTypes.func,
  onPricing: PropTypes.func,
};

export default LandingHeader;
