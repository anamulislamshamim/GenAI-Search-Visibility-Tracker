// src/components/MetricsChart.tsx
import React from "react";
import { Pie } from "react-chartjs-2";
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

type Props = {
  metrics: { total_query: number; average_visibility: number };
};

const MetricsChart: React.FC<Props> = ({ metrics }) => {
  const avg = Math.round(metrics.average_visibility_score);
  const total_query = metrics.total_queries
  const data = {
    labels: ["Average Visibility", "Remaining"],
    datasets: [
      {
        data: [avg, Math.max(0, 100 - avg)],
        // --- CRITICAL CHANGE: Added backgroundColor for slices ---
        backgroundColor: [
          '#4CAF50', // Green for Average Visibility
          '#F44336'  // Red for Remaining
        ],
        borderColor: [
          '#4CAF50',
          '#F44336'
        ],
        borderWidth: 1,
      },
    ],
  };

  return (
    <div className="chart-container max-w-lg mx-auto mt-8">
      <h3 className="text-2xl font-bold text-gray-800 text-center">
        Visibility Metrics
      </h3>

      <p className="text-center text-gray-600 mt-2">
        Total Queries:{" "} {/* Removed redundant {total_query} here */}
        <span className="font-semibold text-indigo-600">
          {total_query} {/* Displaying total_query */}
        </span>
      </p>

      <div className="flex justify-center mt-6">
        <div className="w-64 h-64">
          <Pie data={data} />
        </div>
      </div>

      <div className="mt-4 text-center text-gray-500 text-sm">
        Visibility Score:{" "}
        <span className="font-semibold text-indigo-700">{avg}%</span>
      </div>
    </div>
  );
};

export default MetricsChart;