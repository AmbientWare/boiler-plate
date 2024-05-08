import client from "./client";

const getUserCredentials = () => client.get("/credentials");

const getAllComponentsCredentials = () => client.get("/credentials/components");

const getSpecificCredential = (id) => client.get(`/credentials/${id}`);

const getCredentialsByNames = (names) =>
  client.get(`/credentials/names/${names}`);

const getSpecificComponentCredential = (name) =>
  client.get(`/credentials/components/${name}`);

const createCredential = (body) => client.post(`/credentials/new`, body);

const updateCredential = (id, body) => client.put(`/credentials/${id}`, body);

const deleteCredential = (id) => client.delete(`/credentials/${id}`);

export default {
  getUserCredentials,
  getAllComponentsCredentials,
  getSpecificCredential,
  getCredentialsByNames,
  getSpecificComponentCredential,
  createCredential,
  updateCredential,
  deleteCredential,
};
