import {Navigate} from 'react-router-dom';
import {isTokenValid} from './utils/token';

interface ProtectedRouteInterface {
  children: JSX.Element;
}

export const ProtectedRoute: React.FC<ProtectedRouteInterface> = ({
  children,
}) => {
  const isUserAuthenticated = isTokenValid();
  return isUserAuthenticated ? children : <Navigate to="/login" replace />;
};
