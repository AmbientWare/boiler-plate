import { PropTypes } from "prop-types";
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Link,
} from "@mui/material";

// project imports
import { StyledButton } from "@components/button/StyledButton";

function InfoDialog({ isOpen, onClose }) {
  return (
    <Dialog open={isOpen} onClose={onClose}>
      <DialogTitle variant="h1">Help Make HXMX Better</DialogTitle>
      <DialogContent sx={{ display: "flex", justifyContent: "center" }}>
        <DialogContentText variant="h2">
          HXMX software is currently undergoing Beta testing! Please give
          use feedback about improvements and bugs! Please email us at{" "}
          <Link
            href="mailto:info@hxmx.co"
            target="_blank"
            rel="noopener noreferrer"
          >
            info@hxmx.co
          </Link>
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <StyledButton
          type="submit"
          variant="contained"
          color="primary"
          onClick={() => {
            onClose();
          }}
        >
          Close
        </StyledButton>
      </DialogActions>
    </Dialog>
  );
}

InfoDialog.propTypes = {
  isOpen: PropTypes.bool,
  onClose: PropTypes.func,
};

export default InfoDialog;
