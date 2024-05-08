import { lazy } from "react";

// project imports
import MainLayout from "@layout/MainLayout";
import Loadable from "@components/loading/Loadable";

// dashboard routing
const Home = Loadable(lazy(() => import('@src/views/home')))

// ==============================|| MAIN ROUTING ||============================== //

const MainRoutes = {
  path: "/app",
  element: <MainLayout />,
  children: [
    {
      path: "/app/home",
      element: <Home />,
    },
  ],
};

export default MainRoutes;
