import PropTypes from "prop-types";

// material-ui
import { useTheme } from "@mui/material/styles";
import { styled } from "@mui/material/styles";
import { Box, Grid, Typography } from "@mui/material";
import { IconStar } from "@tabler/icons-react";

// project imports
import MainCard from "@components/cards/MainCard";
import SkeletonCard from "@components/cards/Skeleton/SkeletonCard";

const CardWrapper = styled(MainCard)(({ theme }) => ({
  background: theme.palette.card.main,
  color: theme.darkTextPrimary,
  border: "1px solid",
  borderColor: theme.palette.primary[200] + 75,
  overflow: "auto",
  position: "relative",
  boxShadow: "0 20px 56px 0 rgb(32 40 45 / 30%)",
  cursor: "pointer",
  "&:hover": {
    background: theme.palette.card.hover,
    boxShadow: "0 2px 14px 0 rgb(32 40 45 / 50%)",
  },
  maxHeight: "500px",
  maxWidth: "500px",
  overflowWrap: "break-word",
  whiteSpace: "pre-line",
}));

// ===========================|| CONTRACT CARD ||=========================== //

const ReviewCard = ({ isLoading, data }) => {
  const theme = useTheme();

  return (
    <>
      {isLoading ? (
        <SkeletonCard />
      ) : (
        <CardWrapper border={false} content={false}>
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              p: 2.25,
              alignItems: "center",
              alignContent: "center",
              justifyContent: "center",
            }}
          >
            <img
              style={{
                objectFit: "contain",
                height: "auto",
                width: 80,
                borderRadius: "50%",
                border: "5px solid",
                borderColor: theme.palette.primary[800] + 75,
              }}
              src={data.userImage}
              alt=" Boilerplate User"
            />
            <Grid container direction="column" height={"100%"}>
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                }}
              >
                <Typography
                  sx={{
                    fontSize: "1.5rem",
                    fontWeight: 500,
                    overflowWrap: "break-word",
                    whiteSpace: "pre-line",
                  }}
                >
                  {data.templateName || data.name}
                </Typography>
                {data.message && (
                  <span
                    style={{
                      marginTop: 10,
                      overflowWrap: "break-word",
                      whiteSpace: "pre-line",
                    }}
                  >
                    {
                      // Check if the message is longer than 75 characters
                      data.message.length > 75
                        ? // If yes, slice to 75 characters then find the last complete word within this limit
                          data.message.slice(0, 75).replace(/\s+\S*$/, "") +
                          "..."
                        : // If no, just use the message as is
                          data.message
                    }
                  </span>
                )}
              </div>
              <Box sx={{ flexGrow: 1, pb: "15px" }} />

              <div
                style={{
                  display: "flex",
                  flexDirection: "row",
                  justifyContent: "center",
                }}
              >
                {[...Array(5)].map((_, index) => (
                  <IconStar
                    key={index}
                    strokeWidth={1.5}
                    size="2.0rem"
                    style={{
                      marginTop: "auto",
                      marginBottom: "auto",
                      color:
                        index < data.numStars
                          ? theme.palette.warning.main
                          : "grey",
                    }}
                  />
                ))}
              </div>
            </Grid>
          </Box>
        </CardWrapper>
      )}
    </>
  );
};

ReviewCard.propTypes = {
  isLoading: PropTypes.bool,
  data: PropTypes.object,
  userImage: PropTypes.string,
};

export default ReviewCard;
