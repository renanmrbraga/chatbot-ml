import { cn } from '@/lib/utils';
import { NavigationMenu as Nav } from '@radix-ui/react-navigation-menu';
import * as React from 'react';

export const NavigationMenuList = React.forwardRef<
  React.ElementRef<typeof Nav.List>,
  React.ComponentPropsWithoutRef<typeof Nav.List>
>(({ className, ...props }, ref) => (
  <Nav.List
    ref={ref}
    className={cn('group flex flex-1 list-none items-center justify-center space-x-1', className)}
    {...props}
  />
));

NavigationMenuList.displayName = Nav.List.displayName;
