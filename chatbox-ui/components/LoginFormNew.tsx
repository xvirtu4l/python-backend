import { useAuth } from '@/context/AuthContext';
import { Button, Form, Input, message } from 'antd';

type LoginFormValues = {
    username: string;
    password: string;
};

type LoginFormProps = {
    onLogin: (token: string) => void;
}

export default function LoginForm({ onLogin }: LoginFormProps) {
    const [form] = Form.useForm();
    const { login, loading } = useAuth();

    const onFinish = async (values: LoginFormValues) => {
        try {
            await login(values.username, values.password);
            message.success('Login successful!');
            onLogin("");
        } catch {
            message.error('Invalid credentials');
        }
    };

    return (
        <Form
            form={form}
            name="login"
            onFinish={onFinish}
            layout="vertical"
        >
            <Form.Item
                name="username"
                rules={[{ required: true, message: 'Please input your username!' }]}
            >
                <Input placeholder="Username" />
            </Form.Item>

            <Form.Item
                name="password"
                rules={[{ required: true, message: 'Please input your password!' }]}
            >
                <Input.Password placeholder="Password" />
            </Form.Item>

            <Form.Item>
                <Button type="primary" htmlType="submit" block loading={loading}>
                    Login
                </Button>
            </Form.Item>
        </Form>
    );
}
