"use client";

import SidebarNew from "@/components/SidebarNew";
import ChatWindow from "@/components/ChatWindow";
import ChatInput from "@/components/ChatInput";
import { useEffect, useRef, useState } from "react";
import { chatService } from "@/services/chatService";
import { Message, Conversation } from "@/types/chat";
import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";

export default function Home() {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();
  const [currentChatId, setCurrentChatId] = useState<number | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] =
    useState<Conversation | null>(null);
  const [loadingMessages, setLoadingMessages] = useState(true);
  const [loadingConversations, setLoadingConversations] = useState(true);
  const [bootstrappingPage, setBootstrappingPage] = useState(true);
  const [conversationError, setConversationError] = useState<string | null>(null);
  const [chatError, setChatError] = useState<string | null>(null);
  const skipNextMessageReloadRef = useRef(false);
  const currentChatIdRef = useRef<number | null>(null);

  useEffect(() => {
    currentChatIdRef.current = currentChatId;
  }, [currentChatId]);

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.push("/login");
      return;
    }

    if (isAuthenticated) {
      fetchConversations(null, false);
    }
  }, [isAuthenticated, loading, router]);

  const fetchConversations = async (
    preferredConversationId?: number | null,
    selectConversation = true,
    showLoadingState = true
  ) => {
    try {
      if (showLoadingState) {
        setLoadingConversations(true);
      }
      const data = await chatService
        .getConversations()
        .then((items) =>
          [...items].sort(
            (a, b) =>
              new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
          )
        );
      setConversations(data);
      if (!selectConversation) {
        setSelectedConversation(null);
        setCurrentChatId(null);
        setMessages([]);
        setLoadingMessages(false);
        setConversationError(null);
      } else if (data.length > 0) {
        const nextConversation =
          data.find((conversation) => conversation.id === preferredConversationId) ??
          data[0];
        setSelectedConversation(nextConversation);
        setCurrentChatId(nextConversation.id);
        setConversationError(null);
      } else {
        setSelectedConversation(null);
        setCurrentChatId(null);
        setMessages([]);
        setLoadingMessages(false);
        setConversationError(null);
      }

      return data;
    } catch {
      setConversationError("Failed to fetch conversations");
      return [];
    } finally {
      if (showLoadingState) {
        setLoadingConversations(false);
      }
      setBootstrappingPage(false);
    }
  };

  useEffect(() => {
    const loadMessages = async () => {
      if (!currentChatId) {
        setLoadingMessages(false);
        return;
      }

      if (skipNextMessageReloadRef.current) {
        skipNextMessageReloadRef.current = false;
        setLoadingMessages(false);
        return;
      }

      try {
        setLoadingMessages(true);
        const data = await chatService.getConversationMessages(currentChatId);
        setMessages(data);
        setChatError(null);
      } catch {
        setChatError("Failed to fetch messages");
      } finally {
        setLoadingMessages(false);
      }
    };

    loadMessages();
  }, [currentChatId]);

  const wait = (ms: number) =>
    new Promise((resolve) => {
      window.setTimeout(resolve, ms);
    });

  const pollForAssistantReply = async (
    conversationId: number,
    userMessageId?: number
  ) => {
    const maxAttempts = 25;

    for (let attempt = 0; attempt < maxAttempts; attempt += 1) {
      await wait(1200);

      try {
        const fetchedMessages = await chatService.getConversationMessages(conversationId);
        const assistantReply = fetchedMessages.find(
          (message) =>
            message.role === "assistant" &&
            (userMessageId === undefined || (message.id ?? 0) > userMessageId)
        );

        if (assistantReply) {
          if (currentChatIdRef.current === conversationId) {
            setMessages(fetchedMessages);
            setChatError(null);
          }

          await fetchConversations(conversationId, true, false);
          return;
        }
      } catch {
        // Keep polling quietly; the normal page error state handles persistent failures.
      }
    }

    if (currentChatIdRef.current === conversationId) {
      setMessages((prev) =>
        prev.map((message) =>
          message.pending
            ? {
                ...message,
                pending: false,
                content: "The assistant is taking longer than expected. Please wait a moment and reopen the conversation.",
              }
            : message
        )
      );
    }
  };

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    try {
      const response = await chatService.sendMessage(text, currentChatId);
      const pendingAssistantMessage: Message = {
        id: -(response.user_message.id ?? Date.now()),
        role: "assistant",
        content: "Thinking...",
        pending: true,
      };

      setMessages((prev) => [...prev, response.user_message, pendingAssistantMessage]);
      setChatError(null);
      const updatedConversations = await fetchConversations(
        response.conversation_id,
        true,
        false
      );

      const matchingConversation = updatedConversations.find(
        (conversation) => conversation.id === response.conversation_id
      );

      if (matchingConversation) {
        setConversations(updatedConversations);
        setSelectedConversation(matchingConversation);
        if (currentChatId !== matchingConversation.id) {
          skipNextMessageReloadRef.current = true;
          setCurrentChatId(matchingConversation.id);
        }
      }

      void pollForAssistantReply(response.conversation_id, response.user_message.id);
    } catch {
      setChatError("Failed to send message");
    }
  };

  const handleChatChange = (conversation: Conversation) => {
    setSelectedConversation(conversation);
    setCurrentChatId(conversation.id);
  };

  const handleDeleteConversation = async (conversationId: number) => {
    await chatService.deleteConversation(conversationId);

    const remainingConversations = conversations.filter(
      (conversation) => conversation.id !== conversationId
    );

    setConversations(remainingConversations);

    if (currentChatId === conversationId) {
      if (remainingConversations.length > 0) {
        const nextConversation = remainingConversations[0];
        setSelectedConversation(nextConversation);
        setCurrentChatId(nextConversation.id);
      } else {
        setSelectedConversation(null);
        setCurrentChatId(null);
        setMessages([]);
        setLoadingMessages(false);
      }
    }
  };

  const handleNewChat = () => {
    setSelectedConversation(null);
    setCurrentChatId(null);
    setMessages([]);
    setLoadingMessages(false);
    setChatError(null);
  };

  if (loading || bootstrappingPage) {
    return (
      <div className="flex min-h-screen items-center justify-center px-6">
        <div className="panel-card rounded-full px-6 py-4 text-sm text-(--ink-soft)">
          Loading your workspace...
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen overflow-hidden p-3 sm:p-5">
      <div className="app-shell grid h-[calc(100vh-1.5rem)] overflow-hidden rounded-[34px] border border-(--border) lg:grid-cols-[360px_minmax(0,1fr)]">
      <div className="min-h-0 border-b border-(--border) lg:border-b-0 lg:border-r">
        <SidebarNew
          conversations={conversations}
          currentChatId={currentChatId ?? 0}
          setCurrentChatId={handleChatChange}
          onNewChat={handleNewChat}
          onDeleteConversation={handleDeleteConversation}
          loading={loadingConversations}
        />
        {conversationError && (
          <div className="px-5 pb-4 text-sm text-(--accent-deep)">{conversationError}</div>
        )}
      </div>

      <div className="flex min-h-0 flex-col">
        <div className="shrink-0 flex items-center justify-between border-b border-(--border) px-6 py-5">
          <div>
            <div className="text-xs uppercase tracking-[0.28em] text-(--ink-soft)">
              Active Conversation
            </div>
            <div className="mt-2 text-2xl font-semibold">
              {selectedConversation?.title || "Fresh conversation"}
            </div>
          </div>
          <div className="hidden rounded-full bg-white/60 px-4 py-2 text-xs font-medium text-(--ink-soft) sm:block">
            {messages.length} messages
          </div>
        </div>

        {loadingMessages ? (
          <div className="flex min-h-0 flex-1 items-center justify-center px-6">
            <div className="rounded-full border border-(--border) bg-white/70 px-5 py-3 text-sm text-(--ink-soft)">
              Loading messages...
            </div>
          </div>
        ) : (
          <ChatWindow messages={messages} error={chatError ?? undefined} />
        )}
        <ChatInput onSend={handleSendMessage} />
      </div>
      </div>
    </div>
  );
}
