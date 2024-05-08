import PropTypes from "prop-types";
import { FormControl, Switch } from "@mui/material";

export const SwitchInput = ({ value, onChange, disabled = false }) => {
  return (
    <>
      <FormControl sx={{ width: "100%" }} size="small">
        <Switch
          disabled={disabled}
          checked={value}
          onChange={(event) => {
            onChange(event.target.checked);
          }}
        />
      </FormControl>
    </>
  );
};

SwitchInput.propTypes = {
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.bool]),
  onChange: PropTypes.func,
  disabled: PropTypes.bool,
};
