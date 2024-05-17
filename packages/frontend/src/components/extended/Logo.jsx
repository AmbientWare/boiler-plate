import logoWhite from "@assets/images/logo-white.png";
import logoBlack from "@assets/images/logo-black.png";

import { useSelector } from "react-redux";

// ==============================|| LOGO ||============================== //

const Logo = () => {
  const customization = useSelector((state) => state.customization);

  return (
    <div
      style={{ alignItems: "center", display: "flex", flexDirection: "row" }}
    >
      <img
        style={{ objectFit: "contain", height: "auto", width: 75 }}
        src={customization.isDarkMode ? logoBlack : logoWhite}
        alt="Callmates"
      />
    </div>
  );
};

export default Logo;
