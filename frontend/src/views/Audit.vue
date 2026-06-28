<template>
  <el-card v-loading="loading">
    <template #header>
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span>📜 审计日志</span>
        <el-button :icon="Download" @click="exportCsv" :disabled="!list.length">导出 CSV</el-button>
      </div>
    </template>
    <el-table :data="list" stripe>
      <el-table-column prop="ts" label="时间" width="160" />
      <el-table-column prop="user" label="操作人" width="100" />
      <el-table-column prop="action" label="操作" />
      <el-table-column prop="target" label="对象" />
      <el-table-column label="结果" width="100">
        <template #default="{row}">
          <el-tag :type="row.result==='成功'||row.result==='通过'?'success':'warning'" size="small">{{ row.result }}</el-tag>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Download } from '@element-plus/icons-vue'
import { getAudits } from '../api'

const list = ref([])
const loading = ref(true)

const exportCsv = () => {
  if (!list.value.length) {
    ElMessage.warning('无数据可导出')
    return
  }
  try {
    const head = '时间,操作人,操作,对象,结果\n'
    const body = list.value.map(r => `${r.ts},${r.user},${r.action},${r.target},${r.result}`).join('\n')
    const blob = new Blob(['\ufeff' + head + body], { type: 'text/csv;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `audit_${new Date().toISOString().slice(0, 10)}.csv`
    a.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    ElMessage.error('导出失败：' + (e.message || '未知错误'))
  }
}

onMounted(async () => {
  try {
    const res = await getAudits()
    list.value = res.data
  } catch (e) {
    ElMessage.error('审计日志加载失败：' + (e.message || '未知错误'))
  } finally {
    loading.value = false
  }
})
</script>
