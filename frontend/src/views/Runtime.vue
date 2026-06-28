<template>
  <el-row :gutter="20">
    <el-col :span="10">
      <el-card v-loading="loading">
        <template #header>▶ 运行记录</template>
        <el-table :data="list" highlight-current-row @current-change="select" size="small">
          <el-table-column prop="id" label="任务 ID" />
          <el-table-column prop="agent" label="Agent" width="120" />
          <el-table-column label="状态" width="90">
            <template #default="{row}">
              <el-tag :type="row.status==='success'?'success':row.status==='failed'?'danger':'warning'" size="small">{{ row.status }}</el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-col>
    <el-col :span="14">
      <el-card v-if="detail">
        <template #header>🔍 调用链 Trace · {{ detail.id }}</template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="Agent">{{ detail.agent }}</el-descriptions-item>
          <el-descriptions-item label="项目">{{ detail.project }}</el-descriptions-item>
          <el-descriptions-item label="耗时">{{ detail.duration }} s</el-descriptions-item>
          <el-descriptions-item label="成本">¥ {{ detail.cost }}</el-descriptions-item>
        </el-descriptions>
        <h4 style="margin-top:16px;">Prompt</h4>
        <el-input type="textarea" :rows="2" :model-value="detail.prompt" readonly />
        <h4 style="margin-top:16px;">调用链</h4>
        <el-timeline>
          <el-timeline-item v-for="(t, i) in detail.trace" :key="i" :type="typeColor(t.type)" :timestamp="t.ts">
            <el-tag size="small">{{ t.type }}</el-tag> {{ t.msg }}
          </el-timeline-item>
        </el-timeline>
        <h4>输出</h4>
        <el-alert :title="detail.output" type="success" :closable="false" />
      </el-card>
      <el-empty v-else description="点击左侧选择一条运行记录查看详情" />
    </el-col>
  </el-row>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getRuns, getRun } from '../api'

const list = ref([])
const loading = ref(true)
const detail = ref(null)

const typeColor = t => ({ input: 'primary', tool: 'warning', reason: 'info', output: 'success' }[t] || 'info')

const select = async row => {
  if (!row) { detail.value = null; return }
  try {
    detail.value = (await getRun(row.id)).data
  } catch (e) {
    ElMessage.error('运行详情加载失败：' + (e.message || '未知错误'))
    detail.value = null
  }
}

onMounted(async () => {
  try {
    const res = await getRuns()
    list.value = res.data
    if (list.value.length) await select(list.value[0])
  } catch (e) {
    ElMessage.error('运行记录加载失败：' + (e.message || '未知错误'))
  } finally {
    loading.value = false
  }
})
</script>
