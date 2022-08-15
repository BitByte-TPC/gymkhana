import {Router} from './Routes';
import 'react-toastify/dist/ReactToastify.css';
import {DarkModeProvider} from './components/Contexts/DarkModeContext';

export function App() {
  return (
    <DarkModeProvider>
      <Router />
    </DarkModeProvider>
  );
}
