import { useEffect, useMemo, useRef, useState } from "react";
import { Button, Modal } from "antd";
import { useAuth } from "@/context/AuthContext";
import { authService } from "@/services/authService";
import { message } from "antd";
import { Conversation } from "@/types/chat";

type Props = {
  conversations: Conversation[];
  currentChatId: number;
  setCurrentChatId: (conversation: Conversation) => void;
  onNewChat: () => void;
  onDeleteConversation: (conversationId: number) => Promise<void>;
  loading: boolean;
};

export default function SidebarNew({ 
  conversations, 
  currentChatId, 
  setCurrentChatId,
  onNewChat,
  onDeleteConversation,
  loading 
}: Props) {
  const { user, logout, isAuthenticated, refreshUser } = useAuth();
  const [avatarSrc, setAvatarSrc] = useState<string | null>(null);
  const [uploadingAvatar, setUploadingAvatar] = useState(false);
  const [deletingConversationId, setDeletingConversationId] = useState<number | null>(null);
  const [pendingDeleteConversation, setPendingDeleteConversation] = useState<Conversation | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const initials = useMemo(() => {
    const label = user?.username?.trim() || user?.email?.trim() || "U";
    return label.slice(0, 1).toUpperCase();
  }, [user?.email, user?.username]);

  useEffect(() => {
    const loadAvatar = async () => {
      if (!user?.avatar_url) {
        setAvatarSrc(null);
        return;
      }

      try {
        const downloadUrl = await authService.getFileUrl(user.avatar_url);
        setAvatarSrc(downloadUrl);
      } catch {
        setAvatarSrc(null);
      }
    };

    loadAvatar();
  }, [user?.avatar_url]);

  const handleLogout = async () => {
    try {
      await logout();
      message.success("Logged out successfully");
    } catch {
      message.error("Logout failed");
    }
  };

  const handleNewChat = async () => {
    try {
      onNewChat();
      message.success("Start a new chat by sending your first message");
    } catch {
      message.error("Failed to create new chat");
    }
  };

  const handleAvatarUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    try {
      setUploadingAvatar(true);
      await authService.uploadAvatar(file);
      await refreshUser();
      message.success("Avatar updated successfully");
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Failed to upload avatar";
      message.error(errorMessage);
    } finally {
      setUploadingAvatar(false);
      event.target.value = "";
    }
  };

  const handleDeleteConversation = async () => {
    if (!pendingDeleteConversation) {
      return;
    }

    try {
      setDeletingConversationId(pendingDeleteConversation.id);
      await onDeleteConversation(pendingDeleteConversation.id);
      message.success("Conversation deleted");
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Failed to delete conversation";
      message.error(errorMessage);
    } finally {
      setDeletingConversationId(null);
      setPendingDeleteConversation(null);
    }
  };

  if (loading) {
    return (
      <div className="flex h-full flex-col p-5">
        <div className="panel-card mb-4 rounded-[28px] p-5">
          <div className="mb-2 flex items-center justify-between">
            <span className="text-lg font-semibold">Chatbox</span>
          </div>
          <div className="h-4 w-36 animate-pulse rounded-full bg-[rgba(95,74,55,0.1)]" />
        </div>
        <div className="panel-card flex-1 rounded-[28px] p-5">Loading...</div>
      </div>
    );
  }

  return (
    <div className="flex h-full min-h-0 flex-col p-5">
      <div className="panel-card mb-4 shrink-0 rounded-[28px] p-5">
        <div className="mb-4 flex items-center justify-between">
          <div>
            <div className="text-xs uppercase tracking-[0.28em] text-[var(--ink-soft)]">
              Workspace
            </div>
            <div className="mt-1 text-2xl font-semibold">Chatbox</div>
          </div>
          <div className="rounded-full bg-[var(--accent-soft)] px-3 py-1 text-xs font-medium text-[var(--accent-deep)]">
            {conversations.length} threads
          </div>
        </div>
        <div className="flex items-start gap-3">
          <div className="flex h-14 w-14 shrink-0 items-center justify-center overflow-hidden rounded-full bg-[linear-gradient(135deg,#d76c45,#f0cfb0)] text-lg font-semibold text-white shadow-[0_12px_24px_rgba(187,90,52,0.28)]">
            {avatarSrc ? (
              // eslint-disable-next-line @next/next/no-img-element
              <img
                src={avatarSrc}
                alt={`${user?.username || "User"} avatar`}
                className="h-full w-full object-cover"
              />
            ) : (
              initials
            )}
          </div>

          <div className="min-w-0 flex-1">
            <div className="truncate text-lg font-semibold">
              {user?.username || "Chatbox"}
            </div>
            {isAuthenticated && (
              <div className="truncate text-sm text-[var(--ink-soft)]">
                {user?.email}
              </div>
            )}
            <div className="mt-3 flex flex-wrap gap-2">
              <input
                ref={fileInputRef}
                type="file"
                accept="image/png,image/jpeg,image/jpg,image/webp"
                className="hidden"
                onChange={handleAvatarUpload}
              />
              <Button
                size="small"
                loading={uploadingAvatar}
                onClick={() => fileInputRef.current?.click()}
                className="!rounded-full !border-[var(--border)] !bg-white/70 !px-4"
              >
                {avatarSrc ? "Change Avatar" : "Upload Avatar"}
              </Button>
              {isAuthenticated && (
                <Button
                  size="small"
                  onClick={handleLogout}
                  className="!rounded-full !border-[var(--border)] !bg-white/70 !px-4"
                >
                  Logout
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>

      <Button
        type="primary"
        block
        className="!mb-4 !h-12 !rounded-2xl !border-0 !bg-[var(--accent)] !font-medium !shadow-[0_16px_28px_rgba(187,90,52,0.28)] hover:!bg-[var(--accent-deep)]"
        onClick={handleNewChat}
      >
        + New Chat
      </Button>

      <div className="panel-card chat-scroll min-h-0 flex-1 overflow-y-auto rounded-[28px] p-3">
        <div className="mb-3 px-3 pt-2 text-xs uppercase tracking-[0.24em] text-[var(--ink-soft)]">
          Recent Conversations
        </div>
        {conversations.length === 0 ? (
          <div className="flex h-full flex-col items-center justify-center rounded-[22px] border border-dashed border-[var(--border)] bg-white/40 px-5 text-center">
            <div className="text-base font-medium">No conversations yet</div>
            <div className="mt-2 text-sm text-[var(--ink-soft)]">
              Start a new thread and it will appear here instantly.
            </div>
          </div>
        ) : (
          conversations.map((item) => (
            <div
              key={item.id}
              className={`mb-2 rounded-[22px] border p-3 transition ${
                currentChatId === item.id 
                  ? "border-transparent bg-[linear-gradient(135deg,var(--highlight),var(--highlight-strong))] text-[var(--highlight-text)] shadow-[0_18px_30px_rgba(255,191,60,0.32)]"
                  : "border-[var(--border)] bg-white/65 text-[var(--foreground)] hover:bg-white"
              }`}
            >
              <div className="flex items-center justify-between gap-2">
                <button
                  className="min-w-0 flex-1 text-left"
                  onClick={() => setCurrentChatId(item)}
                >
                  <div className="truncate text-sm font-medium">{item.title}</div>
                  <div className="mt-1 text-xs opacity-70">
                    {new Date(item.updated_at).toLocaleString()}
                  </div>
                </button>
                <button
                  className={`shrink-0 rounded px-2 py-1 text-xs ${
                    currentChatId === item.id
                      ? "bg-black/10 text-[var(--highlight-text)] hover:bg-black/15"
                      : "bg-[#f7e3db] text-[var(--accent-deep)] hover:bg-[#f1d2c5]"
                  }`}
                  onClick={(event) => {
                    event.stopPropagation();
                    setPendingDeleteConversation(item);
                  }}
                  disabled={deletingConversationId === item.id}
                >
                  {deletingConversationId === item.id ? "..." : "Delete"}
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      <Modal
        open={!!pendingDeleteConversation}
        title="Delete conversation?"
        onCancel={() => setPendingDeleteConversation(null)}
        onOk={handleDeleteConversation}
        centered
        okText="Delete"
        cancelText="Keep it"
        okButtonProps={{
          danger: true,
          loading: deletingConversationId === pendingDeleteConversation?.id,
        }}
      >
        <p className="text-sm text-[var(--ink-soft)]">
          This will permanently remove{" "}
          <span className="font-medium text-[var(--foreground)]">
            {pendingDeleteConversation?.title || "this conversation"}
          </span>
          . This action cannot be undone.
        </p>
      </Modal>
    </div>
  );
}
