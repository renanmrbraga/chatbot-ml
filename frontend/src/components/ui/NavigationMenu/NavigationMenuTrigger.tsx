import { cn } from '@/lib/utils';
import { NavigationMenu as Nav } from '@radix-ui/react-navigation-menu';
import { ChevronDown } from 'lucide-react';
import * as React from 'react';
import { navigationMenuTriggerStyle } from './navigation-menu.styles';

export const NavigationMenuTrigger = React.forwardRef<
  React.ElementRef<typeof Nav.Trigger>,
  React.ComponentPropsWithoutRef<typeof Nav.Trigger>
>(({ className, children, ...props }, ref) => (
  <Nav.Trigger
    ref={ref}
    className={cn(navigationMenuTriggerStyle(), 'group', className)}
    {...props}
  >
    {children}
    <ChevronDown
      className="relative top-[1px] ml-1 h-3 w-3 transition duration-200 group-data-[state=open]:rotate-180"
      aria-hidden="true"
    />
  </Nav.Trigger>
));

NavigationMenuTrigger.displayName = Nav.Trigger.displayName;
