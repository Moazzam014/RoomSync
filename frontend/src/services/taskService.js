
import api from "./api";

export const getRoomTasks = async (roomId) => {
  const response = await api.get(
    `/tasks/room/${roomId}`
  );

  return response.data;
};

export const getTask = async (taskId) => {
  const response = await api.get(
    `/tasks/${taskId}`
  );

  return response.data;
};

export const createTask = async (taskData) => {
  const response = await api.post(
    "/tasks/",
    {
      name: taskData.name,
      description: taskData.description || null,
      frequency: taskData.frequency || "daily",
      room_id: Number(taskData.room_id),
    }
  );

  return response.data;
};

export const updateTask = async (taskId, taskData) => {
  const payload = {};

  if (taskData.name !== undefined) {
    payload.name = taskData.name;
  }

  if (taskData.description !== undefined) {
    payload.description = taskData.description;
  }

  if (taskData.frequency !== undefined) {
    payload.frequency = taskData.frequency;
  }

  const response = await api.patch(
    `/tasks/${taskId}`,
    payload
  );

  return response.data;
};

export const deactivateTask = async (taskId) => {
  const response = await api.delete(
    `/tasks/${taskId}`
  );

  return response.data;
};
