"use client";

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Button, Form, Input, message } from "antd";
import { Suspense, useState } from "react";

import { authService } from "@/services/authService";

type ResetPasswordValues = {
  token: string;
  newPassword: string;
  confirmPassword: string;
};

function ResetPasswordContent() {
  const [form] = Form.useForm<ResetPasswordValues>();
  const [submitting, setSubmitting] = useState(false);
  const [completed, setCompleted] = useState(false);
  const searchParams = useSearchParams();
  const router = useRouter();
  const resetToken = searchParams.get("token") ?? "";

  const handleFinish = async (values: ResetPasswordValues) => {
    try {
      setSubmitting(true);
      await authService.resetPassword(values.token.trim(), values.newPassword);
      setCompleted(true);
      message.success("Password reset successful");
      form.resetFields(["newPassword", "confirmPassword"]);
      window.setTimeout(() => {
        router.push("/login");
      }, 1200);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Failed to reset password";
      message.error("Error: " + errorMessage);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="relative min-h-screen overflow-hidden px-6 py-10">
      <div className="pointer-events-none absolute inset-0">
        <div className="absolute -left-24 top-0 h-72 w-72 rounded-full bg-[#f1bb90]/30 blur-3xl" />
        <div className="absolute bottom-0 right-0 h-80 w-80 rounded-full bg-[#c98f67]/20 blur-3xl" />
      </div>

      <div className="relative mx-auto flex min-h-[calc(100vh-5rem)] max-w-4xl items-center justify-center">
        <div className="grid w-full overflow-hidden rounded-4xl border border-(--border) bg-[rgba(255,250,242,0.84)] shadow-[0_30px_100px_rgba(72,48,30,0.16)] backdrop-blur md:grid-cols-[0.95fr_1.05fr]">
          <section className="hidden bg-[linear-gradient(160deg,#2f221d_0%,#7f3a22_42%,#c56a44_100%)] p-10 text-[#fff8ef] md:flex md:flex-col md:justify-between">
            <div>
              <div className="mb-6 inline-flex rounded-full border border-white/20 px-4 py-1 text-xs uppercase tracking-[0.28em] text-white/75">
                Account Recovery
              </div>
              <h1 className="max-w-sm text-4xl font-semibold leading-[1.05]">
                Choose a new password and get back into Chatbox.
              </h1>
              <p className="mt-5 max-w-md text-sm leading-7 text-white/78">
                Paste the reset token from your email or open this page directly from the link we sent you.
              </p>
            </div>

            <div className="rounded-2xl border border-white/15 bg-white/8 p-4 text-sm text-white/80">
              For safety, reset links expire after 15 minutes.
            </div>
          </section>

          <section className="flex items-center justify-center px-6 py-10 sm:px-10">
            <div className="w-full max-w-md">
              <div className="mb-6">
                <div className="text-sm uppercase tracking-[0.28em] text-(--ink-soft)">
                  Reset Password
                </div>
                <h2 className="mt-3 text-4xl font-semibold text-foreground">
                  Set a new password
                </h2>
                <p className="mt-3 text-sm leading-6 text-(--ink-soft)">
                  Use the token from your email to finish the reset flow.
                </p>
              </div>

              <div className="panel-card rounded-[28px] p-4 sm:p-5">
                {completed ? (
                  <div className="rounded-3xl border border-(--border) bg-[rgba(255,248,240,0.82)] p-5">
                    <div className="text-xs uppercase tracking-[0.22em] text-(--ink-soft)">
                      Password updated
                    </div>
                    <p className="mt-3 text-sm leading-6 text-foreground">
                      Your password has been reset successfully. Redirecting you to login now.
                    </p>
                  </div>
                ) : (
                  <Form
                    form={form}
                    layout="vertical"
                    initialValues={{ token: resetToken }}
                    onFinish={handleFinish}
                    className="space-y-1"
                  >
                    <Form.Item
                      label={<span className="text-xs uppercase tracking-[0.22em] text-(--ink-soft)">Reset Token</span>}
                      name="token"
                      rules={[{ required: true, message: "Please enter your reset token" }]}
                    >
                      <Input
                        size="large"
                        placeholder="Paste the token from your email"
                        className="rounded-2xl! border-(--border)! bg-white/70! px-4! py-3!"
                      />
                    </Form.Item>

                    <Form.Item
                      label={<span className="text-xs uppercase tracking-[0.22em] text-(--ink-soft)">New Password</span>}
                      name="newPassword"
                      rules={[{ required: true, message: "Please enter a new password" }]}
                    >
                      <Input.Password
                        size="large"
                        placeholder="Create a strong password"
                        className="rounded-2xl! border-(--border)! bg-white/70! px-4! py-3!"
                      />
                    </Form.Item>

                    <Form.Item
                      label={<span className="text-xs uppercase tracking-[0.22em] text-(--ink-soft)">Confirm Password</span>}
                      name="confirmPassword"
                      dependencies={["newPassword"]}
                      rules={[
                        { required: true, message: "Please confirm your new password" },
                        ({ getFieldValue }) => ({
                          validator(_, value) {
                            if (!value || getFieldValue("newPassword") === value) {
                              return Promise.resolve();
                            }
                            return Promise.reject(new Error("Passwords do not match"));
                          },
                        }),
                      ]}
                    >
                      <Input.Password
                        size="large"
                        placeholder="Re-enter your new password"
                        className="rounded-2xl! border-(--border)! bg-white/70! px-4! py-3!"
                      />
                    </Form.Item>

                    <Button
                      type="primary"
                      htmlType="submit"
                      block
                      loading={submitting}
                      className="mt-4! h-12! rounded-2xl! border-0! bg-(--accent)! font-medium! shadow-[0_14px_30px_rgba(187,90,52,0.28)]! hover:bg-(--accent-deep)!"
                    >
                      Reset Password
                    </Button>
                  </Form>
                )}

                <div className="mt-5 text-center text-sm text-(--ink-soft)">
                  <Link href="/login" className="font-medium text-(--accent-deep) hover:opacity-80">
                    Back to login
                  </Link>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}

export default function ResetPasswordPage() {
  return (
    <Suspense
      fallback={
        <div className="flex min-h-screen items-center justify-center px-6">
          <div className="panel-card rounded-full px-6 py-4 text-sm text-(--ink-soft)">
            Loading reset page...
          </div>
        </div>
      }
    >
      <ResetPasswordContent />
    </Suspense>
  );
}
