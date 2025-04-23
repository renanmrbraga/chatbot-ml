import { Controller, ControllerProps } from 'react-hook-form';
import { FormFieldContext } from './FormFieldContext';

export const FormField = <TFieldValues, TName extends keyof TFieldValues>(
  props: ControllerProps<TFieldValues, TName>,
) => (
  <FormFieldContext.Provider value={{ name: props.name }}>
    <Controller {...props} />
  </FormFieldContext.Provider>
);
FormField.displayName = 'FormField';
