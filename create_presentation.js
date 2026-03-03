#!/usr/bin/env node

const pptxgen = require("pptxgenjs");

// Initialize presentation
const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.author = 'Renewable Energy Initiative';
pres.title = 'The Future of Renewable Energy';

// Ocean Gradient Palette
const colors = {
  primary: "065A82",      // Deep ocean blue
  secondary: "1C7293",    // Medium ocean blue
  accent: "21295C",       // Dark navy accent
  light: "E8F4F8",        // Light blue-white
  white: "FFFFFF",
  darkGray: "2D3E50",
  lightGray: "F0F2F5"
};

// Font configuration
const fonts = {
  header: "Georgia",
  body: "Calibri"
};

// Helper to create shadow
const makeShadow = () => ({
  type: "outer",
  color: "000000",
  blur: 8,
  offset: 3,
  angle: 135,
  opacity: 0.15
});

// Helper to create colored circle icon
function addCircleIcon(slide, x, y, size, bgColor, text, textColor = "FFFFFF", fontSize = 18) {
  slide.addShape(pres.shapes.OVAL, {
    x: x, y: y, w: size, h: size,
    fill: { color: bgColor },
    line: { color: "FFFFFF", width: 2 },
    shadow: makeShadow()
  });
  slide.addText(text, {
    x: x, y: y, w: size, h: size,
    fontSize: fontSize, bold: true, color: textColor,
    align: "center", valign: "middle", fontFace: fonts.body
  });
}

// SLIDE 1: Title Slide (Dark background)
const slide1 = pres.addSlide();
slide1.background = { color: colors.primary };

// Decorative shape at top
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 1.2,
  fill: { color: colors.accent }
});

// Large title
slide1.addText("The Future of Renewable Energy", {
  x: 0.5, y: 1.5, w: 9, h: 1.2,
  fontSize: 54, bold: true, color: colors.white,
  align: "center", fontFace: fonts.header
});

// Decorative line
slide1.addShape(pres.shapes.RECTANGLE, {
  x: 2.5, y: 2.8, w: 5, h: 0.08,
  fill: { color: colors.secondary }
});

// Subtitle
slide1.addText("Harnessing Clean Energy for Tomorrow", {
  x: 0.5, y: 3.2, w: 9, h: 0.6,
  fontSize: 28, color: colors.light, italic: true,
  align: "center", fontFace: fonts.header
});

// Footer
slide1.addText("Renewable Energy Initiative | 2026", {
  x: 0.5, y: 5, w: 9, h: 0.4,
  fontSize: 14, color: "CCCCCC",
  align: "center", fontFace: fonts.body
});

slide1.notes = "Welcome to the presentation on the future of renewable energy. This presentation covers key trends, statistics, and opportunities in the renewable energy sector. We will explore solar, wind, hydro, and emerging technologies shaping the clean energy landscape.";

// SLIDE 2: Agenda (2-column layout with boxes)
const slide2 = pres.addSlide();
slide2.background = { color: colors.lightGray };

slide2.addText("Agenda", {
  x: 0.5, y: 0.3, w: 9, h: 0.5,
  fontSize: 40, bold: true, color: colors.primary,
  fontFace: fonts.header
});

slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 0.78, w: 9.2, h: 0.05,
  fill: { color: colors.secondary }
});

// Left column
const agendaBoxes = [
  { title: "Current State", desc: "Global renewable capacity & adoption" },
  { title: "Solar Power", desc: "Leading technology in growth" },
  { title: "Wind Energy", desc: "Onshore & offshore developments" }
];

let yPos = 1.2;
agendaBoxes.forEach((item, idx) => {
  slide2.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: yPos, w: 4.2, h: 1,
    fill: { color: colors.white },
    line: { color: colors.secondary, width: 2 },
    shadow: makeShadow()
  });
  slide2.addText(item.title, {
    x: 0.6, y: yPos + 0.1, w: 4, h: 0.35,
    fontSize: 16, bold: true, color: colors.primary,
    fontFace: fonts.header
  });
  slide2.addText(item.desc, {
    x: 0.6, y: yPos + 0.45, w: 4, h: 0.45,
    fontSize: 12, color: colors.darkGray,
    fontFace: fonts.body, valign: "top"
  });
  yPos += 1.15;
});

// Right column
const agendaBoxes2 = [
  { title: "Hydroelectric", desc: "Stable renewable base load power" },
  { title: "Emerging Tech", desc: "Geothermal, tidal, and hydrogen" },
  { title: "Future Vision", desc: "Path to carbon-neutral energy" }
];

yPos = 1.2;
agendaBoxes2.forEach((item, idx) => {
  slide2.addShape(pres.shapes.RECTANGLE, {
    x: 5.3, y: yPos, w: 4.2, h: 1,
    fill: { color: colors.light },
    line: { color: colors.primary, width: 2 },
    shadow: makeShadow()
  });
  slide2.addText(item.title, {
    x: 5.4, y: yPos + 0.1, w: 4, h: 0.35,
    fontSize: 16, bold: true, color: colors.accent,
    fontFace: fonts.header
  });
  slide2.addText(item.desc, {
    x: 5.4, y: yPos + 0.45, w: 4, h: 0.45,
    fontSize: 12, color: colors.darkGray,
    fontFace: fonts.body, valign: "top"
  });
  yPos += 1.15;
});

slide2.notes = "This presentation is organized into six key sections. We'll start with the current global state of renewable energy, then dive deep into the three major renewable sources: solar, wind, and hydroelectric power. Following that, we'll explore emerging technologies like geothermal and hydrogen. Finally, we'll discuss our vision for a sustainable energy future.";

// SLIDE 3: Global Renewable Energy Statistics (Large stat callouts)
const slide3 = pres.addSlide();
slide3.background = { color: colors.white };

slide3.addText("Global Renewable Energy Statistics", {
  x: 0.5, y: 0.3, w: 9, h: 0.5,
  fontSize: 40, bold: true, color: colors.primary,
  fontFace: fonts.header
});

slide3.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 0.78, w: 9.2, h: 0.05,
  fill: { color: colors.secondary }
});

// Stat boxes
const stats = [
  { number: "29%", label: "Global Electricity\nfrom Renewables", color: colors.primary },
  { number: "3.8T", label: "Capacity Installed\n(GW)", color: colors.secondary },
  { number: "12%", label: "Annual Growth\nRate", color: colors.accent }
];

let xPos = 0.7;
stats.forEach((stat) => {
  // Background box
  slide3.addShape(pres.shapes.RECTANGLE, {
    x: xPos, y: 1.3, w: 2.8, h: 3.5,
    fill: { color: "F5F9FB" },
    line: { color: stat.color, width: 3 },
    shadow: makeShadow()
  });

  // Accent bar at top
  slide3.addShape(pres.shapes.RECTANGLE, {
    x: xPos, y: 1.3, w: 2.8, h: 0.15,
    fill: { color: stat.color }
  });

  // Number in large font
  slide3.addText(stat.number, {
    x: xPos + 0.1, y: 1.8, w: 2.6, h: 1,
    fontSize: 48, bold: true, color: stat.color,
    align: "center", fontFace: fonts.header
  });

  // Label
  slide3.addText(stat.label, {
    x: xPos + 0.1, y: 2.95, w: 2.6, h: 1,
    fontSize: 14, color: colors.darkGray,
    align: "center", valign: "middle", fontFace: fonts.body
  });

  xPos += 3.1;
});

slide3.notes = "As of 2026, renewable energy represents 29% of global electricity generation, up from 26% in 2024. The world has installed approximately 3.8 trillion watts of renewable capacity, with an annual growth rate of 12%. This accelerating growth is driven by falling costs, government incentives, and corporate commitments to sustainability. Solar and wind are the primary growth drivers.";

// SLIDE 4: Renewable Energy Mix (Pie Chart + Text Columns)
const slide4 = pres.addSlide();
slide4.background = { color: colors.lightGray };

slide4.addText("Energy Mix Composition", {
  x: 0.5, y: 0.3, w: 9, h: 0.5,
  fontSize: 40, bold: true, color: colors.primary,
  fontFace: fonts.header
});

slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 0.78, w: 9.2, h: 0.05,
  fill: { color: colors.secondary }
});

// Pie Chart
const pieData = [{
  name: "Renewable Mix",
  labels: ["Hydroelectric", "Wind", "Solar", "Biomass", "Other"],
  values: [40, 35, 18, 5, 2]
}];

slide4.addChart(pres.charts.PIE, pieData, {
  x: 0.5, y: 1.2, w: 4.5, h: 3.8,
  chartColors: [colors.primary, colors.secondary, colors.accent, "2E7D32", "90CAF9"],
  showTitle: false,
  showPercent: true,
  dataLabelPosition: "outEnd",
  dataLabelFontSize: 12,
  chartArea: { fill: { color: colors.white }, roundedCorners: true }
});

// Text box with breakdown
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 5.3, y: 1.2, w: 4.2, h: 3.8,
  fill: { color: colors.white },
  line: { color: colors.primary, width: 2 },
  shadow: makeShadow()
});

const breakdownText = [
  { text: "RENEWABLE BREAKDOWN\n\n", options: { bold: true, fontSize: 14, color: colors.primary, breakLine: true } },
  { text: "Hydroelectric: 40%\nMost mature technology\n\n", options: { fontSize: 11, breakLine: true } },
  { text: "Wind Power: 35%\nRapid expansion globally\n\n", options: { fontSize: 11, breakLine: true } },
  { text: "Solar Energy: 18%\nFastest growing segment\n\n", options: { fontSize: 11, breakLine: true } },
  { text: "Biomass: 5%\nRenewable organic matter\n\n", options: { fontSize: 11, breakLine: true } },
  { text: "Other: 2%\nGeothermal, tidal", options: { fontSize: 11 } }
];

slide4.addText(breakdownText, {
  x: 5.5, y: 1.4, w: 3.8, h: 3.4,
  fontFace: fonts.body,
  color: colors.darkGray,
  valign: "top"
});

slide4.notes = "The renewable energy mix shows hydroelectric power still leading at 40% due to its maturity and reliability. Wind power has grown to 35% and is increasingly cost-competitive. Solar energy, while only 18% today, is the fastest-growing segment with year-over-year capacity additions exceeding all other sources. Biomass and emerging technologies like geothermal contribute smaller but growing shares.";

// SLIDE 5: Solar Power Overview (Icon + Text Rows)
const slide5 = pres.addSlide();
slide5.background = { color: colors.white };

slide5.addText("Solar Power Revolution", {
  x: 0.5, y: 0.3, w: 9, h: 0.5,
  fontSize: 40, bold: true, color: colors.primary,
  fontFace: fonts.header
});

slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 0.78, w: 9.2, h: 0.05,
  fill: { color: colors.secondary }
});

// Icon + text rows
const solarPoints = [
  { icon: "☀", color: colors.primary, title: "Photovoltaic Efficiency", desc: "Modern panels achieve 20-22% efficiency, up from 15% in 2015" },
  { icon: "📈", color: colors.secondary, title: "Cost Reduction", desc: "70% price drop over last decade drives widespread adoption" },
  { icon: "🏠", color: colors.accent, title: "Rooftop Integration", desc: "Residential solar installations now account for 35% of capacity" },
  { icon: "🔋", color: "2E7D32", title: "Battery Storage", desc: "Paired with energy storage systems for 24/7 renewable power" }
];

yPos = 1.2;
solarPoints.forEach((point) => {
  // Circle icon
  slide5.addShape(pres.shapes.OVAL, {
    x: 0.6, y: yPos, w: 0.5, h: 0.5,
    fill: { color: point.color },
    shadow: makeShadow()
  });

  slide5.addText(point.icon, {
    x: 0.6, y: yPos, w: 0.5, h: 0.5,
    fontSize: 22, color: colors.white,
    align: "center", valign: "middle"
  });

  // Title
  slide5.addText(point.title, {
    x: 1.3, y: yPos, w: 7.5, h: 0.25,
    fontSize: 16, bold: true, color: colors.darkGray,
    fontFace: fonts.header, valign: "top"
  });

  // Description
  slide5.addText(point.desc, {
    x: 1.3, y: yPos + 0.25, w: 7.5, h: 0.25,
    fontSize: 12, color: "666666",
    fontFace: fonts.body, valign: "top"
  });

  yPos += 0.8;
});

slide5.notes = "Solar power has undergone a dramatic transformation. Photovoltaic panel efficiency has improved significantly, making them more productive per square foot. Costs have dropped 70% since 2010, making solar competitive with fossil fuels in many regions. The distributed nature of solar allows for rooftop installations on homes and businesses. When paired with battery storage systems, solar can provide reliable power throughout the day and night.";

// SLIDE 6: Solar Growth Chart (Bar Chart)
const slide6 = pres.addSlide();
slide6.background = { color: colors.lightGray };

slide6.addText("Solar Capacity Growth (2015-2026)", {
  x: 0.5, y: 0.3, w: 9, h: 0.5,
  fontSize: 40, bold: true, color: colors.primary,
  fontFace: fonts.header
});

slide6.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 0.78, w: 9.2, h: 0.05,
  fill: { color: colors.secondary }
});

const solarChartData = [{
  name: "Installed Capacity (GW)",
  labels: ["2015", "2017", "2019", "2021", "2023", "2025", "2026"],
  values: [227, 398, 586, 707, 935, 1200, 1450]
}];

slide6.addChart(pres.charts.BAR, solarChartData, {
  x: 0.5, y: 1.1, w: 9, h: 4,
  barDir: "col",
  chartColors: [colors.primary],
  showTitle: false,
  showValue: true,
  dataLabelPosition: "outEnd",
  chartArea: { fill: { color: colors.white }, roundedCorners: true },
  valGridLine: { color: "E0E0E0", size: 0.5 },
  catAxisLabelColor: colors.darkGray,
  valAxisLabelColor: colors.darkGray,
  legendPos: "b"
});

slide6.notes = "Solar capacity has grown exponentially, from 227 GW in 2015 to 1,450 GW by 2026. This represents a six-fold increase in just over a decade. The growth rate has accelerated, particularly in the last three years as costs have become competitive and governments have implemented supportive policies. We expect this trend to continue as technology improves and deployment becomes more efficient.";

// SLIDE 7: Wind Energy (2-Column Comparison)
const slide7 = pres.addSlide();
slide7.background = { color: colors.white };

slide7.addText("Wind Energy: Onshore vs Offshore", {
  x: 0.5, y: 0.3, w: 9, h: 0.5,
  fontSize: 40, bold: true, color: colors.primary,
  fontFace: fonts.header
});

slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 0.78, w: 9.2, h: 0.05,
  fill: { color: colors.secondary }
});

// Onshore column
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 4.3, h: 4,
  fill: { color: colors.light },
  line: { color: colors.primary, width: 2 },
  shadow: makeShadow()
});

slide7.addText("ONSHORE WIND", {
  x: 0.65, y: 1.25, w: 4, h: 0.35,
  fontSize: 16, bold: true, color: colors.primary,
  fontFace: fonts.header
});

const onshoreContent = [
  { text: "Capacity: 850 GW", options: { bold: true, breakLine: true } },
  { text: "Growth: 10% annually\n\n", options: { breakLine: true } },
  { text: "Advantages:\n", options: { bold: true, breakLine: true } },
  { text: "• Lower installation costs\n• Faster deployment\n• Land can be dual-use\n• Proven technology\n\n", options: { bullet: false, breakLine: true } },
  { text: "Challenges:\n", options: { bold: true, breakLine: true } },
  { text: "• Limited suitable locations\n• Land availability\n• Noise concerns", options: { bullet: false } }
];

slide7.addText(onshoreContent, {
  x: 0.75, y: 1.65, w: 4, h: 3.35,
  fontSize: 11, color: colors.darkGray,
  fontFace: fonts.body, valign: "top"
});

// Offshore column
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.1, w: 4.3, h: 4,
  fill: { color: "F5F8FA" },
  line: { color: colors.secondary, width: 2 },
  shadow: makeShadow()
});

slide7.addText("OFFSHORE WIND", {
  x: 5.35, y: 1.25, w: 4, h: 0.35,
  fontSize: 16, bold: true, color: colors.secondary,
  fontFace: fonts.header
});

const offshoreContent = [
  { text: "Capacity: 55 GW", options: { bold: true, breakLine: true } },
  { text: "Growth: 25% annually\n\n", options: { breakLine: true } },
  { text: "Advantages:\n", options: { bold: true, breakLine: true } },
  { text: "• Higher capacity factors\n• Stronger, consistent winds\n• No land required\n• Scalable potential\n\n", options: { bullet: false, breakLine: true } },
  { text: "Challenges:\n", options: { bold: true, breakLine: true } },
  { text: "• High capital costs\n• Installation complexity\n• Environmental impact", options: { bullet: false } }
];

slide7.addText(offshoreContent, {
  x: 5.35, y: 1.65, w: 4, h: 3.35,
  fontSize: 11, color: colors.darkGray,
  fontFace: fonts.body, valign: "top"
});

slide7.notes = "Wind energy is split between onshore and offshore installations. Onshore wind dominates today with 850 GW of capacity, growing at 10% annually. Offshore wind is the future frontier with only 55 GW installed but growing at 25% annually. Onshore wind is more economical and faster to deploy, but suitable locations are becoming limited. Offshore wind offers tremendous potential with stronger, more consistent winds, but requires significant capital investment and complex marine installation techniques.";

// SLIDE 8: Hydroelectric Power (Timeline/Process Flow)
const slide8 = pres.addSlide();
slide8.background = { color: colors.lightGray };

slide8.addText("Hydroelectric Power: The Stable Foundation", {
  x: 0.5, y: 0.3, w: 9, h: 0.5,
  fontSize: 40, bold: true, color: colors.primary,
  fontFace: fonts.header
});

slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 0.78, w: 9.2, h: 0.05,
  fill: { color: colors.secondary }
});

// Timeline flow
const stages = [
  { label: "1800s-1900s", title: "Industrial Era", desc: "Local hydropower development" },
  { label: "1950s-1980s", title: "Dam Building", desc: "Large-scale infrastructure" },
  { label: "2000s-2015", title: "Optimization", desc: "Efficiency improvements" },
  { label: "2016+", title: "Modernization", desc: "Smart grid integration" }
];

xPos = 0.6;
stages.forEach((stage, idx) => {
  // Box
  slide8.addShape(pres.shapes.RECTANGLE, {
    x: xPos, y: 1.5, w: 2.1, h: 3.2,
    fill: { color: colors.white },
    line: { color: colors.primary, width: 2 },
    shadow: makeShadow()
  });

  // Time period
  slide8.addText(stage.label, {
    x: xPos + 0.1, y: 1.65, w: 1.9, h: 0.3,
    fontSize: 11, bold: true, color: colors.primary,
    align: "center", fontFace: fonts.header
  });

  // Divider
  slide8.addShape(pres.shapes.RECTANGLE, {
    x: xPos + 0.2, y: 2, w: 1.7, h: 0.02,
    fill: { color: colors.secondary }
  });

  // Title
  slide8.addText(stage.title, {
    x: xPos + 0.1, y: 2.15, w: 1.9, h: 0.4,
    fontSize: 12, bold: true, color: colors.accent,
    align: "center", fontFace: fonts.header
  });

  // Description
  slide8.addText(stage.desc, {
    x: xPos + 0.1, y: 2.65, w: 1.9, h: 1.5,
    fontSize: 10, color: colors.darkGray,
    align: "center", valign: "top", fontFace: fonts.body
  });

  // Connection line
  if (idx < stages.length - 1) {
    slide8.addShape(pres.shapes.LINE, {
      x: xPos + 2.2, y: 3.2, w: 0.35, h: 0,
      line: { color: colors.secondary, width: 2 }
    });
  }

  xPos += 2.35;
});

// Stats box at bottom
slide8.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.9, w: 9, h: 0.65,
  fill: { color: colors.primary }
});

slide8.addText("Current Capacity: 1,400 GW  •  Capacity Factor: 42%  •  Estimated Lifespan: 50-100 years", {
  x: 0.7, y: 4.95, w: 8.6, h: 0.55,
  fontSize: 12, bold: true, color: colors.white,
  align: "center", valign: "middle", fontFace: fonts.body
});

slide8.notes = "Hydroelectric power is the oldest and most stable renewable energy source. Development began in the 1800s and accelerated through the industrial era. The mid-20th century saw major dam construction projects worldwide. Modern hydroelectric facilities are being optimized for efficiency and increasingly integrated with smart grid technologies for load balancing. Current global capacity stands at 1,400 GW with a high capacity factor of 42%, meaning hydroelectric plants operate reliably and consistently. Dams have operational lifespans of 50-100 years, making them long-term infrastructure investments.";

// SLIDE 9: Emerging Technologies (Icon circles with text)
const slide9 = pres.addSlide();
slide9.background = { color: colors.white };

slide9.addText("Emerging Renewable Technologies", {
  x: 0.5, y: 0.3, w: 9, h: 0.5,
  fontSize: 40, bold: true, color: colors.primary,
  fontFace: fonts.header
});

slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 0.78, w: 9.2, h: 0.05,
  fill: { color: colors.secondary }
});

// Geothermal
addCircleIcon(slide9, 0.8, 1.4, 0.8, colors.primary, "⚡", colors.white, 36);
slide9.addText("Geothermal", {
  x: 0.5, y: 2.4, w: 1.4, h: 0.3,
  fontSize: 14, bold: true, color: colors.primary,
  align: "center", fontFace: fonts.header
});
slide9.addText("Stable baseload from earth's heat; 14 GW installed", {
  x: 0.3, y: 2.8, w: 1.8, h: 0.8,
  fontSize: 10, color: colors.darkGray,
  align: "center", valign: "top", fontFace: fonts.body
});

// Tidal
addCircleIcon(slide9, 2.8, 1.4, 0.8, colors.secondary, "🌊", colors.white, 32);
slide9.addText("Tidal Energy", {
  x: 2.5, y: 2.4, w: 1.4, h: 0.3,
  fontSize: 14, bold: true, color: colors.secondary,
  align: "center", fontFace: fonts.header
});
slide9.addText("Predictable ocean tidal patterns; 1 GW pilot projects", {
  x: 2.3, y: 2.8, w: 1.8, h: 0.8,
  fontSize: 10, color: colors.darkGray,
  align: "center", valign: "top", fontFace: fonts.body
});

// Green Hydrogen
addCircleIcon(slide9, 4.8, 1.4, 0.8, colors.accent, "H₂", colors.white, 28);
slide9.addText("Green Hydrogen", {
  x: 4.5, y: 2.4, w: 1.4, h: 0.3,
  fontSize: 14, bold: true, color: colors.accent,
  align: "center", fontFace: fonts.header
});
slide9.addText("Renewable fuel from water electrolysis; scaling up", {
  x: 4.3, y: 2.8, w: 1.8, h: 0.8,
  fontSize: 10, color: colors.darkGray,
  align: "center", valign: "top", fontFace: fonts.body
});

// Waste Heat
addCircleIcon(slide9, 6.8, 1.4, 0.8, "FF6B6B", "♻", colors.white, 32);
slide9.addText("Waste Heat Recovery", {
  x: 6.5, y: 2.4, w: 1.4, h: 0.3,
  fontSize: 14, bold: true, color: "CC5555",
  align: "center", fontFace: fonts.header
});
slide9.addText("Converting industrial waste heat; emerging applications", {
  x: 6.3, y: 2.8, w: 1.8, h: 0.8,
  fontSize: 10, color: colors.darkGray,
  align: "center", valign: "top", fontFace: fonts.body
});

// Wave Power
addCircleIcon(slide9, 8.8, 1.4, 0.8, "1E90FF", "≈", colors.white, 42);
slide9.addText("Wave Power", {
  x: 8.5, y: 2.4, w: 1.4, h: 0.3,
  fontSize: 14, bold: true, color: "0066CC",
  align: "center", fontFace: fonts.header
});
slide9.addText("High energy density; test installations worldwide", {
  x: 8.3, y: 2.8, w: 1.8, h: 0.8,
  fontSize: 10, color: colors.darkGray,
  align: "center", valign: "top", fontFace: fonts.body
});

// Bottom info section
slide9.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.8, w: 9, h: 1.6,
  fill: { color: colors.light },
  line: { color: colors.secondary, width: 1 }
});

const emergingText = [
  { text: "Emerging Technologies Overview:\n", options: { bold: true, fontSize: 12, breakLine: true } },
  { text: "While still in early stages, these technologies show tremendous promise. Geothermal provides reliable baseload power in suitable regions. Tidal and wave energy offer predictable renewable sources. Green hydrogen is emerging as a clean fuel for transportation and industry. Combined, these technologies could provide 10-15% of global energy by 2050.", options: { fontSize: 11 } }
];

slide9.addText(emergingText, {
  x: 0.7, y: 3.95, w: 8.6, h: 1.3,
  fontFace: fonts.body,
  color: colors.darkGray,
  valign: "top"
});

slide9.notes = "Beyond the three major renewable sources, several emerging technologies are being developed. Geothermal energy taps into Earth's internal heat and is currently installed in 14 GW globally. Tidal energy harnesses predictable ocean patterns and has several pilot projects. Green hydrogen, produced through renewable energy-powered water electrolysis, is emerging as a clean fuel. Waste heat recovery from industrial processes is being commercialized. Wave power, though nascent, offers high energy density potential. These technologies combined could contribute significantly to our energy mix by 2050.";

// SLIDE 10: Energy Storage Solutions (Comparison table-like layout)
const slide10 = pres.addSlide();
slide10.background = { color: colors.lightGray };

slide10.addText("Energy Storage Technologies", {
  x: 0.5, y: 0.3, w: 9, h: 0.5,
  fontSize: 40, bold: true, color: colors.primary,
  fontFace: fonts.header
});

slide10.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 0.78, w: 9.2, h: 0.05,
  fill: { color: colors.secondary }
});

// Header row
const storageData = [
  ["Technology", "Capacity", "Duration", "Efficiency", "Cost/kWh"],
  ["Battery (Lithium)", "500 GWh", "4-6 hours", "85-90%", "$100-150"],
  ["Pumped Hydro", "160 GWh", "12-24 hours", "70-85%", "$50-100"],
  ["Compressed Air", "50 GWh", "6-10 hours", "60-75%", "$40-80"],
  ["Thermal Storage", "80 GWh", "12-48 hours", "75-90%", "$20-50"],
  ["Hydrogen Storage", "15 GWh", "Days-Months", "35-50%", "$150-300"]
];

const cellWidth = [1.8, 1.6, 1.5, 1.5, 1.5];
let tableY = 1.2;

storageData.forEach((row, rowIdx) => {
  let tableX = 0.5;

  row.forEach((cell, colIdx) => {
    // Determine colors
    let bgColor, textColor;
    if (rowIdx === 0) {
      bgColor = colors.primary;
      textColor = colors.white;
    } else {
      bgColor = rowIdx % 2 === 0 ? colors.white : colors.light;
      textColor = colors.darkGray;
    }

    slide10.addShape(pres.shapes.RECTANGLE, {
      x: tableX, y: tableY, w: cellWidth[colIdx], h: 0.45,
      fill: { color: bgColor },
      line: { color: "CCCCCC", width: 1 }
    });

    slide10.addText(cell, {
      x: tableX + 0.05, y: tableY + 0.05, w: cellWidth[colIdx] - 0.1, h: 0.35,
      fontSize: rowIdx === 0 ? 11 : 10,
      bold: rowIdx === 0,
      color: textColor,
      align: rowIdx === 0 ? "center" : "left",
      valign: "middle",
      fontFace: rowIdx === 0 ? fonts.header : fonts.body
    });

    tableX += cellWidth[colIdx] + 0.05;
  });

  tableY += 0.5;
});

// Summary box
slide10.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.3, w: 9, h: 1.15,
  fill: { color: colors.accent },
  shadow: makeShadow()
});

const storageNote = [
  { text: "KEY INSIGHT: ", options: { bold: true, color: colors.white, fontSize: 12, breakLine: true } },
  { text: "Energy storage is crucial for renewable reliability. Battery costs have dropped 89% since 2010, making them increasingly viable. Multi-hour and multi-day storage solutions are essential for grid stability as renewable penetration increases.", options: { color: colors.light, fontSize: 11 } }
];

slide10.addText(storageNote, {
  x: 0.7, y: 4.45, w: 8.6, h: 0.85,
  fontFace: fonts.body,
  valign: "top"
});

slide10.notes = "Energy storage is the missing piece of the renewable puzzle. Lithium batteries have captured 500 GWh of installed capacity and costs continue dropping. Pumped hydro remains the largest storage solution at 160 GWh. Compressed air and thermal storage offer longer duration options. Green hydrogen storage enables seasonal energy storage. The choice of storage technology depends on duration needs, location, and cost requirements. As renewables scale up, storage capacity will need to grow proportionally to maintain grid stability.";

// SLIDE 11: Global Investment Trends (Line chart)
const slide11 = pres.addSlide();
slide11.background = { color: colors.white };

slide11.addText("Investment in Renewable Energy", {
  x: 0.5, y: 0.3, w: 9, h: 0.5,
  fontSize: 40, bold: true, color: colors.primary,
  fontFace: fonts.header
});

slide11.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 0.78, w: 9.2, h: 0.05,
  fill: { color: colors.secondary }
});

const investmentData = [{
  name: "Annual Investment ($ Billions)",
  labels: ["2016", "2018", "2020", "2022", "2024", "2026"],
  values: [242, 289, 303, 366, 445, 580]
}];

slide11.addChart(pres.charts.LINE, investmentData, {
  x: 0.5, y: 1.1, w: 9, h: 4,
  chartColors: [colors.primary],
  showTitle: false,
  showValue: false,
  lineSize: 3,
  lineSmooth: true,
  chartArea: { fill: { color: colors.white }, roundedCorners: true },
  valGridLine: { color: "E0E0E0", size: 0.5 },
  catAxisLabelColor: colors.darkGray,
  valAxisLabelColor: colors.darkGray,
  legendPos: "b"
});

slide11.notes = "Global investment in renewable energy has grown from $242 billion in 2016 to a projected $580 billion by 2026. This represents a 139% increase over one decade, demonstrating strong and sustained commitment from governments, corporations, and investors worldwide. The steep trajectory reflects both declining costs making renewables more competitive and urgency of climate action. This investment trend is accelerating, with growth rates exceeding 10% annually in recent years.";

// SLIDE 12: Policy & Incentives (Horizontal bars with icons)
const slide12 = pres.addSlide();
slide12.background = { color: colors.lightGray };

slide12.addText("Government Support Mechanisms", {
  x: 0.5, y: 0.3, w: 9, h: 0.5,
  fontSize: 40, bold: true, color: colors.primary,
  fontFace: fonts.header
});

slide12.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 0.78, w: 9.2, h: 0.05,
  fill: { color: colors.secondary }
});

const policies = [
  { name: "Feed-in Tariffs", adoption: "72", icon: "✓" },
  { name: "Renewable Portfolio Standards", adoption: "68", icon: "✓" },
  { name: "Tax Credits & Rebates", adoption: "85", icon: "✓" },
  { name: "Carbon Pricing", adoption: "54", icon: "✓" }
];

yPos = 1.3;
policies.forEach((policy) => {
  // Background bar
  slide12.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: yPos, w: 9, h: 0.65,
    fill: { color: colors.white },
    line: { color: colors.light, width: 1 }
  });

  // Policy name
  slide12.addText(policy.name, {
    x: 0.7, y: yPos + 0.08, w: 3.5, h: 0.5,
    fontSize: 13, bold: true, color: colors.primary,
    fontFace: fonts.header, valign: "middle"
  });

  // Progress bar background
  slide12.addShape(pres.shapes.RECTANGLE, {
    x: 4.5, y: yPos + 0.15, w: 4.3, h: 0.35,
    fill: { color: "E0E0E0" }
  });

  // Progress bar fill
  const barWidth = (4.3 * parseInt(policy.adoption)) / 100;
  slide12.addShape(pres.shapes.RECTANGLE, {
    x: 4.5, y: yPos + 0.15, w: barWidth, h: 0.35,
    fill: { color: colors.secondary }
  });

  // Percentage text
  slide12.addText(policy.adoption + "%", {
    x: 4.6, y: yPos + 0.15, w: 4.1, h: 0.35,
    fontSize: 12, bold: true, color: colors.white,
    align: "center", valign: "middle", fontFace: fonts.body
  });

  yPos += 0.85;
});

// Bottom note
slide12.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 4.6, w: 9, h: 0.9,
  fill: { color: colors.light },
  line: { color: colors.primary, width: 1 }
});

slide12.addText("Countries actively implementing multiple support mechanisms to accelerate renewable adoption and reduce carbon emissions.", {
  x: 0.7, y: 4.7, w: 8.6, h: 0.7,
  fontSize: 11, color: colors.darkGray,
  fontFace: fonts.body, valign: "middle", italic: true
});

slide12.notes = "Government policies and incentives are critical drivers of renewable energy deployment. Feed-in tariffs guarantee long-term prices for renewable electricity, adopted by 72% of countries with renewable targets. Renewable portfolio standards mandate utilities source a percentage of power from renewables (68% adoption). Tax credits and rebates provide direct financial incentives to consumers and businesses (85% adoption). Carbon pricing mechanisms penalize fossil fuels and favor renewables (54% adoption). These policies have proven effective in accelerating market development and private sector investment.";

// SLIDE 13: Challenges & Solutions (2 columns with shapes)
const slide13 = pres.addSlide();
slide13.background = { color: colors.white };

slide13.addText("Challenges and Solutions", {
  x: 0.5, y: 0.3, w: 9, h: 0.5,
  fontSize: 40, bold: true, color: colors.primary,
  fontFace: fonts.header
});

slide13.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 0.78, w: 9.2, h: 0.05,
  fill: { color: colors.secondary }
});

// Challenges column
slide13.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 4.3, h: 4.3,
  fill: { color: "FFE6E6" },
  line: { color: "CC0000", width: 2 },
  shadow: makeShadow()
});

slide13.addText("CHALLENGES", {
  x: 0.65, y: 1.25, w: 4, h: 0.3,
  fontSize: 16, bold: true, color: "CC0000",
  fontFace: fonts.header
});

const challenges = [
  "Grid intermittency",
  "Land use conflicts",
  "Initial capital costs",
  "Supply chain bottlenecks",
  "Grid modernization needed"
];

yPos = 1.7;
challenges.forEach((challenge) => {
  slide13.addText("• " + challenge, {
    x: 0.75, y: yPos, w: 4, h: 0.4,
    fontSize: 11, color: "663333",
    fontFace: fonts.body, valign: "top"
  });
  yPos += 0.55;
});

// Solutions column
slide13.addShape(pres.shapes.RECTANGLE, {
  x: 5.2, y: 1.1, w: 4.3, h: 4.3,
  fill: { color: "E6F2FF" },
  line: { color: "0066CC", width: 2 },
  shadow: makeShadow()
});

slide13.addText("SOLUTIONS", {
  x: 5.35, y: 1.25, w: 4, h: 0.3,
  fontSize: 16, bold: true, color: "0066CC",
  fontFace: fonts.header
});

const solutions = [
  "Energy storage systems",
  "Distributed solar/wind",
  "Economies of scale",
  "Vertical integration",
  "Smart grid technology"
];

yPos = 1.7;
solutions.forEach((solution) => {
  slide13.addText("✓ " + solution, {
    x: 5.35, y: yPos, w: 4, h: 0.4,
    fontSize: 11, color: "003366",
    fontFace: fonts.body, valign: "top"
  });
  yPos += 0.55;
});

slide13.notes = "The renewable energy transition faces several challenges. Grid intermittency from variable solar and wind requires sophisticated management. Land use conflicts arise from competing demands for solar farms and wind installations. While costs have dropped significantly, initial capital requirements remain substantial. Supply chain bottlenecks in manufacturing and installation can limit deployment rates. Traditional electrical grids were designed for centralized fossil fuel power plants and need modernization for distributed renewables. Solutions include deploying energy storage systems to smooth power generation, promoting distributed installations near demand centers, achieving economies of scale to further reduce costs, vertically integrating production and distribution, and implementing smart grid technology for real-time load balancing and demand management.";

// SLIDE 14: Roadmap to 2050 (Stacked sections with timeline)
const slide14 = pres.addSlide();
slide14.background = { color: colors.lightGray };

slide14.addText("Path to Carbon Neutrality by 2050", {
  x: 0.5, y: 0.3, w: 9, h: 0.5,
  fontSize: 40, bold: true, color: colors.primary,
  fontFace: fonts.header
});

slide14.addShape(pres.shapes.RECTANGLE, {
  x: 0.4, y: 0.78, w: 9.2, h: 0.05,
  fill: { color: colors.secondary }
});

const milestones = [
  { year: "2026-2030", title: "Acceleration Phase", target: "60% renewable electricity", color: colors.accent },
  { year: "2030-2040", title: "Transformation", target: "80% renewable electricity", color: colors.secondary },
  { year: "2040-2050", title: "Full Integration", target: "100% renewable + storage", color: colors.primary }
];

yPos = 1.2;
milestones.forEach((milestone) => {
  // Year badge
  slide14.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: yPos, w: 1.2, h: 0.4,
    fill: { color: milestone.color },
    rectRadius: 0.15
  });

  slide14.addText(milestone.year, {
    x: 0.5, y: yPos, w: 1.2, h: 0.4,
    fontSize: 10, bold: true, color: colors.white,
    align: "center", valign: "middle", fontFace: fonts.header
  });

  // Content box
  slide14.addShape(pres.shapes.RECTANGLE, {
    x: 1.9, y: yPos, w: 7.6, h: 0.4,
    fill: { color: colors.white },
    line: { color: milestone.color, width: 2 }
  });

  slide14.addText(milestone.title, {
    x: 2.1, y: yPos + 0.05, w: 3, h: 0.3,
    fontSize: 13, bold: true, color: milestone.color,
    fontFace: fonts.header, valign: "middle"
  });

  slide14.addText(milestone.target, {
    x: 5.3, y: yPos + 0.05, w: 3.1, h: 0.3,
    fontSize: 11, color: colors.darkGray,
    fontFace: fonts.body, valign: "middle", italic: true
  });

  yPos += 0.65;
});

// Details section
slide14.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.2, w: 9, h: 2.25,
  fill: { color: colors.light },
  line: { color: colors.primary, width: 2 },
  shadow: makeShadow()
});

const roadmapDetails = [
  { text: "2026-2030 ACCELERATION PHASE\n", options: { bold: true, fontSize: 12, color: colors.accent, breakLine: true } },
  { text: "Solar and wind become primary sources. Battery costs drop further. Electric vehicle fleet reaches 30% of transportation.\n\n", options: { fontSize: 10, breakLine: true } },

  { text: "2030-2040 TRANSFORMATION PHASE\n", options: { bold: true, fontSize: 12, color: colors.secondary, breakLine: true } },
  { text: "Full grid modernization complete. Energy storage capacity matches renewable output. Industry transitions to clean electricity.\n\n", options: { fontSize: 10, breakLine: true } },

  { text: "2040-2050 FULL INTEGRATION PHASE\n", options: { bold: true, fontSize: 12, color: colors.primary, breakLine: true } },
  { text: "100% renewable electricity achieved globally. Green hydrogen fuels remaining transport and heating. Carbon-neutral economy.", options: { fontSize: 10 } }
];

slide14.addText(roadmapDetails, {
  x: 0.8, y: 3.35, w: 8.4, h: 1.95,
  fontFace: fonts.body,
  color: colors.darkGray,
  valign: "top"
});

slide14.notes = "Our roadmap to carbon neutrality by 2050 is divided into three phases. From 2026-2030, we see accelerating renewable deployment and battery cost reductions, with solar and wind becoming the primary electricity sources. From 2030-2040, transformation occurs as the electrical grid modernizes and energy storage capacity grows to match variable renewable output. Industrial sectors transition to clean electricity. From 2040-2050, we achieve full integration with 100% renewable electricity, green hydrogen fueling remaining transportation and heating demands, and a fully carbon-neutral global economy. This timeline is ambitious but achievable with continued investment and policy support.";

// SLIDE 15: Conclusion / Call to Action (Dark background)
const slide15 = pres.addSlide();
slide15.background = { color: colors.primary };

// Decorative shapes
slide15.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 0.3,
  fill: { color: colors.accent }
});

slide15.addShape(pres.shapes.OVAL, {
  x: 8.5, y: -0.3, w: 2, h: 2,
  fill: { color: colors.secondary, transparency: 40 }
});

// Main title
slide15.addText("The Future Is Now", {
  x: 0.5, y: 1.2, w: 9, h: 0.7,
  fontSize: 48, bold: true, color: colors.light,
  align: "center", fontFace: fonts.header
});

// Subtitle
slide15.addText("Renewable Energy for a Sustainable World", {
  x: 0.5, y: 2, w: 9, h: 0.5,
  fontSize: 24, color: colors.white, italic: true,
  align: "center", fontFace: fonts.header
});

// Call to action boxes
const ctaItems = [
  { text: "Invest in renewables", icon: "💰" },
  { text: "Support clean policies", icon: "📋" },
  { text: "Adopt sustainable practices", icon: "🌱" }
];

xPos = 0.8;
ctaItems.forEach((item) => {
  slide15.addShape(pres.shapes.RECTANGLE, {
    x: xPos, y: 3.1, w: 2.8, h: 1.5,
    fill: { color: colors.white, transparency: 10 },
    line: { color: colors.light, width: 2 },
    shadow: makeShadow()
  });

  slide15.addText(item.icon, {
    x: xPos, y: 3.2, w: 2.8, h: 0.4,
    fontSize: 28, align: "center"
  });

  slide15.addText(item.text, {
    x: xPos + 0.1, y: 3.7, w: 2.6, h: 0.8,
    fontSize: 13, bold: true, color: colors.light,
    align: "center", valign: "middle", fontFace: fonts.body
  });

  xPos += 3.1;
});

// Footer
slide15.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 5.2, w: 10, h: 0.425,
  fill: { color: colors.accent }
});

slide15.addText("Questions? | Contact: energy@initiative.org | www.renewableenergyinitiative.org", {
  x: 0.5, y: 5.25, w: 9, h: 0.325,
  fontSize: 12, bold: true, color: colors.light,
  align: "center", valign: "middle", fontFace: fonts.body
});

slide15.notes = "The future of renewable energy is bright and full of opportunity. The transition to clean energy is not just environmentally necessary but economically compelling. Every stakeholder has a role: investors fund innovation and deployment, policymakers create supportive frameworks, and individuals and organizations adopt sustainable practices. Together, we can achieve a carbon-neutral world powered entirely by renewable energy by 2050. The question is not whether this transition will happen, but how quickly we can execute it. Join us in shaping the sustainable future.";

// Write presentation to file
pres.writeFile({ fileName: "/sessions/gallant-intelligent-ritchie/mnt/etg/STRESS_TEST_PPTX.pptx" });
console.log("Presentation created successfully: /sessions/gallant-intelligent-ritchie/mnt/etg/STRESS_TEST_PPTX.pptx");
