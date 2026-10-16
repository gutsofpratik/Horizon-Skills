#!/usr/bin/env bash
# 断舍离 archive — 把 skill 目录挪进归档（永不 rm），记 MANIFEST，一键可恢复。
# 兼容 macOS 自带 bash 3.2。
set -euo pipefail

ROOT="${DANSHARI_ARCHIVE:-$HOME/.claude/skills-archive}"
MANIFEST="$ROOT/MANIFEST.tsv" # 列: 时间  动作  名字  原路径  归档路径  原因

usage() {
  cat <<'EOF'
用法:
  archive.sh <skill-dir> [<skill-dir>...] [--reason "为什么"]   归档（挪走，不删除）
  archive.sh --list                                             列出归档记录
  archive.sh --restore <name>                                   按名字恢复到原路径
归档根: $DANSHARI_ARCHIVE（默认 ~/.claude/skills-archive）
EOF
  exit 1
}

[ $# -ge 1 ] || usage
mkdir -p "$ROOT"

case "$1" in
--list)
  [ -f "$MANIFEST" ] || { echo "归档为空：$ROOT"; exit 0; }
  { printf '时间\t动作\t名字\t原路径\t归档路径\t原因\n'; cat "$MANIFEST"; } | column -t -s "$(printf '\t')"
  ;;
--restore)
  name="${2:?用法: archive.sh --restore <name>}"
  [ -f "$MANIFEST" ] || { echo "没有 MANIFEST：$MANIFEST"; exit 1; }
  line=$(awk -F '\t' -v n="$name" '$2=="archive" && $3==n' "$MANIFEST" | tail -1)
  [ -n "$line" ] || { echo "MANIFEST 里没有名为 $name 的归档记录"; exit 1; }
  orig=$(printf '%s' "$line" | cut -f4)
  arch=$(printf '%s' "$line" | cut -f5)
  [ -d "$arch" ] || { echo "归档目录不见了：$arch（也许已恢复过）"; exit 1; }
  [ ! -e "$orig" ] || { echo "原路径已被占用：$orig —— 请手动处理后重试"; exit 1; }
  mkdir -p "$(dirname "$orig")"
  mv "$arch" "$orig"
  printf '%s\trestore\t%s\t%s\t%s\t-\n' "$(date +%FT%T)" "$name" "$orig" "$arch" >>"$MANIFEST"
  echo "已恢复：$orig"
  ;;
*)
  reason="-"
  dirs=""
  while [ $# -gt 0 ]; do
    case "$1" in
    --reason)
      reason="${2:?--reason 需要内容}"
      reason=$(printf '%s' "$reason" | tr '\t\n' '  ')
      shift 2
      ;;
    --*) usage ;;
    *)
      dirs="$dirs$1
"
      shift
      ;;
    esac
  done
  [ -n "$dirs" ] || usage
  day=$(date +%F)
  dest_day="$ROOT/$day"
  mkdir -p "$dest_day"
  printf '%s' "$dirs" | while IFS= read -r d; do
    [ -n "$d" ] || continue
    if [ ! -d "$d" ]; then
      echo "跳过（不是目录）：$d"
      continue
    fi
    abs=$(cd "$d" && pwd)
    name=$(basename "$abs")
    dest="$dest_day/$name"
    i=2
    while [ -e "$dest" ]; do
      dest="$dest_day/$name-$i"
      i=$((i + 1))
    done
    mv "$abs" "$dest"
    printf '%s\tarchive\t%s\t%s\t%s\t%s\n' "$(date +%FT%T)" "$name" "$abs" "$dest" "$reason" >>"$MANIFEST"
    echo "已归档：$abs → $dest"
  done
  echo "恢复：$0 --restore <name>"
  ;;
esac
