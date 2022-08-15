import styles from './styles.module.scss';
import {useForm} from 'react-hook-form';
import {zodResolver} from '@hookform/resolvers/zod';
import * as z from 'zod';
import {Input} from '../FormComponents/Input';
import {Button} from '../Button';
import {Textarea} from '../FormComponents/Textarea';
import {useContext} from 'react';
import {DarkModeContext} from '../Contexts/DarkModeContext';

const mobileNumberRegex = /[0-9]{10}/;

const schema = z.object({
  mobileNumber: z.string().regex(mobileNumberRegex, 'Must be 10 digits'),
  address: z.string(),
  bio: z.string(),
  linkedIn: z.string(),
});

type Schema = z.infer<typeof schema>;

const initialValues = {
  mobileNumber: '',
  address: '',
  bio: '',
  linkedIn: '',
};

export const ProfileCard: React.FC = () => {
  const {control, handleSubmit, reset} = useForm<Schema>({
    resolver: zodResolver(schema),
    defaultValues: initialValues,
  });
  const onSubmit = (data: Schema) => {
    reset();
    // eslint-disable-next-line no-console
    console.log(data);
  };

  //@ts-ignore
  const {darkMode} = useContext(DarkModeContext);

  return (
    <div
      className={
        darkMode ? styles.cardContainer : styles.cardContainer_dark_theme
      }
    >
      <div
        className={
          darkMode ? styles.leftContainer : styles.leftContainer_dark_theme
        }
      >
        <img
          src="https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png"
          alt="profile-img"
        />
      </div>
      <form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
        <Input control={control} label="Contact Number" name="mobileNumber" />
        <Input control={control} label="Address" name="address" />
        <Textarea
          control={control}
          {...{style: {height: '10vh'}}}
          label="Bio"
          name="bio"
        />
        <Input control={control} label="LinkedIn" name="linkedIn" />
        <div className={styles.paddingForBtn}></div>
        <Button className={styles.submitBtn} {...{type: 'submit'}}>
          Save
        </Button>
      </form>
    </div>
  );
};
