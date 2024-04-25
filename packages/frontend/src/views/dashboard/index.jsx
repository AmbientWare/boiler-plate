import { useSelector } from "react-redux";

import { useTheme } from "@mui/material/styles";

// project imports
import MainCard from "@components/cards/MainCard";

// ==============================|| Dashboard ||============================== //

const Dashboard = () => {
  const theme = useTheme();
  const customization = useSelector((state) => state.customization);

  return (
    <>
      <MainCard
        sx={{
          background: customization.isDarkMode
            ? theme.palette.common.black
            : "",
          display: "flex",
          flexDirection: "column",
          maxHeight: "calc(100vh - 100px)",
        }}
      ></MainCard>
    </>
  );
};

export default Dashboard;
