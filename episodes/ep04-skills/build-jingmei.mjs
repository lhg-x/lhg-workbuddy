// 第4课分析 PPT —— jingmei-ppt（咨询研报配方）生成脚本
// 风格简报：分析性、紧凑、冷静；张力：数据密集但有人味儿。
// 配色角色：冷灰底 F2F4F7 / 白面板 / 近黑主文字 / 藏青+青色证据色 / 细灰线。
// 字体：微软雅黑（目标环境 Windows）。短 token 走 skill 的文本保护组件。
import PptxGenJS from "pptxgenjs";
import { addSingleLineToken } from "/home/hatch/workspace/custom-skills/jingmei-ppt/scripts/pptx-text-guards.mjs";

const FONT = "微软雅黑";
const BG = "F2F4F7", PANEL = "FFFFFF", INK = "1A2027", MUTED = "5A6B7C";
const NAVY = "1F4E79", TEAL = "0E7C7B", HAIRLINE = "D0D7DE", TINT = "E6F2F2";
const W = 13.333, H = 7.5, ML = 0.6, CW = W - ML * 2;

const pptx = new PptxGenJS();
pptx.defineLayout({ name: "WIDE", width: W, height: H });
pptx.layout = "WIDE";
pptx.title = "技能实在太多了，到底装哪个？";

let page = 0;
function folio(slide, color = MUTED) {
  page += 1;
  addSingleLineToken(slide, `${page}/9`, {
    x: 12.18, y: 7.08, w: 0.55, h: 0.3, fontFace: FONT, fontSize: 11, color, align: "right",
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
function bullets(slide, items, y0, size = 17, gap = 0.62) {
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
function dataTable(slide, header, rows, y0, colW) {
  const body = rows.map((r, i) => r.map((c, j) => ({
    text: c, options: {
      fontFace: FONT, fontSize: 15, color: INK, align: j === 0 ? "left" : "right",
      fill: { color: i % 2 === 0 ? PANEL : BG }, valign: "middle", margin: [0.05, 0.1, 0.05, 0.1],
    },
  })));
  const head = header.map((c, j) => ({
    text: c, options: {
      fontFace: FONT, fontSize: 15, bold: true, color: PANEL, align: j === 0 ? "left" : "right",
      fill: { color: NAVY }, valign: "middle", margin: [0.05, 0.1, 0.05, 0.1],
    },
  }));
  slide.addTable([head, ...body], {
    x: ML, y: y0, w: CW, colW, rowH: 0.58,
    border: { pt: 0.75, color: HAIRLINE }, valign: "middle",
  });
}

// P1 封面（藏青满版锚点）
{
  const s = pptx.addSlide();
  s.background = { color: NAVY };
  s.addShape(pptx.ShapeType.rect, { x: ML, y: 2.15, w: 1.2, h: 0.08, fill: { color: TEAL }, line: { type: "none" } });
  s.addText("第4课 · 分析篇", { x: ML, y: 1.55, w: CW, h: 0.4, fontFace: FONT, fontSize: 15, bold: true, color: "8EC8C8" });
  s.addText("技能实在太多了，到底装哪个？", { x: ML, y: 2.45, w: CW, h: 1.0, fontFace: FONT, fontSize: 40, bold: true, color: PANEL });
  s.addText("WorkBuddy 3 万多个 skill 的全量分析", { x: ML, y: 3.6, w: CW, h: 0.5, fontFace: FONT, fontSize: 18, color: "C7D6E4" });
  const anchors = [["31,740 条", "全量拉取"], ["99.4%", "覆盖率"], ["2026-10-26", "采集日期"]];
  anchors.forEach(([num, lab], i) => {
    const x = ML + i * 4.1;
    s.addText(num, { x, y: 5.7, w: 3.8, h: 0.6, fontFace: FONT, fontSize: 26, bold: true, color: PANEL });
    s.addText(lab, { x, y: 6.35, w: 3.8, h: 0.35, fontFace: FONT, fontSize: 13, color: "8EC8C8" });
  });
  folio(s, "8EC8C8");
}
// P2 别一个个翻了
{
  const s = pptx.addSlide();
  chrome(s, "钩子 · 共情", "别一个个翻了", null);
  bullets(s, [
    "打开 WorkBuddy：3 万多个 skill，翻半天挑不出来",
    "Coze 上也一样：技能越多，越不知道装哪个",
    "一个个翻，翻到崩溃也翻不完",
  ], 2.0, 19, 0.85);
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
// P4 Top5 表格
{
  const s = pptx.addSlide();
  chrome(s, "证据 · 下载量", "下载量最大的 5 个", "来源：WorkBuddy 客户端技能市场，采集 2026-10-26，使用量口径");
  dataTable(s, ["技能", "使用量"], [
    ["PDF 文档处理", "111 万次"], ["AI交付前自检", "93 万次"], ["NeoData金融搜索服务", "76 万次"],
    ["Skill安全审计", "66 万次"], ["Excel 表格处理", "59 万次"],
  ], 1.85, [8.13, 4.0]);
  takeaway(s, "头部 5 个里，3 个是办公场景。");
}
// P5 为什么
{
  const s = pptx.addSlide();
  chrome(s, "解读", "为什么偏偏是它们", null);
  bullets(s, [
    "天天用的办公刚需：PDF、Excel、PPT、Word 全是办公场景",
    "解决具体痛点：自检怕出错，去 AI 味怕被认出是 AI 写的",
    "最火的不是大厂做的：个人开发者占 31,556 个（99.4%），前两名都是个人开发者",
  ], 2.0, 18, 0.85);
}
// P6 分类表格
{
  const s = pptx.addSlide();
  chrome(s, "证据 · 分类", "3 万多个 skill，都分布在哪些分类", "来源：WorkBuddy 客户端技能市场，采集 2026-10-26，使用量口径");
  dataTable(s, ["分类", "数量"], [
    ["效率工具", "15,334"], ["办公协同", "7,681"], ["商业运营", "7,418"],
    ["内容创作", "6,714"], ["数据分析", "4,933"],
  ], 1.85, [8.13, 4.0]);
  takeaway(s, "效率工具一个分类就接近一半。");
}
// P7 倾向：原生柱状图 + 要点
{
  const s = pptx.addSlide();
  chrome(s, "证据 · 用户倾向", "大家最后都只用哪几类", "来源：WorkBuddy 客户端技能市场，采集 2026-10-26，使用量口径");
  s.addChart(pptx.ChartType.bar, [{ name: "占总使用量", labels: ["前 100 名", "前 1000 名"], values: [73, 92] }], {
    x: ML, y: 1.8, w: 6.2, h: 3.1, barDir: "bar", showLegend: false, dataLabelShowValue: true,
    chartColors: [NAVY, TEAL], fontFace: FONT, fontSize: 13,
  });
  const items = [
    "60% 的 skill 总使用量不到 10 次，其中 5062 个是 0 次",
    "最火的两个，都不在官方精选 21 个名单里",
    "打工人日常就四样：文档、表格、演示、知识库",
  ];
  items.forEach((t, i) => {
    s.addText(
      [{ text: "•  ", options: { color: TEAL, bold: true } }, { text: t, options: { color: INK } }],
      { x: 7.2, y: 1.95 + i * 0.85, w: 5.53, h: 0.8, fontFace: FONT, fontSize: 16, valign: "middle" }
    );
  });
  takeaway(s, "结论：大家只用头部那几个，挑 skill 看使用量，别只看精选。");
}
// P8 过渡
{
  const s = pptx.addSlide();
  chrome(s, "过渡", "筛完，剩下这 8 个", null);
  bullets(s, ["下次一页页翻给你看"], 2.0, 19, 0.85);
}
// P9 口径
{
  const s = pptx.addSlide();
  chrome(s, "附录", "数据口径", null);
  bullets(s, [
    "来源：WorkBuddy 客户端技能市场，采集 2026-10-26，使用量口径",
    "一个 skill 可挂多个分类，分类数量合计大于 skill 总数",
  ], 2.0, 18, 0.85);
}

await pptx.writeFile({ fileName: "/tmp/jingmei-build/lesson4-analysis-jingmei.pptx" });
console.log("写出 /tmp/jingmei-build/lesson4-analysis-jingmei.pptx");
