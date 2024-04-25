// assets
import {
  IconHierarchy,
  IconBuildingStore,
  IconKey,
  IconTool,
  IconLock,
  IconRobot,
  IconVariable,
  IconDatabase,
  IconDashboard,
} from "@tabler/icons-react";

// constant
const icons = {
  IconHierarchy,
  IconBuildingStore,
  IconKey,
  IconTool,
  IconLock,
  IconRobot,
  IconVariable,
  IconDatabase,
  IconDashboard,
};

// ==============================|| DASHBOARD MENU ITEMS ||============================== //

const dashboard = {
  id: "dashboard",
  title: "",
  type: "group",
  children: [
    {
      id: "dashboard",
      title: "Dashboard",
      type: "item",
      url: "/app/dashboard",
      icon: icons.IconDashboard,
      breadcrumbs: true,
    },
  ],
};

export default dashboard;
