import api from "./api";

export const getMemberNotifications = async (memberId) => {
  const response = await api.get(
    `/notifications/member/${memberId}`
  );

  return response.data;
};

export const markNotificationAsRead = async (notificationId) => {
  const response = await api.patch(
    `/notifications/${notificationId}/read`
  );

  return response.data;
};