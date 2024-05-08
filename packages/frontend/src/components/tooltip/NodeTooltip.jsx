import { styled } from "@mui/material/styles";
import Tooltip, { tooltipClasses } from "@mui/material/Tooltip";

const ComponentToolTip = styled(({ className, ...props }) => (
  <Tooltip {...props} classes={{ popper: className }} />
))(({ theme }) => ({
  [`& .${tooltipClasses.tooltip}`]: {
    backgroundColor: theme.palette.ComponentToolTip.background,
    color: theme.palette.ComponentToolTip.color,
    boxShadow: theme.shadows[1],
  },
}));

export default ComponentToolTip;
