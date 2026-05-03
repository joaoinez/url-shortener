import type { ChangeEventHandler } from "react"
import GlassSurface from "#/ui/GlassSurface"
import { cn } from "#/utils/cn"

type Props = {
  protocol: string
  url: string
  handleOnChangeURL: ChangeEventHandler<HTMLInputElement>
  handleGenerateURL: () => void
  error: Error | null
}

export default function URLBar({
  protocol,
  url,
  handleOnChangeURL,
  handleGenerateURL,
  error,
}: Props) {
  return (
    <GlassSurface
      className={cn(
        "pl-4",
        Boolean(error) &&
          "outline-2 outline-red-500 drop-shadow-xl drop-shadow-red-500",
      )}
      height="100%"
      width="100%"
      borderRadius={50}
    >
      <span className="pr-1 font-bold text-white">{protocol}</span>
      <input
        autoFocus
        type="text"
        placeholder="Enter URL Here"
        name="url"
        className="h-full w-full bg-transparent py-3 text-white outline-none"
        value={url}
        onChange={handleOnChangeURL}
        onKeyDown={(e) => e.key === "Enter" && handleGenerateURL()}
      />
    </GlassSurface>
  )
}
