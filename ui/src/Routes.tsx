import {Route, Routes} from 'react-router-dom';
import {ProtectedRoute} from './ProtectedRoute';
import React from 'react';
// import {ChromeLogo} from './assets/images/googlechrome-logo';
// import {WallclockLogo} from './assets/images/wallclock-logo';
import {Sidebar} from './components/Sidebar/Sidebar';
import {Home} from './pages/Home';
import {Login} from './pages/Login';
import {LoginRedirect} from './pages/LoginRedirect';

export const Router: React.FC = () => {
  /*  const location = useLocation();
  const sidebarData = [
    {
      name: 'Browse',
      icon: ChromeLogo,
      isActive: location.pathname.startsWith('/sidebar'),
    },
    {
      name: 'Recent',
      icon: WallclockLogo,
      isActive: location.pathname.startsWith('/sidebar'),
    },
  ]; */
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
        {/* <Route path="/sidebar" element={<Sidebar rows={sidebarData} />} /> */}
        <Route path="/sidebar" element={<Sidebar />} />
      </Routes>
    </>
  );
};
