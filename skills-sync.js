// skills-sync.js — 把本包 skills/ 铺到 <dsh-home>/skills/
//
// 与 dsh-tavern-gate 里的同名文件逻辑一致（刻意保持独立拷贝：两个包不该互相依赖，
// 否则装一个就得装另一个）。
//
// 规则（幂等）：
//   · 目标不存在      → 写入
//   · 内容完全相同    → 不写盘（正常启动零 IO 写）
//   · 内容不同        → 旧文件先备份到 <home>/skills-backup/<时间戳>/ 再覆盖
//
// 备份目录刻意放在 skills/ 之外：放在里面会被技能加载器当成一个技能目录。
// 只覆盖同名文件，不删除 <home>/skills 下用户自己放的任何技能。
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs'
import { dirname, join } from 'node:path'

const SKIP_NAMES = new Set(['.DS_Store', 'Thumbs.db', '.git', '.virtfs_metadata', '__pycache__'])

function listFiles(root, prefix) {
  const out = []
  for (const entry of readdirSync(join(root, prefix), { withFileTypes: true })) {
    if (SKIP_NAMES.has(entry.name)) continue
    const rel = prefix === '' ? entry.name : prefix + '/' + entry.name
    if (entry.isDirectory()) out.push(...listFiles(root, rel))
    else if (entry.isFile()) out.push(rel)
  }
  return out
}

export function syncBundledSkills({ source, target, backupRoot, preserve = [] }) {
  if (typeof source !== 'string' || source === '' || !existsSync(source)) {
    return { status: 'no-source', source }
  }
  const files = listFiles(source, '')
  if (files.length === 0) return { status: 'empty-source', source }

  mkdirSync(target, { recursive: true })
  const stamp = new Date().toISOString().replaceAll(':', '-').replaceAll('.', '-')
  const backupDir = join(backupRoot, stamp)
  let copied = 0
  let same = 0
  let backed = 0

  for (const rel of files) {
    const top = rel.split('/')[0]
    if (preserve.some((prefix) => top.startsWith(prefix))) continue
    const src = join(source, rel)
    const dst = join(target, rel)
    let existing
    try { existing = readFileSync(dst) } catch {}
    const next = readFileSync(src)
    if (existing !== undefined && existing.equals(next)) { same += 1; continue }
    if (existing !== undefined) {
      const backupPath = join(backupDir, rel)
      mkdirSync(dirname(backupPath), { recursive: true })
      writeFileSync(backupPath, existing)
      backed += 1
    }
    mkdirSync(dirname(dst), { recursive: true })
    writeFileSync(dst, next)
    copied += 1
  }
  return { status: 'ok', copied, same, backed }
}
