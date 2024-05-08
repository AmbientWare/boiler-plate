export const LandingStyles = {
  pixelGridContainer: {
    width: "100%",
    height: "100%",
    position: "absolute",
    zIndex: 0,
    // borderRadius: "20%",
  },
  contentContainer: {
    display: "flex",
    flexDirection: "column",
    position: "relative",
    zIndex: 1, // Ensures content is above the pixel grid
    pointerEvents: "none",
    justifyContent: "center",
    alignItems: "center",
  },
  interactiveElement: {
    pointerEvents: "auto", // Ensures interactive elements can be clicked
  },
  grid: {
    // px: [0, null, null, "60px", null, "90px"],
    display: "flex",
    justifyContent: "center",
    alignItems: "stretch",
    flexDirection: "row",
    gridGap: ["350px 50px", null, "100px 200x"],
    gridTemplateColumns: [
      "repeat(1,1fr)",
      null,
      "repeat(2,1fr)",
      null,
      "repeat(3,1fr)",
      null,
      "repeat(4,1fr)",
    ],
    // mx: 'auto',
    m: 3,
  },
  models: {
    pt: "50px",
    width: ["100%", "100%", "100%"],
    mx: "auto",
  },
};
