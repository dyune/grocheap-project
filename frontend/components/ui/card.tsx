import * as React from "react";

import { cn } from "@/lib/utils";

export type CardProps = React.HTMLAttributes<HTMLDivElement>;

export const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "rounded-lg border px-6 py-4 shadow-md",
        "bg-card text-foreground border-card-border", // Dark gray card with amber border
        className
      )}
      {...props}
    />
  )
);
Card.displayName = "Card";

export const CardHeader = ({ className, ...props }: CardProps) => (
  <div className={`border-b pb-4 ${className}`} {...props} />
);

export const CardTitle = ({ className, ...props }: CardProps) => (
  <h2 className={`text-xl font-semibold ${className}`} {...props} />
);

export const CardContent = ({ className, ...props }: CardProps) => (
  <div className={`mt-2 ${className}`} {...props} />
);
