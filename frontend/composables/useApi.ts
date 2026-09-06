export function useApi() {
  const config = useRuntimeConfig()

  function get<T>(path: string, params?: Record<string, string>) {
    return $fetch<T>(path, { baseURL: config.public.apiBase, params })
  }

  return { get }
}
