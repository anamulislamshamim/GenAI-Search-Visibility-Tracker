// src/pages/LoginPage.tsx
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthContext } from "../auth/AuthProvider";

const LoginPage: React.FC = () => {
  const { login } = useAuthContext();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const nav = useNavigate();

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr(null);
    setLoading(true);
    try {
      await login(username, password);
      nav("/", { replace: true });
    } catch (error: any) {
      setErr(error?.response?.data?.message ?? "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-lg p-8 space-y-6">
        <h2 className="text-3xl font-bold text-center text-gray-800">Sign In</h2>
        {err && <p className="text-red-500 text-sm text-center">{err}</p>}
        <form onSubmit={onSubmit} className="space-y-5">
          <div>
            <label className="block text-gray-700 font-medium mb-2">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-gray-700 font-medium mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className={`w-full py-3 rounded-lg text-white font-semibold transition-colors ${
              loading ? "bg-blue-300 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700"
            }`}
          >
            {loading ? "Signing in..." : "Sign In"}
          </button>
        </form>
        <p className="text-sm text-gray-500 text-center">
          Don't have an account? <span className="text-blue-600 hover:underline cursor-pointer">Sign Up</span>
        </p>
      </div>
    </div>
  );
};

export default LoginPage;



// // src/pages/LoginPage.tsx
// import React, { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { useAuthContext } from "../auth/AuthProvider";

// const LoginPage: React.FC = () => {
//   const { login } = useAuthContext();
//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");
//   const [err, setErr] = useState<string | null>(null);
//   const [loading, setLoading] = useState(false);
//   const nav = useNavigate();

//   const onSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();
//     setErr(null);
//     setLoading(true);
//     try {
//       await login(username, password);
//       nav("/", { replace: true });
//     } catch (error: any) {
//       setErr(error?.response?.data?.message ?? "Login failed");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="container">
//       <h2>Sign in</h2>
//       <form onSubmit={onSubmit}>
//         <div>
//           <label>Username</label>
//           <input value={username} onChange={(e) => setUsername(e.target.value)} required />
//         </div>
//         <div>
//           <label>Password</label>
//           <input value={password} onChange={(e) => setPassword(e.target.value)} type="password" required />
//         </div>
//         <button type="submit" disabled={loading}>{loading ? "Signing in..." : "Sign in"}</button>
//         {err && <p style={{ color: "red" }}>{err}</p>}
//       </form>
//     </div>
//   );
// };

// export default LoginPage;
