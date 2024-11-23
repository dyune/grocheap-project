import * as React from "react";
import { cn } from "@/lib/utils";

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement>;

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, ...props }, ref) => (
    <button
      ref={ref}
      className={cn(
        "inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2",
        "bg-button text-black hover:bg-button-hover focus:ring-button focus:ring-offset-black", // Black and amber
        className
      )}
      {...props}
    />
  )
);
Button.displayName = "Button";
