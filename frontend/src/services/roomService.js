import api from "./api";

export const getMyRooms = async () => {
  const response = await api.get("/my-rooms/");
  return response.data;
};

export const createMyRoom = async (roomData) => {
  const response = await api.post("/my-rooms/", roomData);
  return response.data;
};

// Keep this for the existing CreateRoomPage
export const createRoom = async (roomData) => {
  const response = await api.post("/rooms/", roomData);
  return response.data;
};

export const getRooms = async () => {
  const response = await api.get("/rooms/");
  return response.data;
};

export const getRoom = async (roomId) => {
  const response = await api.get(`/rooms/${roomId}`);
  return response.data;
};

export const updateRoom = async (roomId, roomData) => {
  const response = await api.patch(
    `/rooms/${roomId}`,
    roomData
  );
  return response.data;
};

export const deleteRoom = async (roomId) => {
  const response = await api.delete(`/rooms/${roomId}`);
  return response.data;
};