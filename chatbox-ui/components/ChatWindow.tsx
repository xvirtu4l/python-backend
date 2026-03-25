"use client";

import { useEffect, useRef } from "react";

interface Message {
  id?: number;
  role: "user" | "assistant";
  content: string;
  created_at?: string;
  pending?: boolean;
}

type Props = {
  messages: Message[];
  loading?: boolean;
  error?: string;
};

export default function ChatWindow({ messages, loading = false, error }: Props) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const shouldStickToBottomRef = useRef(true);

  useEffect(() => {
    const container = scrollRef.current;
    if (!container) {
      return;
    }

    if (shouldStickToBottomRef.current) {
      container.scrollTop = container.scrollHeight;
    }
  }, [messages]);

  const handleScroll = () => {
    const container = scrollRef.current;
    if (!container) {
      return;
    }

    const distanceFromBottom =
      container.scrollHeight - container.scrollTop - container.clientHeight;
    shouldStickToBottomRef.current = distanceFromBottom < 120;
  };

  if (loading) {
    return (
      <div className="chat-scroll flex min-h-0 flex-1 items-center justify-center overflow-y-auto px-6 py-8">
        <div className="flex items-center gap-3 rounded-full border border-(--border) bg-white/70 px-5 py-3 text-sm text-(--ink-soft)">
          <div className="h-5 w-5 animate-spin rounded-full border-2 border-[rgba(187,90,52,0.2)] border-t-(--accent)"></div>
          Fetching the conversation...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="chat-scroll flex min-h-0 flex-1 items-center justify-center overflow-y-auto px-6 py-8">
        <div className="rounded-3xl border border-[#e6b8a7] bg-[#fff3ee] px-6 py-5 text-center text-(--accent-deep) shadow-[0_12px_30px_rgba(139,68,43,0.08)]">
          <div className="text-xs uppercase tracking-[0.28em] opacity-70">Chat Error</div>
          <div className="mt-2 text-sm">
          {error}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      ref={scrollRef}
      onScroll={handleScroll}
      className="chat-scroll min-h-0 flex-1 overflow-y-auto px-6 py-6"
    >
      {messages.length === 0 ? (
        <div className="flex h-full min-h-112 items-center justify-center">
          <div className="max-w-md rounded-[28px] border border-dashed border-(--border) bg-white/45 px-8 py-10 text-center">
            <div className="text-xs uppercase tracking-[0.3em] text-(--ink-soft)">
              New Thread
            </div>
            <div className="mt-3 text-3xl font-semibold leading-tight">
              Start with one clear message.
            </div>
            <p className="mt-4 text-sm leading-7 text-(--ink-soft)">
              Ask a question, paste an idea, or continue a workflow. Your assistant reply will appear here.
            </p>
          </div>
        </div>
      ) : (
        <div className="mx-auto flex w-full max-w-4xl flex-col gap-4">
        {messages.map((m, index) => (
          <div 
            key={m.id ?? `${m.role}-${m.created_at ?? "pending"}-${index}`}
            className={`group max-w-[85%] rounded-[26px] px-5 py-4 shadow-[0_18px_34px_rgba(69,48,28,0.08)] ${
              m.role === "user" 
              ? "self-end bg-[linear-gradient(135deg,var(--highlight),var(--highlight-strong))] text-(--highlight-text)"
              : "surface-soft self-start text-foreground"
            }`}
          >
            {/* <div className="mb-2 text-[10px] uppercase tracking-[0.26em] opacity-65">
              {m.role === "user" ? "You" : "Assistant"}
            </div> */}
            <div className="whitespace-pre-wrap text-sm leading-7">
              {m.content}
            </div>
            {m.pending && (
              <div className="mt-3 text-xs italic text-(--ink-soft)">
                Assistant is thinking...
              </div>
            )}
          </div>
        ))}
        </div>
      )}
    </div>
  );
}
