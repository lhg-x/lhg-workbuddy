// 第4课分析 PPT —— 嵌图版（jingmei 咨询研报配方 + 幻灯片版纯图）
// 流程：封面 → 钩子 → 方法 → 时间线 → 集中度 → 分层 → 长尾 → 来源 → 榜单 → 分类 → 人群 → 筛完+口径
// 风格：冷灰底 F2F4F7 / 白面板（图本身）/ 藏青+青色 / 微软雅黑
import PptxGenJS from "pptxgenjs";
import fs from "node:fs";
import { addSingleLineToken } from "/home/hatch/workspace/custom-skills/jingmei-ppt/scripts/pptx-text-guards.mjs";

const FONT = "微软雅黑";
const BG = "F2F4F7", PANEL = "FFFFFF", INK = "1A2027", MUTED = "5A6B7C";
const NAVY = "1F4E79", TEAL = "0E7C7B", HAIRLINE = "D0D7DE", TINT = "E6F2F2";
const W = 13.333, H = 7.5, ML = 0.6, CW = W - ML * 2;
const CH = "/home/hatch/workspace/skill-market-research/charts/slide";
const TOTAL = 12;

const pptx = new PptxGenJS();
pptx.defineLayout({ name: "WIDE", width: W, height: H });
pptx.layout = "WIDE";
pptx.title = "技能实在太多了，到底装哪个？";

let page = 0;
function folio(slide, color = MUTED) {
  page += 1;
  addSingleLineToken(slide, `${page}/${TOTAL}`, {
    x: 12.03, y: 7.08, w: 0.75, h: 0.3, fontFace: FONT, fontSize: 11, color, align: "right",
  });
}
function chrome(slide, label, title, source) {
  slide.background = { color: BG };
  slide.addText(label, { x: ML, y: 0.35, w: CW, h: 0.3, fontFace: FONT, fontSize: 12, bold: true, color: TEAL });
  slide.addText(title, { x: ML, y: 0.68, w: CW, h: 0.7, fontFace: FONT, fontSize: 28, bold: true, color: INK });
  slide.addShape(pptx.ShapeType.rect, { x: ML, y: 1.48, w: CW, h: 0.02, fill: { color: HAIRLINE }, line: { type: "none" } });
  if (source) slide.addText(source, { x: ML, y: 7.08, w: 9.0, h: 0.3, fontFace: FONT, fontSize: 10, color: MUTED });
  folio(slide);
}
function bullets(slide, items, y0, size = 18, gap = 0.85) {
  items.forEach((t, i) => {
    slide.addText(
      [{ text: "•  ", options: { color: TEAL, bold: true } }, { text: t, options: { color: INK } }],
      { x: ML, y: y0 + i * gap, w: CW, h: 0.55, fontFace: FONT, fontSize: size, valign: "middle" }
    );
  });
}
function takeaway(slide, text, y = 6.45) {
  slide.addShape(pptx.ShapeType.rect, { x: ML, y, w: CW, h: 0.55, fill: { color: TINT }, line: { type: "none" } });
  slide.addShape(pptx.ShapeType.rect, { x: ML, y, w: 0.08, h: 0.55, fill: { color: TEAL }, line: { type: "none" } });
  slide.addText(text, { x: ML + 0.3, y, w: CW - 0.5, h: 0.55, fontFace: FONT, fontSize: 15, bold: true, color: NAVY, valign: "middle" });
}
// 图按 contain 方式放进图区（x 0.6 / y 1.65 / w 12.13 / h 4.65），不变形、不溢出
function chartImage(slide, file) {
  const buf = fs.readFileSync(`${CH}/${file}`);
  const iw = buf.readUInt32BE(16), ih = buf.readUInt32BE(20);
  const bx = ML, by = 1.65, bw = CW, bh = 4.65;
  const s = Math.min(bw / iw, bh / ih);
  slide.addImage({ path: `${CH}/${file}`, x: bx + (bw - iw * s) / 2, y: by + (bh - ih * s) / 2, w: iw * s, h: ih * s });
}
function chartSlide(label, title, file, source, take) {
  const s = pptx.addSlide();
  chrome(s, label, title, source);
  chartImage(s, file);
  takeaway(s, take);
}

// P1 封面
{
  const s = pptx.addSlide();
  s.background = { color: NAVY };
  s.addShape(pptx.ShapeType.rect, { x: ML, y: 2.15, w: 1.2, h: 0.08, fill: { color: TEAL }, line: { type: "none" } });
  s.addText("第4课 · 分析篇", { x: ML, y: 1.55, w: CW, h: 0.4, fontFace: FONT, fontSize: 15, bold: true, color: "8EC8C8" });
  s.addText("技能实在太多了，到底装哪个？", { x: ML, y: 2.45, w: CW, h: 1.0, fontFace: FONT, fontSize: 40, bold: true, color: PANEL });
  s.addText("WorkBuddy 3 万多个 skill 的全量分析", { x: ML, y: 3.6, w: CW, h: 0.5, fontFace: FONT, fontSize: 18, color: "C7D6E4" });
  const anchors = [["31,740 条", "全量拉取"], ["1,380 万次", "总使用量"], ["2 小时", "AI 爬取用时"]];
  anchors.forEach(([num, lab], i) => {
    const x = ML + i * 4.1;
    s.addText(num, { x, y: 5.7, w: 3.8, h: 0.6, fontFace: FONT, fontSize: 26, bold: true, color: PANEL });
    s.addText(lab, { x, y: 6.35, w: 3.8, h: 0.35, fontFace: FONT, fontSize: 13, color: "8EC8C8" });
  });
  folio(s, "8EC8C8");
}
// P2 钩子
{
  const s = pptx.addSlide();
  chrome(s, "钩子 · 共情", "别一个个翻了", null);
  bullets(s, [
    "打开 WorkBuddy：3 万多个 skill，翻半天挑不出来",
    "Coze 上也一样：技能越多，越不知道装哪个",
    "一个个翻，翻到崩溃也翻不完",
  ], 2.0, 19, 0.85);
  takeaway(s, "3 万多个 skill，一个个翻，翻到崩溃也翻不完。");
}
// P3 方法
{
  const s = pptx.addSlide();
  chrome(s, "方法", "我用 AI，两个小时全扒下来了", null);
  const kpis = [["31,740", "全量拉取条数", "服务端 31,940"], ["99.4%", "覆盖率", "基本就是全量"], ["2 小时", "AI 爬取用时", "人只做判断"]];
  kpis.forEach(([num, lab, note], i) => {
    const x = ML + i * (3.84 + 0.3);
    s.addShape(pptx.ShapeType.rect, { x, y: 1.75, w: 3.84, h: 1.9, fill: { color: PANEL }, line: { type: "none" } });
    s.addShape(pptx.ShapeType.rect, { x, y: 1.75, w: 3.84, h: 0.07, fill: { color: TEAL }, line: { type: "none" } });
    s.addText(num, { x: x + 0.25, y: 2.0, w: 3.34, h: 0.65, fontFace: FONT, fontSize: 30, bold: true, color: NAVY, align: "left" });
    s.addText(lab, { x: x + 0.25, y: 2.75, w: 3.34, h: 0.35, fontFace: FONT, fontSize: 14, bold: true, color: INK });
    s.addText(note, { x: x + 0.25, y: 3.15, w: 3.34, h: 0.35, fontFace: FONT, fontSize: 12, color: MUTED });
  });
  bullets(s, ["按使用量排序", "按分类、来源分层", "按打工人日常能不能用上过滤"], 4.05, 17, 0.62);
  takeaway(s, "方法就一句：让 AI 干爬数据的活，人只做判断。");
}
// P4-P11 图页
chartSlide("证据 · 市场", "87% 的 skill，都是最近两个月冒出来的", "s01_timeline.png",
  "来源：WorkBuddy 客户端技能市场，采集 2026-10-26", "9 月一个月上 1.3 万个，10 月又 1.8 万个。");
chartSlide("证据 · 集中度", "前 100 名，占了 73% 的使用量", "s02_concentration.png",
  "来源：WorkBuddy 客户端技能市场，采集 2026-10-26", "前 100 名只占 0.3%，却占了 73% 的使用量。");
chartSlide("证据 · 分层", "头部 22 个，占了一半以上", "s03_tiers.png",
  "来源：WorkBuddy 客户端技能市场，采集 2026-10-26", "头部 22 个占一半以上，剩下 3 万多个分剩下的。");
chartSlide("证据 · 长尾", "88% 的 skill，不足 100 次", "s04_longtail.png",
  "来源：WorkBuddy 客户端技能市场，采集 2026-10-26", "88% 的 skill 不足 100 次，上架基本等于没上架。");
chartSlide("解读 · 为什么", "人多不代表用得多", "s05_sources.png",
  "来源：WorkBuddy 客户端技能市场，采集 2026-10-26", "个人开发者 3 万多个，平均才 286 次。");
chartSlide("证据 · 榜单", "下载量最大的 15 个", "s06_top15.png",
  "来源：WorkBuddy 客户端技能市场，采集 2026-10-26", "前 15 个里，办公场景占一半以上。");
chartSlide("证据 · 分类", "大家最后都只用哪几类", "s07_categories.png",
  "来源：WorkBuddy 客户端技能市场，采集 2026-10-26", "效率工具 687 万次，办公协同 510 万次，遥遥领先。");
chartSlide("证据 · 人群", "一半以上的使用量，是打工人贡献的", "s08_audience.png",
  "来源：WorkBuddy 客户端技能市场，采集 2026-10-26", "按使用量排，再按打工人日常能不能用上过滤。");
// P12 收尾 + 口径
{
  const s = pptx.addSlide();
  chrome(s, "过渡 · 附录", "筛完，剩下这 8 个", null);
  bullets(s, [
    "下次一页页翻给你看",
    "数据口径：来源 WorkBuddy 客户端技能市场，采集 2026-10-26，使用量口径",
    "一个 skill 可挂多个分类，分类数量合计大于 skill 总数",
    "人群足迹跨人群有重叠，数字为相对比较；上架时间可能被重提重置",
    "转化率口径不一，仅作相对参考",
  ], 2.0, 17, 0.75);
  takeaway(s, "按使用量排，再按打工人日常过滤，筛完剩下这 8 个。");
}

await pptx.writeFile({ fileName: "/home/hatch/workspace/lhg-workbuddy/episodes/ep04-skills/lesson4-analysis-charts.pptx" });
console.log("写出 lesson4-analysis-charts.pptx，12 页");
