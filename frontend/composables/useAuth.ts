interface Practitioner {
  id: number
  full_name: string
  email: string
  role: string
}

export function useAuth() {
  const accessToken = useCookie<string | null>('access_token', { default: () => null, sameSite: 'lax' })
  const refreshToken = useCookie<string | null>('refresh_token', { default: () => null, sameSite: 'lax' })
  const practitioner = useState<Practitioner | null>('practitioner', () => null)
  const config = useRuntimeConfig()

  function setTokens(access: string, refresh: string) {
    accessToken.value = access
    refreshToken.value = refresh
  }

  function clearTokens() {
    accessToken.value = null
    refreshToken.value = null
    practitioner.value = null
  }

  async function login(email: string, password: string) {
    const res = await $fetch<{ access_token: string; refresh_token: string }>('/auth/login', {
      baseURL: config.public.apiBase,
      method: 'POST',
      body: { email, password },
    })
    setTokens(res.access_token, res.refresh_token)
    await fetchPractitioner()
  }

  async function refreshAccessToken() {
    if (!refreshToken.value) {
      throw new Error('No refresh token available')
    }
    const res = await $fetch<{ access_token: string; refresh_token: string }>('/auth/refresh', {
      baseURL: config.public.apiBase,
      method: 'POST',
      body: { refresh_token: refreshToken.value },
    })
    setTokens(res.access_token, res.refresh_token)
  }

  async function fetchPractitioner() {
    if (!accessToken.value) {
      practitioner.value = null
      return
    }
    try {
      practitioner.value = await $fetch<Practitioner>('/auth/me', {
        baseURL: config.public.apiBase,
        headers: { Authorization: `Bearer ${accessToken.value}` },
      })
    } catch {
      clearTokens()
    }
  }

  async function logout() {
    const currentRefreshToken = refreshToken.value
    clearTokens()
    if (currentRefreshToken) {
      try {
        await $fetch('/auth/logout', {
          baseURL: config.public.apiBase,
          method: 'POST',
          body: { refresh_token: currentRefreshToken },
        })
      } catch {
        // Best-effort server-side revoke; client tokens are already cleared either way.
      }
    }
  }

  const isAuthenticated = computed(() => !!accessToken.value)

  return {
    accessToken,
    refreshToken,
    practitioner,
    login,
    logout,
    fetchPractitioner,
    refreshAccessToken,
    isAuthenticated,
  }
}
