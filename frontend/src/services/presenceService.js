import api from "./api";

export const recordPresence = async (presenceData) => {
  const response = await api.post("/presence/", presenceData);
  return response.data;
};

export const getMemberPresence = async (memberId) => {
  const response = await api.get(`/presence/member/${memberId}`);
  return response.data;
};