<template>
  <div v-loading="loading">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <template #header>💰 预算与额度</template>
          <div style="text-align:center;padding:20px 0;">
            <el-progress type="dashboard" :percentage="g?.budget?.percent || 0" :width="160" />
            <div style="margin-top:12px;font-size:14px;color:#7f8c8d;">
              月度: ¥ {{ g?.budget?.month_limit }} · 已用: ¥ {{ g?.budget?.used }}
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>✅ 审批工作流</template>
          <el-statistic title="待审批" :value="g?.approvals?.pending || 0" />
          <el-statistic title="今日通过" :value="g?.approvals?.approved_today || 0" />
          <el-statistic title="今日拒绝" :value="g?.approvals?.rejected_today || 0" />
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top:20px;">
      <el-col :span="12">
        <el-card style="background:#fdecea;">
          <template #header>🔴 熔断开关</template>
          <p>一键停止所有 Agent 运行（紧急情况）</p>
          <el-switch v-model="breaker" active-text="已开启" inactive-text="关闭中" @change="toggle"
                     style="--el-switch-on-color: #e74c3c" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>📋 黑白名单</template>
          <div style="margin-bottom:10px;"><strong>黑名单：</strong>
            <el-tag v-for="x in g?.blacklist" :key="x" type="danger" style="margin:0 4px 4px 0;">{{ x }}</el-tag>
          </div>
          <div><strong>白名单：</strong>
            <el-tag v-for="x in g?.whitelist" :key="x" type="success" style="margin:0 4px 4px 0;">{{ x }}</el-tag>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getGovernance, toggleBreaker } from '../api'

const g = ref(null)
const loading = ref(true)
const breaker = ref(false)

const toggle = async v => {
  try {
    await toggleBreaker(v)
    ElMessage.warning(`熔断已${v ? '开启' : '关闭'}`)
  } catch (e) {
    // 回滚 switch 状态
    breaker.value = !v
    ElMessage.error('熔断切换失败：' + (e.message || '未知错误'))
  }
}

onMounted(async () => {
  try {
    const res = await getGovernance()
    g.value = res.data
    breaker.value = g.value.circuit_breaker
  } catch (e) {
    ElMessage.error('治理数据加载失败：' + (e.message || '未知错误'))
  } finally {
    loading.value = false
  }
})
</script>
