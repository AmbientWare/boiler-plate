import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

// material-ui
import { Toolbar, Box, AppBar } from "@mui/material";
import { useTheme } from "@mui/material/styles";

// project imports
import LandingHeader from "../landing/LandingHeader";
import LoginDialog from "@components/dialog/LoginDialog";
import InquireDialog from "@components/dialog/InquireDialog";
import SubscriptionDialog from "@components/dialog/SubscriptionDialog";

// ==============================|| Privacy policy PAGE ||============================== //

const PrivacyPolicy = () => {
  const theme = useTheme();
  const [loginDialogOpen, setLoginDialogOpen] = useState(false);
  const [loginDialogProps, setLoginDialogProps] = useState({});
  const [inquireDialogOpen, setInquireDialogOpen] = useState(false);
  const [subscriptionDialogOpen, setSubscriptionDialogOpen] = useState(false);

  const navigate = useNavigate();

  // useEffect(() => {
  //   // if on mobile device (for now relying on browser width to determine this, navigate to mobile landing page)
  //   if (window.innerWidth < 800) {
  //     navigate("/mobile");
  //   }
  // }, [navigate]);

  useEffect(() => {
    setLoginDialogProps({
      title: "Login",
      confirmButtonName: "Login",
    });
  }, []);

  return (
    <>
      <Box>
        <AppBar
          enableColorOnDark
          position="fixed"
          color="inherit"
          elevation={1}
          sx={{
            bgcolor: theme.palette.background.default,
          }}
        >
          <Toolbar>
            <LandingHeader
              onLogin={() => setLoginDialogOpen(true)}
              onPricing={() => {
                setSubscriptionDialogOpen(true);
              }}
            />
          </Toolbar>
        </AppBar>
        <Box
          sx={{
            height: "100vh",
            width: "100%",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <Box sx={{ height: "calc(100vh - 70px)", width: "90%", pt: 10 }}>
            <h1>Privacy Policy for Callmates</h1>

            <p>
              At Callmates, accessible from www.Callmates.com, one of our main
              priorities is the privacy of our visitors. This Privacy Policy
              document contains types of information that is collected and
              recorded by Callmates and how we use it.
            </p>

            <p>
              If you have additional questions or require more information about
              our Privacy Policy, do not hesitate to contact us.
            </p>

            <h2>Log Files</h2>

            <p>
              Callmates follows a standard procedure of using log files. These
              files log visitors when they visit websites. All hosting companies
              do this and a part of hosting services analytics. The information
              collected by log files include internet protocol (IP) addresses,
              browser type, Internet Service Provider (ISP), date and time
              stamp, referring/exit pages, and possibly the number of clicks.
              These are not linked to any information that is personally
              identifiable. The purpose of the information is for analyzing
              trends, administering the site, tracking users&apos; movement on
              the website, and gathering demographic information. Our Privacy
              Policy was created with the help of the &apos;
              <a href="https://www.privacypolicyonline.com/privacy-policy-generator/">
                Privacy Policy Generator&apos;
              </a>
              .
            </p>

            <h2>Privacy Policies</h2>

            <p>
              You may consult this list to find the Privacy Policy for each of
              the advertising partners of Callmates.
            </p>

            <p>
              Third-party ad servers or ad networks uses technologies like
              cookies, JavaScript, or Web Beacons that are used in their
              respective advertisements and links that appear on Callmates,
              which are sent directly to users&apos; browser. They automatically
              receive your IP address when this occurs. These technologies are
              used to measure the effectiveness of their advertising campaigns
              and/or to personalize the advertising content that you see on
              websites that you visit.
            </p>

            <p>
              Note that Callmates has no access to or control over these
              cookies that are used by third-party advertisers.
            </p>

            <h2>Third Party Privacy Policies</h2>

            <p>
              Callmates&apos;s Privacy Policy does not apply to other
              advertisers or websites. Thus, we are advising you to consult
              consult the respective Privacy Policies of these third-party ad
              servers for more detailed information. It may practices and
              instructions about how to opt-out of certain options.&apos; &apos;
            </p>

            <p>
              You can choose to disable cookies through your individual browser
              options. To know more detailed information about cookie management
              with specific web browsers, it can be found at the browsers&apos;
              respective websites. What Are Cookies?
            </p>

            <h2>Google Data Usage</h2>

            <p>
              Our application, Callmates, may interact with Google services to
              enhance user experience and functionality. This interaction may
              involve the collection, processing, and storage of certain Google
              user data. We are committed to protecting your privacy and
              ensuring that your information is handled securely and
              responsibly. The following outlines how our application accesses,
              uses, stores, or shares Google user data: 1. **Collection of
              Information:** Callmates may collect information, including but
              not limited to, Google user identifiers, email addresses, profile
              information, and other data related to Google services such as
              Drive or GMail. to provide specific features and services within
              the application. 2. **Usage of Information:** The collected Google
              user data is used solely for the purpose of delivering the
              intended features and services of our application. This may
              include personalization, authentication, and interaction with
              Google APIs. 3. **Storage of Information:** Any Google user data
              collected is securely stored on our servers and is retained only
              for as long as necessary to fulfill the purposes outlined in this
              privacy policy. 4. **Sharing of Information:** Callmates does
              not share Google user data with third parties, except as required
              by law or as necessary to provide the requested services. We do
              not sell, lease, or trade any user information. 5. **Security
              Measures:** We employ industry-standard security measures to
              protect against unauthorized access, alteration, disclosure, or
              destruction of Google user data. It&apos;s essential to note that
              your use of Google services within Callmates is subject to
              Google&apos;s own privacy policies and terms of service. Please
              review Google&apos;s policies to understand how your data is
              handled by them. For any questions or concerns regarding the
              handling of Google user data in Callmates, please do not
              hesitate to contact us.
            </p>

            <h2>Children&apos;s Information</h2>

            <p>
              Another part of our priority is adding protection for children
              while using the internet. We encourage parents and guardians to
              observe, participate in, and/or monitor and guide their online
              activity.
            </p>

            <p>
              Callmates does not knowingly collect any Personal Identifiable
              Information from children under the age of 13. If you think that
              your child provided this kind of information on our website, we
              strongly encourage you to contact us immediately and we will do
              our best efforts to promptly remove such information from our
              records.
            </p>

            <h2>Online Privacy Policy Only</h2>

            <p>
              This Privacy Policy applies only to our online activities and is
              valid for visitors to our website with regards to the information
              that they shared and/or collect in Callmates. This policy is not
              applicable to any information collected offline or via channels
              other than this website.
            </p>

            <h2>Consent</h2>

            <p>
              By using our website, you hereby consent to our Privacy Policy and
              agree to its Terms and Conditions.
            </p>
          </Box>
        </Box>
      </Box>
      <LoginDialog
        show={loginDialogOpen}
        dialogProps={loginDialogProps}
        onClose={() => {
          setLoginDialogOpen(false);
        }}
      />
      <InquireDialog
        isOpen={inquireDialogOpen}
        onClose={() => setInquireDialogOpen(false)}
      />
      <SubscriptionDialog
        show={subscriptionDialogOpen}
        onCancel={() => {
          setSubscriptionDialogOpen(false);
        }}
      />
    </>
  );
};

export default PrivacyPolicy;
