// src/pages/Dashboard.tsx
import React, { useState } from "react";
import QueryForm from "../components/QueryForm";
import StatusPoller from "../components/StatusPoller";
import MetricsChart from "../components/MetricsChart";
import { useAuthContext } from "../auth/AuthProvider";

type Metrics = {
  total_query: number;
  average_visibility: number;
};

const Dashboard: React.FC = () => {
  const { logout } = useAuthContext();

  const [brandName, setBrandName] = useState<string | null>(null);
  const [responseId, setResponseId] = useState<string | null>(null);
  const [metrics, setMetrics] = useState<Metrics | null>(null);

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      {/* Logout Button */}
      <button
        onClick={logout}
        className="absolute top-4 right-4 px-4 py-2 bg-red-500 text-white rounded-lg shadow hover:bg-red-600 transition"
      >
        Logout
      </button>
      {/* Header */}
      <header className="w-full flex justify-center mb-8">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 drop-shadow-lg">
          GenAI Search Visibility
        </h1>
      </header>

      {/* Query Form */}
      <div className="max-w-3xl mx-auto mb-10">
        <QueryForm
          onSubmitted={(brand: string, respId: string) => {
            setBrandName(brand);
            setResponseId(respId);
            setMetrics(null);
          }}
        />
      </div>

      {/* Main Content Area */}
      <div className="flex gap-6 items-start">
        {/* LEFT SIDE → Metrics Card (20%) */}
        <aside className="w-1/5 sticky top-6 self-start h-fit">
          <div className="bg-white rounded-xl shadow p-4">
            {metrics ? (
              <MetricsChart metrics={metrics} />
            ) : (
              <div className="text-gray-500 text-sm">
                Calculating Search Visibility...
              </div>
            )}
          </div>
        </aside>

        {/* RIGHT SIDE → StatusPoller (80%) */}
        <main className="w-4/5">
          {responseId && brandName ? (
            <div className="bg-white rounded-xl shadow p-6 max-h-[75vh] overflow-y-auto">
              <StatusPoller
                responseId={responseId}
                brandName={brandName}
                onCompleteMetrics={(m: Metrics) => setMetrics(m)}
              />
            </div>
          ) : (
            <div className="bg-white rounded-xl shadow p-6 text-gray-500 text-sm">
              Submit a query to begin.
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default Dashboard;