// src/components/ui/Command/CommandItem.tsx
import { cn } from '@/lib/utils';
import { Command as CommandPrimitive } from 'cmdk';
import * as React from 'react';

export const CommandItem = React.forwardRef<
  React.ElementRef<typeof CommandPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof CommandPrimitive.Item>
>(({ className, ...props }, ref) => (
  <CommandPrimitive.Item
    ref={ref}
    className={cn(
      `relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none
       data-[disabled=true]:pointer-events-none data-[selected=true]:bg-accent
       data-[selected=true]:text-accent-foreground data-[disabled=true]:opacity-50`,
      className,
    )}
    {...props}
  />
));
CommandItem.displayName = CommandPrimitive.Item.displayName;

export const CommandShortcut = ({ className, ...props }: React.HTMLAttributes<HTMLSpanElement>) => {
  return (
    <span
      className={cn('ml-auto text-xs tracking-widest text-muted-foreground', className)}
      {...props}
    />
  );
};
CommandShortcut.displayName = 'CommandShortcut';
