import { lazy } from 'react'

// project imports
import MainLayout from "@layout/MainLayout";
import Loadable from '@components/loading/Loadable'

// dashboard routing
const Dashboard = Loadable(lazy(() => import('@views/dashboard')))

// ==============================|| MAIN ROUTING ||============================== //

const MainRoutes = {
  path: "/app",
  element: <MainLayout />,
  children: [
    {
        path: '/app/dashboard',
        element: <Dashboard />
    },
  ],
};

export default MainRoutes;
