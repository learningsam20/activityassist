import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    BarChart, Activity, LogOut, Sun, Moon,
    Users, AlertTriangle, CheckCircle
} from 'lucide-react';

interface DashboardProps {
    theme: string;
    toggleTheme: () => void;
}

const Dashboard: React.FC<DashboardProps> = ({ theme, toggleTheme }) => {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState('overview');

    useEffect(() => {
        // Check if token exists
        // const token = localStorage.getItem('token');
        // If we want hard auth: if (!token) navigate('/login');
    }, [navigate]);

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    return (
        <div className="app-container">
            {/* Sidebar Navigation */}
            <aside className="sidebar">
                <div style={{ display: 'flex', alignItems: 'center', marginBottom: '3rem', color: 'var(--primary-color)' }}>
                    <Activity size={32} style={{ marginRight: '1rem' }} />
                    <h2>Activity Assist</h2>
                </div>

                <nav style={{ display: 'flex', flexDirection: 'column', gap: '1rem', flex: 1 }}>
                    <button
                        className={`btn ${activeTab === 'overview' ? '' : 'btn-secondary'}`}
                        style={{ justifyContent: 'flex-start', border: 'none' }}
                        onClick={() => setActiveTab('overview')}
                    >
                        <BarChart size={20} style={{ marginRight: '1rem' }} />
                        Overview
                    </button>

                    <button
                        className={`btn ${activeTab === 'sops' ? '' : 'btn-secondary'}`}
                        style={{ justifyContent: 'flex-start', border: 'none' }}
                        onClick={() => setActiveTab('sops')}
                    >
                        <CheckCircle size={20} style={{ marginRight: '1rem' }} />
                        Approve SOPs
                    </button>

                    <button
                        className={`btn ${activeTab === 'anomalies' ? '' : 'btn-secondary'}`}
                        style={{ justifyContent: 'flex-start', border: 'none' }}
                        onClick={() => setActiveTab('anomalies')}
                    >
                        <AlertTriangle size={20} style={{ marginRight: '1rem' }} />
                        Anomalies
                    </button>
                </nav>

                <div style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <button className="btn btn-secondary" style={{ justifyContent: 'flex-start', border: 'none' }} onClick={toggleTheme}>
                        {theme === 'light' ? <Moon size={20} style={{ marginRight: '1rem' }} /> : <Sun size={20} style={{ marginRight: '1rem' }} />}
                        {theme === 'light' ? 'Dark Mode' : 'Light Mode'}
                    </button>
                    <button onClick={handleLogout} className="btn" style={{ background: 'var(--danger-color)', justifyContent: 'flex-start' }}>
                        <LogOut size={20} style={{ marginRight: '1rem' }} />
                        Logout
                    </button>
                </div>
            </aside>

            {/* Main Content Area */}
            <main className="main-content">
                <header className="navbar">
                    <div>
                        <h1 style={{ textTransform: 'capitalize' }}>{activeTab}</h1>
                        <p style={{ opacity: 0.7 }}>AI-powered insights for user behavior</p>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
                        <div style={{ width: 40, height: 40, borderRadius: '50%', background: 'var(--primary-color)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white' }}>
                            <Users size={20} />
                        </div>
                        <span style={{ fontWeight: 500 }}>Admin User</span>
                    </div>
                </header>

                {activeTab === 'overview' && (
                    <div className="animate-fade-in">
                        <div className="grid-cards" style={{ marginBottom: '2rem' }}>
                            <div className="glass-panel card">
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <h3 style={{ margin: 0 }}>Total Activities</h3>
                                    <Activity color="var(--primary-color)" />
                                </div>
                                <h1 style={{ fontSize: '2.5rem', margin: '1rem 0 0' }}>1,248</h1>
                                <p style={{ color: 'var(--secondary-color)', fontSize: '0.875rem' }}>+12% from last week</p>
                            </div>
                            <div className="glass-panel card">
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <h3 style={{ margin: 0 }}>Identified SOPs</h3>
                                    <CheckCircle color="var(--secondary-color)" />
                                </div>
                                <h1 style={{ fontSize: '2.5rem', margin: '1rem 0 0' }}>12</h1>
                                <p style={{ color: 'var(--text-color)', opacity: 0.7, fontSize: '0.875rem' }}>4 waiting for approval</p>
                            </div>
                            <div className="glass-panel card">
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                    <h3 style={{ margin: 0 }}>Anomalies</h3>
                                    <AlertTriangle color="var(--danger-color)" />
                                </div>
                                <h1 style={{ fontSize: '2.5rem', margin: '1rem 0 0' }}>3</h1>
                                <p style={{ color: 'var(--danger-color)', fontSize: '0.875rem' }}>Requires immediate attention</p>
                            </div>
                        </div>

                        <div className="glass-panel">
                            <h2>Activity Pareto Chart</h2>
                            <p style={{ opacity: 0.7, marginBottom: '1rem' }}>Most frequent sequences driving business operations.</p>
                            {/* Placeholder for the Pareto chart */}
                            <div className="chart-container">
                                <div style={{ textAlign: 'center' }}>
                                    <BarChart size={48} color="var(--primary-color)" style={{ marginBottom: '1rem', opacity: 0.8 }} />
                                    <p style={{ fontWeight: 500 }}>Pareto Visualization Rendering</p>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'sops' && (
                    <div className="animate-fade-in">
                        <div className="glass-panel">
                            <h2>Pending AI Approvals</h2>
                            <div style={{ marginTop: '2rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                                <div className="glass-panel" style={{ padding: '1rem 1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: 'rgba(255,255,255,0.02)' }}>
                                    <div>
                                        <h4 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                                            Customer Address Update
                                            <span style={{ fontSize: '0.75rem', padding: '0.2rem 0.5rem', background: 'var(--primary-color)', borderRadius: '12px', color: 'white' }}>AI Proposed</span>
                                        </h4>
                                        <p style={{ fontSize: '0.875rem', opacity: 0.7, margin: '0.25rem 0 0' }}>Sequence of 14 steps observed 45 times.</p>
                                    </div>
                                    <div>
                                        <button className="btn btn-secondary" style={{ marginRight: '1rem' }}>Review Details</button>
                                        <button className="btn" style={{ background: 'var(--secondary-color)' }}>Approve SOP</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'anomalies' && (
                    <div className="animate-fade-in">
                        <div className="glass-panel">
                            <h2>Detected Deviations</h2>
                            <div style={{ marginTop: '2rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                                <div className="glass-panel" style={{ padding: '1rem 1.5rem', borderLeft: '4px solid var(--danger-color)', background: 'rgba(255,255,255,0.02)' }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                                        <div>
                                            <h4 style={{ margin: 0, color: 'var(--danger-color)' }}>Unnecessary Manual Data Entry</h4>
                                            <p style={{ fontSize: '0.875rem', margin: '0.5rem 0 0' }}>User ID 4 typing identical information across two CRM windows instead of using the API lookup.</p>
                                        </div>
                                        <span style={{ fontSize: '0.875rem', opacity: 0.5 }}>10 mins ago</span>
                                    </div>
                                    <div style={{ marginTop: '1rem', padding: '1rem', background: 'rgba(16, 185, 129, 0.1)', borderRadius: '8px', borderLeft: '2px solid var(--secondary-color)' }}>
                                        <strong>💡 AI Optimization Suggestion:</strong> Implement an auto-fill script or train users on the existing unified search feature to save ~2 hours/week.
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

            </main>
        </div>
    );
};

export default Dashboard;
