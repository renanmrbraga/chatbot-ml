import * as React from 'react';

type FormItemContextValue = { id: string };

export const FormItemContext = React.createContext<FormItemContextValue>(
  {} as FormItemContextValue,
);

export const useFormItemContext = (): FormItemContextValue => {
  const context = React.useContext(FormItemContext);
  if (!context) {
    throw new Error('useFormItemContext must be used within a FormItemContext.Provider');
  }
  return context;
};
