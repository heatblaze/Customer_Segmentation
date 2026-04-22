'use client';

import ReactECharts from 'echarts-for-react';

interface RadarChartProps {
  personas: any[];
}

export default function RadarChart({ personas }: RadarChartProps) {
  if (!personas || personas.length === 0) return null;

  const indicator = [
    { name: 'Monetary', max: 10 },
    { name: 'Frequency', max: 10 },
    { name: 'Recency', max: 10 },
    { name: 'Range', max: 10 },
    { name: 'Loyalty', max: 10 },
  ];

  const seriesData = personas.map((p) => {
    // Normalize stats for radar view (0-10 scale)
    // In a real app, we'd use better normalization.
    const stats = p.stats || {};
    return {
      value: [
        Math.min(10, (stats.monetary / 1000) * 10),
        Math.min(10, stats.frequency),
        Math.min(10, (100 / (stats.recency + 1)) * 10), // Inverse recency
        Math.min(10, stats.range_sold),
        Math.min(10, p.score), 
      ],
      name: p.name,
      areaStyle: {
        color: p.color || 'rgba(99, 102, 241, 0.3)'
      },
      lineStyle: {
        width: 2
      },
      itemStyle: {
        color: p.color || '#6366f1'
      }
    };
  });

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item'
    },
    radar: {
      indicator: indicator,
      radius: '50%',
      splitNumber: 4,
      axisNameGap: 15,
      axisName: {
        color: '#94a3b8',
        fontSize: 10,
        fontWeight: 'bold'
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.05)'
        }
      },
      splitArea: {
        show: false
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.05)'
        }
      }
    },
    series: [
      {
        type: 'radar',
        data: seriesData
      }
    ]
  };

  return <ReactECharts option={option} style={{ height: '350px', width: '100%' }} />;
}
