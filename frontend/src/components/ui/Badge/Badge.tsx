import { cn } from '@/lib/utils';
import * as React from 'react';
import { badgeVariants } from './badge.styles';

import type { VariantProps } from 'class-variance-authority';

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

export function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />;
}
