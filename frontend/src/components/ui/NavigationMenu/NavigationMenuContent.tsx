import { cn } from '@/lib/utils';
import { NavigationMenu as Nav } from '@radix-ui/react-navigation-menu';
import * as React from 'react';

export const NavigationMenuContent = React.forwardRef<
  React.ElementRef<typeof Nav.Content>,
  React.ComponentPropsWithoutRef<typeof Nav.Content>
>(({ className, ...props }, ref) => (
  <Nav.Content
    ref={ref}
    className={cn(
      'left-0 top-0 w-full data-[motion^=from-]:animate-in data-[motion^=to-]:animate-out data-[motion^=from-]:fade-in data-[motion^=to-]:fade-out data-[motion=from-end]:slide-in-from-right-52 data-[motion=from-start]:slide-in-from-left-52 data-[motion=to-end]:slide-out-to-right-52 data-[motion=to-start]:slide-out-to-left-52 md:absolute md:w-auto ',
      className,
    )}
    {...props}
  />
));

NavigationMenuContent.displayName = Nav.Content.displayName;
