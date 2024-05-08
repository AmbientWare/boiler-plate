import { useState, useEffect } from "react";
import PropTypes from "prop-types";
import { createPortal } from "react-dom";
import {
  Dialog,
  DialogContent,
  DialogTitle,
  TableContainer,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Paper,
  Typography,
  Box,
} from "@mui/material";

// project imports
import subscriptions from "@api/subscriptions";
import MainCard from "@components/cards/MainCard";
import { getCurrencySymbol } from "@utils/genericHelper";

const SubscriptionDialog = ({ show, onCancel }) => {
  const portalElement = document.getElementById("portal");
  const [options, setOptions] = useState([]);

  const dialogWidth = (250 * options.length).toString() + "px";

  useEffect(() => {
    subscriptions
      .getSubscriptionOptions() // Assuming this returns a promise
      .then((fetchedOptions) => {
        setOptions(fetchedOptions.data); // Set the options state
      })
      .catch((error) => {
        console.error("Error fetching subscription options:", error);
      });
  }, [show]);

  const component = show ? (
    <Dialog
      onClose={onCancel}
      open={show}
      width={dialogWidth}
      maxWidth="md"
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
    >
      <DialogTitle sx={{ fontSize: "2rem" }} id="alert-dialog-title">
        Plans and Pricing
      </DialogTitle>
      <DialogContent>
        <TableContainer component={Paper}>
          <Table aria-label="simple table">
            <TableHead>
              <TableRow>
                {options &&
                  options.map((option) => (
                    <TableCell sx={{ textAlign: "center" }} key={option.name}>
                      <Typography
                        variant="h2"
                        component="div"
                        sx={{ fontWeight: "bold" }}
                      >
                        {option.name}
                      </Typography>
                    </TableCell>
                  ))}
              </TableRow>
            </TableHead>
            <TableBody>
              <TableRow
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                {options &&
                  options.map((option) => (
                    <TableCell
                      sx={{ alignContent: "center" }}
                      align="center"
                      key={option.name}
                      component="th"
                      scope="row"
                    >
                      <ProductDisplay option={option} />
                    </TableCell>
                  ))}
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
      </DialogContent>
    </Dialog>
  ) : null;

  return portalElement ? createPortal(component, portalElement) : null;
};

SubscriptionDialog.propTypes = {
  show: PropTypes.bool.isRequired,
  onCancel: PropTypes.func.isRequired,
};

export default SubscriptionDialog;

const ProductDisplay = ({ option }) => {
  // Corrected to destructure the option prop

  return (
    <section>
      <div
        className="product"
        style={{ display: "flex", justifyContent: "center" }}
      >
        <MainCard sx={{ maxWidth: "250px" }}>
          {/* Plan Description */}
          <Typography variant="h4" sx={{ mb: 2 }}>
            {option.description}
          </Typography>

          {/* Pricing Information */}
          <Box
            sx={{
              mt: 2,
              p: 2,
              bgcolor: "background.paper",
              borderRadius: 1,
              display: "flex",
              alignItems: "baseline",
              justifyContent: "center",
            }}
          >
            <Typography
              variant="h2"
              component="div"
              sx={{ fontWeight: "bold", color: "secondary.main" }}
            >
              {`${getCurrencySymbol(option.currency)}${option.price}`}
            </Typography>
            <Typography variant="subtitle2" sx={{ color: "text.secondary" }}>
              {`/ ${option.recurring ? "Month" : "One time"}`}
            </Typography>
          </Box>

          {/* Gray line as a separator with padding */}
          <Box
            sx={{
              borderBottom: "1px solid grey",
              width: "80%",
              margin: "auto",
              my: 2,
              pt: 2,
            }}
          />

          {/* Features */}
          {option.features.map((feature, index) => (
            <Typography sx={{ mt: 2, mb: 2 }} key={index}>
              {`✓ ${feature.name}`}
            </Typography>
          ))}
        </MainCard>
      </div>
    </section>
  );
};

ProductDisplay.propTypes = {
  option: PropTypes.shape({
    name: PropTypes.string,
    price: PropTypes.string,
    description: PropTypes.string,
    recurring: PropTypes.string,
    priceId: PropTypes.string,
    status: PropTypes.string,
    current: PropTypes.bool,
    features: PropTypes.array,
    currency: PropTypes.string,
    // Add any other properties that option is expected to have
  }).isRequired,
};
