"use client";

import { useState, useRef, useEffect } from "react";
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
  "ฟอร์ม Liverpool 5 นัดล่าสุด",
];

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "bot", text: "สวัสดีครับ! ผม FootballBot วิเคราะห์ฟุตบอลให้ได้เลย EPL, La Liga, Champions League ถามได้ทุกเรื่องครับ" },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

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
    <main className="min-h-screen bg-slate-950 flex flex-col items-center justify-start py-6 px-4">
      <div className="w-full max-w-2xl flex flex-col gap-3 h-screen max-h-screen">

        {/* Header */}
        <div className="bg-slate-900 rounded-2xl border border-slate-800 px-5 py-3 flex items-center gap-3 flex-shrink-0">
          <div className="w-10 h-10 rounded-full bg-sky-500 flex items-center justify-center text-white font-medium text-sm">
            FB
          </div>
          <div>
            <p className="font-medium text-slate-100 text-sm">FootballBot</p>
            <p className="text-xs text-slate-500">EPL · La Liga · Champions League</p>
          </div>
          <div className="ml-auto flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-emerald-400" />
            <span className="text-xs text-slate-500">Online</span>
          </div>
        </div>

        {/* Messages */}
        <div className="bg-slate-900 rounded-2xl border border-slate-800 flex-1 overflow-y-auto p-4 flex flex-col gap-3 min-h-0">
          {messages.map((m, i) => (
            <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
              {m.role === "bot" && (
                <div className="w-6 h-6 rounded-full bg-sky-500 flex items-center justify-center text-white text-xs mr-2 flex-shrink-0 mt-1">
                  F
                </div>
              )}
              <div className={`rounded-2xl px-4 py-2.5 max-w-sm text-sm leading-relaxed whitespace-pre-wrap ${
                m.role === "user"
                  ? "bg-sky-500 text-white rounded-br-sm"
                  : "bg-slate-800 text-slate-200 rounded-bl-sm border border-slate-700"
              }`}>
                {m.text}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start items-center gap-2">
              <div className="w-6 h-6 rounded-full bg-sky-500 flex items-center justify-center text-white text-xs flex-shrink-0">
                F
              </div>
              <div className="bg-slate-800 border border-slate-700 rounded-2xl rounded-bl-sm px-4 py-3 flex gap-1.5 items-center">
                <div className="w-1.5 h-1.5 rounded-full bg-slate-500 animate-bounce" style={{animationDelay:"0ms"}} />
                <div className="w-1.5 h-1.5 rounded-full bg-slate-500 animate-bounce" style={{animationDelay:"150ms"}} />
                <div className="w-1.5 h-1.5 rounded-full bg-slate-500 animate-bounce" style={{animationDelay:"300ms"}} />
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Quick chips */}
        <div className="flex flex-wrap gap-2 flex-shrink-0">
          {QUICK_CHIPS.map((chip) => (
            <button
              key={chip}
              onClick={() => handleSend(chip)}
              disabled={loading}
              className="px-3 py-1.5 rounded-full border border-slate-700 bg-slate-900 text-xs text-slate-400 hover:bg-slate-800 hover:text-slate-200 hover:border-slate-600 transition disabled:opacity-40"
            >
              {chip}
            </button>
          ))}
        </div>

        {/* Input */}
        <div className="bg-slate-900 rounded-2xl border border-slate-700 flex items-center gap-3 px-4 py-3 flex-shrink-0 focus-within:border-sky-500 transition">
          <input
            className="flex-1 text-sm outline-none text-slate-200 placeholder-slate-600 bg-transparent"
            placeholder="ถามเรื่องฟุตบอลได้เลย..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button
            onClick={() => handleSend()}
            disabled={loading || !input.trim()}
            className="bg-sky-500 hover:bg-sky-400 disabled:opacity-30 disabled:cursor-not-allowed text-white text-sm px-4 py-1.5 rounded-full transition font-medium"
          >
            ส่ง
          </button>
        </div>

      </div>
    </main>
  );
}