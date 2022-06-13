import {Route, Routes} from 'react-router-dom';
import {ProtectedRoute} from './ProtectedRoute';
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
      </Routes>
    </>
  );
};
