import { useMutation } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { useEffect, useState } from "react"
import type { ChangeEventHandler } from "react"
import { generateURL } from "#/fetch/generateUrl"
import { API_BASE_URL } from "#/constants"
import ColorBends from "#/ui/ColorBends"
import GlassButton from "#/ui/GlassButton"
import ShortURL from "#/components/ShortURL"
import URLBar from "#/components/URLBar"

export const Route = createFileRoute("/")({ component: Home })

const protocolRegex = /^[a-zA-Z][a-zA-Z0-9+.-]*:\/\//
const initialProtocol = "https://"

function Home() {
  const [protocol, setProtocol] = useState(initialProtocol)
  const [url, setURL] = useState("")

  const generateURLMutation = useMutation({
    mutationFn: generateURL,
  })

  const handleOnChangeURL: ChangeEventHandler<HTMLInputElement> = (e) => {
    if (generateURLMutation.error) generateURLMutation.reset()

    const strippedProtocol = e.currentTarget.value.match(protocolRegex)?.[0]

    if (strippedProtocol && strippedProtocol !== protocol)
      setProtocol(strippedProtocol)

    setURL(e.currentTarget.value.replace(protocolRegex, ""))
  }

  const handleGenerateURL = () =>
    generateURLMutation.mutate(`${protocol}${url.trim()}`)

  useEffect(() => {
    navigator.clipboard.readText().then((clipText) => {
      const strippedProtocol = clipText.match(protocolRegex)?.[0]

      if (strippedProtocol) {
        if (strippedProtocol !== initialProtocol) setProtocol(strippedProtocol)

        setURL(clipText.replace(protocolRegex, ""))
      }
    })
  }, [])

  return (
    <main className="relative flex min-h-screen flex-col items-center justify-center bg-gray-900">
      <div className="absolute inset-0 z-0">
        <ColorBends
          colors={["#ff5c7a", "#8a5cff"]}
          rotation={90}
          speed={0.2}
          scale={1}
          frequency={1}
          warpStrength={1}
          mouseInfluence={1}
          noise={0.2}
          parallax={0.5}
          iterations={1}
          intensity={1}
          bandWidth={6}
          transparent
          autoRotate={0}
        />
      </div>

      <div className="relative flex w-1/2 max-w-5xl gap-4">
        {generateURLMutation.isSuccess && (
          <ShortURL token={generateURLMutation.data.token} />
        )}

        <URLBar
          protocol={protocol}
          url={url}
          handleOnChangeURL={handleOnChangeURL}
          handleGenerateURL={handleGenerateURL}
          error={generateURLMutation.error}
        />

        <GlassButton
          label="Shorten"
          onClick={handleGenerateURL}
          loading={generateURLMutation.isPending}
          disabled={
            !url ||
            generateURLMutation.isPending ||
            Boolean(generateURLMutation.error)
          }
        />
      </div>
    </main>
  )
}
