<template>
  <el-card v-loading="loading">
    <template #header>
      <div style="display:flex;justify-content:space-between;align-items:center;">
        <span>🤖 Agent 列表</span>
        <el-button type="primary" @click="dialog=true" :icon="Plus">新建 Agent</el-button>
      </div>
    </template>

    <!-- 筛选栏 -->
    <div style="margin-bottom:12px;display:flex;gap:12px;align-items:center;">
      <el-select v-model="query.platform" placeholder="全部平台" clearable style="width:160px" @change="query.page=1;load()">
        <el-option label="platform_a" value="platform_a" />
        <el-option label="platform_b" value="platform_b" />
      </el-select>
      <el-select v-model="query.status" placeholder="全部状态" clearable style="width:140px" @change="query.page=1;load()">
        <el-option label="online"  value="online" />
        <el-option label="offline" value="offline" />
      </el-select>
    </div>

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

    <el-pagination
      style="margin-top:16px;justify-content:center;"
      background
      layout="total, sizes, prev, pager, next"
      :total="total" :page-size="query.pageSize" :current-page="query.page"
      :page-sizes="[10, 20, 50]"
      @size-change="s => { query.pageSize=s; query.page=1; load() }"
      @current-change="p => { query.page=p; load() }"
    />

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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getAgents, createAgent } from '../api'

const list = ref([])
const total = ref(0)
const loading = ref(true)
const dialog = ref(false)
const submitting = ref(false)
const form = reactive({ name: '', platform: 'platform_a', owner: '' })
const query = reactive({ page: 1, pageSize: 20, platform: undefined, status: undefined })

const load = async () => {
  loading.value = true
  try {
    const res = await getAgents(query)
    list.value  = res.items
    total.value = res.total
  } catch (e) {
    ElMessage.error('Agent 列表加载失败：' + (e.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

const submit = async () => {
  if (!form.name || !form.owner) { ElMessage.warning('请填写名称和负责人'); return }
  submitting.value = true
  try {
    const r = await createAgent(form)
    ElMessage.success(`已通过适配层创建：${r.data.agent_id}`)
    dialog.value = false
    form.name = ''; form.owner = ''
    query.page = 1
    await load()
  } catch (e) {
    ElMessage.error('创建 Agent 失败：' + (e.message || '未知错误'))
  } finally {
    submitting.value = false
  }
}

onMounted(load)
</script>
