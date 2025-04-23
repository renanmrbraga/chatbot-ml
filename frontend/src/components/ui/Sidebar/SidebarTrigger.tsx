import { Button } from '@/components/ui/Button';
import { cn } from '@/lib/utils';
import { PanelLeft } from 'lucide-react';
import * as React from 'react';
import { useSidebar } from './SidebarContext';

export const SidebarTrigger = React.forwardRef</*…*/>((props, ref) => {
  const { toggleSidebar } = useSidebar();
  return (
    <Button
      ref={ref}
      onClick={(e) => {
        props.onClick?.(e);
        toggleSidebar();
      }}
      variant="ghost"
      size="icon"
      className={cn('h-7 w-7', props.className)}
      {...props}
    >
      <PanelLeft />
      <span className="sr-only">Toggle Sidebar</span>
    </Button>
  );
});
SidebarTrigger.displayName = 'SidebarTrigger';
