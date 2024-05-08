import { lazy } from "react";

// project imports
import MinimalLayout from "@layout/MinimalLayout";
import Loadable from "@components/loading/Loadable";

// login routing
const Landing = Loadable(lazy(() => import("@views/landing")));

// privacy policy routing
const PrivacyPolicy = Loadable(lazy(() => import("@views/privacypolicy")));

// terms and conditions routing
const TermsConditions = Loadable(lazy(() => import("@views/termsconditions")));

// oauth-complete routing
const OauthComplete = Loadable(lazy(() => import("@views/oauth")));

const LandingRoutes = {
  path: "/",
  element: <MinimalLayout />,
  children: [
    {
      path: "/",
      element: <Landing />,
    },
    {
      path: "/oauth-complete/:status",
      element: <OauthComplete />,
    },
    {
      path: "/privacy-policy",
      element: <PrivacyPolicy />,
    },
    {
      path: "/terms-and-conditions",
      element: <TermsConditions />,
    },
  ],
};

export default LandingRoutes;
