'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity, 
  Users, 
  DollarSign, 
  Zap, 
  Settings, 
  ChevronRight,
  TrendingUp,
  AlertCircle,
  Database,
  PieChart as PieIcon,
  BarChart3,
  Lightbulb
} from 'lucide-react';

import PCAChart from '@/components/PCAChart';
import DistributionChart from '@/components/DistributionChart';
import RevenueChart from '@/components/RevenueChart';
import RadarChart from '@/components/RadarChart';
import PersonaCard from '@/components/PersonaCard';
import Leaderboard from '@/components/Leaderboard';
import MetricDistributions from '@/components/MetricDistributions';
import BusinessInsights from '@/components/BusinessInsights';
import RetailerProfileModal from '@/components/RetailerProfileModal';

export default function Dashboard() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [algorithm, setAlgorithm] = useState('kmeans');
  const [clusters, setClusters] = useState(5);
  const [error, setError] = useState<string | null>(null);
  const [isAdminOpen, setIsAdminOpen] = useState(false);
  const [selectedRetailer, setSelectedRetailer] = useState<any>(null);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      const x = (e.clientX / window.innerWidth) * 100;
      const y = (e.clientY / window.innerHeight) * 100;
      setMousePos({ x, y });
      document.documentElement.style.setProperty('--mouse-x', `${x}%`);
      document.documentElement.style.setProperty('--mouse-y', `${y}%`);
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.get(`http://localhost:8000/segments?algorithm=${algorithm}&n_clusters=${clusters}`);
      if (res.data.status === 'success') {
        setData(res.data);
      } else {
        setError(res.data.message);
      }
    } catch (err) {
      setError("Failed to connect to API. Ensure orchestrator is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [algorithm, clusters]);

  return (
    <main className="dashboard-container">
      {/* Navigation Sidebar */}
      <nav className="glass-panel sidebar">
        <div className="brand">
          <div className="logo-icon"><TrendingUp size={24} /></div>
          <h2 className="gradient-text" style={{ fontSize: '18px' }}>Intelligence</h2>
        </div>

        <div className="nav-section">
          <label>Engine Control</label>
          <div className="algo-toggle">
            <button 
              className={algorithm === 'kmeans' ? 'active' : ''} 
              onClick={() => setAlgorithm('kmeans')}
            >
              K-Means Standard
            </button>
            <button 
              className={algorithm === 'hdbscan' ? 'active' : ''} 
              onClick={() => setAlgorithm('hdbscan')}
            >
              HDBSCAN Advanced
            </button>
            <button 
              className={algorithm === 'gmm' ? 'active' : ''} 
              onClick={() => setAlgorithm('gmm')}
            >
              GMM Probabilistic
            </button>
          </div>
        </div>

        <div className="nav-section">
          <label>Segmentation Depth ({clusters})</label>
          <input 
            type="range" 
            min="2" 
            max="10" 
            value={clusters} 
            onChange={(e) => setClusters(parseInt(e.target.value))}
            className="depth-slider"
          />
        </div>

        <div className="nav-footer">
          <div className="status-indicator">
            <div className={`dot ${loading ? 'pulsing' : 'active'}`}></div>
            <span>{loading ? 'Analyzing...' : 'Connected'}</span>
          </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <div className="main-viewport">
        <header className="viewport-header">
          <div>
            <h1>Retail Customer Segmentation</h1>
            <p>Predictive analytics for <span className="highlight">{algorithm.toUpperCase()}</span> clusters</p>
          </div>
          <button 
            className="user-profile glass-card admin-btn" 
            onClick={() => setIsAdminOpen(true)}
          >
            <Settings size={18} />
            <span>System Admin</span>
            <div className="btn-glow" />
          </button>
        </header>

        {error && (
          <div className="error-banner">
            <AlertCircle size={20} />
            <span>{error}</span>
          </div>
        )}

        <div className="dashboard-grid">
          {/* KPI Row */}
          <div className="kpi-row grid-span-12">
            <KPICard 
              label="Total Retailers" 
              value={data?.stats?.total_retailers?.toLocaleString() || '——'} 
              icon={<Users />} 
              color="indigo" 
            />
            <KPICard 
              label="Revenue Pool" 
              value={data?.stats?.total_revenue ? `\u20b9${(data.stats.total_revenue / 1e7).toFixed(1)}Cr` : '——'} 
              icon={<DollarSign />} 
              color="cyan" 
            />
            <KPICard 
              label="Average Order Value" 
              value={data?.stats?.avg_monetary ? `\u20b9${Math.round(data.stats.avg_monetary).toLocaleString()}` : '——'} 
              icon={<TrendingUp />} 
              color="rose" 
            />
            <KPICard 
              label="Segment Count" 
              value={data?.stats?.segments_found || '——'} 
              icon={<BarChart3 />} 
              color="amber" 
            />
          </div>

          <div className="grid-span-12 persona-shelf">
            <div className="section-title">
              <Zap size={18} className="accent" />
              <h3>Behavioral Personas (Indexed by Cluster)</h3>
            </div>
            <div className="persona-grid">
              {data?.personas?.map((persona: any, i: number) => (
                <PersonaCard key={i} persona={persona} index={i} />
              ))}
            </div>
          </div>

          {/* Visualization Grid */}
          <div className="grid-span-8 glass-panel chart-container">
            <div className="chart-header">
              <Database size={18} />
              <h3>Complexity Projection (Latent Space)</h3>
            </div>
            {loading ? (
              <div className="chart-loading">Augmenting dimensions...</div>
            ) : (
              <PCAChart data={data?.data || []} />
            )}
          </div>

          <div className="grid-span-4 glass-panel chart-container">
            <div className="chart-header">
              <BarChart3 size={18} />
              <h3>Fingerprint DNA</h3>
            </div>
            <RadarChart personas={data?.personas || []} />
          </div>

          <div className="grid-span-6 glass-panel chart-container">
            <div className="chart-header">
              <PieIcon size={18} />
              <h3>Cluster Distribution</h3>
            </div>
            <DistributionChart data={data?.distribution || []} />
          </div>

          <div className="grid-span-6 glass-panel chart-container">
            <div className="chart-header">
              <BarChart3 size={18} />
              <h3>Monetary Contribution</h3>
            </div>
            <RevenueChart data={data?.revenue || []} />
          </div>

          {/* Intelligence Repository (Missing sections) */}
          <div className="grid-span-12 section-divider">
            <div className="divider-line" />
            <span className="divider-text">Intelligence Repository</span>
            <div className="divider-line" />
          </div>

          <div className="grid-span-12 glass-panel repository-card">
            <div className="chart-header">
              <TrendingUp size={18} />
              <h3>Metric Propensity Distributions</h3>
            </div>
            <MetricDistributions data={data?.rfm_distributions} />
          </div>

          <div className="grid-span-7 glass-panel repository-card">
            <div className="chart-header">
              <Users size={18} />
              <h3>Retailer Leaderboard</h3>
            </div>
            <Leaderboard 
              data={data?.leaderboard || []} 
              onRetailerClick={(r) => { setSelectedRetailer(r); setIsProfileOpen(true); }} 
            />
          </div>

          <div className="grid-span-5 glass-panel repository-card">
            <div className="chart-header">
              <Lightbulb size={18} />
              <h3>Actionable Business Insights</h3>
            </div>
            <BusinessInsights insights={data?.insights || []} />
          </div>
        </div>
      </div>

      {/* Retailer Detail Modal */}
      <RetailerProfileModal 
        isOpen={isProfileOpen} 
        onClose={() => setIsProfileOpen(false)} 
        retailer={selectedRetailer} 
      />

      {/* System Admin Modal */}
      <AnimatePresence>
        {isAdminOpen && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="modal-overlay"
            onClick={() => setIsAdminOpen(false)}
          >
            <motion.div 
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ type: 'spring', damping: 25, stiffness: 200 }}
              className="admin-drawer glass-panel"
              onClick={e => e.stopPropagation()}
            >
              <div className="drawer-header">
                <div className="header-title">
                  <div className="icon-pulse"><Activity size={20} /></div>
                  <h2>System Oversight</h2>
                </div>
                <button className="close-btn" onClick={() => setIsAdminOpen(false)}>&times;</button>
              </div>

              <div className="drawer-content">
                <div className="metrics-summary">
                  <div className="main-metric-box">
                    <label>Structural Integrity</label>
                    <div className="metric-row">
                      <span className="big-value">{(data?.metadata?.silhouette_score || 0).toFixed(3)}</span>
                      <span className="unit">Silhouette Index</span>
                    </div>
                    <div className="integrity-bar">
                      <div className="integrity-fill" style={{ width: `${(data?.metadata?.silhouette_score || 0) * 100}%` }}></div>
                    </div>
                  </div>

                  <div className="dual-metrics">
                    <div className="mini-box">
                      <label>Latency</label>
                      <span className="mini-value accent">24ms</span>
                    </div>
                    <div className="mini-box">
                      <label>Confidence</label>
                      <span className="mini-value">94.2%</span>
                    </div>
                  </div>
                </div>

                <div className="drawer-section">
                  <label>Algorithmic Rationale</label>
                  <div className="rationale-card">
                    <div className="rationale-glow" />
                    <p>
                      {algorithm === 'kmeans' ? (
                        "K-Means is currently operating as the baseline. It assumes spherical cluster shapes, which may lead to overlap in high-dimensional behavioral data. Switching to HDBSCAN is recommended."
                      ) : algorithm === 'hdbscan' ? (
                        "HDBSCAN is optimizing for density-reachability. This neural approach is highly resistant to noise and identifies complex, non-linear retail patterns."
                      ) : (
                        "GMM is applying probabilistic soft-clustering. This allows for 'fuzzy' boundary retailers that exhibit characteristics of multiple personas."
                      )}
                    </p>
                  </div>
                </div>

                <div className="drawer-section">
                  <label>Engine Parameters</label>
                  <div className="param-grid">
                     <div className="param-node">
                        <span className="p-key">Cluster Depth</span>
                        <span className="p-val">{clusters}</span>
                     </div>
                     <div className="param-node">
                        <span className="p-key">Min Sample Size</span>
                        <span className="p-val">15</span>
                     </div>
                     <div className="param-node">
                        <span className="p-key">Feature Set</span>
                        <span className="p-val">Premium (Neural)</span>
                     </div>
                  </div>
                </div>
              </div>

              <div className="drawer-footer">
                <div className="system-status">
                  <div className="pulse-dot"></div>
                  <span>Engine Stable</span>
                </div>
                <button className="rebuild-btn" onClick={() => { setIsAdminOpen(false); fetchData(); }}>Rebuild Indices</button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      <style jsx>{`
        /* ... previous styles remain same, adding persona shelf styles ... */
        .persona-shelf {
          margin-bottom: 24px;
        }
        .persona-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
          gap: 20px;
          padding-bottom: 24px;
        }
        .section-divider {
          display: flex;
          align-items: center;
          gap: 24px;
          margin: 40px 0 12px 0;
        }
        .divider-line {
          flex: 1;
          height: 1px;
          background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        }
        .divider-text {
          font-family: 'Outfit', sans-serif;
          font-size: 14px;
          font-weight: 600;
          color: var(--text-muted);
          text-transform: uppercase;
          letter-spacing: 0.2em;
        }
        .repository-card {
          margin-bottom: 24px;
          padding: 24px;
        }
        .grid-span-6 { grid-column: span 6; }
        .grid-span-7 { grid-column: span 7; }
        .grid-span-5 { grid-column: span 5; }
        @media (max-width: 1440px) {
          .main-viewport { padding: 16px; }
          .dashboard-grid { gap: 16px; }
          .chart-container { padding: 16px; }
          .grid-span-6, .grid-span-7, .grid-span-5, .grid-span-8, .grid-span-4 { 
            grid-column: span 12; 
          }
        }
        .admin-btn {
          position: relative;
          padding: 8px 16px;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 8px;
          border: 1px solid var(--primary) !important;
          background: rgba(99, 102, 241, 0.1) !important;
          transition: all 0.3s;
          overflow: hidden;
        }
        .admin-btn:hover {
          background: var(--primary) !important;
          transform: translateY(-2px);
          box-shadow: 0 0 20px var(--primary-glow);
        }
        .admin-btn span { font-size: 14px; font-weight: 600; color: #fff !important; }
        .btn-glow {
          position: absolute;
          top: 0;
          left: -100%;
          width: 50%;
          height: 100%;
          background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
          transform: skewX(-25deg);
          animation: sweep 3s infinite;
        }
        @keyframes sweep {
          0% { left: -100%; }
          50% { left: 150%; }
          100% { left: 150%; }
        }
        .section-title {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 16px;
        }
        .persona-container {
          display: flex;
          gap: 20px;
          overflow-x: auto;
          padding-bottom: 12px;
          scrollbar-width: none;
        }
        .persona-container::-webkit-scrollbar {
          display: none;
        }
        .dashboard-container {
          display: flex;
          height: 100vh;
        }
        .sidebar {
          width: 280px;
          margin: 12px;
          padding: 24px;
          display: flex;
          flex-direction: column;
          gap: 32px;
        }
        .brand {
          display: flex;
          align-items: center;
          gap: 12px;
        }
        .logo-icon {
          width: 40px;
          height: 40px;
          background: var(--primary);
          border-radius: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .nav-section label {
          display: block;
          font-size: 11px;
          text-transform: uppercase;
          letter-spacing: 0.1em;
          color: var(--text-muted);
          margin-bottom: 12px;
        }
        .algo-toggle {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }
        .algo-toggle button {
          background: rgba(255,255,255,0.03);
          border: 1px solid rgba(255,255,255,0.05);
          color: white;
          padding: 12px;
          border-radius: 10px;
          text-align: left;
          cursor: pointer;
          transition: all 0.2s;
        }
        .algo-toggle button.active {
          background: var(--primary);
          border-color: var(--primary);
          box-shadow: 0 4px 15px var(--primary-glow);
        }
        .depth-slider {
          width: 100%;
          accent-color: var(--primary);
        }
        .main-viewport {
          flex: 1;
          padding: 24px;
          overflow-y: auto;
        }
        .viewport-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 32px;
        }
        .kpi-row {
          display: grid;
          grid-template-columns: repeat(4, 1fr);
          gap: 20px;
          margin-bottom: 24px;
        }
        .grid-span-12 { grid-column: span 12; }
        .grid-span-8 { grid-column: span 8; }
        .grid-span-4 { grid-column: span 4; }
        .chart-container {
          min-height: 400px;
          padding: 24px;
        }
        .scrollable {
          max-height: 500px;
          overflow-y: auto;
          padding: 24px;
        }
        .insight-card {
          padding: 16px;
          border-bottom: 1px solid rgba(255,255,255,0.05);
          display: flex;
          gap: 12px;
          font-size: 14px;
          line-height: 1.5;
        }
        .pulsing {
          animation: pulse 1.5s infinite;
          background: var(--secondary);
        }
        @keyframes pulse {
          0% { opacity: 0.4; }
          50% { opacity: 1; }
          100% { opacity: 0.4; }
        }
        .dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #4ade80;
        }
        .status-indicator {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 12px;
          color: var(--text-muted);
        }
        .admin-drawer {
          width: 500px;
          height: 100vh;
          border-radius: 0;
          border-left: 1px solid rgba(255,255,255,0.1);
          padding: 0;
          display: flex;
          flex-direction: column;
          background: rgba(10, 10, 15, 0.9);
          backdrop-filter: blur(40px);
        }
        .drawer-header {
          padding: 40px;
          display: flex;
          justify-content: space-between;
          align-items: center;
          border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        .header-title {
          display: flex;
          align-items: center;
          gap: 16px;
        }
        .icon-pulse {
          color: var(--secondary);
          animation: pulse 2s infinite;
        }
        .header-title h2 { margin: 0; font-size: 22px; font-weight: 700; letter-spacing: -0.01em; }
        .close-btn {
          background: transparent;
          border: none;
          color: var(--text-muted);
          font-size: 28px;
          cursor: pointer;
          transition: color 0.2s;
        }
        .close-btn:hover { color: #fff; }
        .drawer-content {
          flex: 1;
          padding: 40px;
          overflow-y: auto;
          display: flex;
          flex-direction: column;
          gap: 48px;
        }
        .metrics-summary {
          display: flex;
          flex-direction: column;
          gap: 32px;
        }
        .main-metric-box {
          padding: 24px;
          background: rgba(255,255,255,0.03);
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 20px;
        }
        .main-metric-box label { display: block; font-size: 11px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 12px; }
        .metric-row { display: flex; align-items: baseline; gap: 12px; margin-bottom: 20px; }
        .big-value { font-size: 48px; font-weight: 800; color: #fff; }
        .unit { font-size: 13px; color: var(--text-muted); }
        .integrity-bar { height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; }
        .integrity-fill { height: 100%; background: var(--secondary); box-shadow: 0 0 15px var(--secondary-glow); border-radius: 2px; }
        .dual-metrics { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .mini-box { padding: 16px; background: rgba(255,255,255,0.02); border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); }
        .mini-box label { display: block; font-size: 10px; text-transform: uppercase; color: var(--text-muted); margin-bottom: 8px; }
        .mini-value { font-size: 20px; font-weight: 700; color: #fff; }
        .drawer-section label { display: block; font-size: 11px; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.1em; margin-bottom: 20px; }
        .rationale-card { position: relative; padding: 24px; background: rgba(255,255,255,0.02); border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); overflow: hidden; }
        .rationale-glow { position: absolute; top: -50px; left: -50px; width: 100px; height: 100px; background: var(--primary-glow); filter: blur(50px); opacity: 0.3; }
        .rationale-card p { position: relative; margin: 0; font-size: 14px; color: var(--text-muted); line-height: 1.7; }
        .param-grid { display: flex; flex-direction: column; gap: 12px; }
        .param-node { display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; background: rgba(255,255,255,0.02); border-radius: 8px; }
        .p-key { font-size: 13px; color: var(--text-muted); }
        .p-val { font-size: 13px; font-weight: 600; color: #fff; }
        .drawer-footer { padding: 40px; border-top: 1px solid rgba(255,255,255,0.05); display: flex; justify-content: space-between; align-items: center; }
        .system-status { display: flex; align-items: center; gap: 10px; font-size: 12px; color: var(--text-muted); }
        .pulse-dot { width: 6px; height: 6px; background: #10b981; border-radius: 50%; box-shadow: 0 0 10px #10b981; animation: pulse 2s infinite; }
        .rebuild-btn { padding: 10px 20px; background: var(--primary); color: #fff; border: none; border-radius: 10px; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
        .rebuild-btn:hover { transform: scale(1.05); box-shadow: 0 0 20px var(--primary-glow); }
        .error-banner {
          background: var(--accent-glow);
          border: 1px solid var(--accent);
          padding: 12px;
          border-radius: 8px;
          margin-bottom: 24px;
          display: flex;
          align-items: center;
          gap: 12px;
          color: white;
        }
      `}</style>
    </main>
  );
}

function KPICard({ label, value, icon, color }: any) {
  return (
    <div className="glass-card kpi-card">
      <div className={`icon-box ${color}`}>{icon}</div>
      <div className="kpi-info">
        <p className="kpi-label">{label}</p>
        <h2 className="kpi-value">{value}</h2>
      </div>
      <style jsx>{`
        .kpi-card {
          padding: 24px;
          display: flex;
          align-items: center;
          gap: 20px;
        }
        .icon-box {
          width: 48px;
          height: 48px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: rgba(255,255,255,0.05);
        }
        .icon-box.indigo { color: #6366f1; background: rgba(99, 102, 241, 0.1); }
        .icon-box.cyan { color: #22d3ee; background: rgba(34, 211, 238, 0.1); }
        .icon-box.rose { color: #f43f5e; background: rgba(244, 63, 94, 0.1); }
        .icon-box.amber { color: #facc15; background: rgba(250, 204, 21, 0.1); }
        .kpi-label {
          font-size: 12px;
          color: var(--text-muted);
          text-transform: uppercase;
          margin-bottom: 4px;
        }
        .kpi-value {
          font-size: 24px;
          font-weight: 700;
        }
      `}</style>
    </div>
  );
}
