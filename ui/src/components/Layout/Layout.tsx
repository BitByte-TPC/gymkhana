import classNames from 'classnames';
import {useState, useRef, useEffect} from 'react';
import {Sidebar} from '../../components/Sidebar/Sidebar';
import {TopBar} from '../../components/TopBar';
import styles from './styles.module.scss';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = props => {
  const sidebarRef = useRef<HTMLDivElement>(null);
  const [isSidebarOpenOnMobile, setIsSidebarOpenOnMobile] = useState(false);
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        sidebarRef.current &&
        !sidebarRef.current.contains(event.target as Node)
      ) {
        setIsSidebarOpenOnMobile(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  });
  return (
    <div className={styles.container}>
      <div
        ref={sidebarRef}
        className={classNames(styles.sidebarContainer, {
          [styles.openSidebar]: isSidebarOpenOnMobile,
        })}
      >
        <Sidebar />
      </div>
      <div
        className={classNames(styles.mainContent, {
          [styles.mainContentBlur]: isSidebarOpenOnMobile,
        })}
      >
        <TopBar setSidebarVisibility={setIsSidebarOpenOnMobile} />
        <div>{props.children}</div>
      </div>
    </div>
  );
};
