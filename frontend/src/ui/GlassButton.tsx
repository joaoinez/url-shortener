import { LoaderCircle } from "lucide-react"
import { cn } from "../utils/cn"
import GlassSurface from "./GlassSurface"
import type { ComponentPropsWithoutRef } from "react"

type Props = Omit<ComponentPropsWithoutRef<"button">, "children"> & {
  label: string
  loading?: boolean
}

export default function GlassButton({
  label,
  className,
  disabled,
  loading,
  ...props
}: Props) {
  return (
    <button
      className={cn(
        "group relative",
        disabled ? "cursor-not-allowed" : "cursor-pointer",
        className,
      )}
      disabled={disabled}
      {...props}
    >
      <div
        className={cn(
          "absolute inset-0",
          !disabled &&
            "scale-100 transition-all duration-200 group-hover:scale-110 group-active:scale-95",
        )}
      >
        <GlassSurface height="100%" width="100%" borderRadius={50} />
      </div>
      <span className="relative z-10 flex h-full w-full items-center justify-center px-4 py-2 font-bold text-white">
        {loading ? <LoaderCircle className="animate-spin" /> : label}
      </span>
    </button>
  )
}
