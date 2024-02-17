// assets
import {
  IconTrash,
  IconFileUpload,
  IconFileExport,
  IconCopy,
  IconSearch,
  IconMessage,
  IconPictureInPictureOff,
} from "@tabler/icons-react";

// constant
const icons = {
  IconTrash,
  IconFileUpload,
  IconFileExport,
  IconCopy,
  IconSearch,
  IconMessage,
  IconPictureInPictureOff,
};

// ==============================|| SETTINGS MENU ITEMS ||============================== //

const settings = {
  id: "settings",
  title: "",
  type: "group",
  children: [
    {
      id: "duplicateChatflow",
      title: "Duplicate Model",
      type: "item",
      url: "",
      icon: icons.IconCopy,
    },
    {
      id: "loadChatflow",
      title: "Load Model",
      type: "item",
      url: "",
      icon: icons.IconFileUpload,
    },
    {
      id: "exportChatflow",
      title: "Export Model",
      type: "item",
      url: "",
      icon: icons.IconFileExport,
    },
    {
      id: "deleteChatflow",
      title: "Delete Model",
      type: "item",
      url: "",
      icon: icons.IconTrash,
    },
  ],
};

export default settings;
