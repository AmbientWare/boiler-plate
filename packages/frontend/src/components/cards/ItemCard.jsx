import PropTypes from "prop-types";

// material-ui
import { useTheme } from "@mui/material/styles";
import { styled } from "@mui/material/styles";
import { Box, Grid, Typography } from "@mui/material";

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
  maxHeight: "300px",
  maxWidth: "300px",
  overflowWrap: "break-word",
  whiteSpace: "pre-line",
}));

// ===========================|| CONTRACT CARD ||=========================== //

const ItemCard = ({ isLoading, data, images, onClick }) => {
  const theme = useTheme();
  const Icon = data.icon;

  return (
    <>
      {isLoading ? (
        <SkeletonCard />
      ) : (
        <CardWrapper border={false} content={false} onClick={onClick}>
          <Box sx={{ p: 2.25, height: "200px", minWidth: "200px" }}>
            <Grid container direction="column" height={"100%"}>
              <div
                style={{
                  display: "flex",
                  flexDirection: "row",
                  alignItems: "center",
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
              </div>
              {data.description && (
                <span
                  style={{
                    marginTop: 10,
                    overflowWrap: "break-word",
                    whiteSpace: "pre-line",
                  }}
                >
                  {
                    // Check if the description is longer than 75 characters
                    data.description.length > 75
                      ? // If yes, slice to 75 characters then find the last complete word within this limit
                        data.description.slice(0, 75).replace(/\s+\S*$/, "") +
                        "..."
                      : // If no, just use the description as is
                        data.description
                  }
                </span>
              )}
              {images && (
                <div
                  style={{
                    display: "flex",
                    flexDirection: "row",
                    flexWrap: "wrap",
                    marginTop: 5,
                  }}
                >
                  {images.map((img) => (
                    <div
                      key={img}
                      style={{
                        width: 35,
                        height: 35,
                        marginRight: 5,
                        borderRadius: "50%",
                        backgroundColor: "white",
                        marginTop: 5,
                      }}
                    >
                      <img
                        style={{
                          width: "100%",
                          height: "100%",
                          padding: 5,
                          objectFit: "contain",
                        }}
                        alt=""
                        src={img}
                      />
                    </div>
                  ))}
                </div>
              )}
              <Box sx={{ flexGrow: 1 }} />
              {data.icon && (
                <div
                  style={{
                    display: "flex",
                    flexDirection: "row",
                    justifyContent: "right",
                  }}
                >
                  <Icon
                    strokeWidth={1.5}
                    size="3.0rem"
                    style={{
                      marginTop: "auto",
                      marginBottom: "auto",
                      color: theme.palette.primary[200],
                    }}
                  />
                </div>
              )}
            </Grid>
          </Box>
        </CardWrapper>
      )}
    </>
  );
};

ItemCard.propTypes = {
  isLoading: PropTypes.bool,
  data: PropTypes.object,
  images: PropTypes.array,
  onClick: PropTypes.func,
};

export default ItemCard;
