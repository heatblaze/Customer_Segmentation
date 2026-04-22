'use client';

import ReactECharts from 'echarts-for-react';

export default function PCAChart({ data }: { data: any[] }) {
  if (!data || data.length === 0) return <div>No data available</div>;

  // Map data to ECharts format
  // Assuming the API returns recency_scaled, frequency_scaled etc.
  // For a simple 2D view, we'll use recency_scaled and frequency_scaled as placeholders 
  // until we implement actual PCA on the backend or frontend.
  
  const series = Array.from(new Set(data.map(d => d.value_label))).map(label => {
    const segmentData = data.filter(d => d.value_label === label);
    const color = segmentData[0]?.color || '#6366f1';
    return {
      name: label,
      type: 'scatter',
      symbolSize: (data: any) => {
        // Size nodes by monetary importance
        return Math.min(12, Math.max(4, data[2] * 4));
      },
      data: segmentData.map(d => [d.recency_scaled, d.frequency_scaled, d.monetary_scaled]),
      itemStyle: {
        color: color,
        shadowBlur: 10,
        shadowColor: color,
        opacity: 0.8
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 20,
          opacity: 1
        }
      }
    };
  });

  const option = {
    backgroundColor: 'transparent',
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '5%',
      containLabel: true
    },
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(10, 10, 15, 0.9)',
      borderColor: 'rgba(255,255,255,0.1)',
      textStyle: { color: '#fff' },
      formatter: (params: any) => {
        return `<div style="padding: 4px">
          <b style="color:${params.color}">${params.seriesName}</b><br/>
          <span style="font-size:11px; opacity:0.7">Cluster Signature</span>
        </div>`;
      }
    },
    legend: {
      textStyle: { color: '#94a3b8', fontSize: 10 },
      bottom: 0,
      itemWidth: 10,
      itemHeight: 10
    },
    xAxis: {
      name: 'Velocity',
      nameLocation: 'middle',
      nameGap: 25,
      splitLine: { lineStyle: { type: 'dashed', color: 'rgba(255,255,255,0.03)' } },
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } },
      axisLabel: { color: '#64748b', fontSize: 10 }
    },
    yAxis: {
      name: 'Engagement',
      nameLocation: 'middle',
      nameGap: 35,
      splitLine: { lineStyle: { type: 'dashed', color: 'rgba(255,255,255,0.03)' } },
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } },
      axisLabel: { color: '#64748b', fontSize: 10 }
    },
    series: series
  };

  return <ReactECharts option={option} style={{ height: '400px', width: '100%' }} />;
}
