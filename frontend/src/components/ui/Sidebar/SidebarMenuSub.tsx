import { cn } from '@/lib/utils';
import * as React from 'react';

export const SidebarMenuSub = React.forwardRef<HTMLUListElement, React.ComponentProps<'ul'>>(
  ({ className, ...props }, ref) => (
    <ul
      ref={ref}
      data-sidebar="menu-sub"
      className={cn(
        'mx-3.5 flex min-w-0 translate-x-px flex-col gap-1 border-l border-sidebar-border px-2.5 py-0.5 group-data-[collapsible=icon]:hidden',
        className,
      )}
      {...props}
    />
  ),
);
SidebarMenuSub.displayName = 'SidebarMenuSub';

export const SidebarMenuSubItem = React.forwardRef<HTMLLIElement, React.ComponentProps<'li'>>(
  ({ ...props }, ref) => <li ref={ref} data-sidebar="menu-sub-item" {...props} />,
);
SidebarMenuSubItem.displayName = 'SidebarMenuSubItem';

export const SidebarMenuSubButton = React.forwardRef<HTMLAnchorElement, React.ComponentProps<'a'>>(
  ({ className, ...props }, ref) => (
    <a
      ref={ref}
      data-sidebar="menu-sub-button"
      className={cn(
        'flex h-7 min-w-0 -translate-x-px items-center gap-2 overflow-hidden rounded-md px-2 text-sidebar-foreground outline-none ring-sidebar-ring hover:bg-sidebar-accent hover:text-sidebar-accent-foreground focus-visible:ring-2 data-[active=true]:bg-sidebar-accent data-[active=true]:text-sidebar-accent-foreground disabled:pointer-events-none disabled:opacity-50 aria-disabled:pointer-events-none aria-disabled:opacity-50 [&>span:last-child]:truncate [&>svg]:size-4 [&>svg]:shrink-0 group-data-[collapsible=icon]:hidden',
        className,
      )}
      {...props}
    />
  ),
);
SidebarMenuSubButton.displayName = 'SidebarMenuSubButton';
