"use client";

// import { useState } from "react";
import { Button } from "antd";
import { conversations, Conversation } from "@/mock/conversations";

type Props = {
  currentChatId: number;
  setCurrentChatId: (id: number) => void;
};

export default function sidebar({ currentChatId, setCurrentChatId }: Props) {
  return (
    <div className="p-4 h-full flex flex-col">
      <Button type="primary" block className="mb-3">
        + New Chat
      </Button>

      <div className="flex flex-col gap-2">
        {conversations.map((item) => (
          <button
            key={item.id}
            className={`text-left p-2 rounded cursor-pointer ${
              currentChatId === item.id 
              ?  "bg-blue-500 text-white" 
              : "bg-gray-100 text-black hover:bg-gray-300"
            }`}
            onClick={() => setCurrentChatId(item.id)}
          >
            {item.title}
          </button>
        ))}
      </div>
    </div>
  );
}
