# final-submission-executor

面向科研与图件生产项目"最后一公里"的 Agent Skill：把一份 final execution 规格变成真正写入磁盘、经过检查并完成同步的交付物。

适用场景是"再写一份清单就等于失败"的阶段。它把流程固定下来：复用已有有效结果、解决阻塞、只计算缺失部分、渲染并目视检查、原子覆盖 canonical 文件、同步登记信息、按实测结果汇报完成情况。

它不提供数据、算力或领域判断，只提供一套防止"看起来完成的包"被当成"真正完成的包"的纪律。

## 安装

克隆到你的 Agent 读取 skills 的目录：

```bash
git clone https://github.com/mingeric/final-submission-executor.git
# 将生成的目录放到客户端识别的项目 skill 位置
```

仅依赖 Python 3.9+ 标准库。

## 快速开始

```bash
python3 scripts/check_skill.py .
python3 -m unittest discover -s tests -v

python3 scripts/validate_final_submission.py \
  --workspace path/to/project \
  --ledger path/to/project/TASK_LEDGER.tsv \
  --manifest path/to/project/CANONICAL_MANIFEST.tsv
```

校验器输出 JSON 报告；只要 canonical 文件缺失、无法解码、颜色模式/尺寸/DPI 不符、SHA256 不匹配，或任务台账中存在未处理的 PENDING 项，就以非零退出。写明具体原因的 `BLOCKED` 可以通过；没有原因的阻塞不能。

## 执行方式

1. 只读规格一次，提取权威路径、写入范围、交付契约与验收条件。
2. 把 `templates/TASK_LEDGER.tsv` 复制到项目，为每个可独立验收的任务建一行。
3. 按顺序解决阻塞：环境、路径、归属、可读性、过期 staging 产物。
4. 只用可追溯来源；保留真实阴性结果；防止泄漏与伪重复。
5. 渲染、看整图、看密集区域裁片，发现问题就修并重新渲染。
6. 逐个提交验证过的替换：备份 → 原子交换 → 重算哈希 → 同步 manifest/registry/图注/稿件。
7. 只清理授权目录内已核实的冗余文件。
8. 按磁盘实测填写 `templates/FINAL_ACCEPTANCE.md`。

细节见 `references/`：执行契约、阻塞处理、科学计算门禁、视觉 QA、覆盖协议、最终汇报格式。

## 边界

校验器检查的是证据字段，不是科学真伪。它无法判断分析设计是否合理，也无法判断图件是否如实反映数据。这些判断由执行者承担；未解决的证据缺口必须如实报告，不能用看似合理的结果填补。

## 许可

MIT，见 `LICENSE`。
