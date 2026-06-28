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
    <el-pagination
      style="margin-top:16px;justify-content:center;"
      background
      layout="total, sizes, prev, pager, next"
      :total="total" :page-size="query.pageSize" :current-page="query.page"
      :page-sizes="[10, 20, 50]"
      @size-change="onSizeChange" @current-change="onPageChange"
    />
  </el-card>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getProjects } from '../api'

const list = ref([])
const total = ref(0)
const loading = ref(true)
const query = reactive({ page: 1, pageSize: 20 })

const tag = s => s === '进行中' ? 'primary' : s === '已完成' ? 'success' : 'info'

const load = async () => {
  loading.value = true
  try {
    const res = await getProjects(query)
    list.value  = res.items
    total.value = res.total
  } catch (e) {
    ElMessage.error('项目列表加载失败：' + (e.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

const onPageChange = p => { query.page = p; load() }
const onSizeChange = s => { query.pageSize = s; query.page = 1; load() }

onMounted(load)
</script>
