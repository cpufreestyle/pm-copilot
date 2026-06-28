<template>
  <el-card v-loading="loading">
    <template #header>
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span>📜 审计日志</span>
        <el-button :icon="Download" @click="exportCsv" :disabled="!list.length">导出 CSV</el-button>
      </div>
    </template>

    <!-- 筛选 -->
    <div style="margin-bottom:12px;display:flex;gap:12px;align-items:center;">
      <el-input v-model="query.user" placeholder="按操作人筛选" clearable style="width:180px"
                @clear="query.page=1;load()">
        <template #prefix><User /></template>
      </el-input>
      <el-button @click="query.page=1;load()">筛选</el-button>
    </div>

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

    <el-pagination
      style="margin-top:16px;justify-content:center;"
      background
      layout="total, sizes, prev, pager, next"
      :total="total" :page-size="query.pageSize" :current-page="query.page"
      :page-sizes="[10, 20, 50]"
      @size-change="s => { query.pageSize=s; query.page=1; load() }"
      @current-change="p => { query.page=p; load() }"
    />
  </el-card>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Download, User } from '@element-plus/icons-vue'
import { getAudits } from '../api'

const list = ref([])
const total = ref(0)
const loading = ref(true)
const query = reactive({ page: 1, pageSize: 20, user: undefined })

const exportCsv = () => {
  if (!list.value.length) { ElMessage.warning('无数据可导出'); return }
  try {
    const head = '时间,操作人,操作,对象,结果\n'
    const body = list.value.map(r => `${r.ts},${r.user},${r.action},${r.target},${r.result}`).join('\n')
    const blob = new Blob(['\ufeff' + head + body], { type: 'text/csv;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url; a.download = `audit_${new Date().toISOString().slice(0, 10)}.csv`; a.click()
    URL.revokeObjectURL(url)
  } catch (e) {
    ElMessage.error('导出失败：' + (e.message || '未知错误'))
  }
}

const load = async () => {
  loading.value = true
  try {
    const res = await getAudits(query)
    list.value  = res.items
    total.value = res.total
  } catch (e) {
    ElMessage.error('审计日志加载失败：' + (e.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>
