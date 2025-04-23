import * as React from 'react';
import { FieldPath, FieldValues } from 'react-hook-form';

export type FormFieldContextValue<
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>,
> = { name: TName };

export const FormFieldContext = React.createContext<FormFieldContextValue>(
  {} as FormFieldContextValue,
);

export const useFormFieldContext = <
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>,
>(): FormFieldContextValue<TFieldValues, TName> => {
  const context = React.useContext(FormFieldContext) as FormFieldContextValue<TFieldValues, TName>;
  if (!context) {
    throw new Error('useFormFieldContext must be used within a FormFieldContext.Provider');
  }
  return context;
};
