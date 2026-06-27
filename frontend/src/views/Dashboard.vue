<template>
  <div v-loading="loading">
    <el-row :gutter="20">
      <el-col :span="6" v-for="(s, i) in stats" :key="i">
        <el-card class="stat" :style="{borderTopColor: s.color}">
          <div class="num" :style="{color: s.color}">{{ s.value }}</div>
          <div class="lbl">{{ s.label }}</div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="16">
        <el-card><template #header>📈 运行趋势</template>
          <div ref="chartRef" style="height: 320px;"></div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card><template #header>⚠ 异常告警 Top</template>
          <el-empty v-if="!data?.top_alerts?.length" description="无告警" />
          <div v-else>
            <div v-for="(a, i) in data.top_alerts" :key="i" class="alert">
              <el-tag :type="a.level==='high'?'danger':'warning'" size="small">{{ a.level }}</el-tag>
              <span>{{ a.msg }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>
<script setup>
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import { getDashboard } from '../api'

const loading = ref(true); const data = ref(null); const chartRef = ref(null)
const stats = ref([])

onMounted(async () => {
  try {
    const res = await getDashboard()
    data.value = res.data
    stats.value = [
      { label: '项目数', value: data.value.projects, color: '#3498db' },
      { label: 'Agent 数', value: data.value.agents, color: '#16a085' },
      { label: '运行中', value: data.value.running, color: '#e67e22' },
      { label: '今日成本', value: '¥' + data.value.today_cost, color: '#e74c3c' },
    ]
    await nextTick()
    const chart = echarts.init(chartRef.value)
    chart.setOption({
      tooltip: { trigger: 'axis' },
      legend: { data: ['任务数', '成本(¥)'] },
      xAxis: { type: 'category', data: data.value.trend.map(t => t.date) },
      yAxis: [{ type: 'value', name: '任务数' }, { type: 'value', name: '成本' }],
      series: [
        { name: '任务数', type: 'line', smooth: true, data: data.value.trend.map(t => t.tasks), itemStyle: { color: '#3498db' } },
        { name: '成本(¥)', type: 'bar', yAxisIndex: 1, data: data.value.trend.map(t => t.cost), itemStyle: { color: '#e67e22' } },
      ]
    })
  } finally { loading.value = false }
})
</script>
<style scoped>
.stat { text-align: center; border-top: 4px solid; }
.num { font-size: 32px; font-weight: bold; }
.lbl { color: #7f8c8d; margin-top: 6px; }
.alert { padding: 10px 0; border-bottom: 1px solid #f0f0f0; display: flex; align-items: center; gap: 10px; }
</style>
