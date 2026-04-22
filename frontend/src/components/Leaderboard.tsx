'use client';

import React from 'react';
import { ExternalLink, TrendingUp, Users } from 'lucide-react';

interface LeaderboardProps {
  data: any[];
  onRetailerClick: (retailer: any) => void;
}

export default function Leaderboard({ data, onRetailerClick }: LeaderboardProps) {
  if (!data || data.length === 0) return null;

  return (
    <div className="leaderboard-table">
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Retailer ID</th>
            <th>Segment</th>
            <th>Revenue (₹)</th>
            <th>Frequency</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i} onClick={() => onRetailerClick(row)} className="clickable-row">
              <td className="rank">#{i + 1}</td>
              <td className="retailer-id">{row.retailer}</td>
              <td>
                <span className="badge" style={{ backgroundColor: `${row.color}22`, color: row.color, border: `1px solid ${row.color}33` }}>
                  {row.value_label}
                </span>
              </td>
              <td className="monetary">₹{Math.round(row.monetary).toLocaleString()}</td>
              <td className="frequency">{row.frequency} orders</td>
              <td className="action">
                <button className="view-btn">
                  <ExternalLink size={14} />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <style jsx>{`
        .leaderboard-table {
          width: 100%;
          overflow-x: auto;
        }
        table {
          width: 100%;
          border-collapse: collapse;
          text-align: left;
        }
        th {
          padding: 16px;
          font-size: 11px;
          text-transform: uppercase;
          color: var(--text-muted);
          border-bottom: 1px solid rgba(255,255,255,0.05);
          letter-spacing: 0.1em;
        }
        td {
          padding: 16px;
          font-size: 14px;
          border-bottom: 1px solid rgba(255,255,255,0.02);
          color: #cbd5e1;
        }
        .clickable-row {
          cursor: pointer;
          transition: background 0.2s;
        }
        .clickable-row:hover {
          background: rgba(255,255,255,0.03);
        }
        .rank { font-weight: 700; color: var(--secondary); width: 60px; }
        .retailer-id { font-weight: 600; color: #fff; }
        .badge {
          padding: 4px 10px;
          border-radius: 6px;
          font-size: 11px;
          font-weight: 600;
        }
        .monetary { font-weight: 700; color: #fff; }
        .view-btn {
          background: rgba(255,255,255,0.05);
          border: 1px solid rgba(255,255,255,0.1);
          color: var(--text-muted);
          width: 32px;
          height: 32px;
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: all 0.2s;
        }
        .view-btn:hover {
          background: var(--primary);
          color: white;
          border-color: var(--primary);
        }
      `}</style>
    </div>
  );
}
