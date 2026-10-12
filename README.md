# claude-orange-ysm

非官方 Claude 女性拟人 **YSM（是，史蒂夫模型 / Yes Steve Model）** 玩家模型：铜橙长发、琥珀棕瞳、普通人耳与橙白长裙，围裙配放射花形标志。保留眨眼，头发带随走动和转身变化的骨骼弹性摆动。

> 这是 Java 版 YSM 的 3D 玩家模型，**不是**原版皮肤 PNG，也不是基岩版附加包。
> 本项目是非官方同人二创，与 Anthropic 无隶属关系，未声称得到其官方授权或认可。

## 下载

到 [Releases](../../releases) 下载 `claude_orange.zip`，或直接克隆本仓库使用 `claude_orange/` 文件夹（两者内容一致）。

## 安装

### 单人

1. 找到实际游戏目录，即同时含 `mods`、`config` 的目录；Prism 实例内可能名为 `minecraft`。
2. 把 `claude_orange` 文件夹（或 `claude_orange.zip`）放进 `config/yes_steve_model/custom/`。
3. 确认路径是 `custom/claude_orange/ysm.json`，不能多套一层同名文件夹。
4. 进游戏执行 `/ysm model reload`；无权限就退出存档再进入，仍不更新则重启游戏。
5. 按键设置 →「是，史蒂夫模型 → 打开玩家模型界面」，搜索 Claude 选择。

### 服务器

放进服务器的 `config/yes_steve_model/custom/`，再在控制台执行 `ysm model reload`。玩家客户端也应使用匹配版本的 YSM。

文件夹与 ZIP 二选一，避免菜单里出现重复项。

## 运行环境

- Minecraft Java 版 1.21.1
- NeoForge 21.1.217
- [Yes Steve Model 2.6.5](https://modrinth.com/mod/yes-steve-model)（不随本仓库分发）
- Windows 11 —— 其它系统、加载器、YSM 版本未做兼容验收

## 内容

- 无头饰，暖橙配色，普通人耳，无尾巴，加长裙与分层长发
- 30 根骨骼的弹性摆动，保留原眨眼与动作
- 琥珀棕瞳，围裙放射花形标志
- 轮盘名称、道具与头顶字幕包含 B 站 Claude 娘同人梗，动画 ID 未改，表情映射不受影响

## 本版不含音频

0.2.1 起删除了 `sounds/` 全部 14 个 OGG。原工程里只有 `get_down`、`zufolo_impazzito` 被实际引用，分别是 `getdown`（36 秒）和 `乱舞`（23 秒）的舞蹈 BGM，其余 12 个无任何 JSON 引用；因全部音频的作者与再分发授权都无法确认，故整体移除。

**这两个舞蹈动作照常能跳，只是没有音乐。** 想听就自己在游戏外播放。

## 署名

| 作者 | 贡献 |
| --- | --- |
| Maks | 原始模型 |
| Ykisan | 原始动画 |
| muxueliunian | 二创改造：暖橙材质、长裙与后发造型、围裙标志、眼睛与脸颊 |

原始工程是 DeepSeek 鲸鱼娘（`ds_whale`），原授权字段为 `All Right Reserved / 保留所有权利`，该字段在模型中保留未改。本二创在获得原作者同意的范围内发布。详见 [作者与来源.txt](作者与来源.txt)。

## 自己构建

```bash
python tools/build.py
```

需要 Python 3.10 或以上，只用标准库，不联网、不修改游戏。脚本会校验清单引用、骨骼层级、JSON 与 PNG 尺寸，逐字节比对生成的 ZIP，输出到 `dist/claude_orange.zip`。

## 已知限制

- 头发是骨骼弹性摆动，没有发丝碰撞；游泳、鞘翅、睡姿尚未完整回归。
- 0.2.0 的贴图与轮盘名称改动尚未进游戏逐项验收。
- 使用光影时颜色随照明变化。

## 授权

**保留所有权利。** 转载、搬运、整合进整合包，以及二次创作后发布，都请先联系作者取得同意；个人自用不需要额外许可。原作品的著作权归 Maks、Ykisan 所有。详见 [LICENSE.md](LICENSE.md)。
