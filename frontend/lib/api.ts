import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export async function sendMessage(message: string, sessionId: string) {
  const res = await api.post("/api/chat", {
    message,
    session_id: sessionId,
  });
  return res.data;
}