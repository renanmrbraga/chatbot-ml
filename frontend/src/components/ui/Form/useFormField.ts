import { useFormContext } from 'react-hook-form';
import { useFormFieldContext } from './FormField';
import { useFormItemContext } from './FormItem';

export const useFormField = () => {
  const fieldContext = useFormFieldContext();
  const itemContext = useFormItemContext();
  const { getFieldState, formState } = useFormContext();

  if (!fieldContext) {
    throw new Error('useFormField should be used within <FormField>');
  }

  const fieldState = getFieldState(fieldContext.name, formState);
  const { id } = itemContext;

  return {
    id,
    name: fieldContext.name,
    formItemId: `${id}-form-item`,
    formDescriptionId: `${id}-form-item-description`,
    formMessageId: `${id}-form-item-message`,
    ...fieldState,
  };
};
