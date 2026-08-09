import React, { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem("fv_token"));

  const login = (newToken) => {
    localStorage.setItem("fv_token", newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem("fv_token");
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ token, login, logout, isAdmin: !!token }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
