import axios from 'axios'

const api = axios.create({ baseURL: '/api', timeout: 10000 })
api.interceptors.response.use(r => r.data, e => Promise.reject(e))

export const getDashboard  = () => api.get('/dashboard')
export const getProjects   = () => api.get('/projects')
export const getProject    = (id) => api.get(`/projects/${id}`)
export const getAgents     = (params) => api.get('/agents', { params })
export const createAgent   = (data) => api.post('/agents', data)
export const getRuns       = () => api.get('/runs')
export const getRun        = (id) => api.get(`/runs/${id}`)
export const getGovernance = () => api.get('/governance')
export const toggleBreaker = (enable) => api.post('/governance/circuit-breaker', null, { params: { enable } })
export const getAudits     = () => api.get('/audits')
export const getAdapters   = () => api.get('/adapters')
