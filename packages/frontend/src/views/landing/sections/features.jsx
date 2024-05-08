import { PropTypes } from "prop-types";
import { Box, Typography } from "@mui/material";
import { Grid } from "@mui/material";
import {
  IconLock,
  IconPhoneIncoming,
  IconMessage2,
  IconBell,
} from "@tabler/icons-react";

// project imports
import ItemCard from "@components/cards/ItemCard";
import { gridSpacing } from "@store/constant";

// ===========================|| Grid Items ||=========================== //
const gridItems = [
  {
    name: "Daily Calls",
    description: "Never miss a day.",
    icon: IconPhoneIncoming,
  },
  {
    name: "Secure communications",
    description: "Your results are private.",
    icon: IconLock,
  },
  {
    name: "Custom notifications",
    description: "Notifications via email and/or text.",
    icon: IconMessage2,
  },
  {
    name: "Reliable systems",
    description: "Fail-safes for each step in the process.",
    icon: IconBell,
  },
  {
    name: "Daily Calls",
    description: "Never miss a day.",
    icon: IconPhoneIncoming,
  },
  {
    name: "Secure communications",
    description: "Your results are private.",
    icon: IconLock,
  },
  {
    name: "Custom notifications",
    description: "Notifications via email and/or text.",
    icon: IconMessage2,
  },
  {
    name: "Reliable systems",
    description: "Fail-safes for each step in the process.",
    icon: IconBell,
  },
];

export default function Features() {
  return (
    <>
      <Box
        display={"flex"}
        sx={{
          mt: "50px",
          pb: "25px",
        }}
      >
        <Typography
          sx={{
            fontSize: "50px",
            color: "black",
            textAlign: "left",
            zIndex: 1,
          }}
        >
          What `Boilerplate` can do for you:
        </Typography>
      </Box>
      <Grid
        container
        spacing={gridSpacing}
        width={"100%"}
        justifyContent={"center"}
      >
        {gridItems.map((data, index) => (
          <Grid index={index} item lg={3} md={4} sm={6} xs={12} key={index}>
            <ItemCard
              data={{
                name: data.name,
                description: data.description,
                icon: data.icon,
              }}
              isTablerIcon={true}
            />
          </Grid>
        ))}
      </Grid>
    </>
  );
}

Features.propTypes = {
  onInquire: PropTypes.func,
  onSignUp: PropTypes.func,
};
