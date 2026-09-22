import api from "./api";

export const register = async (userData) => {
  const response = await api.post("/auth/register", userData);
  return response.data;
};

export const login = async (username, password) => {
  const response = await api.post("/auth/login", {
    username,
    password,
  });

  localStorage.setItem("roomsync_token", response.data.access_token);
  localStorage.setItem(
    "roomsync_user",
    JSON.stringify(response.data.user)
  );

  return response.data;
};

export const logout = () => {
  localStorage.removeItem("roomsync_token");
  localStorage.removeItem("roomsync_user");
};

export const getStoredUser = () => {
  const user = localStorage.getItem("roomsync_user");

  return user ? JSON.parse(user) : null;
};

export const getToken = () => {
  return localStorage.getItem("roomsync_token");
};

export const isLoggedIn = () => {
  return Boolean(localStorage.getItem("roomsync_token"));
};