import React from 'react';
import ReactDOM from 'react-dom/client';
import {App} from './App';
import {BrowserRouter} from 'react-router-dom';
import './index.scss';
import {SWRConfig} from 'swr';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <SWRConfig>
        <App />
      </SWRConfig>
    </BrowserRouter>
  </React.StrictMode>
);
