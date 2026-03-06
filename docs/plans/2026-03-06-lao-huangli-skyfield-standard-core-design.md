# Lao Huangli Skyfield Standard Core Design

## 目标

把 `skills/lao-huangli` 的基础历法层从近似表升级为基于天文历算的实现，为后续对齐 `GB/T 33661-2017` 提供真实可扩展的底座。

## 方案

- 新增 `astronomy.py`，封装 `Skyfield + JPL ephemeris` 的天文事件查询。
- `calendar_core.py` 不直接做近似节气表判断，改为消费 `astronomy.py` 的节气与朔结果。
- 先完成可替换接口与最小落地：
  - 节气时刻查询
  - 节气窗口输出
  - 精度元数据从 `day-approximate` 升级为 `astronomical`
- 先不在这一轮一次性做完整的闰月/定朔农历重写，但会把接口与测试改成可继续推进的形态。

## 边界

- 这一轮优先升级 `solar_terms` 相关基础能力。
- 规则层 `rule_engine.py` 不做行为变化，只消费更准确的 `calendar_context`。
- 现有 `market-folk-v1 / xiejibianfang-v1 / bazi-v1` 输出结构保持兼容。

## 依赖策略

- 使用 `uv` 创建本地 `.venv`
- 安装 `skyfield` 与 `jplephem`
- 星历文件通过 `Skyfield` 标准加载方式管理

## 验证

- 先写失败测试，锁定：
  - `solar_terms.precision`
  - `solar_terms.calculationMode`
  - 节气交接时刻前后的窗口行为
- 再做最小实现并跑全量 `unittest`
