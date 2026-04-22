'use client';

import ReactECharts from 'echarts-for-react';

export default function DistributionChart({ data }: { data: any[] }) {
  if (!data || data.length === 0) return null;

  const option = {
    backgroundColor: 'transparent',
    tooltip: { trigger: 'item' },
    legend: {
      orient: 'horizontal',
      bottom: '0',
      left: 'center',
      padding: [10, 0],
      textStyle: { color: '#94a3b8', fontSize: 10 }
    },
    grid: { bottom: '20%' },
    series: [
      {
        name: 'Segment Size',
        type: 'pie',
        radius: ['50%', '80%'],
        center: ['50%', '45%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 12,
          borderColor: 'rgba(0,0,0,0.5)',
          borderWidth: 2
        },
        label: { 
          show: false,
          position: 'center'
        },
        emphasis: {
          scaleSize: 10,
          label: {
            show: true,
            fontSize: '24',
            fontWeight: 'bold',
            color: '#fff',
            formatter: '{b}\n{d}%'
          }
        },
        labelLine: { show: false },
        data: data.map(d => ({
          value: d.retailer_count,
          name: d.value_label,
          itemStyle: { color: d.color }
        }))
      }
    ]
  };

  return <ReactECharts option={option} style={{ height: '450px', width: '100%' }} />;
}
