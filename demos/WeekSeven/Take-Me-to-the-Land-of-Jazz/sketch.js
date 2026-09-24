/* The drawing is a pure function of the recording's currentTime. Seeking stays in sync. */
const W=1280,H=720,DURATION=164.336;
const C={night:'#191735',navy:'#182344',berry:'#5a3158',plum:'#35233e',cream:'#f8e9c9',gold:'#ffc966',coral:'#fb8975',pink:'#f9a7a2',teal:'#56bfb5',mint:'#9fd5b6',blue:'#7daec7',dark:'#18172d'};
const cues=[
  [0,3,'A record spins; an entire city waits in the groove.','overture'],
  [3,14,'A little melody begins its journey in Tennessee.','map'],
  [14,27,'Notes escape the piano and go looking for a cabaret.','piano'],
  [27,50,'The whole cabaret joins the parade.','cabaret'],
  [50,63,'The chorus sails toward Memphis on a river of blues.','river'],
  [63,73,'A very enthusiastic pair of shoes finds its pep.','shoes'],
  [73,84,'Razz-ma-tazz: gravity is politely dismissed.','dance'],
  [84,97,'The breeze seems to have learned the tune.','wind'],
  [97,113,'Of course the trees grow trombones.','tree'],
  [113,126,'Everyone joins the fun.','duet'],
  [126,139,'One more ticket to the Land of Jazz!','train'],
  [139,152,'A friendly warning: morning may have to wait.','clock'],
  [152,162,'The entire orchestra gets the last word.','finale'],
  [162,165,'The land of jazz is still playing.','end']
];
let audio,seek,play,caption,notes,analysis=window.JAZZ_ANALYSIS||{fps:40,levels:[],accents:[]},pauseScrub=false;
let t=0,energy=0,sceneIndex=0,sceneStart=0,sceneEnd=0,scene='',sceneP=0;
const fract=x=>x-Math.floor(x),hash=x=>fract(Math.sin(x*127.13+78.23)*43758.5453);
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
const ease=x=>{x=clamp(x);return x*x*(3-2*x)};
const cyc=(speed=2)=>Math.sin(t*speed*2*Math.PI);
const interp=(a,b,k)=>a+(b-a)*k;

function setup(){
  const c=createCanvas(W,H);c.parent('stage');pixelDensity(1);frameRate(30);
  audio=document.getElementById('score');seek=document.getElementById('seek');play=document.getElementById('play');caption=document.getElementById('caption');notes=document.getElementById('captions');
  play.onclick=()=>audio.paused?audio.play():audio.pause();
  document.getElementById('replay').onclick=()=>{audio.currentTime=0;audio.play()};
  seek.oninput=()=>{pauseScrub=true;audio.currentTime=+seek.value};seek.onchange=()=>pauseScrub=false;
  audio.onplay=()=>play.textContent='❚❚ Pause';audio.onpause=()=>play.textContent='▶ Play';
  audio.onended=()=>play.textContent='↶ Play again';
  document.addEventListener('keydown',e=>{if(e.code==='Space'&&e.target.tagName!=='BUTTON'&&e.target.tagName!=='INPUT'){e.preventDefault();play.click()}});
}
function draw(){
  t=audio.currentTime||0;
  if(audio.ended)t=Math.min(t,DURATION);
  const ix=Math.min(analysis.levels.length-1,Math.floor(t*(analysis.fps||40)));
  energy=ix>=0?(analysis.levels[ix]||0):0;
  sceneIndex=cues.findIndex(c=>t>=c[0]&&t<c[1]);if(sceneIndex<0)sceneIndex=cues.length-1;
  [sceneStart,sceneEnd,,scene]=cues[sceneIndex];sceneP=clamp((t-sceneStart)/(sceneEnd-sceneStart));
  randomSeed(1337);noiseSeed(2026);
  stage();
  const fn={overture, map:mapScene,piano,cabaret,river,shoes,dance,wind,tree,duet,train,clock,finale,end}[scene];fn();
  foreground();
  // A painted iris covers the splice, so each scene arrives on a musical phrase.
  const edge=Math.min(t-sceneStart,sceneEnd-t);
  if(sceneIndex>0&&edge<0.43){noStroke();fill(22,17,42,230*(1-ease(edge/.43)));rect(0,0,W,H)}
  if(!pauseScrub)seek.value=t;
  document.getElementById('clock').textContent=fmt(t)+' / 2:44';
  caption.textContent=notes.checked?cues[sceneIndex][2]:'';
}
function fmt(v){return Math.floor(v/60)+':'+String(Math.floor(v%60)).padStart(2,'0')}

function strokePath(points,color,width=6,rough=1,alpha=255){
  const col=window.color(color);col.setAlpha(alpha);
  noFill();strokeCap(ROUND);strokeJoin(ROUND);
  for(let pass=0;pass<3;pass++){
    const shade=window.color(color);shade.setAlpha(pass===0?alpha*.18:pass===1?alpha*.47:alpha*.8);
    stroke(shade);strokeWeight(width*(pass===0?2.35:pass===1?1.25:.58));
    beginShape();for(let i=0;i<points.length;i++){
      let [x,y]=points[i],h=hash(i*9.7+pass*32.5+points.length*22);
      curveVertex(x+(h-.5)*rough,y+(hash(i*19+pass*12)-.5)*rough);
    }endShape();
  }
}
function brush(a,b,c,d,col,w=7,rough=1,alpha=255){
  let pts=[];for(let i=0;i<=9;i++){let u=i/9;pts.push([interp(a,c,u),interp(b,d,u)])}strokePath(pts,col,w,rough,alpha)
}
function blob(x,y,w,h,col,phase=0){
  noStroke();fill(col);beginShape();for(let i=0;i<40;i++){
    let a=i*Math.PI*2/40,j=1+.035*Math.sin(i*2.4+phase);vertex(x+Math.cos(a)*w*j,y+Math.sin(a)*h*j)
  }endShape(CLOSE);
  for(let i=0;i<9;i++){let a=i*.7+phase;brush(x+Math.cos(a)*w*.52,y+Math.sin(a)*h*.52,x+Math.cos(a+.24)*w*.63,y+Math.sin(a+.24)*h*.63,C.cream,1,3,46)}
}
function textArt(txt,x,y,size=52,col=C.cream,align=CENTER){
  textAlign(align,CENTER);textFont('Georgia');textStyle(BOLD);textSize(size);noStroke();fill(17,15,30,100);text(txt,x+3,y+5);fill(col);text(txt,x,y)
}
function small(txt,x,y,size=22,col=C.cream){textAlign(CENTER,CENTER);textFont('Georgia');textStyle(NORMAL);textSize(size);noStroke();fill(col);text(txt,x,y)}
function note(x,y,s=1,c=C.gold,rot=0){
  push();translate(x,y);rotate(rot);noStroke();fill(c);ellipse(-9*s,10*s,22*s,14*s);ellipse(13*s,4*s,22*s,14*s);stroke(c);strokeWeight(5*s);line(0,9*s,0,-31*s);line(22*s,4*s,22*s,-35*s);line(0,-31*s,22*s,-35*s);pop()
}
function star(x,y,r=12,col=C.gold){stroke(col);strokeWeight(2);line(x-r,y,x+r,y);line(x,y-r,x,y+r);noStroke();fill(col);circle(x,y,r*.35)}
function stage(){
  let palettes={overture:[C.night,'#634568'],map:['#2c395c','#526578'],piano:['#293b53','#806066'],cabaret:['#432b4f','#a04f5e'],river:['#193d58','#3a6680'],shoes:['#463552','#91665b'],dance:['#452952','#955b70'],wind:['#31566a','#8b8095'],tree:['#294e53','#807458'],duet:['#403e55','#86657b'],train:['#273c55','#80617a'],clock:['#272b50','#714f72'],finale:['#512c57','#be735c'],end:['#181936','#4c3862']};
  const ctx=drawingContext,gr=ctx.createLinearGradient(0,0,W,H);gr.addColorStop(0,palettes[scene][0]);gr.addColorStop(1,palettes[scene][1]);ctx.fillStyle=gr;ctx.fillRect(0,0,W,H);
  push();translate(W/2,H/2);for(let i=0;i<38;i++){
    let a=i*Math.PI*2/38+Math.sin(t*.05)*.05;
    stroke(255,221,171,10);strokeWeight(i%4===0?16:4);line(Math.cos(a)*140,Math.sin(a)*140,Math.cos(a)*860,Math.sin(a)*860)
  }pop();
  for(let i=0;i<110;i++){let x=hash(i*31)*W,y=hash(i*41+4)*H;noStroke();fill(255,220,181,8+hash(i+4)*11);circle(x,y,1+hash(i*19)*3)}
  // Scalloped proscenium and gold inner trim.
  noFill();stroke('#d4aa79');strokeWeight(3);rect(25,25,W-50,H-50,20);stroke(255,222,172,110);strokeWeight(1);rect(36,36,W-72,H-72,16);
  for(let i=0;i<11;i++){let x=58+i*116;star(x,46,5,C.gold);star(x,H-46,5,C.gold)}
}
function foreground(){
  // The bottom brushstroke is a tiny audio meter, tied to the actual recording.
  noStroke();fill(249,222,178,64);rect(55,671,1170,2);
  fill(C.gold);rect(55,668,(1170*clamp(t/DURATION)),7,4);
  for(let i=0;i<34;i++){let a=hash(i*89)*2*Math.PI,r=hash(i*11+3)*390+60;
    let x=640+Math.cos(a+t*.07*(i%3-1))*r,y=360+Math.sin(a+t*.08)*r*.55;
    fill(255,232,193,18+energy*30);circle(x,y,1.5+energy*3)
  }
  fill(C.cream);textFont('Georgia');textSize(15);textStyle(ITALIC);textAlign(LEFT);text('A PAINTED LITTLE SYMPHONY',55,62);
  textAlign(RIGHT);text(('0'+(sceneIndex+1)).slice(-2)+' / '+('0'+cues.length).slice(-2),1225,62)
}
function overture(){
  push();translate(640,354);let angle=t*.52;rotate(angle);
  noStroke();fill('#100f22');circle(0,0,500);for(let i=0;i<7;i++){noFill();stroke(240,199,139,34+i*3);strokeWeight(2);circle(0,0,140+i*47)}
  fill(C.gold);circle(0,0,168);fill(C.coral);circle(0,0,148);fill(C.cream);circle(0,0,15);pop();
  textArt('TAKE ME TO THE',640,310,54,C.cream);textArt('LAND OF JAZZ',640,380,76,C.gold);
  small('a very improbable orchestra',640,453,25,C.mint);
  for(let i=0;i<7;i++)note(120+i*170,470+Math.sin(i*3+t*3)*40,.7,C.coral,-.3)
}
function mapScene(){
  for(let i=0;i<6;i++)blob(250+i*175,505+20*Math.sin(i),110,54,i%2?C.teal:C.blue,i);
  // A meandering Mississippi, stylized as an oversized painted ribbon.
  strokePath([[78,540],[250,472],[397,492],[560,420],[715,437],[860,360],[1074,385],[1220,300]],C.teal,63,9,200);
  strokePath([[78,540],[250,472],[397,492],[560,420],[715,437],[860,360],[1074,385],[1220,300]],C.cream,3,3,120);
  for(let i=0;i<12;i++){
    let x=100+i*92,y=228+30*Math.sin(i*1.7);star(x,y,5+i%3*3,i%2?C.coral:C.gold)
  }
  // The suitcase is our excitable little guide through the song.
  let x=140+sceneP*920,y=500-105*Math.sin(sceneP*Math.PI);
  suitcase(x,y,1.5);
  textArt('TENNESSEE',640,153,68,C.cream);small('where the melody packs its bags',640,215,25,C.gold);
  for(let i=0;i<8;i++)note(x-90-i*46,440+35*Math.sin(t*2+i),.55,C.gold,.3)
}
function piano(){
  // A floor of enormous ivory keys that undulates when the record gets loud.
  for(let i=0;i<13;i++){
    let x=80+i*90,y=440+25*Math.sin(t*4+i*.7)*energy;
    stroke(C.dark);strokeWeight(6);fill(C.cream);rect(x,y,87,190,8);
    if([0,1,3,4,5].includes(i%7)){fill(C.dark);rect(x+60,y,53,110,7)}
  }
  for(let i=0;i<11;i++){
    let a=t*.9+i*.9,x=125+i*100+25*Math.sin(a),y=380-180*Math.abs(Math.sin(a*.65+i));
    note(x,y,.6+energy*.3,[C.gold,C.coral,C.teal][i%3],Math.sin(a)*.35)
  }
  textArt('THE PIANO',640,186,69,C.cream);small('cannot keep its notes to itself',640,249,27,C.gold)
}
function expressiveFace(x,y,r,phase=0,style=0){
  push();translate(x,y);
  let blink=fract((t+phase*.61)/3.7)<.028, gaze=Math.sin(t*1.4+phase)*r*.09;
  let singing=energy>.4&&Math.sin(t*10+phase*1.8)>.08;
  // Hair and hats make the three cabaret performers distinct even in silhouette.
  if(style===1){noStroke();fill(C.dark);ellipse(0,5,r*2.37,r*1.9)}
  fill(C.cream);stroke(C.dark);strokeWeight(4);ellipse(0,0,r*2,r*1.88);
  noStroke();fill(C.pink);ellipse(-r*.65,r*.20,r*.37,r*.20);ellipse(r*.65,r*.20,r*.37,r*.20);
  if(style===0){fill(C.dark);beginShape();vertex(-r*.89,-r*.40);vertex(-r*.45,-r*1.03);vertex(r*.29,-r*.99);vertex(r*.84,-r*.48);vertex(r*.22,-r*.69);vertex(-r*.28,-r*.53);endShape(CLOSE)}
  if(style===1){fill(C.dark);ellipse(-r*.86,-r*.06,r*.33,r*1.25);ellipse(r*.86,-r*.06,r*.33,r*1.25);stroke(C.gold);strokeWeight(4);arc(0,-r*.63,r*1.4,r*.26,PI,TWO_PI)}
  if(style===2){fill(C.dark);arc(0,-r*.66,r*1.77,r*.81,PI,TWO_PI);fill(C.gold);stroke(C.dark);strokeWeight(3);rect(-r*.74,-r*1.06,r*1.48,r*.24,5);rect(-r*.46,-r*1.63,r*.92,r*.66,5)}
  stroke(C.dark);strokeWeight(3);noFill();
  let eyebrow=Math.sin(t*2+phase)*r*.07;
  brush(-r*.55,-r*.36-eyebrow,-r*.19,-r*.44+eyebrow,C.dark,2);
  brush(r*.20,-r*.44+eyebrow,r*.55,-r*.36-eyebrow,C.dark,2);
  if(blink){brush(-r*.48,-r*.05,-r*.15,-r*.05,C.dark,3);brush(r*.15,-r*.05,r*.48,-r*.05,C.dark,3)}
  else{noStroke();fill(C.dark);ellipse(-r*.31+gaze,-r*.04,r*.15,r*.27);ellipse(r*.31+gaze,-r*.04,r*.15,r*.27);fill(C.cream);circle(-r*.34+gaze,-r*.12,r*.07);circle(r*.28+gaze,-r*.12,r*.07)}
  if(singing){stroke(C.dark);strokeWeight(3);fill('#9c3d58');ellipse(0,r*.42,r*.42,r*.42+energy*r*.24);noStroke();fill(C.pink);ellipse(0,r*.56,r*.19,r*.07)}
  else{noFill();stroke(C.dark);strokeWeight(3);arc(0,r*.19,r*.79,r*.55,0,PI)}
  pop()
}
function suitcase(x,y,s=1){
  push();translate(x,y+Math.sin(t*9)*3);rotate(Math.sin(t*6)*.045);scale(s);
  let wave=Math.sin(t*6.6);
  brush(-48,-20,-76,-43-wave*18,C.cream,8);brush(48,-20,79,-56+wave*18,C.cream,8);
  noStroke();fill(C.cream);circle(-79,-45-wave*18,13);circle(82,-56+wave*18,13);
  fill(C.coral);stroke(C.dark);strokeWeight(5);rect(-56,-53,112,94,16);
  noFill();stroke(C.gold);strokeWeight(8);arc(0,-52,43,38,PI,TWO_PI);
  fill(C.gold);noStroke();rect(-54,-4,108,9,2);rect(-48,31,17,8,3);rect(31,31,17,8,3);
  fill(C.dark);circle(-36,45,19);circle(36,45,19);fill(C.gold);circle(-36,45,7);circle(36,45,7);
  // Eyebrows, rosy cheeks and a singing mouth travel with the melody.
  let blink=fract((t+.35)/4.3)<.025,look=Math.sin(t*1.6)*2;
  brush(-37,-36,-11,-40,C.dark,2);brush(11,-40,38,-36,C.dark,2);
  noStroke();fill(C.pink);ellipse(-32,8,18,9);ellipse(32,8,18,9);
  if(blink){brush(-29,-20,-15,-20,C.dark,3);brush(15,-20,29,-20,C.dark,3)}
  else{fill(C.dark);ellipse(-22+look,-18,8,13);ellipse(22+look,-18,8,13);fill(C.cream);circle(-24+look,-21,3);circle(20+look,-21,3)}
  let open=energy>.43&&Math.sin(t*10)>.1;
  if(open){fill(C.dark);ellipse(0,7,18,23);fill(C.pink);ellipse(0,14,9,5)}
  else{noFill();stroke(C.dark);strokeWeight(3);arc(0,4,25,17,0,PI)}
  push();translate(42,-58);rotate(.15+wave*.13);fill(C.cream);stroke(C.dark);strokeWeight(2);rect(-3,-3,35,26,4);note(13,10,.19,C.coral);pop();pop()
}
function dancer(x,y,s=1,phase=0,shirt=C.coral){
  let sw=Math.sin(t*6.8+phase),lift=Math.max(0,Math.sin(t*6.8+phase))*13*(.5+energy);
  push();translate(x,y-lift);scale(s);
  let leftKnee=-39-sw*26,rightKnee=39-sw*26;
  strokePath([[-17,-27],[leftKnee,27],[-53-sw*48,73]],C.cream,14,2);
  strokePath([[17,-27],[rightKnee,24],[54-sw*48,73]],C.cream,14,2);
  noStroke();fill(C.dark);ellipse(-58-sw*48,78,76,25);ellipse(59-sw*48,78,76,25);
  fill(C.gold);circle(-34-sw*48,77,6);circle(84-sw*48,77,6);
  let lhand=[-95-sw*30,-129-sw*23],rhand=[96-sw*27,-131+sw*24];
  strokePath([[-31,-99],[-74-sw*14,-90-sw*17],lhand],shirt,17,2);
  strokePath([[31,-99],[73-sw*16,-89+sw*17],rhand],shirt,17,2);
  noStroke();fill(C.cream);circle(...lhand,18);circle(...rhand,18);
  stroke(C.dark);strokeWeight(5);fill(shirt);ellipse(0,-76,78,110);
  fill(C.cream);noStroke();triangle(-25,-108,-4,-77,-21,-65);triangle(25,-108,4,-77,21,-65);
  fill(C.gold);triangle(-7,-87,0,-79,-7,-72);triangle(7,-87,0,-79,7,-72);
  fill(C.dark);circle(0,-57,5);circle(0,-37,5);
  expressiveFace(0,-153,36,phase,Math.round(phase)%3);
  pop()
}
function cabaret(){
  noStroke();fill(35,25,49,200);rect(67,452,1145,178);for(let i=0;i<9;i++){let x=103+i*135;stroke(C.gold);strokeWeight(8);line(x,450,x+60,600)}
  for(let i=0;i<14;i++){let x=96+i*83,y=111+Math.sin(i*2)*28;noStroke();fill(i%2?C.gold:C.coral);ellipse(x,y,13,18);stroke(C.gold);strokeWeight(2);line(x,y,x+22,79)}
  dancer(400,491,1.22,0,C.coral);dancer(640,520,1.05,2,C.teal);dancer(885,492,1.22,4,C.gold);
  textArt('CABARET!',640,204,81,C.cream);small('somebody started a parade',640,269,26,C.gold)
}
function river(){
  let ctx=drawingContext,g=ctx.createLinearGradient(0,360,0,660);g.addColorStop(0,'#438e9c');g.addColorStop(1,'#17384f');ctx.fillStyle=g;ctx.fillRect(55,370,1170,282);
  for(let j=0;j<13;j++){let y=390+j*20;strokePath([[70,y],[280,y+8*Math.sin(t*1.5+j)],[480,y],[720,y+10*Math.cos(t+j)],[970,y],[1200,y+7*Math.sin(t+j)]],j%2?C.mint:C.blue,2+j%3,3,110)}
  push();translate(620+Math.sin(t*.7)*60,382+Math.sin(t*3)*8);fill(C.cream);stroke(C.dark);strokeWeight(5);beginShape();vertex(-230,0);vertex(230,0);vertex(156,68);vertex(-156,68);endShape(CLOSE);fill(C.coral);rect(-137,-71,275,70,15);fill(C.gold);rect(-90,-129,180,57,15);for(let i=0;i<4;i++){fill(C.dark);circle(-102+i*67,-37,24)}
  // The riverboat conducts the chorus with a grin and a raised paddle.
  noStroke();fill(C.cream);ellipse(-40,-105,15,17);ellipse(39,-105,15,17);fill(C.dark);circle(-38+Math.sin(t)*3,-102,7);circle(42+Math.sin(t)*3,-102,7);
  fill(C.pink);ellipse(-65,-91,20,8);ellipse(66,-91,20,8);
  if(energy>.58){fill(C.dark);ellipse(0,-88,16,14)}else{noFill();stroke(C.dark);strokeWeight(3);arc(0,-98,32,22,0,PI)}
  brush(129,-19,169,-100+Math.sin(t*5)*16,C.cream,10);noStroke();fill(C.gold);circle(170,-103+Math.sin(t*5)*16,17);
  fill(C.dark);rect(117,-145,30,76);for(let i=0;i<3;i++)blob(148+i*25,-164-i*21,22+i*6,14+i*2,C.blue,t);pop();
  for(let i=0;i<8;i++)note(165+i*125,326+30*Math.sin(t*2+i),.6,C.gold,.2);
  textArt('MEMPHIS BLUES',640,179,67,C.cream);small('the chorus arrives by riverboat',640,242,24,C.gold)
}
function shoes(){
  noStroke();fill(C.dark);ellipse(640,590,980,110);for(let i=0;i<2;i++){
    let side=i?1:-1,bob=Math.abs(Math.sin(t*7.8+i*PI))*65;
    push();translate(640+side*178,450-bob);rotate(side*.14*Math.sin(t*8));
    fill(i?C.coral:C.teal);stroke(C.dark);strokeWeight(7);rect(-41,-113,82,152,25);
    brush(-37,-55,-73+Math.sin(t*8+i)*18,-13,C.cream,9);brush(39,-57,70-Math.sin(t*8+i)*18,-16,C.cream,9);
    noStroke();fill(C.gold);circle(-75+Math.sin(t*8+i)*18,-13,12);circle(72-Math.sin(t*8+i)*18,-16,12);
    fill(i?C.coral:C.teal);stroke(C.dark);strokeWeight(8);
    beginShape();vertex(-44,20);vertex(25,18);vertex(54,70);vertex(126,86);vertex(130,118);vertex(-68,118);vertex(-70,73);endShape(CLOSE);
    brush(-55,99,121,100,C.cream,5);for(let j=0;j<3;j++)star(17+j*33,62,6,C.gold);
    let blinking=fract((t+i*1.7)/3.1)<.035;
    brush(-30,-89,-10,-94,C.dark,2);brush(10,-94,31,-89,C.dark,2);
    if(blinking){brush(-27,-73,-9,-73,C.dark,3);brush(9,-73,27,-73,C.dark,3)}
    else{noStroke();fill(C.dark);ellipse(-18,-72,8,12);ellipse(18,-72,8,12);fill(C.cream);circle(-20,-76,3);circle(16,-76,3)}
    noStroke();fill(C.pink);ellipse(-31,-53,13,8);ellipse(32,-53,13,8);
    if(energy>.57&&Math.sin(t*9+i)>.15){fill(C.dark);ellipse(0,-48,13,17)}
    else{noFill();stroke(C.dark);strokeWeight(3);arc(0,-52,27,19,0,PI)}
    pop()
  }
  for(let i=0;i<16;i++)star(180+i*57,365+25*Math.sin(i*7+t*5),4+i%3*3,C.gold);
  textArt('GINGER + PEP',640,192,72,C.cream);small('these shoes have absolutely no chill',640,252,25,C.gold)
}
function dance(){
  for(let i=0;i<9;i++){let r=65+i*44;noFill();stroke(i%2?C.gold:C.teal);strokeWeight(4+i%3);arc(640,376,r*2,r*1.4,t*.7+i*.24,t*.7+i*.24+PI*1.24)}
  for(let i=0;i<25;i++){let a=i*2.4+t*(i%2?1:-1)*.8,r=70+i*16;
    star(640+Math.cos(a)*r,369+Math.sin(a)*r*.57,4+i%5,[C.cream,C.coral,C.gold,C.teal][i%4])
  }
  dancer(608+Math.sin(t*3)*30,528,.9,0,C.coral);
  textArt('RAZZ-MA-TAZZ!',640,181,72,C.cream);small('please leave gravity at the door',640,243,25,C.gold)
}
function wind(){
  for(let i=0;i<13;i++){
    let y=90+i*43,x=(t*(50+i*3)+i*170)%1550-130;
    strokePath([[x-260,y+34],[x-180,y-20],[x-64,y+27],[x+55,y-28],[x+178,y+9],[x+260,y-27]],i%2?C.mint:C.cream,5+i%4,12,160)
  }
  for(let i=0;i<15;i++){let x=(i*119+t*(90+i*2))%1410-70,y=340+140*Math.sin(i*.5+t*.5);note(x,y,.45+i%3*.15,i%2?C.coral:C.gold,Math.sin(t+i)*.4)}
  textArt('MUSIC IN THE BREEZE',640,185,59,C.cream);small('the air cannot help humming along',640,245,25,C.gold)
}
function horn(x,y,s=1,ang=0,col=C.gold){
  push();translate(x,y);rotate(ang);scale(s);noFill();stroke(col);strokeWeight(13);bezier(-103,73,-51,35,-93,-46,27,-22);line(27,-22,92,-52);strokeWeight(5);line(20,-35,20,5);line(42,-44,42,-4);line(64,-52,64,-12);
  fill(col);stroke(C.dark);strokeWeight(4);beginShape();vertex(84,-60);vertex(118,-90);vertex(134,-18);vertex(88,-42);endShape(CLOSE);stroke(col);strokeWeight(8);arc(-100,66,42,40,0,PI);pop()
}
function tree(){
  noStroke();fill('#223e43');ellipse(640,600,1120,170);
  strokePath([[620,605],[626,427],[610,282]],C.gold,54,5);strokePath([[622,449],[470,378],[339,314]],C.gold,28,5);strokePath([[610,390],[802,340],[928,258]],C.gold,27,5);
  for(let i=0;i<26;i++){
    let a=i*2.4,r=170+hash(i*3)*125,x=630+Math.cos(a)*r,y=337+Math.sin(a)*r*.72;
    blob(x,y,50+hash(i)*25,25+hash(i+5)*15,i%3===0?C.mint:C.teal,i)
  }
  horn(371,315,.63,-.36,C.coral);horn(892,263,.7,.3,C.gold);horn(610,263,.55,-.18,C.cream);
  for(let i=0;i<7;i++)note(220+i*135,535-50*Math.sin(t*2+i),.45,C.gold,.3);
  textArt('TROMBONES ON TREES',640,108,61,C.cream);small('botany becomes extremely musical',640,625,24,C.gold)
}
function duet(){
  dancer(432,540,1.35,0,C.coral);dancer(843,540,1.35,3,C.teal);
  for(let i=0;i<9;i++){
    let x=282+i*92,y=230-70*Math.sin(t*2+i*.7);note(x,y,.65,i%2?C.gold:C.cream,Math.sin(t+i)*.3)
  }
  textArt('JOIN THE FUN',640,163,75,C.cream);small('even the instruments came as a duet',640,228,23,C.gold)
}
function train(){
  // The vehicle is a saxophone-ish locomotive, with a jingling row of carriages.
  for(let i=0;i<8;i++)brush(0,573+i*14,W,573+i*14,C.cream,i%2?2:4,3,80);
  let x=200+sceneP*920;push();translate(x,472+Math.sin(t*13)*4);
  stroke(C.dark);strokeWeight(7);fill(C.coral);rect(-225,-57,305,116,15);fill(C.gold);rect(58,-110,188,170,22);fill(C.cream);rect(95,-82,83,53,7);fill(C.dark);rect(192,-162,31,56);for(let i=0;i<3;i++)blob(220+i*36,-198-i*38,32+i*7,19,C.blue,t+i);
  fill(C.dark);noStroke();ellipse(121,-55,8,12);ellipse(158,-55,8,12);fill(C.pink);ellipse(100,-7,15,8);ellipse(180,-7,15,8);
  if(energy>.59){fill(C.dark);ellipse(140,0,19,17)}else{noFill();stroke(C.dark);strokeWeight(4);arc(140,-11,38,31,0,PI)}
  for(let i=0;i<4;i++){fill(C.dark);circle(-169+i*107,67,57);fill(C.gold);circle(-169+i*107,67,25)}fill(C.gold);triangle(243,21,308,60,243,60);pop();
  for(let i=0;i<11;i++)note(x-200-i*65,341+25*Math.sin(t*5+i),.55,C.gold,.2);
  textArt('NEXT STOP: JAZZ',640,171,68,C.cream);small('all aboard the last chorus',640,236,25,C.gold)
}
function clock(){
  let sun=clamp((t-143)/9);noStroke();fill(C.cream);circle(960,226,155);fill('#67516d');circle(945,218,137);
  push();translate(535,375);fill(C.gold);stroke(C.dark);strokeWeight(12);circle(0,0,380);fill(C.cream);circle(0,0,327);
  for(let i=0;i<12;i++){let a=i*TWO_PI/12;brush(Math.sin(a)*128,-Math.cos(a)*128,Math.sin(a)*149,-Math.cos(a)*149,C.dark,6)}
  let blink=fract(t/4.1)<.07;
  if(blink){brush(-77,-42,-40,-42,C.dark,5);brush(34,-42,73,-42,C.dark,5)}
  else{noStroke();fill(C.dark);ellipse(-62,-42,12,20);ellipse(58,-42,12,20)}
  noStroke();fill(C.pink);ellipse(-93,12,27,14);ellipse(89,12,27,14);
  if(t>147){fill(C.dark);ellipse(0,86,31,26)}else{noFill();stroke(C.dark);strokeWeight(4);arc(0,53,70,62,0,PI)}
  brush(0,0,94*Math.sin(t*.5),-94*Math.cos(t*.5),C.dark,10);brush(0,0,118*Math.sin(t*2),-118*Math.cos(t*2),C.coral,7);fill(C.dark);circle(0,0,19);pop();
  for(let i=0;i<7;i++)star(155+i*158,160+20*Math.sin(i),7,C.gold);
  textArt('UNTIL MORNING…',965,438,48,C.cream);small('the moon asks for one more dance',965,500,22,C.gold)
}
function finale(){
  for(let i=0;i<70;i++){
    let x=(hash(i*13)*W+t*(i%2?20:-22)+1300)%1400-60;
    let y=(hash(i*38)*H+t*(25+i%6*11))%800-40;
    push();translate(x,y);rotate(t*(i%3-1)*.4);noStroke();fill([C.gold,C.coral,C.teal,C.cream][i%4]);rect(-3,-8,6,16);pop()
  }
  horn(300,475,1,-.28,C.gold);horn(930,485,1.1,.24,C.coral);
  dancer(480,578,.72,0,C.coral);dancer(650,581,.77,2,C.teal);dancer(816,578,.72,4,C.gold);
  for(let i=0;i<9;i++){let x=220+i*103,y=400+80*Math.sin(t*2+i);note(x,y,.65+energy*.4,C.cream,.25)}
  textArt('EVERYBODY!',640,237,92,C.cream);textArt('JAZZ!',640,335,95,C.gold)
}
function end(){
  push();translate(640,355);noFill();stroke(C.gold);strokeWeight(12);circle(0,0,480);stroke(C.coral);strokeWeight(4);circle(0,0,520);pop();
  textArt('THE LAND OF JAZZ',640,308,65,C.cream);small('is still playing',640,387,39,C.gold);
  suitcase(310,538,.8);dancer(973,577,.55,2,C.teal);
  for(let i=0;i<8;i++)note(205+i*125,520+15*Math.sin(i),.6,C.teal,.2)
}
