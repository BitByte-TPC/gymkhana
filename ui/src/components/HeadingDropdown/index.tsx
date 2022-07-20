import Select from 'react-select';

interface OptionType {
  value: string;
  label: string;
}

interface HeadingDropdownProps {
  options: OptionType[];
  selectedOption: OptionType;
  setSelectedOption: React.Dispatch<React.SetStateAction<OptionType>>;
}

export const HeadingDropdown: React.FC<HeadingDropdownProps> = ({
  options,
  selectedOption,
  setSelectedOption,
}) => {
  return (
    <Select
      defaultValue={selectedOption}
      // eslint-disable-next-line @typescript-eslint/ban-ts-comment
      // @ts-ignore
      onChange={setSelectedOption}
      options={options}
      isSearchable={false}
      className="dropdown-container"
      classNamePrefix="dropdown"
    />
  );
};
