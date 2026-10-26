// dsh-research-skills — host 半边
//
// 职责只有一个：把本包 skills/ 铺到 <dsh-home>/skills/，让这些科研技能在
// DSH 的技能目录里可用。
//
// 为什么单独成包而不是塞进酒馆插件：科研技能（文献检索、证据提取、写作规范、
// 统计分析、文档工具链、学术润色、论文翻译）与酒馆（人物卡文字游戏）毫无关系，
// 混在一起会让装酒馆的人莫名收到一堆科研工具，也让人分不清该去哪儿升级。
//
// 刻意做成「开机就铺、无 UI、无路由」：技能是纯数据，铺好之后由 DSH 的技能
// 加载器接管，本包不再参与运行时。
import { fileURLToPath } from 'node:url'
import { existsSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { syncBundledSkills } from './skills-sync.js'

export const name = 'dsh-research-skills'
// 不依赖任何服务：只在 apply 里做文件同步，做完即结束。
export const inject = []

const PROFILE_DIR = fileURLToPath(new URL('..', import.meta.url))
const HOME_DIR = process.env.DSH_HOME || resolve(PROFILE_DIR, '../..')

function syncSkillsAtBoot() {
  try {
    // 技能放在本包 skills/。升级（重贴链接或覆盖 packages/*）时会一起刷新。
    const source = join(PROFILE_DIR, 'skills')
    if (!existsSync(source)) return
    const report = syncBundledSkills({
      source,
      target: join(HOME_DIR, 'skills'),
      backupRoot: join(HOME_DIR, 'skills-backup'),
      // 不覆盖 DSHM 环境自带的 ohos-* 说明，也不碰用户自装技能。
      preserve: ['ohos-'],
    })
    if (report.copied > 0 || report.backed > 0) {
      console.log('[research-skills] 已同步技能：' + JSON.stringify(report))
    }
  } catch (error) {
    console.warn('[research-skills] 技能同步失败：' + String((error && error.message) || error))
  }
}

export function apply() {
  syncSkillsAtBoot()
}
