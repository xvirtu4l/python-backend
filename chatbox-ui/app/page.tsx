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

  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    const newMessage: Message = {
      id: Date.now(),
      role: "user",
      content: text,
    };
    setMessages((prev) => [...prev, newMessage]);

    try {
      const response = await chatService.sendMessage(text, currentChatId);
      const persistedMessages: Message[] = [
        response.user_message,
        response.assistant_message,
      ];

      setMessages((prev) => [...prev.slice(0, -1), ...persistedMessages]);
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
    } catch {
      setChatError("Failed to send message");
      setMessages((prev) => prev.filter((m) => m.id !== newMessage.id));
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
