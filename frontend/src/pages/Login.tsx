import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sun, Moon, Activity } from 'lucide-react';

interface LoginProps {
    theme: string;
    toggleTheme: () => void;
}

const Login: React.FC<LoginProps> = ({ theme, toggleTheme }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            // Mock login for now, but configured for real API later
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            const res = await fetch('http://localhost:8000/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: formData.toString()
            });

            if (res.ok) {
                const data = await res.json();
                localStorage.setItem('token', data.access_token);
                navigate('/');
            } else {
                setError('Invalid credentials. (Hint: Register first or mock for now)');
                // FOR MOCKING in dev without backend:
                // localStorage.setItem('token', 'mock_token');
                // navigate('/');
            }
        } catch (err) {
            console.error(err);
            setError('Connection error. Is the backend running?');
        }
    };

    return (
        <div style={{ display: 'flex', minHeight: '100vh', width: '100%', alignItems: 'center', justifyContent: 'center' }}>
            <button
                onClick={toggleTheme}
                style={{ position: 'absolute', top: '2rem', right: '2rem', background: 'transparent', border: 'none', cursor: 'pointer', color: 'var(--text-color)' }}
            >
                {theme === 'light' ? <Moon size={24} /> : <Sun size={24} />}
            </button>

            <div className="glass-panel animate-fade-in" style={{ width: '100%', maxWidth: '400px' }}>
                <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                    <Activity size={48} color="var(--primary-color)" style={{ marginBottom: '1rem' }} />
                    <h2>AI Activity Assist</h2>
                    <p style={{ opacity: 0.7 }}>Login to view insights</p>
                </div>

                {error && <div style={{ color: 'var(--danger-color)', marginBottom: '1rem', textAlign: 'center' }}>{error}</div>}

                <form onSubmit={handleLogin}>
                    <div className="input-group">
                        <label>Username</label>
                        <input
                            type="text"
                            className="input-field"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    <div className="input-group">
                        <label>Password</label>
                        <input
                            type="password"
                            className="input-field"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" className="btn" style={{ width: '100%' }}>
                        Sign In
                    </button>
                </form>
            </div>
        </div>
    );
};

export default Login;
