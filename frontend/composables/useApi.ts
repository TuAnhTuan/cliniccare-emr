// Shared across calls so multiple requests failing at once trigger only one
// refresh call instead of a stampede of concurrent /auth/refresh requests.
let refreshPromise: Promise<void> | null = null

export function useApi() {
  const config = useRuntimeConfig()
  const { accessToken, refreshToken, refreshAccessToken, logout } = useAuth()
  const router = useRouter()

  function authHeaders(): Record<string, string> {
    return accessToken.value ? { Authorization: `Bearer ${accessToken.value}` } : {}
  }

  async function ensureFreshToken() {
    if (!refreshPromise) {
      refreshPromise = refreshAccessToken().finally(() => {
        refreshPromise = null
      })
    }
    return refreshPromise
  }

  async function redirectToLogin() {
    await logout()
    await router.push('/login')
  }

  async function request<T>(path: string, opts: Record<string, unknown>): Promise<T> {
    try {
      return await $fetch<T>(path, { baseURL: config.public.apiBase, ...opts, headers: authHeaders() })
    } catch (err: any) {
      const status = err?.response?.status ?? err?.statusCode

      if (status !== 401) {
        throw err
      }

      if (!refreshToken.value) {
        await redirectToLogin()
        throw err
      }

      try {
        await ensureFreshToken()
      } catch {
        await redirectToLogin()
        throw err
      }

      // Retry exactly once with the freshly refreshed access token.
      return await $fetch<T>(path, { baseURL: config.public.apiBase, ...opts, headers: authHeaders() })
    }
  }

  function get<T>(path: string, params?: Record<string, string>) {
    return request<T>(path, { params })
  }

  function post<T>(path: string, body: object) {
    return request<T>(path, { method: 'POST', body })
  }

  return { get, post }
}
