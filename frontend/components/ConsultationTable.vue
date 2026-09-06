<script setup lang="ts">
import type { Consultation } from '~/types'

defineProps<{
  consultations: Consultation[] | null
  pending: boolean
  error: boolean
  emptyMessage?: string
}>()

function formatDate(value: string) {
  return new Date(value).toLocaleString('en-SG', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function initials(name: string) {
  return name
    .split(' ')
    .map((part) => part[0])
    .slice(0, 2)
    .join('')
    .toUpperCase()
}
</script>

<template>
  <div class="card">
    <p v-if="pending" class="state-message">Loading consultations…</p>
    <p v-else-if="error" class="state-message state-message--error">Failed to load consultations.</p>
    <p v-else-if="!consultations?.length" class="state-message">
      {{ emptyMessage || 'No consultations recorded yet.' }}
    </p>

    <table v-else class="table">
      <thead>
        <tr>
          <th>Patient</th>
          <th>Diagnosis</th>
          <th>Note</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="consultation in consultations" :key="consultation.id">
          <td>
            <div class="patient-cell">
              <span class="patient-avatar">{{ initials(consultation.patient.name) }}</span>
              {{ consultation.patient.name }}
            </div>
          </td>
          <td>
            <span
              v-for="diagnosis in consultation.diagnoses"
              :key="diagnosis.id"
              class="badge"
              :title="diagnosis.description"
            >
              {{ diagnosis.icd10_code }}
            </span>
          </td>
          <td class="note-cell">{{ consultation.note }}</td>
          <td class="date-cell">{{ formatDate(consultation.created_at) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
}

.state-message {
  margin: 0;
  padding: 40px 24px;
  text-align: center;
  color: var(--color-text-muted);
}

.state-message--error {
  color: #b91c1c;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th {
  text-align: left;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--color-text-muted);
  padding: 12px 20px;
  border-bottom: 1px solid var(--color-border);
  background: #f1f5f9;
}

.table td {
  padding: 14px 20px;
  border-bottom: 1px solid var(--color-border);
  font-size: 14px;
  vertical-align: top;
}

.table tbody tr:last-child td {
  border-bottom: none;
}

.table tbody tr:hover {
  background: #f8fafc;
}

.patient-cell {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
}

.patient-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--color-primary-light);
  color: var(--color-primary-dark);
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
}

.badge {
  display: inline-block;
  background: #eff6ff;
  color: #1d4ed8;
  border: 1px solid #bfdbfe;
  font-size: 12px;
  font-weight: 600;
  padding: 3px 9px;
  border-radius: 6px;
  margin: 2px 4px 2px 0;
  cursor: help;
}

.note-cell {
  color: var(--color-text);
  max-width: 320px;
}

.date-cell {
  color: var(--color-text-muted);
  white-space: nowrap;
}
</style>
