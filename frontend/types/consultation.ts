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

export interface ConsultationCreatePayload {
  patient_name: string
  patient_dob?: string | null
  patient_gender?: 'male' | 'female' | 'other' | null
  note: string
  diagnosis_codes: string[]
}
