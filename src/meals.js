/* ---------- meal plan ----------
   [끼니, 장소/메뉴, 설명, 태그]  태그: rsv=예약 추천, home=집밥, air=기내·공항, cash=현금만 */
const MP = {
 A:{
  "11/25":[["점심","학교 · 회사","",""],["저녁","얼바인 집에서 이른 저녁","공항 가기 전 든든하게, 국물 요리 추천",'home'],["밤","기내 간식 · 피닉스 공항","환승 시간에 물과 간식 사 두기",'air']],
  "11/26":[["아침","필라델피아 공항 (환승 중)","커피와 샌드위치",'air'],["점심","Chez Ashton","1969년 퀘벡시티에서 시작한 푸틴 가게, 카운터 주문",""],["저녁","Aux Anciens Canadiens","1675년 지은 ‘자케 집’에서 먹는 투르티에르와 메이플 슈거파이",'rsv']],
  "11/27":[["아침","Paillard (생장 거리)","크루아상과 핫초콜릿, 아침 일찍 줄이 짧음",""],["점심","La Midinette (오를레앙섬 생장 마을)","9–16시, 수프·샌드위치·크레프, 1인 CAD $10–20",""],["저녁","Le Lapin Sauté (프티 샹플랭)","토끼·오리 요리와 메이플 크렘 브륄레, 아이 메뉴 있음",'rsv']],
  "11/28":[["아침","Le Petit Cochon Dingue","1979년부터 프티 샹플랭의 아침 카페, 에그 베네딕트",""],["점심","기차 도시락 (Paillard 샌드위치)","VIA 이코노미 간식 카트도 있음",""],["저녁","Schwartz's Deli","1928년부터 이어진 몬트리올 훈제고기 샌드위치, 예약 없이 줄 서기",""]],
  "11/29":[["아침","St-Viateur Bagel","24시간 장작 오븐, 갓 나온 참깨 베이글과 크림치즈",""],["점심","몬트리올 공항 (미국 사전입국심사 뒤)","심사 뒤 탑승구 쪽 식당에서",'air'],["저녁","기내 · 집","19:01 SNA 도착, 피자 배달 추천",'home']]
 }
};
const MTAG = {inc:"포함", rsv:"예약 추천", home:"집밥", air:"공항·기내", cash:"현금"};
function mealsBlock(team, d, kids, override){
  const m = override || MP[team][d]; if(!m) return "";
  if(kids) return `<div class="meals"><h4>오늘 뭐 먹지?</h4>${m.map(([k,w])=>`<div><b>${k}</b><span>${w}</span></div>`).join("")}</div>`;
  return `<div class="meals"><h4>오늘의 식사</h4>${m.map(([k,w,n,t])=>`<div><b>${k}</b><span>${w}${t?`<span class="mtag ${t}">${MTAG[t]}</span>`:""}${n?`<small>${n}</small>`:""}</span></div>`).join("")}</div>`;
}
const highlightMeal = (team,d) => { const m=MP[team][d]||[]; const pick = m.find(x=>x[3]==="rsv") || m.find(x=>!x[3] && x[2]) || m[2]; return pick ? `${pick[0]} · ${pick[1].replace(/ \(.*\)$/,"")}` : ""; };
