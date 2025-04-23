import { cn } from '@/lib/utils';
import { NavigationMenu as Nav } from '@radix-ui/react-navigation-menu';
import * as React from 'react';

export const NavigationMenuIndicator = React.forwardRef<
  React.ElementRef<typeof Nav.Indicator>,
  React.ComponentPropsWithoutRef<typeof Nav.Indicator>
>(({ className, ...props }, ref) => (
  <Nav.Indicator
    ref={ref}
    className={cn(
      'top-full z-[1] flex h-1.5 items-end justify-center overflow-hidden data-[state=visible]:animate-in data-[state=hidden]:animate-out data-[state=hidden]:fade-out data-[state=visible]:fade-in',
      className,
    )}
    {...props}
  >
    <div className="relative top-[60%] h-2 w-2 rotate-45 rounded-tl-sm bg-border shadow-md" />
  </Nav.Indicator>
));

NavigationMenuIndicator.displayName = Nav.Indicator.displayName;
