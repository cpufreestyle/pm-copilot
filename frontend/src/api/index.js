import axios from 'axios'

const api = axios.create({ baseURL: '/api', timeout: 10000 })
api.interceptors.response.use(r => r.data, e => Promise.reject(e))

// 通用分页请求封装
// 自动从响应中提取 items，返回 { items, total, page, page_size, pages }
const paginated = (fn) => async (params = {}) => {
  const res = await fn(params)
  return {
    items:     res.data.items,
    total:     res.data.total,
    page:      res.data.page,
    pageSize:  res.data.page_size,
    pages:     res.data.pages,
  }
}

export const getDashboard  = () => api.get('/dashboard')
export const getProjects   = paginated(p => api.get('/projects', { params: p }))
export const getProject    = (id) => api.get(`/projects/${id}`)
export const getAgents     = paginated(p => api.get('/agents', { params: p }))
export const createAgent   = (data) => api.post('/agents', data)
export const getRuns       = paginated(p => api.get('/runs', { params: p }))
export const getRun        = (id) => api.get(`/runs/${id}`)
export const getGovernance = () => api.get('/governance')
export const toggleBreaker = (enable) => api.post('/governance/circuit-breaker', null, { params: { enable } })
export const getAudits     = paginated(p => api.get('/audits', { params: p }))
export const getAdapters   = () => api.get('/adapters')
