// assets
import { IconHome } from "@tabler/icons-react";

// constant
const icons = {
  IconHome,
};

// ==============================|| DASHBOARD MENU ITEMS ||============================== //

const dashboard = {
  id: "dashboard",
  title: "",
  type: "group",
  children: [
    {
      id: "home",
      title: "Home",
      type: "item",
      url: "/app/home",
      icon: icons.IconHome,
      breadcrumbs: true,
    },
  ],
};

export default dashboard;
