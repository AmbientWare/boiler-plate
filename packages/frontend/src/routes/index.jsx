import { useRoutes } from "react-router-dom";

// routes
import MainRoutes from "./MainRoutes";
import LandingRoutes from "./LandingRoutes";
import config from "../config";

// ==============================|| ROUTING RENDER ||============================== //

export default function ThemeRoutes() {
  return useRoutes([MainRoutes, LandingRoutes], config.basename);
}
