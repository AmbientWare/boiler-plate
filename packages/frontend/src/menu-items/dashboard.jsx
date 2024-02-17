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
      url: "/dashboards",
      icon: icons.IconDashboard,
      breadcrumbs: true,
    },
    {
      id: "models",
      title: "Models",
      type: "item",
      url: "/models",
      icon: icons.IconHierarchy,
      breadcrumbs: true,
    },
    // {
    //     id: 'tools',
    //     title: 'Tools',
    //     type: 'item',
    //     url: '/tools',
    //     icon: icons.IconTool,
    //     breadcrumbs: true
    // },
    {
      id: "collections",
      title: "Collections",
      type: "item",
      url: "/collections",
      icon: icons.IconDatabase,
      breadcrumbs: true,
    },
    // {
    //     id: 'customize',
    //     title: 'Custom Actions',
    //     type: 'item',
    //     url: '/customize',
    //     icon: icons.IconSettingsAutomation,
    //     breadcrumbs: true
    // },
    // {
    //     id: 'marketplaces',
    //     title: 'Templates',
    //     type: 'item',
    //     url: '/marketplaces',
    //     icon: icons.IconTemplate,
    //     breadcrumbs: true
    // },
    // {
    //     id: 'assistants',
    //     title: 'Assistants',
    //     type: 'item',
    //     url: '/assistants',
    //     icon: icons.IconRobot,
    //     breadcrumbs: true
    // },
    {
      id: "credentials",
      title: "Credentials",
      type: "item",
      url: "/credentials",
      icon: icons.IconLock,
      breadcrumbs: true,
    },
    {
      id: "variables",
      title: "Variables",
      type: "item",
      url: "/variables",
      icon: icons.IconVariable,
      breadcrumbs: true,
    },
    {
      id: "apikey",
      title: "API Keys",
      type: "item",
      url: "/apikey",
      icon: icons.IconKey,
      breadcrumbs: true,
    },
  ],
};

export default dashboard;
