import { CopyIcon, CheckIcon } from "lucide-react"
import { useState } from "react"

import { API_BASE_URL } from "#/constants"

type Props = {
  token: string
}
export default function ShortURL({ token }: Props) {
  const shortURL = `${API_BASE_URL.replace("/api", "")}/${token}`

  const [copied, setCopied] = useState(false)

  const handleCopyURLToClipboard = () => {
    navigator.clipboard.writeText(shortURL)

    setCopied(true)

    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="animate-slide-up absolute top-0 left-1/2 -translate-x-1/2">
      <div className="relative">
        <a href={shortURL} className="text-lg text-white underline">
          {shortURL}
        </a>
        <button
          className="absolute top-1/2 -right-2 translate-x-full -translate-y-1/2 cursor-pointer"
          onClick={handleCopyURLToClipboard}
        >
          {copied ? (
            <CheckIcon className="text-white" size={20} />
          ) : (
            <CopyIcon className="text-white" size={20} />
          )}
        </button>
      </div>
    </div>
  )
}
