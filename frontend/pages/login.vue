<script setup lang="ts">
definePageMeta({ layout: 'blank' })

const { login } = useAuth()
const router = useRouter()

const email = ref('')
const password = ref('')
const submitting = ref(false)
const errorMessage = ref('')

async function submit() {
  errorMessage.value = ''
  submitting.value = true
  try {
    await login(email.value.trim(), password.value)
    await router.push('/consultations')
  } catch (err: any) {
    errorMessage.value = err?.data?.detail || 'Invalid email or password.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <form class="card login-form" @submit.prevent="submit">
      <div class="login-brand">
        <span class="login-brand__icon">+</span>
        ClinicCare
      </div>
      <p class="login-subtitle">Sign in to manage patient consultations</p>

      <p v-if="errorMessage" class="form-error">{{ errorMessage }}</p>

      <label class="field">
        <span class="field__label">Email</span>
        <input v-model="email" type="email" class="input" placeholder="doctor@cliniccare.sg" required />
      </label>

      <label class="field">
        <span class="field__label">Password</span>
        <input v-model="password" type="password" class="input" placeholder="••••••••" required />
      </label>

      <button type="submit" class="button button--primary" :disabled="submitting">
        {{ submitting ? 'Signing in…' : 'Sign in' }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

.login-form {
  padding: 32px;
  width: 100%;
  max-width: 360px;
}

.login-brand {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 22px;
  font-weight: 700;
  color: var(--color-primary);
  margin-bottom: 4px;
}

.login-brand__icon {
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

.login-subtitle {
  text-align: center;
  color: var(--color-text-muted);
  font-size: 13px;
  margin: 0 0 24px;
}

.form-error {
  background: #fef2f2;
  color: #b91c1c;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 13px;
  margin: 0 0 16px;
}

.field {
  display: block;
  margin-bottom: 16px;
}

.field__label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 6px;
}

.input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
}

.input:focus {
  outline: none;
  border-color: var(--color-primary);
}

.button {
  width: 100%;
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  border: 1px solid transparent;
  cursor: pointer;
  margin-top: 8px;
}

.button--primary {
  background: var(--color-primary);
  color: white;
}

.button--primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
