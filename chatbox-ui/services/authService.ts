import axios from "axios";
import apiClient from "./api";
import type {
  AuthResponse,
  AvatarUploadResponse,
  FileDownloadResponse,
  LoginResponse,
  UserResponse,
} from "@/types/auth";

function getErrorMessage(error: unknown, fallback: string) {
  if (axios.isAxiosError(error)) {
    return error.response?.data?.detail || fallback;
  }

  return fallback;
}

class AuthService {
  async login(username: string, password: string): Promise<LoginResponse> {
    try {
      const payload = new URLSearchParams();
      payload.append("username", username);
      payload.append("password", password);

      const response = await apiClient.post<LoginResponse>(
        "/api/auth/login",
        payload,
        {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
        }
      );
      
      return response.data;
    } catch (error: unknown) {
      throw new Error(getErrorMessage(error, "Login failed"));
    }
  }

  async register(
    email: string,
    username: string,
    password: string
  ): Promise<UserResponse> {
    try {
      const response = await apiClient.post<UserResponse>("/users/create", {
        email,
        username,
        password,
      });
      return response.data;
    } catch (error: unknown) {
      throw new Error(getErrorMessage(error, "Registration failed"));
    }
  }

  async logout() {
    try {
      await apiClient.post("/api/auth/logout");
      return true;
    } catch (error: unknown) {
      throw new Error(getErrorMessage(error, "Logout failed"));
    }
  }

  async getCurrentUser(): Promise<AuthResponse> {
    try {
      const response = await apiClient.get<AuthResponse>("/api/auth/me");
      return response.data;
    } catch (error: unknown) {
      throw new Error(getErrorMessage(error, "Failed to get user info"));
    }
  }

  async changePassword(currentPassword: string, newPassword: string) {
    try {
      const response = await apiClient.post("/api/auth/change-password", null, {
        params: {
          current_password: currentPassword,
          new_password: newPassword,
        },
      });
      return response.data;
    } catch (error: unknown) {
      throw new Error(getErrorMessage(error, "Failed to change password"));
    }
  }

  async forgotPassword(email: string) {
    try {
      const response = await apiClient.post("/api/auth/forgot-password", null, {
        params: { email },
      });
      return response.data;
    } catch (error: unknown) {
      throw new Error(getErrorMessage(error, "Failed to request password reset"));
    }
  }

  async resetPassword(token: string, newPassword: string) {
    try {
      const response = await apiClient.post("/api/auth/reset-password", null, {
        params: {
          token,
          new_password: newPassword,
        },
      });
      return response.data;
    } catch (error: unknown) {
      throw new Error(getErrorMessage(error, "Failed to reset password"));
    }
  }

  async uploadAvatar(file: File): Promise<AvatarUploadResponse> {
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await apiClient.put<AvatarUploadResponse>(
        "/users/avatar",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
      return response.data;
    } catch (error: unknown) {
      throw new Error(getErrorMessage(error, "Failed to upload avatar"));
    }
  }

  async getFileUrl(fileName: string): Promise<string> {
    try {
      const response = await apiClient.get<FileDownloadResponse>(
        `/files/${encodeURIComponent(fileName)}`
      );
      return response.data.download_url;
    } catch (error: unknown) {
      throw new Error(getErrorMessage(error, "Failed to load avatar"));
    }
  }
}

export const authService = new AuthService();
