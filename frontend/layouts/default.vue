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
  justify-content: space-between;
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

.app-main {
  flex: 1;
  max-width: 960px;
  width: 100%;
  margin: 0 auto;
  padding: 32px 24px;
}
</style>
