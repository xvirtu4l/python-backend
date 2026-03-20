import { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { Button, Form, Input, message } from "antd";
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
  const { login, register, loading } = useAuth();
  const router = useRouter();

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

  return (
    <div className="panel-card rounded-[28px] p-3 sm:p-4">
      <div className="mb-5 grid grid-cols-2 gap-2 rounded-[20px] bg-[rgba(95,74,55,0.08)] p-1.5">
        <button
          type="button"
          onClick={() => setIsLogin(true)}
          className={`rounded-2xl px-4 py-3 text-sm font-medium transition ${
            isLogin
              ? "bg-[var(--highlight)] text-[var(--highlight-text)] shadow-[0_14px_30px_rgba(255,191,60,0.24)]"
              : "text-[var(--ink-soft)] hover:bg-white/60"
          }`}
        >
          Login
        </button>

        <button
          type="button"
          onClick={() => setIsLogin(false)}
          className={`rounded-2xl px-4 py-3 text-sm font-medium transition ${
            !isLogin
              ? "bg-[var(--highlight)] text-[var(--highlight-text)] shadow-[0_14px_30px_rgba(255,191,60,0.24)]"
              : "text-[var(--ink-soft)] hover:bg-white/60"
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
              label={<span className="text-xs uppercase tracking-[0.22em] text-[var(--ink-soft)]">Username or Email</span>}
              name="username"
              rules={[
                { required: true, message: "Please input your username or email!" },
              ]}
            >
              <Input
                size="large"
                placeholder="yourname or you@example.com"
                className="!rounded-2xl !border-[var(--border)] !bg-white/70 !px-4 !py-3"
              />
            </Form.Item>

            <Form.Item
              label={<span className="text-xs uppercase tracking-[0.22em] text-[var(--ink-soft)]">Password</span>}
              name="password"
              rules={[
                { required: true, message: "Please input your password!" },
              ]}
            >
              <Input.Password
                size="large"
                placeholder="Enter your password"
                className="!rounded-2xl !border-[var(--border)] !bg-white/70 !px-4 !py-3"
              />
            </Form.Item>
          </>
        ) : (
          <>
            <Form.Item
              label={<span className="text-xs uppercase tracking-[0.22em] text-[var(--ink-soft)]">Email</span>}
              name="email"
              rules={[{ required: true, message: "Please input your email!" }]}
            >
              <Input
                size="large"
                placeholder="you@example.com"
                className="!rounded-2xl !border-[var(--border)] !bg-white/70 !px-4 !py-3"
              />
            </Form.Item>

            <Form.Item
              label={<span className="text-xs uppercase tracking-[0.22em] text-[var(--ink-soft)]">Username</span>}
              name="username"
              rules={[
                { required: true, message: "Please input your username!" },
              ]}
            >
              <Input
                size="large"
                placeholder="Choose a username"
                className="!rounded-2xl !border-[var(--border)] !bg-white/70 !px-4 !py-3"
              />
            </Form.Item>

            <Form.Item
              label={<span className="text-xs uppercase tracking-[0.22em] text-[var(--ink-soft)]">Password</span>}
              name="password"
              rules={[
                { required: true, message: "Please input your password!" },
              ]}
            >
              <Input.Password
                size="large"
                placeholder="Create a strong password"
                className="!rounded-2xl !border-[var(--border)] !bg-white/70 !px-4 !py-3"
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
            className="!mt-4 !h-12 !rounded-2xl !border-0 !bg-[var(--accent)] !font-medium !shadow-[0_14px_30px_rgba(187,90,52,0.28)] hover:!bg-[var(--accent-deep)]"
          >
            {isLogin ? "Login" : "Register"}
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}
