import React, { createContext, useContext, useState, useEffect } from "react";
import api from "../api/apiClient.ts"; // FIX: Added '.ts' extension to resolve path error

type AuthContextType = {
  isAuthenticated: boolean;
  // Renamed argument for clarity: username -> email
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

  useEffect(() => {
    // We skip automatic verification for now.
  }, []);

  // Updated function signature: username -> email
  const login = async (email: string, password: string) => {
    // FIX: The payload key is changed from 'username' to 'email' 
    // to match the FastAPI Pydantic model.
    await api.post("/auth/login", { email, password }); 
    setIsAuthenticated(true);
  };

  const logout = async () => {
    try {
      await api.post("/auth/logout"); // optional: if backend supports logout
    } catch (e) { /* ignore */ }
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuthContext = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuthContext must be used within AuthProvider");
  return ctx;
};