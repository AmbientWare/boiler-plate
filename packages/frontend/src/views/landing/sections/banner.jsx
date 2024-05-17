import { useEffect, useState } from "react";
import { PropTypes } from "prop-types";
import { Box, Typography } from "@mui/material";
import { IconInfoSquareRounded, IconCalendar } from "@tabler/icons-react";

// project imports
import SectionHeader from "@components/section/section-header";
import { StyledButton } from "@components/button/StyledButton";
import BannerImage from "@assets/images/banner-img.png";

export default function Banner({ onInquire, onSignUp }) {
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);

  useEffect(() => {
    // Function to update the state with the current window width
    const handleResize = () => {
      setWindowWidth(window.innerWidth);
    };

    // Setting up the event listener
    window.addEventListener("resize", handleResize);

    // Cleanup function
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []); // Ensuring the effect runs only once (like componentDidMount)

  return (
    <>
      <Box
        display={"flex"}
        flexDirection={"row"}
        alignItems={"flex-start"}
        minHeight={"500px"}
      >
        <Box sx={{ width: windowWidth > 1075 ? "50%" : "100%" }}>
          <SectionHeader
            isWhite={false}
            title="Never miss a test with automated daily notifications"
          />
          <Typography
            sx={{
              fontSize: "18px",
              color: "black",
              textAlign: "left",
              pb: "25px",
            }}
          >
            Callmates takes care of the calling process for you - ensuring
            you never forget to call. We make your call for you every day and
            update you along the way.
          </Typography>
          <Box
            sx={{
              display: "flex",
              justifyContent: "left",
              alignItems: "center",
              gap: "25px",
            }}
          >
            <StyledButton
              type="submit"
              variant="contained"
              color="secondary"
              sx={{
                pointerEvents: "auto",
                color: "black",
                fontSize: "24px",
                padding: "10px 20px",
                borderRadius: "30px",
                height: "60px",
                minWidth: "200px",
              }}
              startIcon={<IconCalendar />}
              onClick={() => onSignUp()}
            >
              Sign Up Now!
            </StyledButton>
            <StyledButton
              type="submit"
              variant="contained"
              color="secondary"
              sx={{
                pointerEvents: "auto",
                color: "black",
                fontSize: "24px",
                padding: "10px 20px",
                borderRadius: "30px",
                height: "60px",
                minWidth: "175px",
              }}
              startIcon={<IconInfoSquareRounded />}
              onClick={() => onInquire()}
            >
              Contact Us
            </StyledButton>
          </Box>
        </Box>
        <Box
          sx={{
            display: windowWidth < 1075 ? "none" : "flex",
            height: "80%",
            flexGrow: 1,
            alignItems: "flex-start",
            boxShadow: "none",
          }}
          style={{
            backgroundImage: `url(${BannerImage})`,
            backgroundSize: "cover",
            backgroundPosition: "center top",
            backgroundRepeat: "no-repeat",
            boxShadow: "none",
          }}
        />
      </Box>
    </>
  );
}

Banner.propTypes = {
  onInquire: PropTypes.func,
  onSignUp: PropTypes.func,
};
