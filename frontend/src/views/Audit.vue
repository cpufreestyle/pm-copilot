<template>
  <el-card v-loading="loading">
    <template #header>
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span>📜 审计日志</span>
        <el-button :icon="Download" @click="exportCsv">导出 CSV</el-button>
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
import { Download } from '@element-plus/icons-vue'
import { getAudits } from '../api'
const list = ref([]); const loading = ref(true)
const exportCsv = () => {
  const head = '时间,操作人,操作,对象,结果\n'
  const body = list.value.map(r => `${r.ts},${r.user},${r.action},${r.target},${r.result}`).join('\n')
  const blob = new Blob(['\ufeff'+head+body], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a'); a.href = url; a.download = 'audit.csv'; a.click()
}
onMounted(async () => { list.value = (await getAudits()).data; loading.value = false })
</script>
