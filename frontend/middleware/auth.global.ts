export default defineNuxtRouteMiddleware((to) => {
  if (to.path === '/login') return

  // refresh_token is the long-lived credential — if it's gone, there's no way
  // to silently recover a session even if a (possibly expired) access_token
  // cookie still lingers.
  const refreshToken = useCookie<string | null>('refresh_token')
  if (!refreshToken.value) {
    return navigateTo('/login')
  }
})
