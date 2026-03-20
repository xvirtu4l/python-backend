import axios from "axios";
import apiClient from "./api";

function getErrorMessage(error: unknown, fallback: string) {
  if (axios.isAxiosError(error)) {
    return error.response?.data?.detail || fallback;
  }

  return fallback;
}

export interface Message {
  id?: number;
  role: "user" | "assistant";
  content: string;
  created_at?: string;
}

export interface Conversation {
  id: number;
  title: string;
  created_at: string;
  updated_at: string;
}

export interface ChatAPIResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}

export interface ChatResponse {
  conversation_id: number;
  user_message: Message;
  assistant_message: Message;
}

class ChatService {
  async getConversations(): Promise<Conversation[]> {
    try {
      const response = await apiClient.get<Conversation[]>("/chatbot/conversations");
      return response.data;
    } catch (error: unknown) {
      throw new Error(getErrorMessage(error, "Failed to fetch conversations"));
    }
  }

  async getConversationMessages(conversationId: number): Promise<Message[]> {
    try {
      const response = await apiClient.get<{
        conversation: Conversation;
        messages: Message[];
      }>(`/chatbot/conversations/${conversationId}`);
      return response.data.messages;
    } catch (error: unknown) {
      throw new Error(getErrorMessage(error, "Failed to fetch messages"));
    }
  }

  async sendMessage(
    content: string,
    conversationId?: number | null
  ): Promise<ChatResponse> {
    try {
      const response = await apiClient.post<ChatResponse>("/chatbot/chat", {
        conversation_id: conversationId ?? null,
        message: content,
      });

      return response.data;
    } catch (error: unknown) {
      throw new Error(getErrorMessage(error, "Failed to send message"));
    }
  }

  async deleteConversation(conversationId: number): Promise<void> {
    try {
      await apiClient.delete(`/chatbot/conversations/${conversationId}`);
    } catch (error: unknown) {
      throw new Error(getErrorMessage(error, "Failed to delete conversation"));
    }
  }

  async createConversation(
    content: string
  ): Promise<ChatResponse> {
    return this.sendMessage(content, null);
  }
}

export const chatService = new ChatService();
