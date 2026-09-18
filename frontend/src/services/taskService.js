import api from "./api";

export const getRoomTasks = async (roomId) => {
  const response = await api.get(`/tasks/room/${roomId}`);
  return response.data;
};

export const getTask = async (taskId) => {
  const response = await api.get(`/tasks/${taskId}`);
  return response.data;
};

export const createTask = async (taskData) => {
  const response = await api.post("/tasks/", taskData);
  return response.data;
};

export const updateTask = async (taskId, taskData) => {
  const response = await api.patch(`/tasks/${taskId}`, taskData);
  return response.data;
};

export const deactivateTask = async (taskId) => {
  const response = await api.delete(`/tasks/${taskId}`);
  return response.data;
};