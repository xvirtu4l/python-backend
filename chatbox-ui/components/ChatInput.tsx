"use client";

import { useState } from "react";
import { Button, Input } from "antd";

type Props = {
    onSend: (message: string) => void;
    disabled?: boolean;
};


export default function ChatInput( {onSend, disabled = false}: Props) {
    const [text, setText] = useState("");

    const handleSend = () => {
        if (!text.trim() || disabled) return;
        onSend(text.trim());
        setText("");
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="border-t border-(--border) bg-[rgba(255,248,240,0.9)] px-4 py-4 sm:px-6">
            <div className="mx-auto flex max-w-4xl items-end gap-3 rounded-[28px] border border-[rgba(115,87,58,0.12)] bg-[rgba(255,252,247,0.96)] px-3 py-3 shadow-[0_12px_24px_rgba(69,48,28,0.08)]">
            <Input.TextArea
            placeholder="Ask something, continue a thread, or drop in a task..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            variant="borderless"
            autoSize={{ minRows: 1, maxRows: 6 }}
            className="rounded-[22px]! bg-transparent! px-4! py-3! text-[15px]! leading-7! text-foreground! placeholder:text-(--ink-soft)!"
            />

            <Button
                type="primary"
                onClick={handleSend}
                disabled={!text.trim() || disabled}
                className="h-11 rounded-full border-0 bg-(--accent)! px-6 font-semibold! shadow-none! hover:bg-(--accent-deep)! disabled:bg-[rgba(187,90,52,0.35)]! disabled:text-white/80!"
            >
                {disabled ? "Thinking..." : "Send"}
            </Button>
            </div>
            <div className="mx-auto mt-2 max-w-4xl px-2 text-xs text-(--ink-soft)">
                Press Enter to send, Shift+Enter for a new line
            </div>
        </div>
    );
}
