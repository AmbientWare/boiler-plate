import logoWhite from "@assets/images/hxmx_logo.png";
import logoBlack from "@assets/images/hxmx_logo.png";

import { useSelector } from "react-redux";

// ==============================|| LOGO ||============================== //

const Logo = () => {
  const customization = useSelector((state) => state.customization);

  return (
    <div
      style={{ alignItems: "center", display: "flex", flexDirection: "row" }}
    >
      <img
        style={{ objectFit: "contain", height: "50px", width: 150 }}
        src={customization.isDarkMode ? logoWhite : logoBlack}
        alt="HXMX"
      />
    </div>
  );
};

export default Logo;
