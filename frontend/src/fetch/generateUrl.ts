export const API_BASE_URL = "http://localhost:8000/api"

interface ApiError extends Error {
  status: number
}

type GenerateURLResponse = {
  token: string
}

export const generateURL = async (url: string) => {
  const response = await fetch(`${API_BASE_URL}/url`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url }),
  })

  if (response.ok) return response.json() as Promise<GenerateURLResponse>

  const error = new Error(await response.text()) as ApiError

  error.status = response.status

  throw error
}
