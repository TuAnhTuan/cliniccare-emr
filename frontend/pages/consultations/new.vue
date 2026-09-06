<script setup lang="ts">
import type { ConsultationCreatePayload, Diagnosis } from '~/types'

const { post } = useApi()
const router = useRouter()

const MAX_PATIENT_AGE_YEARS = 130

const todayIso = new Date().toISOString().slice(0, 10)
const earliestDobIso = (() => {
  const d = new Date()
  d.setFullYear(d.getFullYear() - MAX_PATIENT_AGE_YEARS)
  return d.toISOString().slice(0, 10)
})()

const patientName = ref('')
const patientDob = ref('')
const patientGender = ref<'' | 'male' | 'female' | 'other'>('')
const note = ref('')
const selectedDiagnoses = ref<Diagnosis[]>([])
const submitting = ref(false)
const errorMessage = ref('')

async function submit() {
  errorMessage.value = ''

  if (!patientName.value.trim() || !note.value.trim() || !selectedDiagnoses.value.length) {
    errorMessage.value = 'Please fill in patient name, note, and at least one diagnosis code.'
    return
  }

  if (patientDob.value) {
    if (patientDob.value > todayIso) {
      errorMessage.value = 'Date of birth cannot be in the future.'
      return
    }
    if (patientDob.value < earliestDobIso) {
      errorMessage.value = `Date of birth cannot be more than ${MAX_PATIENT_AGE_YEARS} years ago.`
      return
    }
  }

  submitting.value = true
  try {
    const payload: ConsultationCreatePayload = {
      patient_name: patientName.value.trim(),
      patient_dob: patientDob.value || null,
      patient_gender: patientGender.value || null,
      note: note.value.trim(),
      diagnosis_codes: selectedDiagnoses.value.map((d) => d.icd10_code),
    }
    await post('/consultation', payload)
    await router.push('/consultations')
  } catch (err: any) {
    errorMessage.value = err?.data?.detail || 'Failed to save the consultation. Please try again.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div>
    <div class="page-header">
      <h1 class="page-title">New consultation</h1>
      <p class="page-subtitle">Record a patient visit with the relevant diagnosis codes</p>
    </div>

    <form class="card form" @submit.prevent="submit">
      <p v-if="errorMessage" class="form-error">{{ errorMessage }}</p>

      <label class="field">
        <span class="field__label">Patient name</span>
        <input v-model="patientName" type="text" class="input" placeholder="e.g. Tuan Le" />
      </label>

      <div class="field-row">
        <label class="field">
          <span class="field__label">Date of birth <span class="field__optional">(optional)</span></span>
          <input v-model="patientDob" type="date" class="input" :min="earliestDobIso" :max="todayIso" />
        </label>

        <label class="field">
          <span class="field__label">Gender <span class="field__optional">(optional)</span></span>
          <select v-model="patientGender" class="input">
            <option value="">Not specified</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </label>
      </div>
      <p class="field-hint">Only used when creating a new patient record; ignored if the patient already exists.</p>

      <label class="field">
        <span class="field__label">Diagnosis codes</span>
        <DiagnosisPicker v-model="selectedDiagnoses" />
      </label>

      <label class="field">
        <span class="field__label">Consultation note</span>
        <textarea v-model="note" class="input textarea" rows="5" placeholder="What did the doctor observe or advise?" />
      </label>

      <div class="form-actions">
        <NuxtLink to="/consultations" class="button button--ghost">Cancel</NuxtLink>
        <button type="submit" class="button button--primary" :disabled="submitting">
          {{ submitting ? 'Saving…' : 'Save consultation' }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.page-header {
  margin-bottom: 20px;
  text-align: center;
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

.form {
  padding: 24px;
  max-width: 480px;
  margin: 0 auto;
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
  margin-bottom: 18px;
}

.field__label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 6px;
}

.field__optional {
  font-weight: 400;
  color: var(--color-text-muted);
}

.field-row {
  display: flex;
  gap: 12px;
}

.field-row .field {
  flex: 1;
}

.field-hint {
  margin: -10px 0 18px;
  font-size: 12px;
  color: var(--color-text-muted);
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

.textarea {
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 8px;
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

.button--ghost {
  background: transparent;
  border-color: var(--color-border);
  color: var(--color-text-muted);
  display: inline-flex;
  align-items: center;
}
</style>
