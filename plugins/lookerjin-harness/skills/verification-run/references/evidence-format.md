# 可选证据导出格式

负责人先从用户目标与项目配方确定验收 ID，再将运行记录导出。示例中的占位值必须由实际内容替换：

```json
{
  "version": 1,
  "records": [{
    "id": "public-entry",
    "criterion": "调用公开入口得到约定结果和副作用",
    "surface": "CLI / UI / API 的具体入口",
    "conditions": "输入、数据与配置前提",
    "action": "实际执行的命令或操作",
    "expected": "应观察到的结果",
    "observed": "实际观察结果",
    "environment": "实际运行器、构建和环境身份；不含秘密",
    "observed_at": "2026-10-23T00:00:00Z",
    "boundaries": ["未覆盖的真实外部服务"],
    "status": "VERIFIED",
    "inputs": [{"path": "src/app.py", "sha256": "实际文件 SHA-256"}],
    "artifacts": [{"path": "evidence/run.log", "sha256": "实际日志 SHA-256"}]
  }]
}
```

```bash
python <skill>/scripts/check-evidence.py <records.json> --root <project> --require public-entry
```

每项验收用一次 `--require`；要求来自任务契约，不能只把报告里刚好通过的 ID 作为完整目标。`inputs` 列声明结论实际依赖的源码、配置、锁文件或构建产物；有未提交修改时也按实际文件指纹绑定。`artifacts` 是仍存在的原始证据。路径相对 root，拒绝目录逃逸、符号链接和重复路径；工具不联网、不启动被测程序、不写项目文件。

VERIFIED 要求非空 inputs / artifacts；NOT_VERIFIED 的 reason 为 FAILED 或 NOT_RUN；INCONCLUSIVE 给出具体 reason。未执行可保留空数组，但必须明确各字段未取得的内容。时间为带时区 ISO 时间，不能用报告时间冒充运行时间。

退出 0 只意味着：声明的必要 ID 全为 VERIFIED，记录字段完整，文件仍存在且哈希一致。它不证明动作确实运行过、日志是真的、输入依赖列全了、环境相同或结论正确。负责人必须核对原始记录及语义。任一必要项未通过、缺失或文件变化则退出 1。脚本不自动刷新指纹来掩盖旧证据。
