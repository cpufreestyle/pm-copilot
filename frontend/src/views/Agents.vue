<template>
  <el-card v-loading="loading">
    <template #header>
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span>🤖 Agent 列表</span>
        <el-button type="primary" @click="dialog=true" :icon="Plus">新建 Agent</el-button>
      </div>
    </template>
    <el-table :data="list" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="name" label="名称" />
      <el-table-column label="平台" width="140">
        <template #default="{row}"><el-tag>{{ row.platform }}</el-tag></template>
      </el-table-column>
      <el-table-column prop="version" label="版本" width="80" />
      <el-table-column label="状态" width="100">
        <template #default="{row}">
          <el-tag :type="row.status==='online'?'success':'info'">{{ row.status }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="owner" label="负责人" width="100" />
      <el-table-column prop="project" label="所属项目" width="120" />
    </el-table>

    <el-dialog v-model="dialog" title="新建 Agent（演示适配层）" width="460">
      <el-form :model="form" label-width="80">
        <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="平台">
          <el-select v-model="form.platform" style="width:100%">
            <el-option label="platform_a" value="platform_a" />
            <el-option label="platform_b" value="platform_b" />
          </el-select>
        </el-form-item>
        <el-form-item label="负责人"><el-input v-model="form.owner" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog=false">取消</el-button>
        <el-button type="primary" @click="submit" :loading="submitting">提交</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getAgents, createAgent } from '../api'

const list = ref([])
const loading = ref(true)
const dialog = ref(false)
const submitting = ref(false)
const form = reactive({ name: '', platform: 'platform_a', owner: '' })

const load = async () => {
  try {
    const res = await getAgents()
    list.value = res.data
  } catch (e) {
    ElMessage.error('Agent 列表加载失败：' + (e.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

const submit = async () => {
  if (!form.name || !form.owner) {
    ElMessage.warning('请填写名称和负责人')
    return
  }
  submitting.value = true
  try {
    const r = await createAgent(form)
    ElMessage.success(`已通过适配层创建：${r.data.agent_id}`)
    dialog.value = false
    form.name = ''
    form.owner = ''
    await load()
  } catch (e) {
    ElMessage.error('创建 Agent 失败：' + (e.message || '未知错误'))
  } finally {
    submitting.value = false
  }
}

onMounted(load)
</script>
