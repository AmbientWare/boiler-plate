// import PropTypes from "prop-types";
import { useState, useEffect } from "react";
import { useDispatch } from "react-redux";
import parser from "html-react-parser";

// Material
import { Button, Box } from "@mui/material";

// Project imports
import SectionHeader from "@components/section/section-header";
import { StyledButton } from "@components/button/StyledButton";
import ConfirmDialog from "@components/dialog/ConfirmDialog";
import ComponentInputHandler from "@components/input/ComponentInputHandler";

// Icons
import { IconX } from "@tabler/icons-react";

// API
import credentialsApi from "@api/credentials";

// Hooks
import useApi from "@hooks/useApi";

// utils
import useNotifier from "@utils/useNotifier";

// const
import {
  enqueueSnackbar as enqueueSnackbarAction,
  closeSnackbar as closeSnackbarAction,
} from "@store/actions";
import MainCard from "@src/components/cards/MainCard";

const Home = () => {
  const dispatch = useDispatch();

  // ==============================|| Snackbar ||============================== //

  useNotifier();

  const enqueueSnackbar = (...args) => dispatch(enqueueSnackbarAction(...args));
  const closeSnackbar = (...args) => dispatch(closeSnackbarAction(...args));

  const getSpecificComponentCredentialApi = useApi(
    credentialsApi.getSpecificComponentCredential
  );
  const getUserCredentialApi = useApi(credentialsApi.getUserCredentials);

  const [credential, setCredential] = useState({});
  const [name, setName] = useState("");
  const [credentialData, setCredentialData] = useState({});
  const [componentCredential, setComponentCredential] = useState({});

  useEffect(() => {
    if (getUserCredentialApi.data) {
      const cred = getUserCredentialApi.data[0];
      setCredential(cred);
      if (cred.name) {
        setName(cred.name);
      }
      if (cred.credential) {
        setCredentialData(cred.credential);
      }
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [getUserCredentialApi.data]);

  useEffect(() => {
    if (getSpecificComponentCredentialApi.data) {
      setComponentCredential(getSpecificComponentCredentialApi.data);
    }
  }, [getSpecificComponentCredentialApi.data]);

  useEffect(() => {
    getSpecificComponentCredentialApi.request("CallmatesInfo");
    getUserCredentialApi.request();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const checkCredentialData = (cred) => {
    // ensure all the non optional fields are filled
    for (const key in cred.inputs) {
      if (
        !componentCredential.inputs[key].optional &&
        !credentialData[componentCredential.inputs[key].name]
      ) {
        enqueueSnackbar({
          message: `Please fill in all required input fields`,
          options: {
            key: new Date().getTime() + Math.random(),
            variant: "error",
            persist: true,
            action: (key) => (
              <Button
                style={{ color: "white" }}
                onClick={() => closeSnackbar(key)}
              >
                <IconX />
              </Button>
            ),
          },
        });
        return false;
      }
    }
    return true;
  };

  const addNew = async () => {
    try {
      const obj = {
        name: "user_credential",
        credentialName: componentCredential.name,
        credentialObj: credentialData,
      };
      // ensure all the non optional fields are filled
      if (!checkCredentialData(componentCredential)) return;

      const createResp = await credentialsApi.createCredential(obj);
      if (createResp.data) {
        enqueueSnackbar({
          message: "Information added",
          options: {
            key: new Date().getTime() + Math.random(),
            variant: "success",
            action: (key) => (
              <Button
                style={{ color: "white" }}
                onClick={() => closeSnackbar(key)}
              >
                <IconX />
              </Button>
            ),
          },
        });
      }
    } catch (error) {
      const errorData = `${error.response.status}: ${error.response.data.detail}`;
      enqueueSnackbar({
        message: `Failed to add information: ${errorData}`,
        options: {
          key: new Date().getTime() + Math.random(),
          variant: "error",
          persist: true,
          action: (key) => (
            <Button
              style={{ color: "white" }}
              onClick={() => closeSnackbar(key)}
            >
              <IconX />
            </Button>
          ),
        },
      });
    }
  };

  const save = async () => {
    try {
      const saveObj = {
        name,
        credentialName: componentCredential.name,
      };

      // ensure all the non optional fields are filled
      if (!checkCredentialData(componentCredential)) return;

      let credentialObj = {};
      for (const key in credentialData) {
        credentialObj[key] = credentialData[key];
      }
      if (Object.keys(credentialObj).length)
        saveObj.credentialObj = credentialObj;

      const saveResp = await credentialsApi.updateCredential(
        credential.id,
        saveObj
      );
      if (saveResp.data) {
        enqueueSnackbar({
          message: "Information updated!",
          options: {
            key: new Date().getTime() + Math.random(),
            variant: "success",
            action: (key) => (
              <Button
                style={{ color: "white" }}
                onClick={() => closeSnackbar(key)}
              >
                <IconX />
              </Button>
            ),
          },
        });
      }
    } catch (error) {
      const errorData = `${error.response.status}: ${error.response.data.detail}`;
      enqueueSnackbar({
        message: `Failed to save information: ${errorData}`,
        options: {
          key: new Date().getTime() + Math.random(),
          variant: "error",
          persist: true,
          action: (key) => (
            <Button
              style={{ color: "white" }}
              onClick={() => closeSnackbar(key)}
            >
              <IconX />
            </Button>
          ),
        },
      });
    }
  };

  return (
    <>
      <MainCard>
        <SectionHeader isWhite={false} title="User Information" />
        <Box>
          {componentCredential && componentCredential.description && (
            <Box sx={{ pl: 2, pr: 2 }}>
              <div
                style={{
                  display: "flex",
                  flexDirection: "row",
                  borderRadius: 10,
                  background: "rgb(254,252,191)",
                  padding: 10,
                  marginTop: 10,
                  marginBottom: 10,
                }}
              >
                <span style={{ color: "rgb(116,66,16)" }}>
                  {parser(componentCredential.description)}
                </span>
              </div>
            </Box>
          )}
          {componentCredential &&
            componentCredential.inputs &&
            componentCredential.inputs.map((inputParam, index) => (
              <ComponentInputHandler
                key={index}
                inputParam={inputParam}
                data={credentialData}
              />
            ))}
          {componentCredential && componentCredential.inputs && (
            <Box sx={{ p: 2 }}>
              <StyledButton
                onClick={credential.id ? save : addNew}
                color="primary"
                variant="contained"
              >
                Save
              </StyledButton>
            </Box>
          )}
        </Box>
        <ConfirmDialog />
      </MainCard>
    </>
  );
};

Home.propTypes = {};

export default Home;
