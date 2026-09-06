<script setup lang="ts">
import type { Diagnosis } from '~/types'

const modelValue = defineModel<Diagnosis[]>({ default: () => [] })

const { get } = useApi()
const searchTerm = ref('')
const results = ref<Diagnosis[]>([])
const searching = ref(false)

let debounceTimer: ReturnType<typeof setTimeout> | undefined

watch(searchTerm, (term) => {
  clearTimeout(debounceTimer)
  if (!term.trim()) {
    results.value = []
    return
  }
  debounceTimer = setTimeout(async () => {
    searching.value = true
    try {
      results.value = await get<Diagnosis[]>('/diagnosis', { search: term, limit: '10' })
    } finally {
      searching.value = false
    }
  }, 300)
})

function isSelected(diagnosis: Diagnosis) {
  return modelValue.value.some((d) => d.id === diagnosis.id)
}

function addDiagnosis(diagnosis: Diagnosis) {
  if (!isSelected(diagnosis)) {
    modelValue.value = [...modelValue.value, diagnosis]
  }
  searchTerm.value = ''
  results.value = []
}

function removeDiagnosis(diagnosis: Diagnosis) {
  modelValue.value = modelValue.value.filter((d) => d.id !== diagnosis.id)
}
</script>

<template>
  <div class="picker">
    <div v-if="modelValue.length" class="chips">
      <span v-for="diagnosis in modelValue" :key="diagnosis.id" class="chip" :title="diagnosis.description">
        {{ diagnosis.icd10_code }}
        <button type="button" class="chip__remove" aria-label="Remove" @click="removeDiagnosis(diagnosis)">×</button>
      </span>
    </div>

    <input
      v-model="searchTerm"
      type="text"
      class="input"
      placeholder="Search ICD-10 code or description…"
    />

    <ul v-if="searchTerm && (results.length || searching)" class="results">
      <li v-if="searching" class="results__hint">Searching…</li>
      <li
        v-for="diagnosis in results"
        :key="diagnosis.id"
        class="results__item"
        :class="{ 'results__item--selected': isSelected(diagnosis) }"
        @mousedown.prevent="addDiagnosis(diagnosis)"
      >
        <strong>{{ diagnosis.icd10_code }}</strong> — {{ diagnosis.description }}
      </li>
      <li v-if="!searching && !results.length" class="results__hint">No matching codes.</li>
    </ul>
  </div>
</template>

<style scoped>
.picker {
  position: relative;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 8px;
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--color-primary-light);
  color: var(--color-primary-dark);
  font-size: 13px;
  font-weight: 600;
  padding: 4px 6px 4px 10px;
  border-radius: 6px;
}

.chip__remove {
  border: none;
  background: transparent;
  color: inherit;
  font-size: 15px;
  line-height: 1;
  cursor: pointer;
  padding: 0 2px;
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

.results {
  position: absolute;
  z-index: 10;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 4px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  box-shadow: var(--shadow);
  max-height: 240px;
  overflow-y: auto;
  list-style: none;
  padding: 6px;
}

.results__item {
  padding: 8px 10px;
  font-size: 13px;
  border-radius: 6px;
  cursor: pointer;
}

.results__item:hover {
  background: var(--color-primary-light);
}

.results__item--selected {
  opacity: 0.5;
  cursor: default;
}

.results__hint {
  padding: 8px 10px;
  font-size: 13px;
  color: var(--color-text-muted);
}
</style>
