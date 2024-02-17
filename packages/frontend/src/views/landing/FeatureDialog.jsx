import { useEffect, useState } from "react";
import { PropTypes } from "prop-types";
import {
  Dialog,
  DialogTitle,
  CircularProgress,
  DialogContent,
  DialogContentText,
  DialogActions,
  Box,
} from "@mui/material";

// project imports
import { StyledButton } from "components/button/StyledButton";

function FeatureDialog({ dialogProps, isOpen, onClose }) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [src, setSrc] = useState("");
  const [type, setType] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const clearDialog = () => {
    setTitle("");
    setContent("");
    setSrc("");
    setType("");
  };

  useEffect(() => {
    if (dialogProps) {
      if (dialogProps.type === "video") {
        setIsLoading(true);
      }

      setTitle(dialogProps.title || "");
      setContent(dialogProps.content || "");
      setSrc(dialogProps.src || "");
      setType(dialogProps.type || "");
    }
  }, [dialogProps]);

  return (
    <>
      {src && (
        <Dialog
          maxWidth={"none"}
          open={isOpen}
          onClose={onClose}
          sx={{ maxWidth: "1000px", width: "80%", mx: "auto" }}
        >
          <DialogTitle variant="h1">{title}</DialogTitle>
          <DialogContent
            sx={{
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              overflowY: "scroll",
            }}
          >
            <DialogContentText padding={2} textAlign={"center"} variant="h2">
              {content}
            </DialogContentText>
            {type === "img" && (
              <Box
                component={"img"}
                alt={""}
                src={src}
                borderRadius={"10px"}
                height={300}
              />
            )}
            {isLoading && (
              <Box display="flex" justifyContent="center" alignItems="center">
                <CircularProgress />
              </Box>
            )}
            {type === "video" && (
              <Box
                display={isLoading ? "none" : "block"}
                component={"video"}
                alt={"Video content"}
                src={src}
                borderRadius={"10px"}
                width={"85%"}
                autoPlay
                muted
                loop
                onLoadedData={() => setIsLoading(false)}
              >
                Your browser does not support the video tag.
              </Box>
            )}
          </DialogContent>
          <DialogActions>
            <StyledButton
              type="submit"
              variant="contained"
              color="primary"
              onClick={() => {
                clearDialog();
                onClose();
              }}
            >
              Close
            </StyledButton>
          </DialogActions>
        </Dialog>
      )}
    </>
  );
}

FeatureDialog.propTypes = {
  dialogProps: PropTypes.object,
  isOpen: PropTypes.bool,
  onClose: PropTypes.func,
};

export default FeatureDialog;
