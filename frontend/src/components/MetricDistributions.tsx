'use client';

import React from 'react';
import ReactECharts from 'echarts-for-react';

interface MetricDistributionsProps {
  data: any;
}

export default function MetricDistributions({ data }: MetricDistributionsProps) {
  if (!data) return null;

  const renderChart = (metric: string, title: string, color: string) => {
    const metricData = data[metric];
    if (!metricData) return null;

    const option = {
      backgroundColor: 'transparent',
      title: {
        text: title,
        textStyle: { color: '#94a3b8', fontSize: 13, fontWeight: 500 },
        left: 'center'
      },
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      grid: { left: '3%', right: '4%', bottom: '15%', containLabel: true },
      xAxis: {
        type: 'category',
        data: metricData.bins.slice(0, -1).map((b: number) => Math.round(b).toLocaleString()),
        axisLabel: { color: '#64748b', fontSize: 10, rotate: 45 }
      },
      yAxis: {
        type: 'value',
        axisLabel: { color: '#64748b', fontSize: 10 },
        splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } }
      },
      series: [
        {
          data: metricData.counts,
          type: 'bar',
          itemStyle: { 
            color: color,
            borderRadius: [4, 4, 0, 0]
          }
        }
      ]
    };

    return <ReactECharts option={option} style={{ height: '220px', width: '100%' }} />;
  };

  return (
    <div className="distributions-grid">
      <div className="dist-item">{renderChart('recency', 'Recency (Days)', '#6366f1')}</div>
      <div className="dist-item">{renderChart('frequency', 'Frequency (Orders)', '#22d3ee')}</div>
      <div className="dist-item">{renderChart('monetary', 'Monetary (Revenue)', '#f43f5e')}</div>

      <style jsx>{`
        .distributions-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
          gap: 20px;
          margin-top: 20px;
        }
        .dist-item {
          background: rgba(255,255,255,0.02);
          border-radius: 12px;
          padding: 16px;
          border: 1px solid rgba(255,255,255,0.05);
        }
      `}</style>
    </div>
  );
}
