export function useApi() {
  const config = useRuntimeConfig()

  function get<T>(path: string, params?: Record<string, string>) {
    return $fetch<T>(path, { baseURL: config.public.apiBase, params })
  }

  function post<T>(path: string, body: object) {
    return $fetch<T>(path, { baseURL: config.public.apiBase, method: 'POST', body })
  }

  return { get, post }
}
