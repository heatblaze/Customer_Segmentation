'use client';

import React from 'react';
import { Lightbulb, CheckCircle2 } from 'lucide-react';

export default function BusinessInsights({ insights }: { insights: string[] }) {
  if (!insights || insights.length === 0) return null;

  return (
    <div className="insights-board">
      <div className="insights-grid">
        {insights.map((insight, i) => (
          <div key={i} className="insight-card">
            <div className="insight-icon">
              <Lightbulb size={18} />
            </div>
            <div className="insight-content" dangerouslySetInnerHTML={{ __html: insight }} />
            <div className="insight-action">
              <CheckCircle2 size={16} />
            </div>
          </div>
        ))}
      </div>

      <style jsx>{`
        .insights-board {
          display: flex;
          flex-direction: column;
          gap: 24px;
        }
        .insights-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
          gap: 16px;
        }
        .insight-card {
          background: rgba(255,255,255,0.03);
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 16px;
          padding: 20px;
          display: flex;
          align-items: flex-start;
          gap: 16px;
          transition: transform 0.2s, border-color 0.2s;
        }
        .insight-card:hover {
          transform: translateY(-2px);
          border-color: var(--primary);
          background: rgba(99, 102, 241, 0.05);
        }
        .insight-icon {
          width: 36px;
          height: 36px;
          border-radius: 10px;
          background: rgba(99, 102, 241, 0.1);
          color: var(--primary);
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
        }
        .insight-content {
          font-size: 14px;
          color: #cbd5e1;
          line-height: 1.6;
          flex: 1;
        }
        .insight-action {
          color: #4ade80;
          opacity: 0.4;
          margin-top: 4px;
        }
        .insight-card:hover .insight-action {
          opacity: 1;
        }
      `}</style>
    </div>
  );
}
