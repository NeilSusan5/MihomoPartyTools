#!/bin/bash

# 设置要清理的目录
LOG_DIR="."

# 检查目录是否存在
if [ ! -d "$LOG_DIR" ]; then
  echo "错误: 目录 $LOG_DIR 不存在。"
  exit 1
fi

# 删除所有.log文件
echo "正在从 $LOG_DIR 删除 .log 文件..."
find "$LOG_DIR" -name "*.log" -type f -delete

echo "清理完成，操作用户: $(whoami)。"
