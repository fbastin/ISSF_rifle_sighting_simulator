const c = document.getElementById("c");
const ctx = c.getContext("2d");

const W = c.width, H_canvas = c.height;
const split = W / 2;
const panelH = 85; // Increased panel height to fit new controls
const cx = W / 4, cy = (H_canvas - panelH) / 2;

// --- PHYSICAL CONSTANTS & SCALE ---
const PX_PER_MM = 6.0; 
const rearZ = 220;   
const frontZ = 350;  
const targetZ = 480; 
const GRAVITY = 9.81; 

// --- UPDATED DEFAULTS ---
let eyeZ = 190;            
let rearAperture_mm = 1.6; 
let frontIris_mm = 3.8;    
let frontThickness_mm = 2.0; 
let sightHeight_mm = 60.0; 
let cant = 0;
let targetType = "10m";

// --- WIND DEFAULTS ---
let windSpeed_ms = 0.0;     
let windDir_rad = Math.PI / 2; // 90 deg = crosswind from left to right

// Geometry offsets (pixels)
let eyeXoff = 0, eyeYoff = 0;
let frontXoff = 0, frontYoff = 0;

// INPUT HANDLING
c.addEventListener("mousemove", e => {
  const r = c.getBoundingClientRect();
  eyeXoff = (e.clientX - r.left) - cx;
  eyeYoff = (e.clientY - r.top) - cy;
});

document.addEventListener("keydown", e => {
  const key = e.key.toLowerCase();
  
  if(e.key === "ArrowUp") frontYoff -= 1;
  if(e.key === "ArrowDown") frontYoff += 1;
  if(e.key === "ArrowLeft") frontXoff -= 1;
  if(e.key === "ArrowRight") frontXoff += 1;

  if(key === "a") rearAperture_mm = Math.max(0.8, rearAperture_mm - 0.1);
  if(key === "d") rearAperture_mm = Math.min(2.2, rearAperture_mm + 0.1);
  if(key === "q") frontIris_mm = Math.max(2.4, frontIris_mm - 0.1);
  if(key === "e") frontIris_mm = Math.min(7.0, frontIris_mm + 0.1);
  
  if(key === "c") frontThickness_mm = Math.max(0.5, frontThickness_mm - 0.1);
  if(key === "v") frontThickness_mm = Math.min(5.0, frontThickness_mm + 0.1);

  if(key === "u") eyeZ = Math.min(rearZ - 5, eyeZ + 1); 
  if(key === "j") eyeZ = Math.max(50, eyeZ - 1);        
  
  if(key === "z") cant -= 0.01;
  if(key === "x") cant += 0.01;
  if(key === "w") sightHeight_mm += 1;
  if(key === "s") sightHeight_mm = Math.max(20, sightHeight_mm - 1);
  
  // NEW: Wind Controls
  if(key === "o") windSpeed_ms = Math.max(0, windSpeed_ms - 0.5);
  if(key === "p") windSpeed_ms = Math.min(10, windSpeed_ms + 0.5);
  if(key === "k") windDir_rad -= 0.15; // Rotate CCW
  if(key === "l") windDir_rad += 0.15; // Rotate CW

  if(key === "t") targetType = targetType === "10m" ? "50m" : "10m";
});

function compute() {
  const scale = (targetZ - eyeZ) / (rearZ - eyeZ);
  let px = eyeXoff + (0 - eyeXoff) * scale;
  let py = eyeYoff + (0 - eyeYoff) * scale;

  const f = Math.max(0.05, rearAperture_mm / 4.5); 
  px *= f; py *= f;

  const mechanicalScale = (targetZ - rearZ) / (frontZ - rearZ);
  const tx = frontXoff * mechanicalScale;
  const ty = frontYoff * mechanicalScale;

  const dist_m = targetType === "10m" ? 10 : 50;
  const velocity_ms = targetType === "10m" ? 175.0 : 330.0; 
  const time_s = dist_m / velocity_ms;
  const gravityDrop_mm = 0.5 * GRAVITY * (time_s * time_s) * 1000;

  // Cant Physics
  const totalComp_mm = sightHeight_mm + gravityDrop_mm;
  const shiftX_mm = totalComp_mm * Math.sin(cant);
  const shiftY_mm = totalComp_mm * (1 - Math.cos(cant));

  // NEW: Wind Deflection Physics
  // Wind factor: mm of drift per 1 m/s of crosswind
  const windFactor = targetType === "10m" ? 1.2 : 10.5; 
  const windDriftX_mm = windSpeed_ms * windFactor * Math.sin(windDir_rad);
  // Head/tailwind has a minor effect on vertical impact compared to lateral crosswind
  const windDriftY_mm = windSpeed_ms * (windFactor * 0.2) * Math.cos(windDir_rad);

  return {
    px: cx + px, py: cy + py,
    gravityDrop_mm: gravityDrop_mm,
    finalX: cx + px + tx + ((shiftX_mm + windDriftX_mm) * PX_PER_MM),
    // Subtract windDriftY because Canvas +Y is down, but mathematical +Y (up) should push impact UP
    finalY: cy + py + ty + (shiftY_mm * PX_PER_MM) - (windDriftY_mm * PX_PER_MM) 
  };
}

function computeScore(x, y) {
  const dist_mm = Math.hypot(x - cx, y - cy) / PX_PER_MM;
  return Math.max(0, Math.min(10.9, 11.0 - (dist_mm / 2.5)));
}

function drawLeft(d) {
  ctx.fillStyle = "#e6d3a3";
  ctx.fillRect(0, 0, split, H_canvas - panelH);

  const targetBlur = Math.max(0, (rearAperture_mm - 0.9) * 4);
  ctx.filter = `blur(${targetBlur}px)`;
  
  const targetScale = targetType === "10m" ? 1.0 : 0.74; 
  ctx.beginPath();
  ctx.arc(cx + (d.finalX - cx)*0.22, cy + (d.finalY - cy)*0.22, 38 * targetScale, 0, Math.PI*2);
  ctx.fillStyle = "#000";
  ctx.fill();
  
  ctx.filter = 'none'; 

  const fx = cx + eyeXoff*0.18 + frontXoff;
  const fy = cy + eyeYoff*0.18 + frontYoff;

  ctx.save();
  ctx.translate(fx, fy);
  ctx.rotate(cant);

  const iris_px = frontIris_mm * 14;
  const tunnelRadius = iris_px + 45;
  const tunnelEdge = tunnelRadius + 6; 

  const barrelTop = sightHeight_mm * 1.8; 
  ctx.fillStyle = "#0a0a0a";
  
  const actualBarrelTop = Math.max(barrelTop, tunnelEdge + 10);
  ctx.fillRect(-45, tunnelEdge, 90, actualBarrelTop - tunnelEdge + 10); 
  ctx.beginPath();
  ctx.arc(0, actualBarrelTop + 150, 150, 0, Math.PI*2); 
  ctx.fill();

  ctx.beginPath();
  ctx.arc(0, 0, tunnelRadius, 0, Math.PI*2);
  ctx.lineWidth = 12; 
  ctx.strokeStyle = "rgba(10,10,10,0.9)";
  ctx.stroke();

  const outer = iris_px + (frontThickness_mm * 10);
  ctx.beginPath();
  ctx.arc(0, 0, outer, 0, Math.PI*2);
  ctx.arc(0, 0, iris_px, 0, Math.PI*2, true);
  ctx.fillStyle = "rgba(15,15,15,0.98)";
  ctx.fill();

  ctx.fillStyle = "rgba(15,15,15,0.98)";
  const barLength = tunnelRadius - outer;
  ctx.fillRect(-tunnelRadius, -4, barLength, 8); 
  ctx.fillRect(outer, -4, barLength, 8);

  ctx.restore();

  const relief = Math.max(5, rearZ - eyeZ);
  const rearR = (rearAperture_mm * 10) * (250 / relief);
  
  ctx.fillStyle = "rgba(10,10,10,0.98)";
  ctx.beginPath();
  ctx.rect(0, 0, split, H_canvas - panelH);
  ctx.arc(cx, cy, rearR, 0, Math.PI*2, true);
  ctx.fill();

  const grad = ctx.createRadialGradient(cx, cy, rearR - 8, cx, cy, rearR + 15);
  grad.addColorStop(0, "rgba(10,10,10,0)");
  grad.addColorStop(1, "rgba(10,10,10,1)");
  ctx.fillStyle = grad;
  ctx.beginPath();
  ctx.arc(cx, cy, rearR + 20, 0, Math.PI*2);
  ctx.arc(cx, cy, rearR - 20, 0, Math.PI*2, true);
  ctx.fill();
  
  const bx = cx, by = H_canvas - panelH - 40;
  ctx.fillStyle = "#222";
  ctx.fillRect(bx - 60, by - 10, 120, 20);
  
  ctx.beginPath();
  ctx.arc(bx + Math.sin(cant)*40, by, 6, 0, Math.PI*2);
  ctx.fillStyle = "lime";
  ctx.fill();
  
  ctx.fillStyle = "#fff";
  ctx.fillRect(bx - 10, by - 10, 2, 20);
  ctx.fillRect(bx + 8, by - 10, 2, 20);
}

function drawRight(d) {
  const o = split;
  ctx.fillStyle = "#e6d3a3";
  ctx.fillRect(o, 0, split, H_canvas - panelH);
  
  const tx = o + split/2;
  const step = 15; 
  
  const blackAimingMarkRadius = targetType === "10m" ? 6 * step : 6.4 * step;
  ctx.beginPath();
  ctx.arc(tx, cy, blackAimingMarkRadius, 0, Math.PI*2);
  ctx.fillStyle = "#000"; 
  ctx.fill();

  ctx.textAlign="center";
  ctx.textBaseline="middle";

  for(let v=1; v<=9; v++){
    let r = (10 - v) * step;
    
    ctx.beginPath();
    ctx.arc(tx, cy, r, 0, Math.PI*2);
    ctx.strokeStyle = (v >= 4) ? "#fff" : "#000"; 
    ctx.lineWidth = 1;
    ctx.stroke();

    if (v <= 8) {
      ctx.fillStyle = (v >= 4) ? "#fff" : "#000";
      ctx.font = "12px Arial";
      let offset = r - step/2; 
      ctx.fillText(v, tx, cy - offset);      
      ctx.fillText(v, tx, cy + offset);      
      ctx.fillText(v, tx - offset, cy);      
      ctx.fillText(v, tx + offset, cy);      
    }
  }

  ctx.beginPath();
  ctx.arc(tx, cy, 1.5, 0, Math.PI*2);
  ctx.fillStyle = "white";
  ctx.fill();

  const scale = 1.2;

  ctx.beginPath();
  ctx.arc(tx + (d.px - cx)*scale, cy + (d.py - cy)*scale, 6, 0, Math.PI*2);
  ctx.strokeStyle = "cyan";
  ctx.lineWidth = 2;
  ctx.stroke();
  
  ctx.beginPath();
  ctx.arc(tx + (d.finalX - cx)*scale, cy + (d.finalY - cy)*scale, 4, 0, Math.PI*2);
  ctx.fillStyle = "red"; 
  ctx.fill();

  // NEW: Draw Wind Indicator (Clock/Arrow)
  const wx = W - 60, wy = 60;
  
  // Clock face
  ctx.beginPath();
  ctx.arc(wx, wy, 25, 0, Math.PI*2);
  ctx.fillStyle = "rgba(255, 255, 255, 0.8)";
  ctx.fill();
  ctx.strokeStyle = "#555";
  ctx.lineWidth = 2;
  ctx.stroke();
  
  // Wind vector arrow
  if (windSpeed_ms > 0) {
    ctx.beginPath();
    ctx.moveTo(wx, wy);
    // Note: Canvas Y is inverted, so we subtract Cos for mathematical correctness
    const endX = wx + Math.sin(windDir_rad) * 20;
    const endY = wy - Math.cos(windDir_rad) * 20;
    ctx.lineTo(endX, endY);
    ctx.strokeStyle = "blue";
    ctx.lineWidth = 3;
    ctx.stroke();
    
    // Arrow head
    ctx.beginPath();
    ctx.arc(endX, endY, 3, 0, Math.PI*2);
    ctx.fillStyle = "blue";
    ctx.fill();
  }
  
  // Wind Speed Text
  ctx.fillStyle = "black";
  ctx.font = "bold 12px Arial";
  ctx.fillText(`${windSpeed_ms.toFixed(1)} m/s`, wx, wy + 40);
}

function drawPanel(d) {
  ctx.fillStyle = "#222"; ctx.fillRect(0, H_canvas-panelH, W, panelH);
  ctx.fillStyle = "#0f0"; ctx.font = "12px monospace";
  ctx.textAlign = "left";
  ctx.textBaseline = "alphabetic";
  
  const offsetX_mm = ((d.finalX - cx) / PX_PER_MM);
  const offsetY_mm = (-(d.finalY - cy) / PX_PER_MM);
  const xStr = (offsetX_mm > 0 ? "+" : "") + offsetX_mm.toFixed(1);
  const yStr = (offsetY_mm > 0 ? "+" : "") + offsetY_mm.toFixed(1);

  const clickX = (frontXoff > 0 ? "+" : "") + frontXoff;
  const clickY = (-frontYoff > 0 ? "+" : "") + (-frontYoff);

  let degreesDir = (windDir_rad * 180 / Math.PI) % 360;
  if(degreesDir < 0) degreesDir += 360;

  const relief_mm = (rearZ - eyeZ).toFixed(0);
  
  // Row 1
  ctx.fillText(`Rear: ${rearAperture_mm.toFixed(1)}mm | Front: ${frontIris_mm.toFixed(1)}mm | Thick: ${frontThickness_mm.toFixed(1)}mm | Relief: ${relief_mm}mm`, 10, H_canvas-65);
  ctx.fillText(`Target: ${targetType}`, 500, H_canvas-65);
  ctx.fillText(`Score: ${computeScore(d.finalX, d.finalY).toFixed(1)}  (Offset: X:${xStr} Y:${yStr}mm)`, 650, H_canvas-65);

  // Row 2
  ctx.fillText(`Drop: ${d.gravityDrop_mm.toFixed(1)}mm | Cant: ${(cant*180/Math.PI).toFixed(1)}° | Height: ${sightHeight_mm}mm | Clicks(X,Y): ${clickX},${clickY}`, 10, H_canvas-45);
  ctx.fillStyle = "cyan"; ctx.fillText("○ Cyan: Parallax", 500, H_canvas-45);
  ctx.fillStyle = "red";  ctx.fillText("● Red: Impact", 650, H_canvas-45);
  ctx.fillStyle = "#0f0"; ctx.fillText(`Wind: ${windSpeed_ms.toFixed(1)} m/s @ ${degreesDir.toFixed(0)}°`, 800, H_canvas-45);

  // Row 3 (Controls)
  ctx.fillStyle = "#aaa";
  ctx.fillText("Ctrl 1: C/V(Thick) | A/D(Rear) | Q/E(Front) | U/J(Relief) | W/S(Sight H.) | Z/X(Cant)", 10, H_canvas-25);
  ctx.fillText("Ctrl 2: Arrows(Clicks) | O/P(Wind Spd) | K/L(Wind Dir) | T(Toggle Target)", 10, H_canvas-10);
}

function loop() {
  const d = compute();
  drawLeft(d); drawRight(d); drawPanel(d);
  
  ctx.beginPath();
  ctx.moveTo(split, 0);
  ctx.lineTo(split, H_canvas - panelH);
  ctx.strokeStyle = "#888";
  ctx.lineWidth = 1;
  ctx.stroke();
  
  requestAnimationFrame(loop);
}

loop();