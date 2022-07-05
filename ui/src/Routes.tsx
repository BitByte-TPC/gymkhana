import {Route, Routes} from 'react-router-dom';
import {ProtectedRoute} from './ProtectedRoute';
import React from 'react';
import {Sidebar} from './components/Sidebar/Sidebar';
import {Home} from './pages/Home';
import {Login} from './pages/Login';
import {LoginRedirect} from './pages/LoginRedirect';

export const Router: React.FC = () => {
  return (
    <>
      <Routes>
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
        <Route path="/login" element={<Login />} />
        <Route path="/login/redirect" element={<LoginRedirect />} />
        <Route path="/homepage" element={<Sidebar />} />
      </Routes>
    </>
  );
};
