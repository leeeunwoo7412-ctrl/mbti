import streamlit as st
import time

# 1. 페이지 설정 (웹브라우저 탭에 표시될 내용)
st.set_page_config(
    page_title="오 마이 포켓몬! MBTI 추천",
    page_icon="🐾",
    layout="centered"
)

# 2. 커스텀 CSS로 아기자기하고 귀여운 스타일 적용
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gamja+Flower&display=swap');
    
    /* 전체 폰트를 귀여운 감자꽃체로 설정 */
    html, body, [class*="css"]  {
        font-family: 'Gamja Flower', cursive;
    }
    
    .main-title {
        font-size: 45px;
        font-weight: bold;
        text-align: center;
        color: #ffcb05;
        text-shadow: 3px 3px 0px #3b4cca;
        margin-bottom: 10px;
    }
    .sub-title {
        font-size: 20px;
        text-align: center;
        color: #555555;
        margin-bottom: 30px;
    }
    .result-card {
        background-color: #f0f8ff;
        border: 3px dashed #3b4cca;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
    }
    .poke-name {
        font-size: 32px;
        color: #ff3f3f;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .poke-type {
        display: inline-block;
        background-color: #e2e2e2;
        padding: 5px 15px;
        border-radius: 50px;
        font-size: 14px;
        color: #333;
        margin-bottom: 15px;
    }
    .poke-desc {
        font-size: 18px;
        line-height: 1.6;
        color: #444;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 데이터 설정 (16가지 MBTI별 귀여운 포켓몬 매칭)
pokemon_data = {
    "ISTJ": {
        "name": "꼬부기 (Squirtle) 🐢",
        "type": "💧 물 타입",
        "desc": "꼼꼼하고 책임감이 강한 바른 생활의 표본! 규칙을 잘 지키고 성실한 모습이 꼬부기와 완전 똑 닮았어요! 💙",
        "phrase": "“약속 시간은 무조건 칼같이! 내 사전에 지각은 없다!”"
    },
    "ISFJ": {
        "name": "치코리타 (Chikorita) 🌿",
        "type": "🍃 풀 타입",
        "desc": "주변 사람들을 소리 없이 다정하게 챙겨주는 따뜻한 수호자! 배려심 깊은 초록빛 다정함이 치코리타를 생각나게 해요. 💚",
        "phrase": "“너 아픈 데는 없어? 내가 챙겨줄게!”"
    },
    "INFJ": {
        "name": "신용 (Dragonair) 🐉",
        "type": "🔮 드래곤 타입",
        "desc": "조용하고 신비로운 분위기를 풍기는 깊은 통찰력의 소유자! 겉은 차분해 보이지만 마음속엔 거대한 이상향을 품고 있어요. ✨",
        "phrase": "“너의 고민을 들어줄게. 삶의 깊은 의미를 찾아서...”"
    },
    "INTJ": {
        "name": "메타그로스 (Metagross) 🤖",
        "type": "🧠 강철 / 에스퍼 타입",
        "desc": "엄청난 두뇌와 이성적인 판단력으로 철저하게 계획을 세우는 전략가! 똑 부러진 매력으로 무장한 독립적인 지적 강자입니다! 🔥",
        "phrase": "“모든 일은 내 예상 시나리오 안에 있어.”"
    },
    "ISTP": {
        "name": "브케인 (Cyndaquil) 🔥",
        "type": "🔥 불꽃 타입",
        "desc": "평소엔 조용하고 느긋해 보이지만 필요할 땐 불꽃 같은 집중력을 발휘하는 만능 재주꾼! 과묵하면서도 실력파인 마이웨이 스타일! 😎",
        "phrase": "“간섭은 거절한다! 내 방식대로 조용히 해결할게.”"
    },
    "ISFP": {
        "name": "메타몽 (Ditto) 🫠",
        "type": "⭐ 노말 타입",
        "desc": "어떤 상황이든 말랑말랑 유연하게 적응하는 평화주의 예술가! 따뜻한 감성을 지녔고 흘러가는 대로 자유롭게 살아가는 것을 좋아해요. 🎨",
        "phrase": "“좋은 게 좋은 거지~ 흘러가는 대로 살자구!”"
    },
    "INFP": {
        "name": "이브이 (Eevee) 🦊",
        "type": "⭐ 노말 타입",
        "desc": "무한한 가능성과 다채로운 꿈을 품은 낭만 가득한 예술가! 감수성이 풍부하고 여린 마음씨를 가진 우리들의 소중한 이브이네요! 💕",
        "phrase": "“나만의 특별한 세계와 꿈이 있어. 언젠가 멋지게 진화할 거야!”"
    },
    "INTP": {
        "name": "폴리곤 (Porygon) 👾",
        "type": "⭐ 노말 타입",
        "desc": "호기심이 넘치고 끊임없이 생각하는 아이디어 뱅크! 논리적이고 과학적인 분석을 좋아해서 컴퓨터 속 세상이 잘 어울리는 천재 포켓몬! 💻",
        "phrase": "“왜 그럴까? 원인을 과학적으로 증명해보자!”"
    },
    "ESTP": {
        "name": "피카츄 (Pikachu) ⚡",
        "type": "⚡ 전기 타입",
        "desc": "에너지가 뿜뿜 솟아나고 스릴을 즐기는 모험가! 넘치는 친화력과 행동력으로 어디서나 주인공이 되는 인기쟁이 피카츄랍니다! 💛",
        "phrase": "“일단 해보는 거야! 피카피카! 고민할 시간에 고!”"
    },
    "ESFP": {
        "name": "푸린 (Jigglypuff) 🎵",
        "type": "🎤 페어리 타입",
        "desc": "노래 부르고 춤추는 것을 좋아하는 분위기 메이커! 사람들의 관심을 먹고 사는 사랑스러운 스타성에 애교까지 넘쳐나요! 💕",
        "phrase": "“모두 나를 주목해! 오늘은 내가 주인공~ 랄라라~🎵”"
    },
    "ENFP": {
        "name": "뮤 (Mew) ✨",
        "type": "🔮 에스퍼 타입",
        "desc": "호기심 많고 장난기 넘치며 매일 새로운 에너지를 뿜어내는 긍정 대마왕! 사람들을 기분 좋게 만드는 마법 같은 매력을 지녔어요! 🌈",
        "phrase": "“와! 저건 뭐지? 매일매일이 흥미진진하고 신나!”"
    },
    "ENTP": {
        "name": "팬텀 (Gengar) 😈",
        "type": "👻 고스트 / 독 타입",
        "desc": "재치 있는 드립과 독창적인 생각으로 무장한 유쾌한 장난꾸러기! 토론과 도전을 즐기며 남들이 가지 않는 새로운 길을 창조합니다! 💜",
        "phrase": "“뻔한 건 재미없잖아? 내 매력에 한번 빠져볼래?”"
    },
    "ESTJ": {
        "name": "윈디 (Arcanine) 🦁",
        "type": "🔥 불꽃 타입",
        "desc": "강력한 리더십과 듬직함을 겸비한 타고난 대장님! 일 처리가 확실하고 주변을 통솔하는 능력이 뛰어나서 신뢰감이 가득해요! 👑",
        "phrase": "“나를 따르라! 완벽하게 마무리지어 주지.”"
    },
    "ESFJ": {
        "name": "토게피 (Togepi) 🥚",
        "type": "🧚 페어리 타입",
        "desc": "누구에게나 친절하고 다정한 사교성 최고봉! 친구들의 경조사를 가장 먼저 챙기고, 모두가 행복하길 바라는 사랑스러운 평화주의자입니다! 💞",
        "phrase": "“다 같이 행복하게 지내자! 맛있는 거 먹으러 갈 사람?”"
    },
    "ENFJ": {
        "name": "망나뇽 (Dragonite) 🧡",
        "type": "🐉 드래곤 / 비행 타입",
        "desc": "곤경에 처한 사람을 절대 지나치지 못하는 따뜻하고 정의로운 영웅! 사람들을 긍정적으로 이끌어주는 멋진 멘토 역할을 톡톡히 해내요. 🌟",
        "phrase": "“힘들 땐 언제든 내 넓은 날개에 기대렴!”"
    },
    "ENTJ": {
        "name": "리자몽 (Charizard) 🔥",
        "type": "🔥 불꽃 / 비행 타입",
        "desc": "한 번 정한 목표는 불꽃처럼 거침없이 돌파하는 열정적인 지도자! 자신감 넘치고 강력한 추진력으로 사람들을 이끄는 카리스마 보스입니다! 🦖",
        "phrase": "“불가능은 없다! 오직 앞만 보고 전진한다!”"
    }
}

# 4. 화면 구성
st.markdown('<div class="main-title">🐾 오 마이 포켓몬! 🐾</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">성향을 선택하고 나에게 꼭 맞는 귀여운 포켓몬을 만나보세요!</div>', unsafe_allow_html=True)

# 이름 입력 받기
name = st.text_input("당신의 이름을 알려주세요! 😊", "으누")

st.divider()

# 인터랙티브한 MBTI 선택기 (4열 구성)
col1, col2, col3, col4 = st.columns(4)

with col1:
    e_i = st.radio("에너지 방향 🔋", ["E (외향형)", "I (내향형)"])
with col2:
    s_n = st.radio("인식 방식 👁️", ["S (감각형)", "N (직관형)"])
with col3:
    t_f = st.radio("판단 방식 🧠", ["T (사고형)", "F (감정형)"])
with col4:
    j_p = st.radio("대처 방식 📅", ["J (판단형)", "P (인식형)"])

# 선택된 성향에서 이니셜만 추출 (예: "E (외향형)" -> "E")
mbti_result = e_i[0] + s_n[0] + t_f[0] + j_p[0]

st.write("")

# 결과 확인 버튼
if st.button("🌟 내 운명의 포켓몬 찾기! 🌟", use_container_width=True):
    # 재미있는 딜레이 효과
    with st.spinner("두구두구... 당신의 성향을 포켓몬 볼에 분석 중... 🔴"):
        time.sleep(1.5)
    
    # 풍선 효과!
    st.balloons()
    
    # 매칭되는 포켓몬 데이터 가져오기
    pokemon = pokemon_data.get(mbti_result)
    
    if pokemon:
        # 귀여운 결과 카드 렌더링
        st.markdown(f"""
            <div class="result-card">
                <h2>{name}님의 MBTI 결과: <b>{mbti_result}</b></h2>
                <div class="poke-name">{pokemon['name']}</div>
                <div class="poke-type">{pokemon['type']}</div>
                <p class="poke-desc">“ {pokemon['phrase']} ”</p>
                <hr style="border:1px dashed #ccc;">
                <p class="poke-desc">{pokemon['desc']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.success(f"🎉 축하합니다! {name}님은 정말 멋진 포켓몬과 닮으셨네요!")
