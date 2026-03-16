import { useState, useEffect } from "react";

function PieChart({ data, total }) {
  const cx=90, cy=90, r=72, ir=44;
  const pieTotal = data.reduce((s,d)=>s+d.value,0);
  let angle = -Math.PI/2;
  const slices = data.map(d => {
    const sweep = (d.value/pieTotal)*2*Math.PI;
    const x1=cx+r*Math.cos(angle), y1=cy+r*Math.sin(angle);
    angle+=sweep;
    const x2=cx+r*Math.cos(angle), y2=cy+r*Math.sin(angle);
    const ix1=cx+ir*Math.cos(angle-sweep), iy1=cy+ir*Math.sin(angle-sweep);
    const ix2=cx+ir*Math.cos(angle), iy2=cy+ir*Math.sin(angle);
    const large=sweep>Math.PI?1:0;
    return {...d, path:`M ${x1} ${y1} A ${r} ${r} 0 ${large} 1 ${x2} ${y2} L ${ix2} ${iy2} A ${ir} ${ir} 0 ${large} 0 ${ix1} ${iy1} Z`};
  });
  return (
    <svg width="180" height="180">
      {slices.map((s,i)=><path key={i} d={s.path} fill={s.color} stroke="#0f1117" strokeWidth="2"/>)}
      <text x={cx} y={cy-6} textAnchor="middle" fill="#e2e8f0" fontSize="20" fontWeight="500">{total}</text>
      <text x={cx} y={cy+12} textAnchor="middle" fill="#64748b" fontSize="9" letterSpacing="2">TOTAL</text>
    </svg>
  );
}

function StockBar({ days, leadTime }) {
  const pct = Math.min((days/30)*100,100);
  const color = days < leadTime ? "#ef4444" : days < leadTime*1.5 ? "#f59e0b" : "#10b981";
  return (
    <div style={{display:"flex",alignItems:"center",gap:"8px"}}>
      <div style={{flex:1,height:"5px",background:"#1e2535",borderRadius:"3px",overflow:"hidden"}}>
        <div style={{width:`${pct}%`,height:"100%",background:color,borderRadius:"3px"}}/>
      </div>
      <span style={{fontSize:"11px",color,fontFamily:"'DM Mono', monospace",minWidth:"36px"}}>{days.toFixed(1)}d</span>
    </div>
  );
}

function getStatus(days, lead) {
  if (days < lead) return { label:"CRITICAL", color:"#ef4444" };
  if (days < lead*1.5) return { label:"WARNING", color:"#f59e0b" };
  return { label:"HEALTHY", color:"#10b981" };
}

const catColors = {
  "Painkiller":"#6366f1","Antibiotic":"#8b5cf6","Diabetes":"#06b6d4",
  "Blood Pressure":"#f59e0b","Cholesterol":"#10b981","Antacid":"#ef4444",
  "Thyroid":"#ec4899","Antidepressant":"#14b8a6","ADHD":"#f97316",
  "Contraceptive":"#a855f7","Antihistamine":"#06b6d4","Anxiety":"#64748b",
  "Nerve Pain":"#0ea5e9","Muscle Relaxant":"#84cc16","Steroid":"#eab308",
  "Diuretic":"#14b8a6","Asthma":"#6366f1","Sleep Aid":"#8b5cf6",
  "Blood Thinner":"#ef4444","Seizure":"#f59e0b","Antipsychotic":"#10b981",
  "Antifungal":"#ec4899","Nausea":"#06b6d4"
};

export default function App() {
  const [inventory, setInventory] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [forecast, setForecast] = useState(null);
  const [hovered, setHovered] = useState(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [filterStatus, setFilterStatus] = useState("All");

  useEffect(() => {
    fetch("http://localhost:8000/inventory")
      .then(r=>r.json()).then(d=>{setInventory(d);setLoading(false);});
    fetch("http://localhost:8000/alerts")
      .then(r=>r.json()).then(d=>setAlerts(d));
  }, []);

  const getForecast = (id) => {
    fetch(`http://localhost:8000/forecast/${id}`)
      .then(r=>r.json()).then(d=>setForecast(d));
  };

  if (loading) return (
    <div style={{minHeight:"100vh",background:"#0f1117",display:"flex",alignItems:"center",justifyContent:"center",color:"#475569",fontFamily:"system-ui"}}>
      Loading RxTrack...
    </div>
  );

  const critical = inventory.filter(i=>i.days_of_stock_remaining < i.lead_time_days).length;
  const warning = inventory.filter(i=>i.days_of_stock_remaining < i.lead_time_days*1.5 && i.days_of_stock_remaining >= i.lead_time_days).length;
  const ok = inventory.length - critical - warning;
  const avgDays = inventory.length ? (inventory.reduce((s,i)=>s+i.days_of_stock_remaining,0)/inventory.length).toFixed(1) : 0;

  const pieData = [
    {label:"Critical", value:critical || 0.001, color:"#ef4444"},
    {label:"Warning", value:warning || 0.001, color:"#f59e0b"},
    {label:"Healthy", value:ok, color:"#10b981"},
  ];

  const filteredInventory = inventory.filter(item => {
    const matchSearch = item.medication_name.toLowerCase().includes(search.toLowerCase()) ||
                        item.category.toLowerCase().includes(search.toLowerCase());
    const s = getStatus(item.days_of_stock_remaining, item.lead_time_days);
    const matchStatus = filterStatus === "All" || s.label === filterStatus;
    return matchSearch && matchStatus;
  });

  return (
    <div style={{minHeight:"100vh",background:"#0f1117",color:"#e2e8f0",fontFamily:"'DM Sans', system-ui, sans-serif",fontSize:"14px"}}>

      {/* Header */}
      <div style={{background:"#13161f",borderBottom:"1px solid #1e2535",padding:"14px 32px",display:"flex",alignItems:"center",justifyContent:"space-between",position:"sticky",top:0,zIndex:100}}>
        <div style={{display:"flex",alignItems:"center",gap:"12px"}}>
          <div style={{width:"30px",height:"30px",background:"#6366f1",borderRadius:"8px",display:"flex",alignItems:"center",justifyContent:"center",fontSize:"15px"}}>💊</div>
          <div>
            <div style={{fontSize:"17px",fontFamily:"'Instrument Serif', serif",letterSpacing:"-0.3px"}}>RxTrack</div>
            <div style={{fontSize:"10px",color:"#475569",letterSpacing:"1.5px",textTransform:"uppercase"}}>Pharmacy Intelligence</div>
          </div>
        </div>
        <div style={{display:"flex",gap:"8px"}}>
          {alerts.length>0 && <span style={{background:"#ef444420",border:"1px solid #ef444440",color:"#ef4444",padding:"4px 12px",borderRadius:"20px",fontSize:"11px",fontWeight:"500"}}>⚠ {alerts.length} Alert</span>}
          <span style={{background:"#10b98120",border:"1px solid #10b98140",color:"#10b981",padding:"4px 12px",borderRadius:"20px",fontSize:"11px"}}>● Live</span>
        </div>
      </div>

      <div style={{padding:"24px 32px",maxWidth:"1300px",margin:"0 auto"}}>

        {/* Alerts */}
        {alerts.map(a=>(
          <div key={a.medication_id} style={{background:"linear-gradient(90deg,#ef444412,transparent)",border:"1px solid #ef444430",borderLeft:"3px solid #ef4444",borderRadius:"6px",padding:"10px 16px",marginBottom:"14px",display:"flex",alignItems:"center",gap:"10px"}}>
            <span style={{color:"#ef4444"}}>⚠</span>
            <span style={{color:"#ef4444",fontWeight:"500"}}>{a.medication_name}</span>
            <span style={{color:"#64748b",fontSize:"12px"}}>— {a.current_quantity} units · {a.days_of_stock_remaining.toFixed(1)} days stock · {a.lead_time_days}d lead time</span>
            <div style={{marginLeft:"auto",background:"#ef4444",color:"white",padding:"2px 9px",borderRadius:"4px",fontSize:"10px",fontWeight:"700",letterSpacing:"1px"}}>CRITICAL</div>
          </div>
        ))}

        {/* Stats + Pie */}
        <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr 210px",gap:"12px",marginBottom:"20px"}}>
          {[
            {label:"Total medications", value:inventory.length, color:"#6366f1", icon:"💊"},
            {label:"Critical stock", value:critical, color:"#ef4444", icon:"●"},
            {label:"Avg days remaining", value:avgDays+"d", color:"#10b981", icon:"▲"},
          ].map((s,i)=>(
            <div key={i} style={{background:"#13161f",border:"1px solid #1e2535",borderRadius:"10px",padding:"16px 18px"}}>
              <div style={{fontSize:"15px",marginBottom:"8px"}}>{s.icon}</div>
              <div style={{fontSize:"24px",fontWeight:"500",fontFamily:"'DM Mono', monospace",color:s.color}}>{s.value}</div>
              <div style={{fontSize:"11px",color:"#475569",marginTop:"4px",letterSpacing:"0.5px"}}>{s.label}</div>
            </div>
          ))}
          <div style={{background:"#13161f",border:"1px solid #1e2535",borderRadius:"10px",padding:"14px",display:"flex",flexDirection:"column",alignItems:"center",gap:"8px"}}>
            <PieChart data={pieData} total={inventory.length}/>
            <div style={{display:"flex",gap:"10px"}}>
              {pieData.map(d=>(
                <div key={d.label} style={{display:"flex",alignItems:"center",gap:"4px",fontSize:"10px",color:"#64748b"}}>
                  <div style={{width:"7px",height:"7px",borderRadius:"2px",background:d.color}}/>
                  {d.label}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Table */}
        <div style={{background:"#13161f",border:"1px solid #1e2535",borderRadius:"10px",overflow:"hidden"}}>
          <div style={{padding:"14px 20px",borderBottom:"1px solid #1e2535",display:"flex",justifyContent:"space-between",alignItems:"center",gap:"12px"}}>
            <span style={{fontWeight:"500"}}>Inventory overview</span>
            <div style={{display:"flex",gap:"8px",alignItems:"center"}}>
              <input
                value={search}
                onChange={e=>setSearch(e.target.value)}
                placeholder="Search medications..."
                style={{background:"#0f1117",border:"1px solid #2d3548",color:"#e2e8f0",padding:"6px 12px",borderRadius:"6px",fontSize:"12px",outline:"none",width:"200px",fontFamily:"'DM Sans', sans-serif"}}
              />
              {["All","HEALTHY","WARNING","CRITICAL"].map(f=>(
                <button key={f} onClick={()=>setFilterStatus(f)}
                  style={{background:filterStatus===f?"#6366f1":"transparent",border:`1px solid ${filterStatus===f?"#6366f1":"#2d3548"}`,color:filterStatus===f?"white":"#94a3b8",padding:"5px 12px",borderRadius:"6px",fontSize:"11px",cursor:"pointer",fontFamily:"'DM Sans', sans-serif"}}>
                  {f}
                </button>
              ))}
              <span style={{fontSize:"11px",color:"#475569",fontFamily:"'DM Mono', monospace"}}>{filteredInventory.length} medications</span>
            </div>
          </div>
          <table style={{width:"100%",borderCollapse:"collapse"}}>
            <thead>
              <tr style={{borderBottom:"1px solid #1e2535"}}>
                {["Medication","Category","Stock","Daily sales","Days remaining","Status","Action"].map(h=>(
                  <th key={h} style={{padding:"10px 16px",textAlign:"left",fontSize:"10px",color:"#475569",fontWeight:"500",letterSpacing:"1px",textTransform:"uppercase"}}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filteredInventory.map(item=>{
                const s = getStatus(item.days_of_stock_remaining, item.lead_time_days);
                const c = catColors[item.category] || "#6366f1";
                return (
                  <tr key={item.medication_id} onMouseEnter={()=>setHovered(item.medication_id)} onMouseLeave={()=>setHovered(null)}
                    style={{borderBottom:"1px solid #1a1f2e",background:hovered===item.medication_id?"#1a1f2e":"transparent",transition:"background 0.1s"}}>
                    <td style={{padding:"12px 16px",fontWeight:"500",color:"#e2e8f0"}}>{item.medication_name}</td>
                    <td style={{padding:"12px 16px"}}>
                      <span style={{background:`${c}22`,color:c,padding:"2px 8px",borderRadius:"4px",fontSize:"10px",fontWeight:"500"}}>{item.category || "—"}</span>
                    </td>
                    <td style={{padding:"12px 16px",fontFamily:"'DM Mono', monospace",color:"#94a3b8"}}>{item.current_quantity}</td>
                    <td style={{padding:"12px 16px",fontFamily:"'DM Mono', monospace",color:"#94a3b8"}}>{item.avg_daily_sales.toFixed(1)}/d</td>
                    <td style={{padding:"12px 16px",minWidth:"150px"}}><StockBar days={item.days_of_stock_remaining} leadTime={item.lead_time_days}/></td>
                    <td style={{padding:"12px 16px"}}>
                      <span style={{background:`${s.color}20`,color:s.color,border:`1px solid ${s.color}40`,padding:"2px 8px",borderRadius:"4px",fontSize:"10px",fontWeight:"600"}}>{s.label}</span>
                    </td>
                    <td style={{padding:"12px 16px"}}>
                      <button onClick={()=>getForecast(item.medication_id)}
                        style={{background:"transparent",border:"1px solid #2d3548",color:"#94a3b8",padding:"5px 11px",borderRadius:"6px",fontSize:"11px",cursor:"pointer"}}>
                        Forecast →
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal */}
      {forecast && (
        <div onClick={()=>setForecast(null)} style={{position:"fixed",inset:0,background:"rgba(0,0,0,0.75)",backdropFilter:"blur(4px)",display:"flex",alignItems:"center",justifyContent:"center",zIndex:200}}>
          <div onClick={e=>e.stopPropagation()} style={{background:"#13161f",border:"1px solid #1e2535",borderRadius:"12px",padding:"24px",width:"340px"}}>
            <div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:"18px"}}>
              <div>
                <div style={{fontSize:"10px",color:"#475569",letterSpacing:"1.5px",textTransform:"uppercase",marginBottom:"4px"}}>ML Forecast</div>
                <div style={{fontSize:"17px",fontWeight:"500"}}>{forecast.medication_name}</div>
              </div>
              <button onClick={()=>setForecast(null)} style={{background:"transparent",border:"none",color:"#475569",cursor:"pointer",fontSize:"18px"}}>×</button>
            </div>
            {[
              ["Current stock", `${forecast.current_quantity} units`],
              ["Avg daily sales", `${forecast.avg_daily_sales} units/day`],
              ["Predicted days of stock", `${forecast.predicted_days_of_stock} days`],
              ["Lead time", `${forecast.lead_time_days || "—"} days`],
            ].map(([label,value])=>(
              <div key={label} style={{display:"flex",justifyContent:"space-between",padding:"10px 0",borderBottom:"1px solid #1e2535"}}>
                <span style={{fontSize:"13px",color:"#475569"}}>{label}</span>
                <span style={{fontSize:"13px",fontFamily:"'DM Mono', monospace",color:"#e2e8f0"}}>{value}</span>
              </div>
            ))}
            <div style={{marginTop:"16px",padding:"12px",background:forecast.needs_reorder?"#ef444415":"#10b98115",border:`1px solid ${forecast.needs_reorder?"#ef444430":"#10b98130"}`,borderRadius:"8px",textAlign:"center",color:forecast.needs_reorder?"#ef4444":"#10b981",fontWeight:"500",fontSize:"13px"}}>
              {forecast.needs_reorder?"⚠ Immediate reorder required":"✓ Stock levels healthy"}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}