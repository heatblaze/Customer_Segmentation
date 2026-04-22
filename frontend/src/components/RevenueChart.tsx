'use client';

import ReactECharts from 'echarts-for-react';

export default function RevenueChart({ data }: { data: any[] }) {
  if (!data || data.length === 0) return null;

  // Sort data by revenue for better visualization
  const sortedData = [...data].sort((a, b) => a.total_revenue - b.total_revenue);

  const option = {
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    legend: {
      orient: 'horizontal',
      bottom: '0',
      left: 'center',
      padding: [0, 0, 10, 0],
      textStyle: { color: '#94a3b8', fontSize: 10 },
      itemWidth: 10,
      itemHeight: 10
    },
    grid: { left: '5%', right: '5%', bottom: '30%', containLabel: true },
    xAxis: {
      type: 'value',
      splitLine: { lineStyle: { type: 'dashed', color: 'rgba(255,255,255,0.05)' } },
      axisLabel: { 
        color: '#64748b',
        rotate: 45,
        fontSize: 9,
        formatter: (value: number) => {
          if (value >= 1e7) return (value / 1e7).toFixed(1) + 'C';
          if (value >= 1e5) return (value / 1e5).toFixed(1) + 'L';
          return value;
        }
      }
    },
    yAxis: {
      type: 'category',
      data: sortedData.map(d => d.value_label),
      axisLabel: { 
        color: '#94a3b8',
        fontSize: 12,
        fontWeight: 600,
        width: 100,
        overflow: 'break'
      }
    },
    series: [
      {
        name: 'Total Revenue (₹)',
        type: 'bar',
        barWidth: '40%',
        data: sortedData.map(d => ({
          value: d.total_revenue,
          itemStyle: { 
            color: d.color,
            borderRadius: [0, 6, 6, 0],
            shadowBlur: 10,
            shadowColor: 'rgba(0,0,0,0.3)'
          }
        }))
      }
    ]
  };

  return <ReactECharts option={option} style={{ height: '450px', width: '100%' }} />;
}
