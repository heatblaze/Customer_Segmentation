'use client';

import { motion } from 'framer-motion';
import { Zap, TrendingUp, BarChart3, Users } from 'lucide-react';

interface PersonaCardProps {
  persona: any;
  index: number;
}

export default function PersonaCard({ persona, index }: PersonaCardProps) {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      className="glass-card persona-card"
    >
      <div className="persona-header">
        <div className="persona-icon-ring" style={{ borderColor: persona.color }}>
          <Zap size={18} style={{ color: persona.color }} />
        </div>
        <div className="persona-title-group">
          <h4 className="persona-name">{persona.name}</h4>
          <span className="segment-label">{persona.label} Segment</span>
        </div>
      </div>
      
      <p className="persona-desc">{persona.description}</p>
      
      <div className="persona-metrics">
        <div className="mini-metric">
          <span className="metric-label">Dominant Trait</span>
          <span className="metric-value highlight">{persona.top_trait}</span>
        </div>
        <div className="mini-metric">
          <span className="metric-label">Health Score</span>
          <span className="metric-value">{persona.score}/10</span>
        </div>
      </div>

      <style jsx>{`
        .persona-card {
          padding: 32px;
          display: flex;
          flex-direction: column;
          width: 320px;
          min-height: 280px;
          height: auto;
          flex-shrink: 0;
          background: rgba(255, 255, 255, 0.03);
          border: 1px solid rgba(255, 255, 255, 0.08);
          position: relative;
          overflow: hidden;
        }
        .persona-header {
          display: flex;
          align-items: center;
          gap: 20px;
          margin-bottom: 24px;
        }
        .persona-desc {
          font-size: 13px;
          color: var(--text-muted);
          line-height: 1.6;
          margin: 0 0 24px 0;
          opacity: 0.8;
          flex-grow: 1;
        }
        .persona-metrics {
          margin-top: auto;
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 16px;
          padding-top: 20px;
          border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        .persona-icon-ring {
          width: 42px;
          height: 42px;
          border-radius: 12px;
          border: 1px solid rgba(255,255,255,0.1);
          display: flex;
          align-items: center;
          justify-content: center;
          background: rgba(255,255,255,0.03);
        }
        .persona-title-group {
          display: flex;
          flex-direction: column;
          min-width: 0;
        }
        .persona-name {
          font-size: 16px;
          font-weight: 700;
          margin: 0;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          color: #fff;
          letter-spacing: -0.01em;
        }
        .segment-label {
          font-size: 11px;
          color: var(--text-muted);
          text-transform: uppercase;
          font-weight: 500;
          letter-spacing: 0.05em;
          margin-top: 2px;
        }
        .mini-metric {
          display: flex;
          flex-direction: column;
          gap: 6px;
        }
        .metric-label {
          font-size: 10px;
          color: var(--text-muted);
          text-transform: uppercase;
          font-weight: 600;
          letter-spacing: 0.08em;
        }
        .metric-value {
          font-size: 14px;
          font-weight: 700;
          color: #fff;
        }
      `}</style>
    </motion.div>
  );
}
