// src/components/QueryForm.tsx
import React, { useState } from "react";
import api from "../api/apiClient";

type Props = {
  onSubmitted: (brand: string, responseId: string) => void;
};

const QueryForm: React.FC<Props> = ({ onSubmitted }) => {
  const [brand, setBrand] = useState("");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault(); 
    setErr(null);
    setLoading(true);
    try {
      const resp = await api.post("/api/v1/query-brand", { brand_name: brand });
      // assume server returns { response_id, status }
      const data = resp.data;
      if (!data?.response_id) throw new Error("Invalid response from server");
      onSubmitted(brand, data.response_id);
    } catch (error: any) {
      setErr(error?.response?.data?.message ?? String(error));
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={submit} className="max-w-md mx-auto p-4 bg-white rounded shadow-md space-y-4">
  <div>
    <label className="block text-sm font-medium text-gray-700 mb-1">Brand name</label>
    <input
      placeholder="Elelem"
      value={brand}
      onChange={(e) => setBrand(e.target.value)}
      required
      className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
    />
  </div>

  <button
    type="submit"
    disabled={loading}
    className={`w-full py-2 px-4 rounded text-white font-semibold transition-colors ${
      loading ? "bg-gray-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
    }`}
  >
    {loading ? "Submitting..." : "Check Brand Visibility"}
  </button>

  {err && <p className="text-red-500 text-sm">{err}</p>}
</form>
  );
};

export default QueryForm;
