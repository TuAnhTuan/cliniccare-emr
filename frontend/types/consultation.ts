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
  note: string
  diagnosis_codes: string[]
  // TODO: derive this from the authenticated practitioner once JWT login is added
  created_by: number
}
