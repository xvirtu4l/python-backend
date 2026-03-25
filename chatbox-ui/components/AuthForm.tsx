import { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { authService } from "@/services/authService";
import { Button, Form, Input, Modal, message } from "antd";
import Link from "next/link";
import { useRouter } from "next/navigation";

type AuthFormValues = {
  email?: string;
  username: string;
  password: string;
};

type AuthFormProps = {
  onLogin: (token: string) => void;
};

export default function AuthForm({ onLogin }: AuthFormProps) {
  const [isLogin, setIsLogin] = useState(true);
  const [form] = Form.useForm();
  const [forgotForm] = Form.useForm();
  const { login, register, loading } = useAuth();
  const router = useRouter();
  const [forgotPasswordOpen, setForgotPasswordOpen] = useState(false);
  const [forgotPasswordLoading, setForgotPasswordLoading] = useState(false);
  const [forgotPasswordRequested, setForgotPasswordRequested] = useState(false);

  const onFinish = async (values: AuthFormValues) => {
    try {
      const username = values.username.trim();
      const password = values.password;

      if (isLogin) {
        await login(username, password);
        message.success("Login successful!");
        router.push("/");
      } else {
        await register(values.email?.trim() || "", username, password);
        message.success("Registration successful! Redirecting...");
        router.push("/");
      }
      onLogin("");
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "An error occurred";
      message.error("Error: " + errorMessage);
    }
  };

  const handleForgotPassword = async (values: { email: string }) => {
    try {
      setForgotPasswordLoading(true);
      const response = await authService.forgotPassword(values.email.trim());
      setForgotPasswordRequested(true);
      message.success(response.message || "Password reset requested");
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "An error occurred";
      message.error("Error: " + errorMessage);
    } finally {
      setForgotPasswordLoading(false);
    }
  };

  return (
    <div className="panel-card rounded-[28px] p-3 sm:p-4">
      <div className="mb-5 grid grid-cols-2 gap-2 rounded-[20px] bg-[rgba(95,74,55,0.08)] p-1.5">
        <button
          type="button"
          onClick={() => setIsLogin(true)}
          className={`rounded-2xl px-4 py-3 text-sm font-medium transition ${
            isLogin
              ? "bg-(--highlight) text-(--highlight-text) shadow-[0_14px_30px_rgba(255,191,60,0.24)]"
              : "text-(--ink-soft) hover:bg-white/60"
          }`}
        >
          Login
        </button>

        <button
          type="button"
          onClick={() => setIsLogin(false)}
          className={`rounded-2xl px-4 py-3 text-sm font-medium transition ${
            !isLogin
              ? "bg-(--highlight) text-(--highlight-text) shadow-[0_14px_30px_rgba(255,191,60,0.24)]"
              : "text-(--ink-soft) hover:bg-white/60"
          }`}
        >
          Register
        </button>
      </div>

      <Form
        form={form}
        name={isLogin ? "login" : "register"}
        onFinish={onFinish}
        layout="vertical"
        className="space-y-1"
      >
        {isLogin ? (
          <>
            <Form.Item
              label={<span className="text-xs uppercase tracking-[0.22em] text-(--ink-soft)">Username or Email</span>}
              name="username"
              rules={[
                { required: true, message: "Please input your username or email!" },
              ]}
            >
              <Input
                size="large"
                placeholder="Your username or youremail@example.com"
                className="rounded-2xl! border-(--border)! bg-white/70! px-4! py-3!"
              />
            </Form.Item>

            <Form.Item
              label={<span className="text-xs uppercase tracking-[0.22em] text-(--ink-soft)">Password</span>}
              name="password"
              rules={[
                { required: true, message: "Please input your password!" },
              ]}
            >
              <Input.Password
                size="large"
                placeholder="Enter your password"
                className="rounded-2xl! border-(--border)! bg-white/70! px-4! py-3!"
              />
            </Form.Item>
          </>
        ) : (
          <>
            <Form.Item
              label={<span className="text-xs uppercase tracking-[0.22em] text-(--ink-soft)">Email</span>}
              name="email"
              rules={[{ required: true, message: "Please input your email!" }]}
            >
              <Input
                size="large"
                placeholder="you@example.com"
                className="rounded-2xl! border-(--border)! bg-white/70! px-4! py-3!"
              />
            </Form.Item>

            <Form.Item
              label={<span className="text-xs uppercase tracking-[0.22em] text-(--ink-soft)">Username</span>}
              name="username"
              rules={[
                { required: true, message: "Please input your username!" },
              ]}
            >
              <Input
                size="large"
                placeholder="Choose a username"
                className="rounded-2xl! border-(--border)! bg-white/70! px-4! py-3!"
              />
            </Form.Item>

            <Form.Item
              label={<span className="text-xs uppercase tracking-[0.22em] text-(--ink-soft)">Password</span>}
              name="password"
              rules={[
                { required: true, message: "Please input your password!" },
              ]}
            >
              <Input.Password
                size="large"
                placeholder="Create a strong password"
                className="rounded-2xl! border-(--border)! bg-white/70! px-4! py-3!"
              />
            </Form.Item>
          </>
        )}

        <Form.Item>
          <Button
            type="primary"
            htmlType="submit"
            block
            loading={loading}
            className="mt-4! h-12! rounded-2xl! border-0! bg-(--accent)! font-medium! shadow-[0_14px_30px_rgba(187,90,52,0.28)]! hover:bg-(--accent-deep)!"
          >
            {isLogin ? "Login" : "Register"}
          </Button>
        </Form.Item>

        {isLogin && (
          <div className="px-1 pb-2 text-right">
            <button
              type="button"
              onClick={() => setForgotPasswordOpen(true)}
              className="text-sm font-medium text-(--accent-deep) transition hover:opacity-80"
            >
              Forgot password?
            </button>
          </div>
        )}
      </Form>

      <Modal
        open={forgotPasswordOpen}
        title="Forgot password"
        onCancel={() => {
          setForgotPasswordOpen(false);
          forgotForm.resetFields();
          setForgotPasswordRequested(false);
        }}
        footer={null}
        centered
      >
        <Form
          form={forgotForm}
          layout="vertical"
          onFinish={handleForgotPassword}
          className="pt-2"
        >
          <Form.Item
            label="Email"
            name="email"
            rules={[{ required: true, message: "Please input your email!" }]}
          >
            <Input
              size="large"
              placeholder="you@example.com"
              className="rounded-2xl! border-(--border)! bg-white/70! px-4! py-3!"
            />
          </Form.Item>

          {forgotPasswordRequested && (
            <div className="mb-4 rounded-2xl border border-(--border) bg-[rgba(255,248,240,0.8)] p-4">
              <div className="text-xs uppercase tracking-[0.22em] text-(--ink-soft)">
                Check your inbox
              </div>
              <div className="mt-2 text-sm leading-6 text-foreground">
                We sent a password reset link to your email. Open the link in that email to choose a new password.
              </div>
            </div>
          )}

          <Button
            type="primary"
            htmlType="submit"
            block
            loading={forgotPasswordLoading}
            className="h-12! rounded-2xl! border-0! bg-(--accent)! font-medium!"
          >
            Request Reset
          </Button>

          <div className="mt-4 text-center text-sm text-(--ink-soft)">
            Already have a reset token?{" "}
            <Link href="/reset-password" className="font-medium text-(--accent-deep) hover:opacity-80">
              Open reset page
            </Link>
          </div>
        </Form>
      </Modal>
    </div>
  );
}
