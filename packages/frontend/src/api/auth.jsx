import client from "./client";

const loginUser = (data) => client.post("/login", data);

const logoutUser = () => client.get("/logout");

const signUp = (data) => client.post("/signup", data);

const checkAuth = () => client.get("/auth/check");

const authApi = {
  loginUser,
  logoutUser,
  checkAuth,
  signUp,
};

export default authApi;
