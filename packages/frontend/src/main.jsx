// style + assets
import "@assets/scss/style.scss";

import React from "react";
import App from "./App";
import { store } from "@store";
import { createRoot } from "react-dom/client";

// third party
import { BrowserRouter } from "react-router-dom";
import { Provider } from "react-redux";
import { SnackbarProvider } from "notistack";
import ConfirmContextProvider from "@store/context/ConfirmContextProvider";

const container = document.getElementById("root");
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <Provider store={store}>
      <BrowserRouter>
        <SnackbarProvider>
          <ConfirmContextProvider>
            <App />
          </ConfirmContextProvider>
        </SnackbarProvider>
      </BrowserRouter>
    </Provider>
  </React.StrictMode>,
);
