import React, {createContext, useState} from 'react';

//@ts-ignore
const DarkModeContext = createContext();

function DarkModeProvider(props: any) {
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
