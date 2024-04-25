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
            title="Accelerated log correlation for enhanced productivity"
          />
          <Typography
            sx={{
              display: "flex",
              flexDirection: "column",
              alignText: "center",
              pb: "50px",
              fontSize: "24px",
              color: "white",
              textAlign: "center",
              width: "80%",
            }}
          >
            The HXMX Log Correlation Assistant, powered by statistical feature
            analysis, transforms well log correlation. Music recognition apps
            like Shazam identify songs from brief snippets. In a similar
            fashion, HXMX matches hashes in a database to swiftly pick and
            verify tops on well logs in a matter of seconds. This breakthrough
            not only reduces picking time, but also delivers objective
            definitions of tops, identifies missing sections, and offers
            comparative metrics between wells. HXMX Tops Fingerprinting enhances
            the efficiency, accuracy, and depth of geological analysis.
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
