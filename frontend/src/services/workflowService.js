import api from "./api";

export const getRoomWorkflow = async (roomId) => {
  const response = await api.get(`/workflow/room/${roomId}`);
  return response.data;
};

export const getActiveRotations = async (roomId) => {
  const response = await api.get(`/workflow/room/${roomId}/active`);
  return response.data;
};

export const assignTask = async (roomId, taskId) => {
  const response = await api.post(
    `/workflow/room/${roomId}/task/${taskId}/assign`
  );

  return response.data;
};

export const completeRotation = async (rotationId) => {
  const response = await api.patch(
    `/workflow/rotation/${rotationId}/complete`
  );

  return response.data;
};