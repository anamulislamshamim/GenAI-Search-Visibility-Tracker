// src/pages/Dashboard.tsx
import React, { useState } from "react";
import QueryForm from "../components/QueryForm";
import StatusPoller from "../components/StatusPoller";
import MetricsChart from "../components/MetricsChart";

const Dashboard: React.FC = () => {
  const [brandName, setBrandName] = useState<string | null>(null);
  const [responseId, setResponseId] = useState<string | null>(null);
  const [metrics, setMetrics] = useState<{ total_query: number; average_visibility: number } | null>(null);

  return (
    <div>
      <header class="w-full flex justify-center mt-8">
          <h1 class="text-4xl md:text-5xl font-bold text-gray-900 drop-shadow-lg">
            GenAI Search Visibility
          </h1>
      </header>
      <QueryForm
        onSubmitted={(brand, respId) => {
          setBrandName(brand);
          setResponseId(respId);
          setMetrics(null);
        }}
      />
      {responseId && brandName && (
        <StatusPoller
          responseId={responseId}
          brandName={brandName}
          onCompleteMetrics={(m) => setMetrics(m)}
        />
      )}

      {metrics && <MetricsChart metrics={metrics} />}
    </div>
  );
};

export default Dashboard;
