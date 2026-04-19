"use client";

import { useState } from "react";
import { sendMessage } from "../lib/api";

type Message = {
  role: "user" | "bot";
  text: string;
};

const QUICK_CHIPS = [
  "วิเคราะห์ Man City วันนี้",
  "ตารางคะแนน EPL",
  "Top scorers ฤดูกาลนี้",
  "วิเคราะห์ Real vs Barca",
];

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "bot", text: "สวัสดีครับ! ถามเรื่องฟุตบอลได้เลย" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSend(text?: string) {
    const msg = text || input.trim();
    if (!msg || loading) return;

    setMessages((prev) => [...prev, { role: "user", text: msg }]);
    setInput("");
    setLoading(true);

    try {
      const data = await sendMessage(msg, "session1");
      setMessages((prev) => [...prev, { role: "bot", text: data.reply }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "เกิดข้อผิดพลาด กรุณาลองใหม่ครับ" },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 flex flex-col items-center py-8 px-4">
      <div className="w-full max-w-2xl flex flex-col gap-4">
        <div className="bg-white rounded-2xl border border-gray-200 px-5 py-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center text-green-700 font-medium text-sm">
            FB
          </div>
          <div>
            <p className="font-medium text-gray-900">FootballBot</p>
            <p className="text-xs text-gray-400">EPL · La Liga · Champions League</p>
          </div>
          <div className="ml-auto w-2 h-2 rounded-full bg-green-400" />
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 p-4 flex flex-col gap-3 min-h-96">
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
              <div className={`rounded-2xl px-4 py-2 max-w-sm text-sm leading-relaxed ${
                m.role === "user"
                  ? "bg-blue-50 text-blue-900 rounded-br-sm"
                  : "bg-gray-100 text-gray-800 rounded-bl-sm"
              }`}>
                {m.text}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-2xl rounded-bl-sm px-4 py-2 text-sm text-gray-400">
                กำลังวิเคราะห์...
              </div>
            </div>
          )}
        </div>

        <div className="flex flex-wrap gap-2">
          {QUICK_CHIPS.map((chip) => (
            <button
              key={chip}
              onClick={() => handleSend(chip)}
              className="px-3 py-1.5 rounded-full border border-gray-200 bg-white text-sm text-gray-600 hover:bg-gray-50 transition"
            >
              {chip}
            </button>
          ))}
        </div>

        <div className="bg-white rounded-2xl border border-gray-200 flex items-center gap-3 px-4 py-3">
          <input
            className="flex-1 text-sm outline-none text-gray-800 placeholder-gray-400"
            placeholder="ถามเรื่องฟุตบอลได้เลย..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button
            onClick={() => handleSend()}
            disabled={loading}
            className="bg-blue-500 hover:bg-blue-600 disabled:opacity-40 text-white text-sm px-4 py-1.5 rounded-full transition"
          >
            ส่ง
          </button>
        </div>
      </div>
    </main>
  );
}