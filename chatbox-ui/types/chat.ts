export interface Message {
  id?: number;
  role: "user" | "assistant";
  content: string;
  created_at?: string;
  pending?: boolean;
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
