import React, { useEffect, useState, useRef } from "react";
import api from "../api/apiClient";

type Props = {
  responseId: string;
  brandName: string;
  onCompleteMetrics: (metrics: { total_query: number; average_visibility: number }) => void;
};

const POLL_INTERVAL = 3000;

const StatusPoller: React.FC<Props> = ({ responseId, brandName, onCompleteMetrics }) => {
  const [status, setStatus] = useState("Processing");
  const [lastPayload, setLastPayload] = useState<any>(null);

  const timerRef = useRef<number | null>(null);
  const hasCompletedRef = useRef(false);

  useEffect(() => {
    hasCompletedRef.current = false; // reset on new responseId

    const poll = async () => {
      if (hasCompletedRef.current) return;

      try {
        const resp = await api.get(`/api/v1/query/${responseId}`);
        const data = resp.data;

        setLastPayload(data);
        setStatus(data.status || "Processing");

        if (String(data.status).toLowerCase() === "complete") {
          hasCompletedRef.current = true;

          if (timerRef.current) {
            clearInterval(timerRef.current);
            timerRef.current = null;
          }

          const metricsResp = await api.get(
            `/api/v1/metrics/aggregate/brand/${encodeURIComponent(brandName)}`
          );

          onCompleteMetrics(metricsResp.data);
        }
      } catch (error) {
        console.error("Polling error:", error);
      }
    };

    poll();
    timerRef.current = window.setInterval(poll, POLL_INTERVAL);

    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [responseId, brandName]);

  const statusColor =
    status.toLowerCase() === "complete"
      ? "bg-green-100 text-green-800"
      : status.toLowerCase() === "processing"
      ? "bg-yellow-100 text-yellow-800"
      : "bg-gray-100 text-gray-800";

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white rounded-lg shadow-md space-y-6">
      <div className={`inline-block px-3 py-1 rounded-full font-semibold ${statusColor}`}>
        Status: {status}
      </div>

      {status.toLowerCase() === "processing" && (
        <p className="text-gray-600 italic">
          Processing... checking every {POLL_INTERVAL / 1000} seconds
        </p>
      )}

      {lastPayload && (
        <div className="bg-gray-50 p-4 rounded-md border border-gray-200 overflow-auto">
          <h4 className="text-lg font-semibold mb-2">Last Query Result:</h4>
          <p className="mb-2">
            <strong>Brand Name:</strong> {lastPayload.brand_name}
          </p>
          <p className="mb-2">
            <strong>Visibility Score:</strong> {lastPayload.visibility_score}
          </p>
          <p className="mb-2 whitespace-pre-wrap">
            <strong>LLM Response:</strong> {lastPayload.raw_llm_response}
          </p>
          <p className="text-gray-500 text-sm">
            Processed at: {new Date(lastPayload.processed_at).toLocaleString()}
          </p>
        </div>
      )}
    </div>
  );
};

export default StatusPoller;



// import React, { useEffect, useState, useRef } from "react";
// import api from "../api/apiClient";

// type Props = {
//   responseId: string;
//   brandName: string;
//   onCompleteMetrics: (metrics: { total_query: number; average_visibility: number }) => void;
// };

// const POLL_INTERVAL = 3000;

// const StatusPoller: React.FC<Props> = ({ responseId, brandName, onCompleteMetrics }) => {
//   const [status, setStatus] = useState("Processing");
//   const [lastPayload, setLastPayload] = useState<any>(null);

//   const timerRef = useRef<number | null>(null);
//   const hasCompletedRef = useRef(false);  // <-- prevents infinite loop

//   useEffect(() => {
//     hasCompletedRef.current = false;  // reset on new responseId

//     const poll = async () => {
//       if (hasCompletedRef.current) return; // <-- stop future calls

//       try {
//         const resp = await api.get(`/api/v1/query/${responseId}`);
//         const data = resp.data;

//         setLastPayload(data);
//         setStatus(data.status || "Processing");

//         if (String(data.status).toLowerCase() === "complete") {
//           hasCompletedRef.current = true;   // <-- mark completed

//           // stop polling
//           if (timerRef.current) {
//             clearInterval(timerRef.current);
//             timerRef.current = null;
//           }

//           // now safely fetch metrics once
//           const metricsResp = await api.get(
//             `/api/v1/metrics/aggregate/brand/${encodeURIComponent(brandName)}`
//           );

//           onCompleteMetrics(metricsResp.data);
//         }
//       } catch (error) {
//         console.error("Polling error:", error);
//       }
//     };

//     // initial immediate poll
//     poll();

//     // start interval
//     timerRef.current = window.setInterval(poll, POLL_INTERVAL);

//     return () => {
//       if (timerRef.current) clearInterval(timerRef.current);
//     };
//   }, [responseId, brandName]);

//   return (
//     <div>
//       <h3>Status: {status}</h3>
//       {status.toLowerCase() === "processing" && <p>Processing...checking every 3 seconds</p>}
//       <pre>{JSON.stringify(lastPayload, null, 2)}</pre>
//     </div>
//   );
// };

// export default StatusPoller;
