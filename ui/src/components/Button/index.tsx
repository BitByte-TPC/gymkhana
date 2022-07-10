import {ReactNode} from 'react';
import styles from './styles.module.css';

interface ButtonProps {
  className?: string;
  children: ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  className,
  ...props
}) => {
  return (
    <button className={`${className} ${styles.button}`} {...props}>
      {children}
    </button>
  );
};
