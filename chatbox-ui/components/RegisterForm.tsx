"use client";

import { useState } from "react";

type RegisterFormProps = {
    onRegister: (token: string) => void;
};

export default function RegisterForm({ onRegister }: RegisterFormProps) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (e: React.SyntheticEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError("");

        try {

            const res = await fetch("http://localhost:8000/users/create", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded"},
                body: JSON.stringify ({
                    username,
                    password,
                    email,
                }),
            });

            if (!res.ok) {
                const err = await  res.json();
                throw new Error(err.detail || "Đăng ký không thành công");
            }

            const loginRes = await fetch("http://localhost:8000/api/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded"},
                body: new URLSearchParams({
                    username,
                    password,
                }),
            });

            const data = await loginRes.json();
            onRegister(data.access_token);

        } catch (err: unknown) {
            setError(err instanceof Error ? err.message : "Đăng ký không thành công");
        }
    };


    return (
        <form onSubmit={handleSubmit} className="flex flex-col gap-3 p-4 border rounded">

            <h2 className="text-lg font-bold">Đăng ký</h2>

            <input
                value={username}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    setUsername(e.target.value)
                }
                placeholder="Tên đăng nhập"
                className="border p-2"
            />

            <input
                value={email}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    setEmail(e.target.value)
                }
                placeholder="Email"
                className="border p-2"
            />

            <input
                type="password"
                value={password}
                onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    setPassword(e.target.value)
                }
                placeholder="Mật khẩu"
                className="border p-2"
            />

            <button className="bg-green-500 text-white p-2">Đăng ký</button>

            {error && <p className="text-red-500">{error}</p>}
        </form>
    );
}
