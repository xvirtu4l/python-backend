"use client";

import {
  createContext,
  useContext,
  useEffect,
  useState,
  ReactNode,
} from "react";
import TokenManager from "@/utils/tokenManager";
import { authService } from "@/services/authService";
import type { AuthResponse } from "@/types/auth";

type AuthContextType = {
  user: AuthResponse | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (email: string, username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<AuthResponse | null>(null);
  const [loading, setLoading] = useState(true);

  const refreshUser = async () => {
    if (!TokenManager.getToken()) {
      setUser(null);
      return;
    }

    try {
      const currentUser = await authService.getCurrentUser();
      setUser(currentUser);
    } catch {
      TokenManager.removeToken();
      setUser(null);
    }
  };

  useEffect(() => {
    const initializeAuth = async () => {
      try {
        await refreshUser();
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const login = async (username: string, password: string) => {
    const response = await authService.login(username, password);
    TokenManager.setToken(response.access_token);
    await refreshUser();
  };

  const register = async (email: string, username: string, password: string) => {
    await authService.register(email, username, password);
    const response = await authService.login(username, password);
    TokenManager.setToken(response.access_token);
    await refreshUser();
  };

  const logout = async () => {
    try {
      await authService.logout();
    } finally {
      TokenManager.removeToken();
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isAuthenticated: !!user,
        login,
        register,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  return context;
}
