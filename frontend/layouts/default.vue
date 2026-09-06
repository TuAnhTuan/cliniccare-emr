<script setup lang="ts">
const { practitioner, fetchPractitioner, logout } = useAuth()
const router = useRouter()

if (!practitioner.value) {
  await fetchPractitioner()
}

async function handleLogout() {
  await logout()
  await router.push('/login')
}
</script>

<template>
  <div class="app-shell">
    <header class="app-header">
      <div class="app-header__inner">
        <NuxtLink to="/consultations" class="app-brand">
          <span class="app-brand__icon">+</span>
          ClinicCare
        </NuxtLink>
        <nav class="app-nav">
          <NuxtLink to="/consultations" class="app-nav__link">Consultations</NuxtLink>
          <NuxtLink to="/consultations/new" class="app-nav__link">New Consultation</NuxtLink>
          <NuxtLink to="/consultations/search" class="app-nav__link">Search</NuxtLink>
        </nav>
        <div class="app-user">
          <span v-if="practitioner" class="app-user__name">{{ practitioner.full_name }}</span>
          <button type="button" class="app-user__logout" @click="handleLogout">Logout</button>
        </div>
      </div>
    </header>
    <main class="app-main">
      <slot />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100%;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
}

.app-header__inner {
  max-width: 960px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  gap: 24px;
}

.app-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: 700;
  color: var(--color-primary);
}

.app-brand__icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: var(--color-primary);
  color: white;
  font-size: 18px;
  line-height: 1;
}

.app-nav {
  display: flex;
  gap: 4px;
  flex: 1;
}

.app-nav__link {
  padding: 8px 14px;
  border-radius: 8px;
  color: var(--color-text-muted);
  font-weight: 500;
  font-size: 14px;
}

.app-nav__link:hover,
.app-nav__link.router-link-active {
  background: var(--color-primary-light);
  color: var(--color-primary-dark);
}

.app-user {
  display: flex;
  align-items: center;
  gap: 12px;
}

.app-user__name {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text);
}

.app-user__logout {
  padding: 6px 12px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  background: transparent;
  color: var(--color-text-muted);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
}

.app-user__logout:hover {
  background: var(--color-bg);
}

.app-main {
  flex: 1;
  max-width: 960px;
  width: 100%;
  margin: 0 auto;
  padding: 32px 24px;
}
</style>
