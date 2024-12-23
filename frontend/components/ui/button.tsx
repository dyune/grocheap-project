import * as React from "react";
import { cn } from "@/lib/utils";
import { FaSearch } from "react-icons/fa";

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement>;

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ icon, text, className, ...props}, ref) => (
      <button
          ref={ref}
          className={cn(
              "inline-flex items-center justify-center rounded-md px-4 py-2 text-sm font-medium shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2",
              "bg-button text-black hover:bg-button-hover focus:ring-button focus:ring-offset-black", // Black and amber
              className
          )}
          {...props}
      >
          <span
              className="inline-flex h-full w-full cursor-pointer items-center justify-center rounded-lg px-7 gap-2">
              {icon}
              {text}
            </span>
      </button>
  )
);
Button.displayName = "Button";
