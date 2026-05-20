<template>
  <div class="skill-center-page">
    <div class="hero">
      <div>
        <p class="eyebrow">Composable Skills</p>
        <h2>Skill 管理中心</h2>
        <p>借鉴“文件系统存内容、元数据存索引、渐进式加载”的设计，统一治理工具 / 业务 / 定制技能。</p>
      </div>
      <a-space>
        <a-button @click="reset" ghost>重置</a-button>
        <a-button type="primary" @click="saveConfig">保存配置</a-button>
      </a-space>
    </div>

    <a-row :gutter="16" class="stats-row">
      <a-col :span="6" v-for="item in overview" :key="item.key">
        <a-card class="stats-card">
          <div class="value">{{ item.value }}</div>
          <div class="label">{{ item.label }}</div>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="16">
      <a-col :span="16">
        <a-card title="技能模块分组" class="main-card">
          <a-collapse v-model:activeKey="activeGroups" ghost>
            <a-collapse-panel v-for="group in groupedSkills" :key="group.key">
              <template #header>
                <div class="group-header">
                  <div>
                    <a-tag :color="group.color">{{ group.title }}</a-tag>
                    <span class="group-subtitle">{{ group.subtitle }}</span>
                  </div>
                  <span>{{ enabledCount(group.skills) }} / {{ group.skills.length }} 已启用</span>
                </div>
              </template>

              <div class="skill-grid">
                <div v-for="item in group.skills" :key="item.id" class="skill-card" :class="{ enabled: item.enabled }">
                  <div class="skill-card-head">
                    <div>
                      <strong>{{ item.name }}</strong>
                      <div class="skill-meta">{{ item.category }} · {{ item.version }} · {{ item.load_strategy }}</div>
                    </div>
                    <a-switch v-model:checked="item.enabled" />
                  </div>
                  <p>{{ item.description }}</p>
                  <div class="skill-tags">
                    <a-tag v-for="dep in dependencyPreview(item)" :key="dep">{{ dep }}</a-tag>
                    <a-tag v-if="dependencyPreview(item).length === 0">无依赖</a-tag>
                  </div>
                  <a-button type="link" size="small" @click="openDetail(item)">配置与规范</a-button>
                </div>
              </div>
            </a-collapse-panel>
          </a-collapse>
        </a-card>
      </a-col>
      <a-col :span="8">
        <a-card title="渐进式加载策略" class="main-card">
          <a-timeline>
            <a-timeline-item color="blue">
              <strong>阶段一：会话启动</strong>
              <div>展开 skill_dependencies，注入可见 Skill 描述。</div>
            </a-timeline-item>
            <a-timeline-item color="green">
              <strong>阶段二：技能激活</strong>
              <div>按用户意图读取 SKILL.md，加入 activated_skills。</div>
            </a-timeline-item>
            <a-timeline-item color="purple">
              <strong>阶段三：按需加载</strong>
              <div>动态加载工具 / MCP / 业务依赖，降低启动成本。</div>
            </a-timeline-item>
          </a-timeline>
        </a-card>
      </a-col>
    </a-row>

    <a-drawer v-model:open="detailOpen" :title="activeSkill?.name || '技能配置'" width="620">
      <template v-if="activeSkill">
        <a-descriptions bordered :column="1" size="small">
          <a-descriptions-item label="目录路径">{{ activeSkill.dir_path }}</a-descriptions-item>
          <a-descriptions-item label="类型 / 分类">{{ typeTitle(activeSkill.skill_type) }} / {{ activeSkill.category }}</a-descriptions-item>
          <a-descriptions-item label="适用场景">{{ activeSkill.scenarios.join('、') }}</a-descriptions-item>
          <a-descriptions-item label="调用示例">{{ activeSkill.call_example }}</a-descriptions-item>
          <a-descriptions-item label="依赖">
            <a-space wrap>
              <a-tag v-for="dep in allDependencies(activeSkill)" :key="dep">{{ dep }}</a-tag>
              <span v-if="allDependencies(activeSkill).length === 0">无</span>
            </a-space>
          </a-descriptions-item>
        </a-descriptions>
        <a-form layout="vertical" class="drawer-form">
          <a-form-item label="TopK">
            <a-input-number v-model:value="activeSkill.params.top_k" :min="1" :max="50" style="width: 100%" />
          </a-form-item>
          <a-form-item label="温度">
            <a-slider v-model:value="activeSkill.params.temperature" :min="0" :max="1" :step="0.1" />
          </a-form-item>
          <a-form-item label="启用追踪日志">
            <a-switch v-model:checked="activeSkill.params.trace" />
          </a-form-item>
        </a-form>
      </template>
    </a-drawer>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { message } from 'ant-design-vue'
import { defaultSkillModules, skillTypeGroups } from '@/constants/skill_modules'

const skills = ref(JSON.parse(JSON.stringify(defaultSkillModules)))
const detailOpen = ref(false)
const activeSkill = ref(null)
const activeGroups = ref(skillTypeGroups.map(group => group.key))

const groupedSkills = computed(() => skillTypeGroups.map(group => ({
  ...group,
  skills: skills.value.filter(skill => skill.skill_type === group.key)
})))

const overview = computed(() => {
  const total = skills.value.length
  const enabled = skills.value.filter(s => s.enabled).length
  const dependencies = skills.value.reduce((acc, s) => acc + allDependencies(s).length, 0)
  const customCount = skills.value.filter(s => s.skill_type === 'custom').length
  return [
    { key: 'total', label: '模块总数', value: total },
    { key: 'enabled', label: '已启用', value: enabled },
    { key: 'deps', label: '依赖声明', value: dependencies },
    { key: 'custom', label: '定制技能', value: customCount }
  ]
})

const enabledCount = (items) => items.filter(item => item.enabled).length
const typeTitle = (type) => skillTypeGroups.find(group => group.key === type)?.title || type
const allDependencies = (skill) => [
  ...(skill.tool_dependencies || []),
  ...(skill.mcp_dependencies || []),
  ...(skill.skill_dependencies || [])
]
const dependencyPreview = (skill) => allDependencies(skill).slice(0, 3)

const openDetail = (skill) => {
  activeSkill.value = skill
  detailOpen.value = true
}

const saveConfig = () => {
  localStorage.setItem('skill-center-config', JSON.stringify(skills.value))
  message.success('Skill 配置已保存')
}

const reset = () => {
  skills.value = JSON.parse(JSON.stringify(defaultSkillModules))
  message.success('已恢复默认配置')
}
</script>

<style scoped lang="less">
.skill-center-page { padding: 20px; background: linear-gradient(180deg, #f8fbff, #f6f7fb); min-height: 100%; }
.hero { display:flex; justify-content:space-between; align-items:center; background:#fff; border-radius:16px; padding:22px 24px; margin-bottom:16px; border:1px solid #e8eef6; box-shadow:0 12px 30px rgba(15,23,42,.05); }
.hero h2{ margin:0; font-size:26px; }
.hero p{ margin:6px 0 0; color:#6b7280; }
.eyebrow{ margin:0 0 4px!important; color:#0e7490!important; font-size:12px; font-weight:700; letter-spacing:.12em; text-transform:uppercase; }
.stats-row { margin-bottom:16px; }
.stats-card { border-radius:14px; }
.value { font-size:30px; font-weight:800; color:#0f172a; }
.label { color:#64748b; margin-top:4px; }
.main-card { border-radius:14px; }
.group-header{ display:flex; justify-content:space-between; gap:12px; width:100%; }
.group-subtitle{ color:#64748b; margin-left:8px; }
.skill-grid{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; }
.skill-card{ border:1px solid #e5edf6; border-radius:12px; padding:14px; background:#fff; transition:.2s; }
.skill-card.enabled{ border-color:#0e7490; background:#f0fbff; }
.skill-card-head{ display:flex; justify-content:space-between; gap:12px; }
.skill-meta{ color:#64748b; font-size:12px; margin-top:4px; }
.skill-card p{ color:#475569; margin:10px 0; line-height:1.5; }
.skill-tags{ display:flex; gap:6px; flex-wrap:wrap; min-height:24px; }
.drawer-form{ margin-top:18px; }
</style>

