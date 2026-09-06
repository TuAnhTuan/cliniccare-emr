import type { Diagnosis } from './diagnosis'
import type { Patient } from './patient'

export interface Consultation {
  id: number
  patient: Patient
  note: string
  diagnoses: Diagnosis[]
  created_by: number
  created_at: string
}
