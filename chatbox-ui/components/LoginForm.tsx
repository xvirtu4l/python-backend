"use client";

import { useState } from "react";

type LoginFormProps = {
    onLogin: (token: string) => void;
}

export default function LoginForm({ onLogin }: LoginFormProps) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (e: React.SyntheticEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError("");

        try {
            const res = await fetch("http://localhost:8000/api/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded"},
                body: new URLSearchParams({
                    username,
                    password,
                }),
            });

            if (!res.ok) throw new Error("Sai tài khoản hoặc mật khẩu");

            const data = await res.json();
            onLogin(data.access_token);
        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : "Đăng nhập thất bại");
        }
    };


    return (
        <form onSubmit={handleSubmit} className="flex flex-col gap-3 p-4 border rounded">
            <h2 className="text-lg font-bold">Đăng nhập</h2>

            <input
            value={username}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => 
                setUsername(e.target.value)
            }
            placeholder="Tên đăng nhập"
            className="border p-2"
            />

            <input type="password"
            value={password}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                setPassword(e.target.value)
            }
            placeholder="Mật khẩu"
            className="border p-2"
            />

            <button className="bg-blue-500 text-white p-2">Login</button>

            {error && <p className="text-red-500">{error}</p>}
        </form>
    );
}
