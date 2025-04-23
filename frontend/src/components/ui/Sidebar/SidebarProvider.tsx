// src/components/ui/Sidebar/SidebarProvider.tsx
import { TooltipProvider } from '@/components/ui/tooltip';
import { useIsMobile } from '@/hooks/use‑mobile';
import * as React from 'react';
import { SidebarContext, SidebarContextValue } from './SidebarContext';

type SidebarProviderProps = React.ComponentPropsWithoutRef<'div'> & {
  defaultOpen?: boolean;
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
};

export const SidebarProvider = React.forwardRef<HTMLDivElement, SidebarProviderProps>(
  function SidebarProvider(
    { defaultOpen = true, open: openProp, onOpenChange, children, ...divProps },
    ref,
  ) {
    const isMobile = useIsMobile();
    const [openMobile, setOpenMobile] = React.useState(false);
    const [internalOpen, setInternalOpen] = React.useState(defaultOpen);
    const open = openProp ?? internalOpen;

    const setOpen = React.useCallback(
      (v: boolean) => {
        if (onOpenChange) {
          onOpenChange(v);
        } else {
          setInternalOpen(v);
        }
        document.cookie = `sidebar:state=${v};max-age=${60 * 60 * 24 * 7};path=/`;
      },
      [onOpenChange],
    );

    const toggleSidebar = React.useCallback(
      () => (isMobile ? setOpenMobile((o) => !o) : setOpen((o) => !o)),
      [isMobile, setOpen],
    );

    React.useEffect(() => {
      const onKey = (e: KeyboardEvent) => {
        if ((e.metaKey || e.ctrlKey) && e.key === 'b') {
          e.preventDefault();
          toggleSidebar();
        }
      };
      window.addEventListener('keydown', onKey);
      return () => window.removeEventListener('keydown', onKey);
    }, [toggleSidebar]);

    const state = open ? 'expanded' : 'collapsed';

    const value: SidebarContextValue = React.useMemo(
      () => ({
        state,
        open,
        setOpen,
        isMobile,
        openMobile,
        setOpenMobile,
        toggleSidebar,
      }),
      [state, open, setOpen, isMobile, openMobile, toggleSidebar],
    );

    return (
      <SidebarContext.Provider value={value}>
        <TooltipProvider delayDuration={0}>
          <div ref={ref} {...divProps}>
            {children}
          </div>
        </TooltipProvider>
      </SidebarContext.Provider>
    );
  },
);

SidebarProvider.displayName = 'SidebarProvider';
