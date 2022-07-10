import {
  Controller,
  FieldError,
  FieldValues,
  UseControllerProps,
} from 'react-hook-form';
import styles from './styles.module.scss';

interface Props<T> extends UseControllerProps<T> {
  label: string;
  error?: FieldError;
}

export const Input = <T extends FieldValues>({
  name,
  label,
  control,
  ...props
}: Props<T>) => {
  return (
    <Controller
      name={name}
      control={control}
      render={({field, fieldState: {error}}) => (
        <div className={styles.inputContainer}>
          <label className={styles.label}>{label}</label>
          <input className={styles.input} {...field} {...props} />
          {error && <span className={styles.error}>{error.message}</span>}
        </div>
      )}
    ></Controller>
  );
};
