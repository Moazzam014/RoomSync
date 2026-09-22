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
      frequency:
        taskData.frequency || "daily",
      room_id: Number(taskData.room_id),
    }
  );

  return response.data;
};

export const updateTask = async (
  taskId,
  taskData
) => {
  const params = {};

  if (taskData.name !== undefined) {
    params.name = taskData.name;
  }

  if (taskData.description !== undefined) {
    params.description =
      taskData.description;
  }

  if (taskData.frequency !== undefined) {
    params.frequency =
      taskData.frequency;
  }

  if (taskData.is_active !== undefined) {
    params.is_active =
      taskData.is_active;
  }

  const response = await api.patch(
    `/tasks/${taskId}`,
    null,
    {
      params,
    }
  );

  return response.data;
};

export const deactivateTask = async (
  taskId
) => {
  const response = await api.delete(
    `/tasks/${taskId}`
  );

  return response.data;
};