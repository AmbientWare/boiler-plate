// import { lazy } from 'react'

// project imports
import MainLayout from "@layout/MainLayout";
// import Loadable from 'components/loading/Loadable'

// dashboard routing
// const Dashboard = Loadable(lazy(() => import('views/dashboards')))

// ==============================|| MAIN ROUTING ||============================== //

const MainRoutes = {
  path: "/home",
  element: <MainLayout />,
  children: [
    // {
    //     path: '/dashboards',
    //     element: <Dashboard />
    // },
  ],
};

export default MainRoutes;
