import { cn } from '@/lib/utils';
import { NavigationMenu as Nav } from '@radix-ui/react-navigation-menu';
import * as React from 'react';

export const NavigationMenuViewport = React.forwardRef<
  React.ElementRef<typeof Nav.Viewport>,
  React.ComponentPropsWithoutRef<typeof Nav.Viewport>
>(({ className, ...props }, ref) => (
  <div className={cn('absolute left-0 top-full flex justify-center')}>
    <Nav.Viewport
      ref={ref}
      className={cn(
        'origin-top-center relative mt-1.5 h-[var(--radix-navigation-menu-viewport-height)] w-full overflow-hidden rounded-md border bg-popover text-popover-foreground shadow-lg data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-90 md:w-[var(--radix-navigation-menu-viewport-width)]',
        className,
      )}
      {...props}
    />
  </div>
));

NavigationMenuViewport.displayName = Nav.Viewport.displayName;
