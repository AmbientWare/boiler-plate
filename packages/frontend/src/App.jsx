import { useSelector } from "react-redux";
import { ThemeProvider } from "@mui/material/styles";
import { CssBaseline, StyledEngineProvider } from "@mui/material";

// project imports
import "./App.css";

// routing
import Routes from "@routes";

// defaultTheme
import themes from "@themes";

// project imports
import NavigationScroll from "@layout/NavigationScroll";

// api/authentication
import AuthCheck from "@api/AuthCheck";

// ==============================|| APP ||============================== //

const App = () => {
  const customization = useSelector((state) => state.customization);

  return (
    <StyledEngineProvider injectFirst>
      <ThemeProvider theme={themes(customization)}>
        <CssBaseline />
        <NavigationScroll>
          <AuthCheck>
            <Routes />
          </AuthCheck>
        </NavigationScroll>
      </ThemeProvider>
    </StyledEngineProvider>
  );
};

export default App;
