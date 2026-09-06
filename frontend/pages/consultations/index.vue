<script setup lang="ts">
import type { Consultation } from '~/types'

const { get } = useApi()
const { data: consultations, pending, error } = await useAsyncData('consultations', () =>
  get<Consultation[]>('/consultation')
)
</script>

<template>
  <div>
    <div class="page-header">
      <div>
        <h1 class="page-title">Consultations</h1>
        <p class="page-subtitle">Past patient consultation notes</p>
      </div>
      <span v-if="consultations?.length" class="page-count">
        {{ consultations.length }} record{{ consultations.length === 1 ? '' : 's' }}
      </span>
    </div>

    <ConsultationTable :consultations="consultations" :pending="pending" :error="!!error" />
  </div>
</template>

<style scoped>
.page-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
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

.page-count {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-primary-dark);
  background: var(--color-primary-light);
  padding: 4px 12px;
  border-radius: 999px;
  white-space: nowrap;
}
</style>
