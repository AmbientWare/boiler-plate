import { Box } from "@mui/material";
import { Link } from "@mui/material";

export default function Footer() {
  return (
    <>
      <Box
        component="footer"
        display={"flex"}
        justifyContent={"center"}
        sx={{
          mt: "80px",
          py: 3,
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
        <Link color="textSecondary" href="mailto:info@callmates.com">
          Contact Us
        </Link>
      </Box>
      ;
    </>
  );
}

Footer.propTypes = {};
