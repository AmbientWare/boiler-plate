// AuthCheck.js
import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import PropTypes from "prop-types";

// API
import authApi from "./auth";

const allowedRoutes = [
  "/",
  "/login",
  "/privacy-policy",
  "/terms-and-conditions",
  "/mobile",
];

const AuthCheck = ({ children }) => {
  const [isLoading, setIsLoading] = useState(true);

  const location = useLocation();

  useEffect(() => {
    if (!allowedRoutes.includes(location.pathname)) {
      const fetchData = async () => {
        // logit for 401 and redirect to home page is handled by api/client.js
        await authApi
          .checkAuth()
          .then(() => {
            setIsLoading(false);
          })
          .catch(() => {
            window.location.href = "/";
          });
      };

      fetchData();
    } else {
      setIsLoading(false);
    }
  }, [location.pathname]);

  if (!isLoading) {
    return <>{children}</>;
  }
};

AuthCheck.propTypes = {
  children: PropTypes.node.isRequired,
};

export default AuthCheck;
