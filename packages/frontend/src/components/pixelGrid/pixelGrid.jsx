import { useState, useRef, useEffect } from "react";
import { useTheme } from "@mui/material/styles";
import { Box } from "@mui/material";
import "./PixelGrid.css";

export const PixelGrid = () => {
  const theme = useTheme();

  const pixelGridRef = useRef(null);
  const [numberOfPixels, setNumberOfPixels] = useState(0);
  const [gridDimensions, setGridDimensions] = useState({ width: 0, height: 0 });
  const pixelSize = 20;
  const [hoveredPixels, setHoveredPixels] = useState({});

  const generateRandomColor = () => {
    const hue = Math.floor(Math.random() * (40 - 25 + 1)) + 25;
    const saturation = Math.floor(Math.random() * (100 - 50 + 1)) + 50;
    const lightness = Math.floor(Math.random() * (70 - 30 + 1)) + 30;

    return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
  };

  const handleMouseOver = (id) => {
    const color = generateRandomColor();
    setHoveredPixels((prev) => ({ ...prev, [id]: color }));
  };

  const handleMouseOut = (id) => {
    setTimeout(() => {
      setHoveredPixels((prev) => {
        const newHovered = { ...prev };
        delete newHovered[id];
        return newHovered;
      });
    }, 1500);
  };

  useEffect(() => {
    const calculateGridDimensions = () => {
      if (pixelGridRef.current) {
        const width = pixelGridRef.current.offsetWidth;
        const height = pixelGridRef.current.offsetHeight;
        setGridDimensions({ width, height });
      }
    };

    calculateGridDimensions();

    window.addEventListener("resize", calculateGridDimensions);
  }, []);

  useEffect(() => {
    const numPixels =
      Math.floor(gridDimensions.width / pixelSize) *
      Math.floor(gridDimensions.height / pixelSize);
    setNumberOfPixels(numPixels);
  }, [gridDimensions, pixelSize, pixelGridRef]);

  return (
    <Box
      display={"flex"}
      ref={pixelGridRef}
      className="pixelGrid"
      sx={{ backgroundColor: theme.palette.paper, height: "100vh"}}
    >
      {Array.from({ length: numberOfPixels }, (_, id) => (
        <Box
          key={id}
          className={`${hoveredPixels[id] ? "hovered" : "pixel"}`}
          style={{
            backgroundColor: hoveredPixels[id] || "transparent", // Ensures initial background is transparent or any color that allows white dots to be visible
            width: `${pixelSize}px`,
            height: `${pixelSize}px`,
          }}
          onMouseEnter={() => handleMouseOver(id)}
          onMouseLeave={() => handleMouseOut(id)}
          onFocus={() => handleMouseOver(id)}
          onBlur={() => handleMouseOut(id)}
        />
      ))}
    </Box>
  );
};
