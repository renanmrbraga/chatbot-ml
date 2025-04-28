// src/components/ChartRenderer.tsx
import type { EChartsOption } from 'echarts';
import ReactECharts from 'echarts-for-react';
import React from 'react';

export interface ChartData {
  cidades: string[];
  metricas: string[];
  valores: Record<string, number[]>;
}

interface ChartRendererProps {
  data: ChartData;
}

const ChartRenderer: React.FC<ChartRendererProps> = ({ data }) => {
  const { cidades, metricas, valores } = data;

  let option: EChartsOption;

  if (metricas.length === 1) {
    // barras
    option = {
      xAxis: {
        type: 'category',
        data: cidades,
      },
      yAxis: {
        type: 'value',
      },
      tooltip: {
        trigger: 'axis',
      },
      series: [
        {
          data: cidades.map((c) => valores[c][0]),
          type: 'bar',
        },
      ],
    };
  } else if (metricas.length === 2) {
    // scatter
    option = {
      xAxis: {
        name: metricas[0],
        type: 'value',
      },
      yAxis: {
        name: metricas[1],
        type: 'value',
      },
      tooltip: {
        trigger: 'item',
      },
      series: [
        {
          data: cidades.map((c) => valores[c]),
          type: 'scatter',
          symbolSize: 20,
        },
      ],
    };
  } else if (metricas.length > 1 && cidades.length > 1) {
    // radar
    const maxVal = Math.max(...[].concat(...Object.values(valores)));
    option = {
      tooltip: {},
      radar: {
        indicator: metricas.map((m) => ({ name: m, max: maxVal })),
      },
      series: [
        {
          type: 'radar',
          data: cidades.map((c) => ({
            name: c,
            value: valores[c],
          })),
        },
      ],
    };
  } else {
    // fallback para gauge ou outros
    const c = cidades[0];
    option = {
      series: [
        {
          type: 'gauge',
          detail: {
            formatter: '{value}',
          },
          data: [
            {
              value: valores[c][0],
              name: metricas[0],
            },
          ],
        },
      ],
    };
  }

  return <ReactECharts option={option} style={{ height: '300px', width: '100%' }} />;
};

export default ChartRenderer;
