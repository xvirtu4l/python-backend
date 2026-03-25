"use client";

import { useAuth } from "@/context/AuthContext";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import AuthForm from "@/components/AuthForm";

export default function Login() {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && isAuthenticated) {
      router.push("/");
    }
  }, [isAuthenticated, loading, router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="relative min-h-screen overflow-hidden px-6 py-10">
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute -left-32 -top-20 h-72 w-72 rounded-full bg-[#f2b38f]/40 blur-3xl" />
        <div className="absolute -bottom-24 -right-16 h-80 w-80 rounded-full bg-[#d8c1a8]/55 blur-3xl" />
      </div>

      <div className="relative mx-auto flex min-h-[calc(100vh-5rem)] max-w-6xl items-center justify-center">
        <div className="grid w-full overflow-hidden rounded-4xl border border-(--border) bg-[rgba(255,250,242,0.82)] shadow-[0_30px_100px_rgba(72,48,30,0.16)] backdrop-blur md:grid-cols-[1.1fr_0.9fr]">
          <section className="hidden flex-col justify-between bg-[linear-gradient(160deg,#2f221d_0%,#7f3a22_45%,#c56a44_100%)] p-10 text-[#fff8ef] md:flex">
            <div>
              <div className="mb-6 inline-flex rounded-full border border-white/20 px-4 py-1 text-xs uppercase tracking-[0.28em] text-white/75">
                Project Chatbot
              </div>
              <h1 className="max-w-md text-5xl font-semibold leading-[1.02]">
                Conversations that feel organized, fast, and calm.
              </h1>
              <p className="mt-5 max-w-lg text-base leading-7 text-white/78">
                Sign in to continue your workspace, pick up old threads, and manage your assistant history in one place.
              </p>
            </div>

            <div className="grid gap-4 text-sm text-white/82">
              <div className="rounded-2xl border border-white/15 bg-white/8 p-4">
                Thread-aware layout with quick switching between previous conversations.
              </div>
              <div className="rounded-2xl border border-white/15 bg-white/8 p-4">
                Profile tools, avatar upload, and a cleaner dashboard flow.
              </div>
            </div>
          </section>

          <section className="flex items-center justify-center px-6 py-10 sm:px-10">
            <div className="w-full max-w-md">
              <div className="mb-6">
                <div className="text-sm uppercase tracking-[0.28em] text-(--ink-soft)">
                  Welcome Back
                </div>
                <h2 className="mt-3 text-4xl font-semibold text-foreground">
                  Chatbox Access
                </h2>
                <p className="mt-3 text-sm leading-6 text-(--ink-soft)">
                  Use your username or email to sign in. New here? Create an account and start a fresh conversation.
                </p>
              </div>
              <AuthForm onLogin={() => {}} />
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
