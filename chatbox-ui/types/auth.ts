export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface AuthResponse {
  email: string;
  username: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  avatar_url?: string;
}

export interface UserResponse {
  email: string;
  username: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  avatar_url?: string;
}

export interface AvatarUploadResponse {
  message: string;
  object_name: string;
}

export interface FileDownloadResponse {
  file_id: string;
  download_url: string;
}
