<script setup lang="ts">
import type { Consultation } from '~/types'

const { get } = useApi()

const patient = ref('')
const diagnosisCode = ref('')
const hasSearched = ref(false)
const pending = ref(false)
const error = ref(false)
const results = ref<Consultation[]>([])

async function search() {
  pending.value = true
  error.value = false
  hasSearched.value = true
  try {
    const params: Record<string, string> = {}
    if (patient.value.trim()) params.patient = patient.value.trim()
    if (diagnosisCode.value.trim()) params.diagnosis_code = diagnosisCode.value.trim()
    results.value = await get<Consultation[]>('/consultation', params)
  } catch {
    error.value = true
  } finally {
    pending.value = false
  }
}
</script>

<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">Search consultations</h1>
      <p class="page-subtitle">Find past notes by patient name or ICD-10 diagnosis code</p>
    </div>

    <form class="card search-form" @submit.prevent="search">
      <label class="field">
        <span class="field__label">Patient name</span>
        <input v-model="patient" type="text" class="input" placeholder="e.g. Tan Wei Ming" />
      </label>
      <label class="field">
        <span class="field__label">Diagnosis code</span>
        <input v-model="diagnosisCode" type="text" class="input" placeholder="e.g. I10" />
      </label>
      <button type="submit" class="button button--primary" :disabled="pending">
        {{ pending ? 'Searching…' : 'Search' }}
      </button>
    </form>

    <ConsultationTable
      v-if="hasSearched"
      :consultations="results"
      :pending="pending"
      :error="error"
      empty-message="No consultations match your search."
    />
  </div>
</template>

<style scoped>
.page-header {
  margin-bottom: 20px;
}

.page-title {
  margin: 0 0 4px;
  font-size: 26px;
  font-weight: 700;
}

.page-subtitle {
  margin: 0;
  color: var(--color-text-muted);
  font-size: 14px;
}

.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

.search-form {
  padding: 20px 24px;
  margin-bottom: 20px;
  display: flex;
  align-items: flex-end;
  gap: 16px;
  flex-wrap: wrap;
}

.field {
  display: block;
  flex: 1;
  min-width: 200px;
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
  padding: 10px 18px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  border: 1px solid transparent;
  cursor: pointer;
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
