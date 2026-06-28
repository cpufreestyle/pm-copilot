<template>
  <el-card v-loading="loading">
    <template #header>📁 项目列表</template>
    <el-table :data="list" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="项目名称" />
      <el-table-column prop="owner" label="负责人" width="100" />
      <el-table-column label="状态" width="100">
        <template #default="{row}">
          <el-tag :type="tag(row.status)">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="进度" width="200">
        <template #default="{row}"><el-progress :percentage="row.progress" /></template>
      </el-table-column>
      <el-table-column label="风险" width="80">
        <template #default="{row}">
          <el-tag :type="row.risk==='高'?'danger':row.risk==='中'?'warning':'success'" size="small">{{ row.risk }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="agents" label="Agent 数" width="100" align="center" />
      <el-table-column label="成本" width="120">
        <template #default="{row}">¥ {{ row.cost.toFixed(2) }}</template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getProjects } from '../api'

const list = ref([])
const loading = ref(true)
const tag = s => s === '进行中' ? 'primary' : s === '已完成' ? 'success' : 'info'

onMounted(async () => {
  try {
    const res = await getProjects()
    list.value = res.data
  } catch (e) {
    ElMessage.error('项目列表加载失败：' + (e.message || '未知错误'))
  } finally {
    loading.value = false
  }
})
</script>
