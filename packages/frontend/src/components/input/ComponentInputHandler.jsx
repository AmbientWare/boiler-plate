import PropTypes from "prop-types";
import { useRef, useState } from "react";

// material-ui
import { Box, Typography, IconButton } from "@mui/material";
import {
  IconArrowsMaximize,
  IconAlertTriangle,
  IconEdit,
} from "@tabler/icons-react";

import { Dropdown } from "@components/dropdown/Dropdown";
import { AsyncDropdown } from "@components/dropdown/AsyncDropdown";
import { Input } from "@components/input/Input";
import { SwitchInput } from "@components/switch/Switch";
import { TooltipWithParser } from "@components/tooltip/TooltipWithParser";

//api
import credentialsApi from "@api/credentials";

// ===========================|| ComponentInputHandler ||=========================== //

const ComponentInputHandler = ({
  inputParam,
  data,
  onSelect,
  disabled = false,
}) => {
  const ref = useRef(null);

  const [credentialId, setCredentialId] = useState(data?.credential ?? "");

  const [reloadTimestamp, setReloadTimestamp] = useState(Date.now().toString());

  // const addAsyncCredential = async () => {
  //   try {
  //     let names = "";
  //     if (inputParam.credentialNames.length > 1) {
  //       names = inputParam.credentialNames.join("&");
  //     } else {
  //       names = inputParam.credentialNames[0];
  //     }
  //     const componentCredentialsResp =
  //       await credentialsApi.getSpecificComponentCredential(names);
  //     if (componentCredentialsResp.data) {
  //       if (Array.isArray(componentCredentialsResp.data)) {
  //         const dialogProp = {
  //           title: "Add New Credential",
  //           componentsCredentials: componentCredentialsResp.data,
  //         };
  //         // setCredentialListDialogProps(dialogProp);
  //         // setShowCredentialListDialog(true);
  //       } else {
  //         const dialogProp = {
  //           type: "ADD",
  //           cancelButtonName: "Cancel",
  //           confirmButtonName: "Add",
  //           credentialComponent: componentCredentialsResp.data,
  //         };
  //         // setSpecificCredentialDialogProps(dialogProp);
  //         // setShowSpecificCredentialDialog(true);
  //       }
  //     }
  //   } catch (error) {
  //     console.error(error);
  //   }
  // };

  const [showExpandDialog, setShowExpandDialog] = useState(false);
  const [expandDialogProps, setExpandDialogProps] = useState({});

  const onExpandDialogClicked = (value, inputParam) => {
    const dialogProp = {
      value,
      inputParam,
      disabled,
      confirmButtonName: "Save",
      cancelButtonName: "Cancel",
    };
    setExpandDialogProps(dialogProp);
    setShowExpandDialog(true);
  };

  const onExpandDialogSave = (newValue, inputParamName) => {
    setShowExpandDialog(false);
    data[inputParamName] = newValue;
  };

  return (
    <div ref={ref}>
      {inputParam && (
        <>
          <Box sx={{ p: 2 }}>
            <div style={{ display: "flex", flexDirection: "row" }}>
              {inputParam.type !== "oauth" && (
                <Typography>
                  {inputParam.label}
                  {!inputParam.optional && (
                    <span style={{ color: "red" }}>&nbsp;*</span>
                  )}
                  {inputParam.description && (
                    <TooltipWithParser
                      style={{ marginLeft: 10 }}
                      title={inputParam.description}
                    />
                  )}
                </Typography>
              )}
              <div style={{ flexGrow: 1 }}></div>
              {inputParam.type === "string" && inputParam.rows && (
                <IconButton
                  size="small"
                  sx={{
                    height: 25,
                    width: 25,
                  }}
                  title="Expand"
                  color="primary"
                  onClick={() =>
                    onExpandDialogClicked(
                      data[inputParam.name] ?? inputParam.default ?? "",
                      inputParam
                    )
                  }
                >
                  <IconArrowsMaximize />
                </IconButton>
              )}
            </div>
            {inputParam.warning && (
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
                <IconAlertTriangle size={36} color="orange" />
                <span style={{ color: "rgb(116,66,16)", marginLeft: 10 }}>
                  {inputParam.warning}
                </span>
              </div>
            )}

            {inputParam.type === "boolean" && (
              <SwitchInput
                disabled={disabled}
                onChange={(newValue) => (data[inputParam.name] = newValue)}
                value={data[inputParam.name] ?? inputParam.default ?? false}
              />
            )}
            {(inputParam.type === "string" ||
              inputParam.type === "password" ||
              inputParam.type === "number") && (
              <Input
                key={data[inputParam.name]}
                disabled={disabled}
                inputParam={inputParam}
                onChange={(newValue) => {
                  data[inputParam.name] = newValue;
                  inputParam.value = newValue;
                }}
                value={data[inputParam.name] ?? inputParam.default ?? ""}
                showDialog={showExpandDialog}
                dialogProps={expandDialogProps}
                onDialogCancel={() => setShowExpandDialog(false)}
                onDialogConfirm={(newValue, inputParamName) =>
                  onExpandDialogSave(newValue, inputParamName)
                }
              />
            )}
            {inputParam.type === "options" && (
              <Dropdown
                disabled={disabled}
                name={inputParam.name}
                options={inputParam.options}
                onSelect={(newValue) => {
                  data[inputParam.name] = newValue;
                  onSelect(newValue);
                }}
                value={
                  data[inputParam.name] ??
                  inputParam.default ??
                  "choose an option"
                }
              />
            )}
            {inputParam.type === "credential" && (
              <>
                <div style={{ marginTop: 10 }} />
                <div
                  key={reloadTimestamp}
                  style={{ display: "flex", flexDirection: "row" }}
                >
                  <AsyncDropdown
                    disabled={disabled}
                    name={inputParam.name}
                    nodeData={data}
                    value={credentialId ?? "choose an option"}
                    isCreateNewOption={true}
                    credentialNames={inputParam.credentialNames}
                    onSelect={(newValue) => {
                      setCredentialId(newValue);
                      onSelect(newValue);
                    }}
                    // onCreateNew={() => addAsyncCredential(inputParam.name)}
                  />
                  {credentialId && (
                    <IconButton
                      title="Edit"
                      color="primary"
                      size="small"
                      // onClick={() => editCredential(credentialId)}
                    >
                      <IconEdit />
                    </IconButton>
                  )}
                </div>
              </>
            )}
          </Box>
        </>
      )}
    </div>
  );
};

ComponentInputHandler.propTypes = {
  inputAnchor: PropTypes.object,
  inputParam: PropTypes.object,
  onSelect: PropTypes.func,
  data: PropTypes.object,
  disabled: PropTypes.bool,
};

export default ComponentInputHandler;
