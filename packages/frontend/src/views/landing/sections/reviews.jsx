import { PropTypes } from "prop-types";
import { Box, Typography } from "@mui/material";
import { Grid } from "@mui/material";

// project imports
import ReviewCard from "@components/cards/ReviewCard";
import { gridSpacing } from "@store/constant";
import UserOne from "@assets/images/user1.png";
import UserTwo from "@assets/images/user2.png";
import UserThree from "@assets/images/user3.png";

// ===========================|| Grid Items ||=========================== //
const gridItems = [
  {
    name: "David Cameron",
    message: "I never missed a test when I used Boilerplate.",
    userImage: UserOne,
    numStars: 5,
  },
  {
    name: "Daivd Cameron",
    message: "Boilerplate helped me spend less time worrying about calling.",
    userImage: UserTwo,
    numStars: 5,
  },
  {
    name: "David Cameron",
    message: "Boilerplate is the best thing since sliced bread.",
    userImage: UserThree,
    numStars: 4,
  },
];

export default function Reviews() {
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
          Customer Reviews:
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
            <ReviewCard
              data={{
                name: data.name,
                message: data.message,
                userImage: data.userImage,
                numStars: data.numStars,
              }}
              isTablerIcon={true}
            />
          </Grid>
        ))}
      </Grid>
    </>
  );
}

Reviews.propTypes = {
  onInquire: PropTypes.func,
  onSignUp: PropTypes.func,
};
