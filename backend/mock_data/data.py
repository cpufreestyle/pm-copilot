"""Mock 数据"""

PROJECTS = [
    {"id": "P001", "name": "智能客服升级",   "owner": "张三", "status": "进行中", "progress": 65, "risk": "中", "agents": 4, "cost": 1280.5},
    {"id": "P002", "name": "财务对账自动化", "owner": "李四", "status": "进行中", "progress": 42, "risk": "低", "agents": 3, "cost": 860.2},
    {"id": "P003", "name": "营销文案生成",   "owner": "王五", "status": "已完成", "progress": 100, "risk": "低", "agents": 2, "cost": 520.0},
    {"id": "P004", "name": "代码审查助手",   "owner": "赵六", "status": "进行中", "progress": 28, "risk": "高", "agents": 5, "cost": 2150.8},
    {"id": "P005", "name": "数据分析报表",   "owner": "钱七", "status": "待启动", "progress": 0,  "risk": "低", "agents": 1, "cost": 0},
]

AGENTS = [
    {"id": "A01", "name": "Analyzer-01", "platform": "platform_a", "version": "v1.2", "status": "online",  "owner": "李四", "project": "P001"},
    {"id": "A02", "name": "Executor-02", "platform": "platform_b", "version": "v2.0", "status": "online",  "owner": "王五", "project": "P001"},
    {"id": "A03", "name": "Reviewer-03", "platform": "platform_a", "version": "v1.0", "status": "offline", "owner": "赵六", "project": "P002"},
    {"id": "A04", "name": "Planner-04",  "platform": "platform_b", "version": "v1.5", "status": "online",  "owner": "钱七", "project": "P002"},
    {"id": "A05", "name": "Coder-05",    "platform": "platform_a", "version": "v2.1", "status": "online",  "owner": "张三", "project": "P004"},
    {"id": "A06", "name": "Writer-06",   "platform": "platform_b", "version": "v1.3", "status": "online",  "owner": "李四", "project": "P003"},
]

RUNS = [
    {"id": "T20260615-007", "agent": "Analyzer-01", "project": "P001", "status": "success", "duration": 3.2, "cost": 0.42, "ts": "2026-06-15 10:21"},
    {"id": "T20260615-006", "agent": "Executor-02", "project": "P001", "status": "success", "duration": 5.8, "cost": 0.86, "ts": "2026-06-15 10:18"},
    {"id": "T20260615-005", "agent": "Planner-04",  "project": "P002", "status": "failed",  "duration": 1.4, "cost": 0.12, "ts": "2026-06-15 10:05"},
    {"id": "T20260615-004", "agent": "Coder-05",    "project": "P004", "status": "running", "duration": 0,   "cost": 0,    "ts": "2026-06-15 09:58"},
    {"id": "T20260615-003", "agent": "Writer-06",   "project": "P003", "status": "success", "duration": 2.1, "cost": 0.28, "ts": "2026-06-15 09:30"},
]

AUDITS = [
    {"ts": "2026-06-15 10:21", "user": "张三", "action": "启动 Agent",     "target": "Analyzer-01", "result": "成功"},
    {"ts": "2026-06-15 10:18", "user": "李四", "action": "修改预算上限",   "target": "项目 P001",    "result": "成功"},
    {"ts": "2026-06-15 09:55", "user": "系统", "action": "熔断触发",       "target": "全部 Agent",   "result": "已停止"},
    {"ts": "2026-06-15 09:30", "user": "王五", "action": "审批通过",       "target": "申请 #A007",   "result": "通过"},
    {"ts": "2026-06-15 09:12", "user": "赵六", "action": "新建 Agent",     "target": "Coder-05",    "result": "成功"},
    {"ts": "2026-06-15 08:45", "user": "钱七", "action": "停用 Agent",     "target": "Reviewer-03", "result": "成功"},
]

GOVERNANCE = {
    "budget":    {"month_limit": 8000, "used": 3260, "percent": 40.75},
    "approvals": {"pending": 3, "approved_today": 7, "rejected_today": 1},
    "circuit_breaker": False,
    "blacklist": ["external_api_x", "model_unstable_v0"],
    "whitelist": ["search_kb", "send_email", "query_db"],
}

DASHBOARD = {
    "projects": 12,
    "agents": 38,
    "running": 7,
    "alerts": 2,
    "today_cost": 286.5,
    "trend": [
        {"date": "06-09", "tasks": 32, "cost": 180},
        {"date": "06-10", "tasks": 45, "cost": 240},
        {"date": "06-11", "tasks": 38, "cost": 210},
        {"date": "06-12", "tasks": 52, "cost": 290},
        {"date": "06-13", "tasks": 41, "cost": 220},
        {"date": "06-14", "tasks": 48, "cost": 260},
        {"date": "06-15", "tasks": 56, "cost": 286},
    ],
    "top_alerts": [
        {"level": "high",   "msg": "Agent-03 连续超时 3 次"},
        {"level": "medium", "msg": "项目 P001 预算使用率达 85%"},
    ],
}
