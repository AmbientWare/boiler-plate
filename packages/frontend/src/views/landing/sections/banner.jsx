import { PropTypes } from "prop-types";
import { Box, Typography } from "@mui/material";
import { IconInfoSquareRounded, IconCalendar } from "@tabler/icons-react";

// project imports
import { LandingStyles } from "./styles";
import SectionHeader from "@components/section/section-header";
import { StyledButton } from "@components/button/StyledButton";
import { PixelGrid } from "@components/pixelGrid/pixelGrid";
import { scheduleLink } from "@store/constant";

export default function Banner({ onInquire }) {
  return (
    <>
      <Box
        position={"relative"}
        sx={{
          height: "100vh",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
        }}
        id="home"
      >
        <Box sx={LandingStyles.pixelGridContainer}>
          <PixelGrid />
        </Box>
        <Box sx={LandingStyles.contentContainer}>
          <SectionHeader
            isWhite={true}
            title="Your Gateway to Intelligent Applications"
          />
          <Typography
            sx={{
              pb: "50px",
              fontSize: "24px",
              color: "white",
              textAlign: "center",
            }}
          >
            Rapidly build and instantly deploy AI solutions.
          </Typography>
          <Box
            sx={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              gap: "10px",
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
              }}
              startIcon={<IconCalendar />}
              onClick={() => (window.location.href = scheduleLink)}
            >
              Schedule a Demo
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
              }}
              startIcon={<IconInfoSquareRounded />}
              onClick={() => onInquire()}
            >
              Contact Us
            </StyledButton>
          </Box>
        </Box>
      </Box>
    </>
  );
}

Banner.propTypes = {
  onInquire: PropTypes.func,
};
