import {Route, Routes} from 'react-router-dom';
import Homepage from './pages/Homepage';
import Login from './pages/Login';

const Router: React.FC = () => {
  return (
    <>
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </>
  );
};

export default Router;
