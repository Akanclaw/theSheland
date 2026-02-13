export interface Room {
  id: string
  name: string
  creator: string
  seed: string
  max_players: number
  player_count: number
  status: 'waiting' | 'playing' | 'finished'
  current_round: number
  total_rounds: number
  players: Player[]
}

export interface Player {
  id: string
  username: string
  role: 'politician' | 'god' | 'observer'
  is_ready: boolean
  score: number
}

export interface MapRegion {
  id: string
  name: string
  x: number
  y: number
  population: number
  economy: number
  stability: number
  education: number
  culture_type: 'industrial' | 'agricultural' | 'commercial' | 'mixed'
}

export interface Candidate {
  id: string
  name: string
  party?: string
  funds: number
  reputation: number
  policy_economy: number
  policy_social: number
  policy_security: number
}

export interface Round {
  id: string
  round_number: number
  phase: 'campaign' | 'god_intervention' | 'voting' | 'results'
  started_at: string
}