import api from "./api";

export const getRoomMembers = async (roomId) => {
  const response = await api.get(`/members/room/${roomId}`);
  return response.data;
};

export const getMember = async (memberId) => {
  const response = await api.get(`/members/${memberId}`);
  return response.data;
};

export const createMember = async (memberData) => {
  const response = await api.post("/members/", memberData);
  return response.data;
};

export const updateMember = async (memberId, memberData) => {
  const response = await api.patch(`/members/${memberId}`, memberData);
  return response.data;
};

export const deactivateMember = async (memberId) => {
  const response = await api.delete(`/members/${memberId}`);
  return response.data;
};