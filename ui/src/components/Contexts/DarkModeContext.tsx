import React, {createContext, useState} from 'react';

const initialState = {
  darkMode: false,
  toggleDarkMode: () => {},
};

export interface DarkModeProps {
  children: React.ReactNode;
}

const DarkModeContext = createContext(initialState);

function DarkModeProvider(props: DarkModeProps) {
  const [darkMode, setDarkMode] = useState(false);
  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };
  return (
    <div>
      <DarkModeContext.Provider value={{darkMode, toggleDarkMode}}>
        {props.children}
      </DarkModeContext.Provider>
    </div>
  );
}

export {DarkModeContext, DarkModeProvider};
