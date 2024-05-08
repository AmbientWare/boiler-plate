import { PropTypes } from "prop-types";
import { Box, Typography } from "@mui/material";

export default function SectionHeader({ title, isWhite }) {
  return (
    <Box sx={{ pb: { xs: 0, md: "30px", height:'auto' }, textAlign: "left" }}>
      <Typography
        sx={{
          zIndex: 1,
          display: "flex",
          fontSize: { xs: "4em", md: "56px" },
          fontWeight: "bold",
          color: isWhite ? "white" : "black",
        }}
      >
        {title}
      </Typography>
    </Box>
  );
}

SectionHeader.propTypes = {
  title: PropTypes.string.isRequired,
  isWhite: PropTypes.bool,
};
