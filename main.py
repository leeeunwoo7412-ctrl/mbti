import streamlit as st
import time

# 1. 페이지 설정
st.set_page_config(
    page_title="오 마이 포켓몬! MBTI 추천",
    page_icon="⚡",
    layout="centered"
)

# 2. 커스텀 CSS (귀여운 폰트 + 무지갯빛으로 번쩍이는 네온 효과 적용)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gamja+Flower&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Gamja Flower', cursive;
    }
    
    /* 제목 스타일 */
    .main-title {
        font-size: 45px;
        font-weight: bold;
        text-align: center;
        color: #ffcb05;
        text-shadow: 3px 3px 0px #3b4cca;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 20px;
        text-align: center;
        color: #555555;
        margin-bottom: 25px;
    }
    
    /* 기본 결과 카드 */
    .result-card {
        background-color: #ffffff;
        border: 3px dashed #3b4cca;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .poke-name {
        font-size: 32px;
        color: #ff3f3f;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    /* ★ 핵심: 무지갯빛으로 번쩍번쩍 빛나는 네온 애니메이션 효과 ★ */
    @keyframes rainbow-glow {
        0% {
            border-color: #ff4b4b;
            box-shadow: 0 0 15px #ff4b4b, inset 0 0 8px #ff4b4b;
        }
        33% {
            border-color: #00e5ff;
            box-shadow: 0 0 25px #00e5ff, inset 0 0 12px #00e5ff;
        }
        66% {
            border-color: #ffeb3b;
            box-shadow: 0 0 20px #ffeb3b, inset 0 0 10px #ffeb3b;
        }
        100% {
            border-color: #e040fb;
            box-shadow: 0 0 30px #e040fb, inset 0 0 15px #e040fb;
        }
    }
    
    /* 번쩍이는 행동 추천 컨테이너 */
    .sparkle-box {
        background-color: #1a1a1a; /* 어두운 배경에서 네온이 더 잘 번쩍여요! */
        color: #ffffff !important;
        border: 4px solid #ff4b4b;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        margin-top: 25px;
        animation: rainbow-glow 2s infinite alternate ease-in-out; /* 무한 반복 애니메이션 */
    }
    
    .sparkle-title {
        font-size: 26px;
        font-weight: bold;
        color: #ffeb3b;
        text-shadow: 0 0 8px #ffeb3b;
        margin-bottom: 15px;
    }
    
    .action-item {
        font-size: 20px;
        margin: 10px 0;
        background: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 10px;
        display: inline-block;
        width: 90%;
    }
    </style>
""", unsafe_allow_html=True)

# 3. MBTI별 포켓몬 정보 + 번쩍이는 추천 활동 데이터 세팅
pokemon_data = {
    "ISTJ": {
        "name": "꼬부기 (Squirtle) 🐢",
        "type": "💧 물 타입",
        "desc": "꼼꼼하고 책임감이 강한 바른 생활의 표본! 규칙을 잘 지키고 성실한 모습이 꼬부기와 똑 닮았어요! 💙",
        "phrase": "약속 시간은 무조건 칼같이! 내 사전에 지각은 없다!",
        "actions": ["📋 다음 주 플래너 완벽하게 정리하기", "🧹 지저분한 방 서랍 칼각 맞춰 청소하기", "✍️ 오답노트 정독하며 완벽 복습하기"]
    },
    "ISFJ": {
        "name": "치코리타 (Chikorita) 🌿",
        "type": "🍃 풀 타입",
        "desc": "주변 사람들을 소리 없이 다정하게 챙겨주는 따뜻한 수호자! 배려심 깊은 초록빛 다정함을 가졌어요. 💚",
        "phrase": "너 아픈 데는 없어? 내가 약 챙겨줄게!",
        "actions": ["💌 소중한 친구에게 깜짝 비밀 편지 쓰기", "🍪 정성 담긴 홈베이킹으로 가족들 감동 주기", "🪴 방 안의 반려식물 먼지 닦아주고 물 주기"]
    },
    "INFJ": {
        "name": "신용 (Dragonair) 🐉",
        "type": "🔮 드래곤 타입",
        "desc": "조용하고 신비로운 분위기를 풍기는 통찰력의 소유자! 겉은 차분하지만 마음속엔 이상향을 품고 있어요. ✨",
        "phrase": "너의 고민을 들어줄게. 삶의 깊은 의미를 찾아서...",
        "actions": ["📚 잔잔한 재즈를 들으며 철학 책 깊게 읽기", "🎧 나만 알고 싶은 인생 새벽 플레이리스트 짜기", "📝 일기장에 오늘의 깊은 생각들 기록하기"]
    },
    "INTJ": {
        "name": "메타그로스 (Metagross) 🤖",
        "type": "🧠 강철 / 에스퍼 타입",
        "desc": "엄청난 두뇌와 이성적인 판단력으로 철저하게 계획을 세우는 전략가! 똑 부러진 매력의 지적 강자입니다! 🔥",
        "phrase": "모든 일은 내 예상 시나리오 안에 있어.",
        "actions": ["💻 코딩으로 나만의 신박한 프로그램 만들기", "♟️ 고난도 전략 게임이나 체스로 승리 쟁취하기", "🎬 미지의 우주/과학 다큐멘터리 집중 분석하기"]
    },
    "ISTP": {
        "name": "브케인 (Cyndaquil) 🔥",
        "type": "🔥 불꽃 타입",
        "desc": "평소엔 조용하고 느긋해 보이지만 필요할 땐 불꽃 같은 집중력을 발휘하는 재주꾼! 과묵하면서도 실력파인 마이웨이! 😎",
        "phrase": "간섭은 거절한다! 내 방식대로 조용히 해결할게.",
        "actions": ["🔧 망가진 기계나 레고 세트 조립해보기", "🛹 인적 드문 공원에서 보드나 스케이트 타기", "🛋️ 만사 귀찮을 땐 침대에서 멍 때리며 충전하기"]
    },
    "ISFP": {
        "name": "메타몽 (Ditto) 🫠",
        "type": "⭐ 노말 타입",
        "desc": "어떤 상황이든 말랑말랑 유연하게 적응하는 평화주의자! 따뜻한 감성을 지녔고 흘러가는 대로 자유롭게 살아가요. 🎨",
        "phrase": "좋은 게 좋은 거지~ 흘러가는 대로 살자구!",
        "actions": ["🍿 이불 똘똘 말고 넷플릭스 하루 종일 정주행하기", "🎨 좋아하는 색깔 가득 담아 아이패드에 힐링 드로잉하기", "🧸 아기자기하고 귀여운 소품으로 침대 주변 꾸미기"]
    },
    "INFP": {
        "name": "이브이 (Eevee) 🦊",
        "type": "⭐ 노말 타입",
        "desc": "무한한 가능성과 다채로운 꿈을 품은 낭만 가득한 예술가! 감수성이 풍부하고 여린 마음씨를 지녔어요! 💕",
        "phrase": "나만의 특별한 세계가 있어. 언젠가 멋지게 진화할 거야!",
        "actions": ["✍️ 주인공이 되어 환상적인 소설이나 시 쓰기", "🌌 밤하늘 보며 우주의 보이지 않는 비밀 상상하기", "💬 마음 맞는 찐친 한 명과 새벽 감성으로 깊은 대화하기"]
    },
    "INTP": {
        "name": "폴리곤 (Porygon) 👾",
        "type": "⭐ 노말 타입",
        "desc": "호기심이 넘치고 끊임없이 생각하는 아이디어 뱅크! 논리적이고 과학적인 분석을 좋아합니다! 💻",
        "phrase": "왜 그럴까? 원인을 과학적으로 증명해보자!",
        "actions": ["🪐 신비로운 블랙홀과 지구 과학 이론 덕질하기", "🧩 머리 깨지는 고난도 스도쿠나 퍼즐 격파하기", "🤖 새로운 전자기기나 소프트웨어 기능 완전 정복하기"]
    },
    "ESTP": {
        "name": "피카츄 (Pikachu) ⚡",
        "type": "⚡ 전기 타입",
        "desc": "에너지가 뿜뿜 솟아나고 스릴을 즐기는 모험가! 넘치는 친화력과 행동력으로 어디서나 주인공이 됩니다! 💛",
        "phrase": "일단 해보는 거야! 고민할 시간에 바로 고!",
        "actions": ["🏃 친구들 소집해서 즉석 풋살이나 피구 한판 하기", "🎥 맛있는 디저트 먹방 쇼츠/릴스 직접 촬영하기", "🏆 게임 배틀이나 미니 대기 대회에서 압승 거두기"]
    },
    "ESFP": {
        "name": "푸린 (Jigglypuff) 🎵",
        "type": "🎤 페어리 타입",
        "desc": "노래 부르고 춤추는 것을 좋아하는 분위기 메이커! 사람들의 관심을 좋아하는 사랑스러운 스타! 💕",
        "phrase": "모두 나를 주목해! 오늘은 내가 주인공~ 🎵",
        "actions": ["🎤 코인노래방 가서 목이 터져라 최애곡 지르기", "🥳 기분 꿀꿀한 친구들을 위해 깜짝 텐션 업 쇼하기", "👗 내일 입고 나갈 최고로 멋진 OOTD 패션쇼 하기"]
    },
    "ENFP": {
        "name": "뮤 (Mew) ✨",
        "type": "🔮 에스퍼 타입",
        "desc": "호기심 많고 장난기 넘치며 매일 새로운 에너지를 뿜어내는 긍정 대마왕! 사람들을 기분 좋게 만들어요! 🌈",
        "phrase": "와! 저건 뭐지? 매일매일이 흥미진진하고 신나!",
        "actions": ["✈️ 친구에게 '지금 당장 바다 갈래?' 물어보기 (즉흥)", "🐕 산책하는 강아지에게 온갖 이구동성 귀여운 소리 내기", "💡 머릿속에 떠오른 기상천외한 발명 아이디어 친구에게 영업하기"]
    },
    "ENTP": {
        "name": "팬텀 (Gengar) 😈",
        "type": "👻 고스트 / 독 타입",
        "desc": "재치 있는 드립과 독창적인 생각으로 무장한 유쾌한 장난꾸러기! 토론과 도전을 즐기며 새로운 길을 만들어요! 💜",
        "phrase": "뻔한 건 재미없잖아? 내 천재적인 매력에 빠져봐!",
        "actions": ["🧪 유튜브 보고 신기하고 쓸모없는 실험 직접 해보기", "🗣️ 말도 안 되는 주제로 친구랑 핏대 세우며 토론 배틀하기", "🚀 완전히 새로운 이색 취미 찍먹해보기"]
    },
    "ESTJ": {
        "name": "윈디 (Arcanine) 🦁",
        "type": "🔥 불꽃 타입",
        "desc": "강력한 리더십과 듬직함을 겸비한 타고난 대장님! 일 처리가 확실하고 주변을 통솔하는 능력이 뛰어납니다! 👑",
        "phrase": "나를 따르라! 완벽하게 마무리지어 주지.",
        "actions": ["👑 조별 과제나 동아리 리더 맡아서 완벽 캐리하기", "📊 내 수입과 지출 내역 가계부로 철저히 분석하기", "⏱️ 오늘 하루 계획을 분 단위로 체크하며 뿌듯해하기"]
    },
    "ESFJ": {
        "name": "토게피 (Togepi) 🥚",
        "type": "🧚 페어리 타입",
        "desc": "누구에게나 친절하고 다정한 사교성 최고봉! 친구들을 가장 먼저 챙겨주는 사랑스러운 평화주의자! 💞",
        "phrase": "다 같이 행복하게 지내자! 맛있는 거 먹으러 가자!",
        "actions": ["🎁 우울해하는 친구 몰래 음료수 기프티콘 쏴주기", "🍕 친구들 다 모아서 떠들썩하고 행복한 떡볶이 파티 열기", "💬 단톡방에서 친구들 한 명 한 명 리액션 폭발해주기"]
    },
    "ENFJ": {
        "name": "망나뇽 (Dragonite) 🧡",
        "type": "🐉 드래곤 / 비행 타입",
        "desc": "곤경에 처한 사람을 절대 지나치지 못하는 정의로운 영웅! 사람들을 긍정적으로 리드하는 멋진 멘토! 🌟",
        "phrase": "힘들 땐 언제든 내 넓은 날개에 기대렴!",
        "actions": ["🤝 도움이 필요한 학교 후배나 친구 멘토링해주기", "💖 사람들의 하루를 기분 좋게 만들 칭찬 폭격기 되기", "📢 공동의 목표를 이뤄내기 위해 파이팅 구호 외치기"]
    },
    "ENTJ": {
        "name": "리자몽 (Charizard) 🔥",
        "type": "🔥 불꽃 / 비행 타입",
        "desc": "목표는 불꽃처럼 거침없이 돌파하는 지도자! 강력한 추진력으로 사람들을 이끄는 카리스마 보스! 🦖",
        "phrase": "불가능은 없다! 오직 앞만 보고 전진한다!",
        "actions": ["📊 야심 차고 성공 확률 높은 창업 아이디어 구상하기", "🎤 수많은 청중 앞에서 카리스마 넘치는 스피치 하기", "📈 내 성장에 방해되는 안 좋은 버릇 오늘부터 손절하기"]
    }
}

# 4. 화면 구성
st.markdown('<div class="main-title">⚡ 오 마이 포켓몬! ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">당신의 성향을 고르고, 당신에게 딱 맞는 활기찬 에너지를 채워보세요!🌈</div>', unsafe_allow_html=True)

name = st.text_input("당신의 이름을 알려주세요! 😊", "으누")

st.divider()

# MBTI 간편 선택기
col1, col2, col3, col4 = st.columns(4)
with col1:
    e_i = st.radio("에너지 🔋", ["E (외향형)", "I (내향형)"])
with col2:
    s_n = st.radio("인식 👁️", ["S (감각형)", "N (직관형)"])
with col3:
    t_f = st.radio("판단 🧠", ["T (사고형)", "F (감정형)"])
with col4:
    j_p = st.radio("대처 📅", ["J (판단형)", "P (인식형)"])

mbti_result = e_i[0] + s_n[0] + t_f[0] + j_p[0]

st.write("")

# 결과 확인하기 버튼
if st.button("✨ 내 찰떡 포켓몬 & 어울리는 일 확인하기 ✨", use_container_width=True):
    with st.spinner("🌟 몬스터볼 속에서 운명의 포켓몬이 깨어나는 중... 🌟"):
        time.sleep(1.2)
        
    st.balloons()
    
    pokemon = pokemon_data.get(mbti_result)
    
    if pokemon:
        # 일반 결과 화면
        st.markdown(f"""
            <div class="result-card">
                <h3 style="color:#555;">💎 {name}님의 성향 분석: {mbti_result}</h3>
                <div class="poke-name">{pokemon['name']}</div>
                <div style="font-size: 18px; color: #777; margin-bottom: 10px;"><b>{pokemon['type']}</b></div>
                <p style="font-size: 20px; font-style: italic; color: #444;">" {pokemon['phrase']} "</p>
                <hr style="border:1px dashed #ddd;">
                <p style="font-size: 18px; color: #666; line-height: 1.6;">{pokemon['desc']}</p>
            </div>
        """, unsafe_allow_html=True)
        
        # 번쩍이는 효과가 적용된 어울리는 일/행동 카드
        st.markdown(f"""
            <div class="sparkle-box">
                <div class="sparkle-title">✨ {name}님을 심쿵하게 할 추천 행동 리스트 ✨</div>
                <p style="color: #ffeb3b; font-size: 16px;">(하고 나면 만족감 폭발! 네온처럼 번쩍이는 오늘 하루를 보장해요! 💫)</p>
                <div class="action-item">🌟 {pokemon['actions'][0]}</div>
                <div class="action-item">⚡ {pokemon['actions'][1]}</div>
                <div class="action-item">🔥 {pokemon['actions'][2]}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.success(f"🎉 {name}님, 멋진 포켓몬과 함께 오늘 하루도 반짝반짝 빛나길 바랄게요!")
