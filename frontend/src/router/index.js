import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  { path: '/',            component: () => import('../views/Dashboard.vue'),  meta: { title: '总览' } },
  { path: '/projects',    component: () => import('../views/Projects.vue'),   meta: { title: '项目' } },
  { path: '/agents',      component: () => import('../views/Agents.vue'),     meta: { title: 'Agent' } },
  { path: '/runtime',     component: () => import('../views/Runtime.vue'),    meta: { title: '运行' } },
  { path: '/governance',  component: () => import('../views/Governance.vue'), meta: { title: '治理' } },
  { path: '/audit',       component: () => import('../views/Audit.vue'),      meta: { title: '审计' } },
]
export default createRouter({ history: createWebHashHistory(), routes })
