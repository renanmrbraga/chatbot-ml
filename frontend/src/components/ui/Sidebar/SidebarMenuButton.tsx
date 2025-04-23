import { Tooltip, TooltipContent, TooltipTrigger } from '@/components/ui/tooltip';
import { cn } from '@/lib/utils';
import { Slot } from '@radix-ui/react-slot';
import * as React from 'react';
import { useSidebar } from './SidebarContext';
import { sidebarMenuButtonVariants } from './sidebar-menu.styles';

export const SidebarMenuButton = React.forwardRef<
  HTMLButtonElement,
  React.ComponentProps<'button'> & {
    asChild?: boolean;
    isActive?: boolean;
    tooltip?: string | React.ComponentProps<typeof TooltipContent>;
  } & React.ComponentPropsWithoutRef<'button'> & // To pick up standard button props
    ReturnType<typeof sidebarMenuButtonVariants>
>(
  (
    {
      asChild = false,
      isActive = false,
      variant = 'default',
      size = 'default',
      tooltip,
      className,
      children,
      ...props
    },
    ref,
  ) => {
    const { isMobile, state } = useSidebar();
    const Comp = asChild ? Slot : 'button';
    const button = (
      <Comp
        ref={ref}
        data-sidebar="menu-button"
        data-size={size}
        data-active={isActive}
        className={cn(sidebarMenuButtonVariants({ variant, size }), className)}
        {...props}
      >
        {children}
      </Comp>
    );

    if (!tooltip) return button;
    const tl = typeof tooltip === 'string' ? { children: tooltip } : tooltip;

    return (
      <Tooltip>
        <TooltipTrigger asChild>{button}</TooltipTrigger>
        <TooltipContent
          side="right"
          align="center"
          hidden={state !== 'collapsed' || isMobile}
          {...tl}
        />
      </Tooltip>
    );
  },
);
SidebarMenuButton.displayName = 'SidebarMenuButton';

// MenuAction
export const SidebarMenuAction = React.forwardRef<
  HTMLButtonElement,
  React.ComponentProps<'button'> & { asChild?: boolean; showOnHover?: boolean }
>(({ asChild = false, showOnHover = false, className, children, ...props }, ref) => {
  const Comp = asChild ? Slot : 'button';
  return (
    <Comp
      ref={ref}
      data-sidebar="menu-action"
      className={cn(showOnHover && 'hidden', className)}
      {...props}
    >
      {children}
    </Comp>
  );
});
SidebarMenuAction.displayName = 'SidebarMenuAction';

// MenuBadge
export const SidebarMenuBadge = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, children, ...props }, ref) => (
  <div
    ref={ref}
    data-sidebar="menu-badge"
    className={cn(
      'absolute right-1 flex h-5 min-w-5 items-center justify-center rounded-md px-1 text-xs font-medium text-sidebar-foreground select-none pointer-events-none',
      className,
    )}
    {...props}
  >
    {children}
  </div>
));
SidebarMenuBadge.displayName = 'SidebarMenuBadge';

// MenuSkeleton
export const SidebarMenuSkeleton = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { showIcon?: boolean }
>(({ className, showIcon = false, ...props }, ref) => {
  const width = React.useMemo(() => `${Math.floor(Math.random() * 40) + 50}%`, []);
  return (
    <div
      ref={ref}
      data-sidebar="menu-skeleton"
      className={cn('rounded-md h-8 flex gap-2 px-2 items-center', className)}
      {...props}
    >
      {showIcon && <div className="size-4 rounded-md bg-gray-200 animate-pulse" />}
      <div
        style={{ '--skeleton-width': width } as React.CSSProperties}
        className="h-4 flex-1 max-w-[--skeleton-width] bg-gray-200 animate-pulse"
      />
    </div>
  );
});
SidebarMenuSkeleton.displayName = 'SidebarMenuSkeleton';
