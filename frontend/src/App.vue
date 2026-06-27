<template>
  <el-container class="layout">
    <el-aside width="220px" class="aside">
      <div class="logo">🦝 PM Copilot</div>
      <el-menu :default-active="$route.path" router class="menu">
        <el-menu-item index="/"><el-icon><Odometer /></el-icon><span>总览</span></el-menu-item>
        <el-menu-item index="/projects"><el-icon><Folder /></el-icon><span>项目</span></el-menu-item>
        <el-menu-item index="/agents"><el-icon><Cpu /></el-icon><span>Agent</span></el-menu-item>
        <el-menu-item index="/runtime"><el-icon><VideoPlay /></el-icon><span>运行</span></el-menu-item>
        <el-menu-item index="/governance"><el-icon><Lock /></el-icon><span>治理</span></el-menu-item>
        <el-menu-item index="/audit"><el-icon><Document /></el-icon><span>审计</span></el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <span class="title">{{ $route.meta.title || '总览' }}</span>
        <div class="user"><el-icon><User /></el-icon> 管理员</div>
      </el-header>
      <el-main><router-view /></el-main>
    </el-container>
  </el-container>
</template>
<style scoped>
.layout { height: 100vh; }
.aside { background: #2c3e50; color: #fff; }
.logo { padding: 20px; font-size: 18px; font-weight: bold; border-bottom: 1px solid #34495e; color: #e67e22; }
.menu { background: #2c3e50; border-right: none; }
:deep(.el-menu-item) { color: #ecf0f1; }
:deep(.el-menu-item.is-active) { background: #e67e22; color: #fff; }
:deep(.el-menu-item:hover) { background: #34495e; }
.header { background: #fff; border-bottom: 1px solid #e4e7ed; display: flex; align-items: center; justify-content: space-between; }
.title { font-size: 18px; font-weight: bold; color: #2c3e50; }
.user { color: #7f8c8d; }
</style>
