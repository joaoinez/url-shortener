import { useMutation } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { useEffect, useState } from "react"
import type { ChangeEventHandler } from "react"
import { cn } from "#/utils/cn"
import { API_BASE_URL, generateURL } from "#/fetch/generateUrl"

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
    generateURLMutation.mutate(`${protocol}${url}`)

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
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-900">
      <h1 className="mb-8 text-3xl text-white">URL Shortener</h1>

      <div
        className={cn(
          "flex w-1/2 max-w-5xl items-center rounded-full bg-gray-50 pl-4",
          generateURLMutation.error && "outline-2 outline-red-500",
        )}
      >
        <span className="pr-1 text-neutral-500">{protocol}</span>
        <input
          autoFocus
          type="text"
          placeholder="Enter URL Here"
          name="url"
          className="h-full w-full bg-transparent py-3 outline-none"
          value={url}
          onChange={handleOnChangeURL}
          onKeyDown={(e) => e.key === "Enter" && handleGenerateURL()}
        />
        <button
          className={cn(
            "translate-x-px cursor-pointer rounded-full bg-amber-500 px-4 py-3 text-white",
            (!url ||
              generateURLMutation.isPending ||
              Boolean(generateURLMutation.error)) &&
              "cursor-default bg-neutral-200",
          )}
          onClick={handleGenerateURL}
          disabled={
            !url ||
            generateURLMutation.isPending ||
            Boolean(generateURLMutation.error)
          }
        >
          Shorten
        </button>
      </div>

      {generateURLMutation.isSuccess && (
        <a
          href={`${API_BASE_URL.replace("/api", "")}/${generateURLMutation.data.token}`}
          className="mt-4 text-white"
        >{`${API_BASE_URL.replace("/api", "")}/${generateURLMutation.data.token}`}</a>
      )}
    </main>
  )
}
