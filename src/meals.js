/* ---------- meal plan ----------
   [끼니, 장소/메뉴, 설명, 태그]  태그: rsv=예약 추천, home=집밥, air=기내·공항 · 프랑스어 이름 뒤 괄호는 발음 */
const MP_ko = {
 A:{
  "11/25":[["점심","학교 · 회사","",""],["저녁","얼바인 집에서 이른 저녁","공항 가기 전 든든하게, 국물 요리 추천",'home'],["밤","기내 간식 · 피닉스 공항","환승 시간에 물과 간식 사 두기",'air']],
  "11/26":[["아침","필라델피아 공항 (환승 중)","커피와 샌드위치",'air'],["점심","Chez Ashton (셰 애슈턴)","1969년 퀘벡시티에서 시작한 푸틴 가게, 카운터 주문",""],["저녁","Aux Anciens Canadiens (오 장시앵 카나디앵)","1675년 지은 ‘자케 집’에서 먹는 투르티에르와 메이플 슈거파이(tarte au sucre, 따르트 오 쒸크르)",'rsv']],
  "11/27":[["아침","Paillard (파야르) · 생장 거리","크루아상과 핫초콜릿(chocolat chaud, 쇼콜라 쇼), 아침 일찍 줄이 짧음",""],["점심","La Midinette (라 미디네트) · 오를레앙섬 생장 마을","9–16시, 수프·샌드위치·크레프, 1인 CAD $10–20",""],["저녁","Le Lapin Sauté (르 라팽 소테) · 프티 샹플랭","토끼·오리 요리와 메이플 크렘 브륄레, 아이 메뉴 있음",'rsv']],
  "11/28":[["아침","Le Petit Cochon Dingue (르 프티 코숑 댕그)","1979년부터 프티 샹플랭의 아침 카페, 에그 베네딕트",""],["점심","기차 도시락 (Paillard 샌드위치)","VIA 이코노미 간식 카트도 있음",""],["저녁","Schwartz's Deli (슈워츠 델리)","1928년부터 이어진 몬트리올 훈제고기 샌드위치, 예약 없이 줄 서기",""]],
  "11/29":[["아침","St-Viateur Bagel (생비아퇴르 베이글)","24시간 장작 오븐, 갓 나온 참깨 베이글과 크림치즈",""],["점심","몬트리올 공항 (미국 사전입국심사 뒤)","심사 뒤 탑승구 쪽 식당에서",'air'],["저녁","기내 · 집","19:01 SNA 도착, 피자 배달 추천",'home']]
 }
};
const MP_en = {
 A:{
  "11/25":[["Lunch","School · work","",""],["Dinner","Early dinner at home in Irvine","Eat well before the airport, soup is a good idea",'home'],["Night","Snacks on board · Phoenix airport","Buy water and snacks during the connection",'air']],
  "11/26":[["Breakfast","Philadelphia airport (connecting)","Coffee and a sandwich",'air'],["Lunch","Chez Ashton (shay ASH-ton)","Quebec City's own poutine chain since 1969, order at the counter",""],["Dinner","Aux Anciens Canadiens (oh zahn-SYAN kah-nah-DYAN)","Tourtière and maple sugar pie (tarte au sucre, tart oh SEW-kruh) in a house built in 1675",'rsv']],
  "11/27":[["Breakfast","Paillard (pie-YAR) · rue Saint-Jean","Croissants and hot chocolate (chocolat chaud, shoh-koh-LAH SHOH); short line early",""],["Lunch","La Midinette (lah mee-dee-NET) · Saint-Jean, Île d'Orléans","9 a.m.–4 p.m., soup, sandwiches, crêpes, CAD $10–20 per person",""],["Dinner","Le Lapin Sauté (luh lah-PAN soh-TAY) · Petit Champlain","Rabbit and duck dishes, maple crème brûlée, kids' menu",'rsv']],
  "11/28":[["Breakfast","Le Petit Cochon Dingue (luh puh-TEE koh-SHOHN DANG)","Petit Champlain breakfast café since 1979, eggs Benedict",""],["Lunch","Train picnic (Paillard sandwiches)","VIA economy also has a snack cart",""],["Dinner","Schwartz's Deli","Montreal smoked meat since 1928, no reservations, line up",""]],
  "11/29":[["Breakfast","St-Viateur Bagel (san vee-ah-TUHR)","Wood-fired oven open 24 hours, hot sesame bagels and cream cheese",""],["Lunch","Montreal airport (after U.S. preclearance)","Eat near the gate after clearing U.S. customs",'air'],["Dinner","On board · home","Land at SNA 7:01 p.m., order pizza",'home']]
 }
};
