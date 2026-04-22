'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, User, DollarSign, Calendar, RefreshCcw, Package } from 'lucide-react';

interface RetailerProfileModalProps {
  isOpen: boolean;
  onClose: () => void;
  retailer: any;
}

export default function RetailerProfileModal({ isOpen, onClose, retailer }: RetailerProfileModalProps) {
  if (!retailer) return null;

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div 
          key={retailer?.retailer || 'modal-overlay'}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="modal-overlay"
          onClick={onClose}
        >
          <motion.div 
            key="modal-content"
            initial={{ scale: 0.9, y: 20 }}
            animate={{ scale: 1, y: 0 }}
            exit={{ scale: 0.9, y: 20 }}
            className="profile-modal glass-panel"
            onClick={e => e.stopPropagation()}
            suppressHydrationWarning
          >
            <div className="modal-header">
              <div className="retailer-title">
                <div className="profile-icon" style={{ background: `${retailer.color}22`, color: retailer.color }}>
                  <User size={24} />
                </div>
                <div>
                  <h2>Retailer ID: {retailer.retailer}</h2>
                  <span className="badge" style={{ backgroundColor: `${retailer.color}22`, color: retailer.color }}>
                    {retailer.value_label}
                  </span>
                </div>
              </div>
              <button className="close-btn" onClick={onClose}><X size={20} /></button>
            </div>

            <div className="modal-body">
              <div className="profile-grid">
                <ProfileItem 
                  icon={<DollarSign size={18} />} 
                  label="Monetary Weight" 
                  value={`₹${Math.round(retailer.monetary || 0).toLocaleString()}`} 
                />
                <ProfileItem 
                  icon={<RefreshCcw size={18} />} 
                  label="Purchase Velocity" 
                  value={`${retailer.frequency || 0} Orders`} 
                />
                <ProfileItem 
                  icon={<Calendar size={18} />} 
                  label="Days Dormant" 
                  value={`${retailer.recency || 0} Days`} 
                />
                <ProfileItem 
                  icon={<Package size={18} />} 
                  label="Diversification" 
                  value={`${retailer.range_sold || 0} Categories`} 
                />
              </div>

              {retailer.loyalty_score && (
                <div className="advanced-metrics">
                   <MetricBar label="Loyalty Score" value={retailer.loyalty_score * 100} color="#10b981" />
                   <MetricBar label="Search Intent" value={retailer.search_intent_score * 100} color="#6366f1" />
                </div>
              )}

              <div className="behavioral-summary">
                <h3>Behavioral Footprint</h3>
                <p>
                  This retailer is classified as <strong>{retailer.value_label}</strong>. 
                  Their purchase patterns indicate high engagement with {retailer.range_sold} different product categories.
                  With a monetary contribution of ₹{Math.round(retailer.monetary).toLocaleString()}, they are a key stakeholder in the {retailer.value_label} segment.
                </p>
              </div>
            </div>

            <div className="modal-footer">
              <button className="action-btn primary">Export Profile</button>
              <button className="action-btn secondary" onClick={onClose}>Close</button>
            </div>
          </motion.div>
        </motion.div>
      )}

      <style jsx>{`
        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0,0,0,0.6);
          backdrop-filter: blur(8px);
          z-index: 2000;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 20px;
        }
        .profile-modal {
          width: 100%;
          max-width: 600px;
          border-radius: 24px;
          padding: 32px;
          background: rgba(15, 23, 42, 0.95);
          border: 1px solid rgba(255,255,255,0.1);
          box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
        }
        .modal-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 32px;
        }
        .retailer-title {
          display: flex;
          align-items: center;
          gap: 20px;
        }
        .profile-icon {
          width: 56px;
          height: 56px;
          border-radius: 16px;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .retailer-title h2 {
          margin: 0;
          font-size: 24px;
          font-weight: 700;
          color: #fff;
        }
        .badge {
          display: inline-block;
          margin-top: 8px;
          padding: 4px 12px;
          border-radius: 100px;
          font-size: 12px;
          font-weight: 600;
          text-transform: uppercase;
        }
        .close-btn {
          background: transparent;
          border: none;
          color: #94a3b8;
          cursor: pointer;
          padding: 8px;
          border-radius: 50%;
          transition: background 0.2s;
        }
        .close-btn:hover { background: rgba(255,255,255,0.05); color: #fff; }
        .profile-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 20px;
          margin-bottom: 32px;
        }
        .behavioral-summary {
          padding: 24px;
          background: rgba(255,255,255,0.03);
          border-radius: 16px;
          border: 1px solid rgba(255,255,255,0.05);
        }
        .behavioral-summary h3 {
          margin: 0 0 12px 0;
          font-size: 16px;
          color: #fff;
        }
        .behavioral-summary p {
          margin: 0;
          font-size: 14px;
          color: #94a3b8;
          line-height: 1.6;
        }
        .modal-footer {
          margin-top: 32px;
          display: flex;
          gap: 12px;
          justify-content: flex-end;
        }
        .action-btn {
          padding: 10px 24px;
          border-radius: 10px;
          font-size: 14px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s;
        }
        .action-btn.primary {
          background: var(--primary);
          color: #fff;
          border: none;
        }
        .action-btn.primary:hover {
          box-shadow: 0 0 20px var(--primary-glow);
          transform: translateY(-1px);
        }
        .action-btn.secondary {
          background: transparent;
          border: 1px solid rgba(255,255,255,0.1);
          color: #94a3b8;
        }
        .action-btn.secondary:hover { background: rgba(255,255,255,0.05); color: #fff; }
      `}</style>
    </AnimatePresence>
  );
}

function ProfileItem({ icon, label, value }: any) {
  return (
    <div className="profile-item">
      <div className="item-icon">{icon}</div>
      <div className="item-info">
        <p className="item-label">{label}</p>
        <p className="item-value">{value}</p>
      </div>
      <style jsx>{`
        .profile-item {
          display: flex;
          gap: 16px;
          align-items: center;
        }
        .item-icon {
          color: var(--primary);
          opacity: 0.8;
        }
        .item-label {
          font-size: 11px;
          color: #64748b;
          text-transform: uppercase;
          margin: 0 0 2px 0;
        }
        .item-value {
          font-size: 16px;
          font-weight: 700;
          color: #fff;
          margin: 0;
        }
      `}</style>
    </div>
  );
}

function MetricBar({ label, value, color }: any) {
  return (
    <div className="metric-bar-container">
      <div className="metric-header">
        <span className="label">{label}</span>
        <span className="value">{Math.round(value)}%</span>
      </div>
      <div className="bar-bg">
        <div className="bar-fill" style={{ width: `${value}%`, backgroundColor: color, boxShadow: `0 0 10px ${color}44` }} />
      </div>
      <style jsx>{`
        .metric-bar-container {
          margin-bottom: 20px;
        }
        .metric-header {
          display: flex;
          justify-content: space-between;
          font-size: 11px;
          text-transform: uppercase;
          color: #64748b;
          margin-bottom: 8px;
        }
        .bar-bg {
          height: 6px;
          background: rgba(255,255,255,0.05);
          border-radius: 3px;
          overflow: hidden;
        }
        .bar-fill {
          height: 100%;
          border-radius: 3px;
          transition: width 0.6s ease-out;
        }
      `}</style>
    </div>
  );
}
