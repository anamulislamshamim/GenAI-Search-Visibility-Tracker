// src/pages/Dashboard.tsx
import React, { useState } from "react";
import QueryForm from "../components/QueryForm";
import StatusPoller from "../components/StatusPoller";
import MetricsChart from "../components/MetricsChart";
import { useAuthContext } from "../auth/AuthProvider";
import get_python_code from "../components/VisibilityCode";

type Metrics = {
  total_query: number;
  average_visibility: number;
};

const Dashboard: React.FC = () => {
  const { logout } = useAuthContext();

  const [brandName, setBrandName] = useState<string | null>(null);
  const [responseId, setResponseId] = useState<string | null>(null);
  const [metrics, setMetrics] = useState<Metrics | null>(null);

  const PythonCode = get_python_code()

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
        <aside className="w-2/5 sticky top-6 self-start h-fit">
          <div className="bg-white rounded-xl shadow p-4">
            {metrics ? (
              <MetricsChart metrics={metrics} />
            ) : (
              <div className="text-gray-500 text-sm">
                BigQuery Visibility Metrics
              </div>
            )}
          </div>
        </aside>

        {/* RIGHT SIDE → StatusPoller (80%) */}
        <main className="w-3/5">
          {responseId && brandName ? (
            <div className="bg-white rounded-xl shadow p-6 max-h-[75vh] overflow-y-auto">
              <StatusPoller
                responseId={responseId}
                brandName={brandName}
                onCompleteMetrics={(m: Metrics) => setMetrics(m)}
              />
            </div>
          ) : (
            <div className="max-w-full mx-auto p-6 bg-gray-800 rounded-xl shadow-lg">
                <h2 className="text-xl font-semibold text-white mb-4">How we calculate Visibility?</h2>
                <pre className="overflow-x-auto p-4 bg-gray-900 rounded-lg text-sm">
                    <code className="text-yellow-300 font-mono whitespace-pre">
                        {PythonCode}
                    </code>
                </pre>
                <p className="mt-4 text-gray-400 text-sm">
                    This code is displayed on the frontend but executes on the backend.
                </p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default Dashboard;