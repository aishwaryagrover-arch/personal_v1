#!/usr/bin/env python3
"""Third part of the v5 build: dimension renames, and the script behind the
technical module, the KPI tables and the learning-and-development table."""
F = "/home/user/personal_v1/MahaPAR_APAR_portal_walkthrough_v5.html"
h = open(F).read()


def swap(old, new, n=1):
    global h
    assert old in h, "anchor not found: " + old[:90]
    h = h.replace(old, new, n)


# ---------------------------------------------------------------- dimensions
h = h.replace("3. Knowledge and its application", "3. Technical knowledge")
h = h.replace("Knowledge and its application", "Technical knowledge")
h = h.replace("4. Judgement and initiative", "4. Judgement and problem-solving")
h = h.replace("Judgement and initiative", "Judgement and problem-solving")
swap("""<div class="cv">Rules, procedures, IT skills, subject knowledge</div>""",
     """<div class="cv">Subject knowledge, rules and procedures, IT skills, applying them to the work</div>""")
swap("""<div class="cv">Decision-making, problem-solving, initiative</div>""",
     """<div class="cv">Decisions under constraint, resourcefulness, solving problems within delegated powers</div>""")

# ------------------------------------------------------------------- the data
swap("const grades={}; let rvScore=null, rvAgree=true;",
"""const grades={}; let rvScore=null, rvAgree=true;

/* ---- technical cadres, their designations and KPI menus ---- */
const MODULES={
 'T1 · Engineering':['Junior Engineer','Assistant Engineer Grade II','Assistant Engineer Grade I',
   'Deputy Engineer (Sub-Divisional Engineer)','Executive Engineer and above'],
 'T2 · Public Health doctors':['Medical Officer','Senior Medical Officer','Public Health Officer',
   'District Health Officer and above'],
 'T3 · Medical and veterinary faculty':['Assistant Professor','Associate Professor','Professor'],
 'T4 · Other college and university faculty':['Assistant Professor','Associate Professor','Professor']
};
/* KPI menu by module. Engineering is drawn from the department's draft list;
   the others are to be designed with the department concerned. */
const KPI_MENU={
 'T1 · Engineering':{
  field:[{k:'Estimates prepared within set days of administrative approval',ev:'Estimates register'},
         {k:'Works completed within contract period (% of works due)',ev:'Works register, measurement books'},
         {k:'Quality tests done against the number required',ev:'Quality-test registers'},
         {k:'Inspections done against required',ev:'Inspection register'},
         {k:'Maintenance targets (km of road, buildings)',ev:'Maintenance register'}],
  senior:[{k:'Physical and financial progress against the annual works programme',ev:'Works programme reports'},
          {k:'Tenders finalised within set time',ev:'e-tendering records'},
          {k:'Bills paid within set time',ev:'Payment records'},
          {k:'Time and cost over-run cases, and savings',ev:'Works register'},
          {k:'Reportees\\u2019 APARs completed on time',ev:'MahaPAR'}]}
};
const SENIOR=['Deputy Engineer (Sub-Divisional Engineer)','Executive Engineer and above',
 'District Health Officer and above','Professor'];
const KPI_RANGE={completed:[7,10],partly:[3,6],not:[1,2]};
const CATLABEL={completed:'Completed',partly:'Partly completed',not:'Not completed'};

/* the official's KPIs for the year, kept in My KPIs and used in 2.1 */
let MYKPIS=[
 {m:0,tgt:'All estimates within 15 days of administrative approval',mid:'7 of 8 within 15 days',rev:'',why:'',
  ys:'partly',ach:'15 of 17 within 15 days',ev:'Estimates register 2025\\u201326, entries 1 to 17'},
 {m:1,tgt:'90% of the 10 works due',mid:'4 of 5 due works completed on time',rev:'',why:'',
  ys:'partly',ach:'8 of 10 works (80%)',ev:'Works register; MB Nos. 211 to 220'},
 {m:2,tgt:'All 240 required quality tests',mid:'118 of 120 done',rev:'',why:'',
  ys:'completed',ach:'240 of 240 done',ev:'Quality-test register, Sub-Division 2'},
 {m:4,tgt:'35 km of road maintained',mid:'12 km',rev:'28 km',why:'Fund release for 7 km moved to 2026\\u201327',
  ys:'partly',ach:'27 km',ev:'Maintenance register; MB No. 225'}
];
let kpiOn=false, kpiMark=[], kpiRem=[];

/* learning and development, 2.4 */
let LND=[
 {type:'iGOT course',name:'eOffice for field offices',by:'iGOT Karmayogi',dates:'Jul 2025',hrs:6,role:'',igot:true},
 {type:'iGOT course',name:'RTI Act: practice and timelines',by:'iGOT Karmayogi',dates:'Sep 2025',hrs:8,role:'',igot:true},
 {type:'Other training',name:'Budget preparation and expenditure tracking',by:'YASHADA, Pune',dates:'8 to 10 Sep 2025',hrs:18,role:''}
];""")

# ------------------------------------------- technical module, KPI, LND script
swap("""/* ---------------- memos ---------------- */""",
"""/* ---------------- technical module and KPIs ---------------- */
function fillModules(){
 const m=document.getElementById('techMod');
 m.innerHTML=Object.keys(MODULES).map(k=>`<option>${k}</option>`).join('');
 fillDesig();
}
function fillDesig(){
 const mod=document.getElementById('techMod').value;
 document.getElementById('techDesig').innerHTML=
  MODULES[mod].map(d=>`<option>${d}</option>`).join('');
 setDesig();
}
function menuFor(){
 const mod=document.getElementById('techMod').value;
 const des=document.getElementById('techDesig').value;
 const m=KPI_MENU[mod]; if(!m)return null;
 return m[SENIOR.includes(des)?'senior':'field'];
}
function setTech(on){
 kpiOn=!!on;
 show('techBox',kpiOn); show('kpiBox',kpiOn); show('kpiGradeBox',kpiOn); show('kpiWroteBox',kpiOn);
 document.getElementById('genBox').style.display=kpiOn?'none':'block';
 document.getElementById('genGradeBox').style.display=kpiOn?'none':'block';
 document.getElementById('genWrote').style.display=kpiOn?'none':'table';
 document.getElementById('kpiOffNote').style.display=kpiOn?'none':'block';
 document.getElementById('chkTech').textContent=kpiOn?'Yes':'No';
 document.getElementById('q31').textContent=kpiOn
  ?'Mark each KPI, then grade the attributes below'
  :'Grade each dimension from 1 to 10, compared with officials at the same level';
 document.getElementById('wOutSrc').textContent=kpiOn?'average of the KPI marks':'average of dimensions 1 and 2';
 document.getElementById('chk21lbl').textContent=kpiOn?'2.1 KPIs':'2.1 Targets';
 if(kpiOn)setDesig(); else {document.getElementById('kpiCountSm').textContent='Opens for technical cadres';
  document.getElementById('chk21').textContent='2 entered';}
 calc();
}
function setDesig(){
 const menu=menuFor();
 const note=document.getElementById('techNote');
 if(!menu){note.innerHTML='&#8505;&#65039; The KPI menu for this module is to be designed with the department concerned. Until then, Part 2.1 stays as the general targets table.';
  show('kpiBox',0); return;}
 note.innerHTML='&#8505;&#65039; MahaPAR opens the KPI menu for this designation. Pick 3 to 5 KPIs in <b>My KPIs</b> at the start of the year.';
 show('kpiBox',1);
 MYKPIS.forEach(r=>{if(r.m>=menu.length)r.m=0;});
 kpiMark=MYKPIS.map(()=>null); kpiRem=MYKPIS.map(()=>'');
 document.getElementById('kpiCountSm').textContent=MYKPIS.length+' KPIs · mid-year progress due 31 Oct';
 document.getElementById('chk21').textContent=MYKPIS.length+' KPIs';
 renderMyKpis(); renderKpiSelf(); renderKpiWrote(); renderKpiGrade(); calc();
}
function renderMyKpis(){
 const menu=menuFor()||[];
 document.getElementById('myKpiTable').innerHTML=
  '<tr><th style="width:34%">KPI</th><th>Target</th><th>Mid-year progress</th><th>Revised target and reason</th></tr>'+
  MYKPIS.map((r,i)=>`<tr><td>${menu[r.m]?menu[r.m].k:'—'}<br><span style="color:var(--muted);font-size:11.5px">Evidence: ${menu[r.m]?menu[r.m].ev:'—'}</span></td>
   <td>${r.tgt}</td><td>${r.mid}</td>
   <td>${r.rev?('<b>'+r.rev+'</b><br><span style="color:var(--muted);font-size:11.5px">'+r.why+'</span>'):'<span style="color:var(--muted)">Not revised</span>'}</td></tr>`).join('');
}
function addMyKpi(){
 const menu=menuFor(); if(!menu){toast('Select a module and designation first.');return;}
 if(MYKPIS.length>=5){toast('Up to five KPIs. Remove one before adding another.');return;}
 MYKPIS.push({m:3,tgt:'Set a target for the year',mid:'Not yet recorded',rev:'',why:'',ys:'partly',ach:'',ev:''});
 kpiMark.push(null);kpiRem.push('');
 renderMyKpis();renderKpiSelf();renderKpiWrote();renderKpiGrade();calc();
 document.getElementById('kpiCountSm').textContent=MYKPIS.length+' KPIs · mid-year progress due 31 Oct';
 document.getElementById('chk21').textContent=MYKPIS.length+' KPIs';
}
function renderKpiSelf(){
 const menu=menuFor()||[];
 document.getElementById('kpiSelf').innerHTML=
  '<tr><th style="width:26%">KPI</th><th>Target</th><th>Year-end status</th><th>What you achieved</th><th>Record</th></tr>'+
  MYKPIS.map((r,i)=>`<tr><td>${menu[r.m]?menu[r.m].k:'—'}</td><td>${r.tgt}${r.rev?'<br><span style="color:var(--muted);font-size:11.5px">Revised at mid-year to '+r.rev+'</span>':''}</td>
   <td><select onchange="setYs(${i},this.value)">
     <option value="completed"${r.ys==='completed'?' selected':''}>Completed</option>
     <option value="partly"${r.ys==='partly'?' selected':''}>Partly completed</option>
     <option value="not"${r.ys==='not'?' selected':''}>Not completed</option></select></td>
   <td><input type="text" value="${r.ach}" oninput="MYKPIS[${i}].ach=this.value;renderKpiWrote()"></td>
   <td><input type="text" value="${r.ev}" oninput="MYKPIS[${i}].ev=this.value;renderKpiWrote()" placeholder="Register, file or measurement book"></td></tr>`).join('');
}
function setYs(i,v){MYKPIS[i].ys=v;kpiMark[i]=null;renderKpiSelf();renderKpiWrote();renderKpiGrade();calc();}
function renderKpiWrote(){
 const menu=menuFor()||[];const el=document.getElementById('kpiWrote');if(!el)return;
 el.innerHTML='<tr><th style="width:28%">KPI</th><th>Target</th><th>Status</th><th>Achievement</th><th>Record</th></tr>'+
  MYKPIS.map(r=>`<tr><td>${menu[r.m]?menu[r.m].k:'—'}</td><td>${r.rev||r.tgt}</td>
   <td>${CATLABEL[r.ys]}</td><td>${r.ach||'—'}</td><td>${r.ev||'—'}</td></tr>`).join('');
}
function renderKpiGrade(){
 const menu=menuFor()||[];const box=document.getElementById('kpiGrade');if(!box)return;
 box.innerHTML=MYKPIS.map((r,i)=>{
  const [lo,hi]=KPI_RANGE[r.ys];
  const btns=Array.from({length:hi-lo+1},(_,x)=>lo+x).map(n=>
    `<button class="${kpiMark[i]===n?'on':''}${kpiMark[i]===n&&(n<=2||n>=9)?' extreme':''}" onclick="setKpiMark(${i},${n})">${n}</button>`).join('');
  const needRem=r.ys==='not'||!!r.rev;
  return `<div class="dim"><div class="nm">${menu[r.m]?menu[r.m].k:'—'}</div>
   <div class="cv">Target: ${r.rev||r.tgt} · achieved: ${r.ach||'not stated'} · record: ${r.ev||'not stated'}</div>
   <div class="sys"><em>Status recorded by the official <b>${CATLABEL[r.ys]}</b></em><em>Marks open <b>${lo} to ${hi}</b></em>${r.rev?'<em class="memo">Target revised at mid-year</em>':''}</div>
   <div class="scale">${btns}</div>
   ${needRem?`<input type="text" style="margin-top:8px" placeholder="Remark (required: ${r.ys==='not'?'not completed':'target revised'})" value="${kpiRem[i]||''}" oninput="kpiRem[${i}]=this.value">`:''}
   </div>`;}).join('');
}
function setKpiMark(i,n){kpiMark[i]=(kpiMark[i]===n?null:n);renderKpiGrade();calc();}

/* ---------------- learning and development (2.4) ---------------- */
function renderLnd(){
 const total=LND.reduce((a,x)=>a+(+x.hrs||0),0);
 const rows=LND.map((x,i)=>`<tr><td>${x.type}${x.igot?' <span class="tag ok">iGOT</span>':''}</td><td>${x.name}</td>
   <td>${x.by}</td><td>${x.dates}</td><td>${x.hrs}</td><td>${x.role||'—'}</td></tr>`).join('');
 const head='<tr><th>Type</th><th style="width:28%">Title</th><th>Institute or organiser</th><th>Dates</th><th>Hours</th><th>Role</th></tr>';
 const foot=`<tr><td colspan="4"><b>Total hours</b></td><td><b>${total}</b></td><td></td></tr>`;
 document.getElementById('lndTable').innerHTML=head+rows+foot;
 const w=document.getElementById('lndWrote');
 if(w)w.innerHTML=head.replace('<th>Role</th>','<th>Role</th>')+rows+foot;
 const c=document.getElementById('chkLnd');
 if(c)c.textContent=LND.length+' entries · '+total+' hours';
}
function addLnd(){
 const g=id=>document.getElementById(id).value.trim();
 if(!g('lTitle')){toast('Enter a title before adding the row.');return;}
 LND.push({type:g('lType'),name:g('lTitle'),by:g('lBy')||'—',dates:g('lDates')||'—',
  hrs:+g('lHrs')||0,role:g('lType')==='Workshop or conference'?g('lRole'):''});
 ['lTitle','lBy','lDates','lHrs'].forEach(id=>document.getElementById(id).value='');
 show('lndAdd',0);renderLnd();toast('Added to your learning and development record.');
}

/* ---------------- memos ---------------- */""")

# --------------------------------------------- calc(), scoreboard, validation
swap("""function calc(){
 const keys=Object.keys(WEIGHTS),have=keys.filter(k=>grades[k]);
 document.getElementById('gradedCount').textContent=have.length+' of 6 dimensions graded';
 const grp=(ks)=>{const g=ks.filter(k=>grades[k]);return g.length?(g.reduce((a,k)=>a+grades[k],0)/g.length).toFixed(1):'—';};
 document.getElementById('wOut').textContent=grp(['d1','d2']);
 document.getElementById('wFun').textContent=grp(['d3','d4']);
 document.getElementById('wPer').textContent=grp(['d5','d6']);
 let overall=null;
 if(have.length===6){overall=keys.reduce((a,k)=>a+grades[k]*WEIGHTS[k],0);
  document.getElementById('bigGrade').textContent=overall.toFixed(1);}
 else document.getElementById('bigGrade').textContent='—';""",
"""function groupAvg(ks){const g=ks.filter(k=>grades[k]);return g.length?g.reduce((a,k)=>a+grades[k],0)/g.length:null;}
function kpiAvg(){const m=kpiMark.filter(x=>x);return m.length?m.reduce((a,b)=>a+b,0)/m.length:null;}
function calc(){
 const f1=n=>n==null?'—':n.toFixed(1);
 const work=kpiOn?kpiAvg():groupAvg(['d1','d2']);
 const fun=groupAvg(['d3','d4']), per=groupAvg(['d5','d6']);
 const attrDone=['d3','d4','d5','d6'].every(k=>grades[k]);
 const workDone=kpiOn?kpiMark.length>0&&kpiMark.every(x=>x):(grades.d1&&grades.d2);
 document.getElementById('gradedCount').textContent=kpiOn
  ?(kpiMark.filter(x=>x).length+' of '+kpiMark.length+' KPIs and '+['d3','d4','d5','d6'].filter(k=>grades[k]).length+' of 4 attributes graded')
  :(Object.keys(WEIGHTS).filter(k=>grades[k]).length+' of 6 dimensions graded');
 document.getElementById('wOut').textContent=f1(work);
 document.getElementById('wFun').textContent=f1(fun);
 document.getElementById('wPer').textContent=f1(per);
 let overall=null;
 if(workDone&&attrDone){overall=work*0.4+fun*0.3+per*0.3;
  document.getElementById('bigGrade').textContent=overall.toFixed(1);}
 else document.getElementById('bigGrade').textContent='—';
 renderRevSummary(work,fun,per,overall);""")

swap(""" document.getElementById('boardNote').textContent=overall===null?'Grade every dimension to see the overall grade.'""",
""" document.getElementById('boardNote').textContent=overall===null?(kpiOn?'Mark every KPI and grade every attribute to see the overall grade.':'Grade every dimension to see the overall grade.')""")

swap(""" const ext=keys.filter(k=>grades[k]&&(grades[k]<=2||grades[k]>=9));
 show('extremeBox',ext.length>0);
 if(ext.length)document.getElementById('extremeList').innerHTML=
  'Open: '+ext.map(k=>DIMNAMES[k]+' <b>('+grades[k]+')</b>').join(', ')+'.';
 // mirror into reviewing + disclosure
 keys.forEach(k=>{const el=document.getElementById('rv'+k[1]);if(el)el.textContent=grades[k]||'—';});""",
""" const keys=Object.keys(WEIGHTS);
 const ext=keys.filter(k=>grades[k]&&(grades[k]<=2||grades[k]>=9)&&(kpiOn?k!=='d1'&&k!=='d2':true))
   .map(k=>DIMNAMES[k]+' <b>('+grades[k]+')</b>');
 if(kpiOn)kpiMark.forEach((m,i)=>{if(m&&(m<=2||m>=9))ext.push('KPI '+(i+1)+' <b>('+m+')</b>');});
 show('extremeBox',ext.length>0);
 if(ext.length)document.getElementById('extremeList').innerHTML='Open: '+ext.join(', ')+'.';
 // mirror into reviewing + disclosure
 keys.forEach(k=>{const el=document.getElementById('rv'+k[1]);if(el)el.textContent=grades[k]||'—';});""")

swap("""function signReporting(){
 const keys=Object.keys(WEIGHTS),have=keys.filter(k=>grades[k]);
 if(have.length<6){toast('Grade all six dimensions before signing.');return;}""",
"""function signReporting(){
 const keys=Object.keys(WEIGHTS);
 const attrDone=['d3','d4','d5','d6'].every(k=>grades[k]);
 const workDone=kpiOn?kpiMark.length>0&&kpiMark.every(x=>x):(grades.d1&&grades.d2);
 if(!workDone){toast(kpiOn?'Mark every KPI before signing.':'Grade all six dimensions before signing.');return;}
 if(!attrDone){toast('Grade every attribute before signing.');return;}
 if(kpiOn){const miss=MYKPIS.findIndex((r,i)=>(r.ys==='not'||r.rev)&&!(kpiRem[i]||'').trim());
  if(miss>-1){toast('A remark is required for KPI '+(miss+1)+': not completed, or the target was revised.');return;}}""")

swap(""" const overall=keys.reduce((a,k)=>a+grades[k]*WEIGHTS[k],0);
 if(overall<6&&!document.getElementById('attachMemo').checked)""",
""" const work=kpiOn?kpiAvg():groupAvg(['d1','d2']);
 const overall=work*0.4+groupAvg(['d3','d4'])*0.3+groupAvg(['d5','d6'])*0.3;
 if(overall<6&&!document.getElementById('attachMemo').checked)""")

# ------------------------------------------- reviewing officer summary table
swap("""/* ---------------- reviewing ---------------- */""",
"""function renderRevSummary(work,fun,per,overall){
 const el=document.getElementById('revSummary');if(!el)return;
 const f=n=>n==null?'—':n.toFixed(1);
 el.innerHTML='<tr><th style="width:58%">Group</th><th>Average</th><th>Weight</th></tr>'
  +`<tr><td>Work output${kpiOn?' · average of the KPI marks':' · average of dimensions 1 and 2'}</td><td><b>${f(work)}</b></td><td>40%</td></tr>`
  +`<tr><td>Functional competence · average of dimensions 3 and 4</td><td><b>${f(fun)}</b></td><td>30%</td></tr>`
  +`<tr><td>Personal attributes · average of dimensions 5 and 6</td><td><b>${f(per)}</b></td><td>30%</td></tr>`
  +`<tr><td><b>Overall grade recorded by the reporting officer</b></td><td><b>${f(overall)}</b></td><td></td></tr>`;
}

/* ---------------- reviewing ---------------- */""")

# ------------------------------------------------- 3.8(b) clickable chips
swap("""function renderRoChips(){
 const box=document.getElementById('roTrainChips');if(!box)return;
 const L=['iGOT course','Domain knowledge','Functional skills','Behavioural skills','Budget management','Project management','Team leadership','Communication'];
 box.innerHTML=L.map((t,i)=>`<button class="chip" onclick="this.classList.toggle('on')">${t}</button>`).join('');
}""",
"""const roPicked=[];
function renderRoChips(){
 const box=document.getElementById('roTrainChips');if(!box)return;
 box.innerHTML=TRAIN.map((t,i)=>`<button class="chip${roPicked.some(p=>p.t===t)?' on':''}" onclick="pickRoNeed('${t.replace(/'/g,"\\\\'")}')">${t}</button>`).join('')
  +`<button class="chip" onclick="pickRoNeed('Other')">Other…</button>`;
 renderRoNeedTable();
}
function pickRoNeed(t){
 const i=roPicked.findIndex(p=>p.t===t);
 if(i>-1){roPicked.splice(i,1);}
 else{if(roPicked.length>=3){toast('Up to three. Clear one to choose another.');return;}
      roPicked.push({t,type:''});}
 renderRoChips();
}
function renderRoNeedTable(){
 const el=document.getElementById('roNeedTable');if(!el)return;
 if(!roPicked.length){el.innerHTML='<tr><td style="color:var(--muted)">Nothing selected yet. Select up to three from the list above.</td></tr>';return;}
 el.innerHTML='<tr><th style="width:55%">Training recommended</th><th>Type</th></tr>'+
  roPicked.map((p,i)=>`<tr><td>${p.t==='Other'?'<input type="text" placeholder="State the training">':p.t}</td>
   <td class="typecell">${['Domain','Functional','Behavioural'].map(ty=>
     `<label><input type="radio" name="rt${i}" ${p.type===ty?'checked':''} onclick="roPicked[${i}].type='${ty}'"> ${ty}</label>`).join('')}</td></tr>`).join('');
}""")

# ---------------------------------------------------------------- selfStep, boot
swap("""function selfStep(n){
 for(let i=1;i<=7;i++)document.getElementById('self'+i).classList.toggle('on',i===n);""",
"""function selfStep(n){
 for(let i=1;i<=8;i++){const el=document.getElementById('self'+i);if(el)el.classList.toggle('on',i===n);}""")
swap(""" document.querySelectorAll('#yearSteps li').forEach((li,i)=>li.classList.toggle('on',n===6+i));""",
""" const YEAR=[8,6,7];
 document.querySelectorAll('#yearSteps li').forEach((li,i)=>li.classList.toggle('on',n===YEAR[i]));""")

swap("buildScales();renderChips();renderRoChips();renderMemos();renderCycle();renderLog();",
     "buildScales();renderChips();renderRoChips();renderMemos();renderCycle();renderLog();fillModules();setTech(0);renderLnd();")

open(F, "w").write(h)
print("part 3 of the patch applied")
