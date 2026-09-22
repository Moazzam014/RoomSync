import api from "./api";

export const sendInvitation = async ({
  room_id,
  invitee_username,
}) => {
  const response = await api.post(
    "/invitations/",
    {
      room_id: Number(room_id),
      invitee_username:
        invitee_username.trim(),
    }
  );

  return response.data;
};

export const getMyInvitations = async () => {
  const response = await api.get(
    "/invitations/me"
  );

  return response.data;
};

export const acceptInvitation = async (
  invitationId
) => {
  const response = await api.patch(
    `/invitations/${invitationId}/accept`
  );

  return response.data;
};

export const declineInvitation = async (
  invitationId
) => {
  const response = await api.patch(
    `/invitations/${invitationId}/decline`
  );

  return response.data;
};