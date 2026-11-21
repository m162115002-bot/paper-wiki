"""Grounded 22-slide dataset for Chapter 11 offline demo & testing."""

CH11_META = {
  "deck_title": "Chapter 11: 疼痛的本質與症狀（The Nature and Symptoms of Pain）",
  "presenter": "黃少杰",
  "course": "健康心理學",
  "date": "2026/11/21"
}

CH11_SLIDES = [
  {
    "slide_no": 1,
    "unit_id": "cover",
    "unit_badge": "Health Psychology · Chapter 11",
    "action_title": "疼痛的本質與症狀：從神經傳導到心理社會與臨床評估",
    "subtitle": "The Nature and Symptoms of Pain — Sarafino & Smith (2017), pp. 288–313",
    "bullets": [
      "單元一：疼痛本質、分類與知覺",
      "單元二：門控理論與神經化學止痛",
      "單元三：心理社會、情緒與因應",
      "單元四：成人多維度疼痛評估",
      "單元五：兒童疼痛與發展評估"
    ],
    "sticker": "brain",
    "theme_tint": "pink",
    "est_minutes": 1.0,
    "speaker_notes": "大家好，我是黃少杰。今天要跟大家分享健康心理學第 11 章——疼痛的本質與症狀。我們平常都很討厭疼痛，但其實疼痛不只是單純的身體受傷訊號，它還跟大腦調節、情緒、記憶、甚至家庭互動緊密相連。接下來大約 25 到 30 分鐘，我會分成五大單元，帶大家從疼痛的定義與生理機制一路看到臨床上怎麼評估成人與兒童的疼痛。",
    "apa_citation": "Sarafino & Smith (2017), pp. 288–313"
  },
  {
    "slide_no": 2,
    "unit_id": "unit_1",
    "unit_badge": "導覽與重要性",
    "action_title": "疼痛雖令人不適，卻是維繫生存的保護警訊與最普遍的就醫原因",
    "highlight_stats": [
      {
        "value": "> 80%",
        "label": "所有醫師就診主訴與疼痛相關 (Gatchel et al., 2007)"
      },
      {
        "value": "27% / 28%",
        "label": "美國 ≥18 歲成人 3 個月內關節痛 / 下背痛盛行率 (NCHS, 2014)"
      },
      {
        "value": "29 歲",
        "label": "先天性無痛症個案因未察覺傷病而早逝 (Bakal, 1979)"
      }
    ],
    "bullets": [
      "生存價值：先天性無痛症（congenital insensitivity to pain）患者因感受不到燙傷、咬傷或盲腸炎等急症，常因未及時治療而早逝。",
      "生活與經濟衝擊：頭痛、背痛與關節痛是美國最常見的工作缺席與失能原因，每年造成數百億美元生產力與醫療支出（Thorn & Walker, 2011）。",
      "健康心理學視角：疼痛直接決定人們是否及時就醫與遵從醫囑，並深刻衝擊情緒、工作與人際適應。"
    ],
    "sticker": "bell",
    "theme_tint": "lemon",
    "est_minutes": 1.5,
    "speaker_notes": "很多人可能想過，如果一輩子都不會痛該有多好？但課本一開頭就舉了一個震撼的例子：先天性無痛症患者天生感覺不到痛，連咬斷舌尖或跪在滾燙暖氣上三度灼傷都沒感覺，這名個案最後因為無法察覺嚴重傷病而在 29 歲過世。可見疼痛是重要的生存保護訊號。在臨床上，超過八成的就醫主訴都跟疼痛有關，美國成年人每三個月就有近三成經歷關節痛或下背痛。今天我們就會沿著五大單元，逐步拆解疼痛的全貌。",
    "apa_citation": "Sarafino & Smith (2017), pp. 288–289; Gatchel et al. (2007); NCHS (2014)"
  },
  {
    "slide_no": 3,
    "unit_id": "unit_1",
    "unit_badge": "單元一 · 疼痛本質",
    "action_title": "器質性與心因性疼痛是連續體，無器質病因不代表疼痛是想像的",
    "bullets": [
      "疼痛定義（AMA, 2003）：與實際或潛在組織損傷或刺激相關的「感覺與情緒不適經驗」。",
      "疼痛質性依位置而異：表層皮膚短暫傷害常呈「銳痛（sharp）」；深層組織損傷多呈「鈍痛、痠痛或搏動痛（dull/aching/throbbing）」。",
      "破除二分迷思：過去誤把找不到生理病因的「心因性疼痛（psychogenic pain）」當成病人想像；Bakal（1979）強調心因性與器質性疼痛同樣真實且同樣痛苦。",
      "中樞敏感化：長期持續疼痛本身即會造成神經系統結構與功能改變，使個體對痛刺激高度敏感（Woolf, 2011）。"
    ],
    "sticker": "heart_chat",
    "theme_tint": "pink",
    "est_minutes": 1.5,
    "speaker_notes": "首先進入第一單元：什麼是疼痛？按照美國醫學會的定義，疼痛同時包含感覺與情緒兩個成分。過去醫界常把找不到生理病因的痛叫心因性疼痛，甚至誤以為病人在裝病或自己想像。但其實疼痛研究者 Bakal 早就指出，心因性和器質性疼痛感受上完全一樣，都會讓人非常痛苦。現在我們把它看作一個連續體——幾乎所有疼痛都是生理和心理因素共同作用，而且痛久了本身就會改變神經系統，讓身體變得更敏感。",
    "apa_citation": "Sarafino & Smith (2017), pp. 289–290; Bakal (1979); Woolf (2011)"
  },
  {
    "slide_no": 4,
    "unit_id": "unit_1",
    "unit_badge": "單元一 · 急性與慢性痛",
    "action_title": "慢性疼痛不只是變長的急性痛，而是會全面重塑患者的心理世界",
    "bullets": [
      "急性痛（Acute Pain，< 3 個月）：焦慮隨復原消退；以燒傷為例（美國年逾 480,000 例），除止痛藥外，心理準備增強控制感與 VR 分心皆可顯著減少用藥需求（Wernick, 1983; Hoffman et al., 2011）。",
      "慢性痛（Chronic Pain）：持續逾預期病程或數月，常伴隨高度焦慮、無助、無望感，生活圈萎縮至「家、診所與藥局」。"
    ],
    "table": {
      "headers": [
        "慢性痛類型（Turk et al., 1983）",
        "病因性質",
        "發作型態",
        "常見代表例子"
      ],
      "rows": [
        [
          "慢性復發型（Chronic-recurrent）",
          "良性",
          "劇烈發作與無痛期交替",
          "偏頭痛、緊張型頭痛、肌筋膜痛"
        ],
        [
          "慢性難治良性型（Chronic-intractable-benign）",
          "良性",
          "持續存在、強度起伏",
          "部分慢性下背痛"
        ],
        [
          "慢性漸進型（Chronic-progressive）",
          "惡性",
          "持續且隨病程惡化加劇",
          "類風濕性關節炎、癌症"
        ]
      ]
    },
    "sticker": "bandaid",
    "theme_tint": "peach",
    "est_minutes": 1.5,
    "speaker_notes": "時間維度是區分疼痛的另一個關鍵。小於三個月的急性痛雖然當下讓人很焦慮，但只要傷口好了，焦慮就會跟著消退；像課本特別介紹的燒傷急性痛，除了止痛藥，透過心理準備增強控制感或用 VR 轉移注意力，都能有效減少用藥。相對地，慢性痛絕對不只是拉長版的急性痛，患者容易陷入無助、無望，整個生活圈萎縮到只剩家裡、診所和藥局。臨床上常依病因良惡性與持續度，把慢性痛分成慢性復發型、慢性難治良性型與慢性漸進型三大類。",
    "apa_citation": "Sarafino & Smith (2017), pp. 290–292; Turk et al. (1983); ABA (2015)"
  },
  {
    "slide_no": 5,
    "unit_id": "unit_1",
    "unit_badge": "單元一 · 疼痛與睡眠",
    "action_title": "疼痛與睡眠形成逐日雙向惡性循環，長期缺眠會提高痛覺敏感度",
    "bullets": [
      "逐日雙向預測：白天高強度疼痛 → 當晚睡眠品質差 → 隔日疼痛顯著加劇（O'Brien et al., 2011）。",
      "情緒與認知共犯：除了疼痛本身，憂鬱（depression）、侵入性思考（intrusive thoughts）與擔憂（worry）同樣會顯著破壞睡眠（Nicassio et al., 2012; Smith et al., 2000）。",
      "長期睡眠剝奪效應：會升高負向情感、提高痛覺敏感度，並增加未來數週經歷的疼痛總量（Hamilton et al., 2008; Kundermann et al., 2004; Quartana et al., 2010）。"
    ],
    "wiki_gap_note": "[Wiki 缺口: 目前僅收錄教科書摘要，尚未納入 O'Brien et al. (2011) 與 CBT-I 介入慢性痛原始論文]",
    "sticker": "sleep_cloud",
    "theme_tint": "lavender",
    "est_minutes": 1.5,
    "speaker_notes": "這一頁特別值得注意疼痛跟睡眠的關係。許多慢性痛患者常說，只要能睡個好覺，我就能忍受這些痛。實證研究確實發現兩者呈現逐日雙向惡性循環：白天越痛晚上越睡不好，而睡不好隔天就會更痛。此外，憂鬱、反覆的侵入性思考跟擔憂也會一起干擾睡眠；如果長期睡眠剝奪，還會進一步升高負向情緒與痛覺敏感度，讓未來好幾週的疼痛量都跟著增加。",
    "apa_citation": "Sarafino & Smith (2017), p. 291; O'Brien et al. (2011); Nicassio et al. (2012); Hamilton et al. (2008)"
  },
  {
    "slide_no": 6,
    "unit_id": "unit_1",
    "unit_badge": "單元一 · 疼痛生理傳導",
    "action_title": "痛覺透過快慢雙重周邊神經纖維傳遞，分別主導銳痛警訊與情緒反應",
    "bullets": [
      "痛覺三大獨特性：無只傳痛覺的專屬受器細胞、可由多種傷害刺激觸發、幾乎總伴隨強烈情緒成分。",
      "周邊活化：組織受損釋放血清素（serotonin）、組織胺（histamine）與緩激肽（bradykinin），引發發炎並活化全身（腦部除外）的傷害受器（nociceptors）。"
    ],
    "table": {
      "headers": [
        "纖維類型",
        "髓鞘",
        "傳導速度",
        "痛覺質性",
        "主要大腦終點與功能"
      ],
      "rows": [
        [
          "A-delta 纖維",
          "有",
          "極快",
          "銳利、定位明確",
          "感覺與運動皮質（促成快速防禦反應）"
        ],
        [
          "C 纖維",
          "無",
          "較慢",
          "瀰漫、鈍痛、灼痛、痠痛",
          "腦幹與前腦廣泛網絡（強烈影響情緒與動機）"
        ]
      ]
    },
    "sticker": "neuron",
    "theme_tint": "mint",
    "est_minutes": 1.5,
    "speaker_notes": "接著看生理層面。痛覺跟視覺很不一樣，身體裡並沒有只傳疼痛的專屬受器，而且幾乎一定帶著強烈情緒。當皮膚割傷或燙傷時，局部會釋放血清素、組織胺和緩激肽，活化傷害受器。訊號會走兩條路：有髓鞘的 A-delta 纖維傳得非常快，讓我們立刻感到銳痛並縮手保護；沒有髓鞘的 C 纖維傳得比較慢，帶來隱隱作痛或灼熱感，它主要連到腦幹和前腦，所以特別容易拉低我們的情緒與動機。",
    "apa_citation": "Sarafino & Smith (2017), pp. 291, 293; Mann & Carr (2006); Tortora & Derrickson (2012)"
  },
  {
    "slide_no": 7,
    "unit_id": "unit_1",
    "unit_badge": "單元一 · 三大特殊痛覺現象",
    "action_title": "轉移痛、神經病變痛與「疼痛意義」推翻組織損傷與痛感的一對一假設",
    "highlight_stats": [
      {
        "value": "49% / 32%",
        "label": "二戰重傷士兵：中重度痛 / 要求止痛藥 (Beecher, 1956)"
      },
      {
        "value": "75% / 83%",
        "label": "術後平民男性：中重度痛 / 要求止痛藥 (Beecher, 1956)"
      }
    ],
    "bullets": [
      "轉移痛（Referred Pain）：內臟與體表皮膚共用脊髓傳導路徑，使心臟病痛常被知覺在肩膀、胸口與手臂。",
      "神經病變痛（Neuropathic Pain）：無現存傷害刺激卻持續劇痛，含神經痛（neuralgia，如三叉神經痛）、灼痛（causalgia / CRPS）與幻肢痛（phantom limb pain）。",
      "疼痛的意義（Meaning）：士兵的傷口代表「戰爭結束、可以回家」，而平民手術傷口代表「人生問題開始」，使相同部位痛感與用藥需求天差地遠。"
    ],
    "sticker": "heart_chat",
    "theme_tint": "pink",
    "est_minutes": 1.5,
    "speaker_notes": "如果疼痛只是單純的物理訊號，就沒辦法解釋三個很有趣的現象。第一是轉移痛，像心肌梗塞卻覺得左肩痛，因為內臟跟皮膚共用脊髓路徑。第二是神經病變痛，包括三叉神經痛、灼痛和幻肢痛，明明傷口早就癒合甚至肢體都不在了，輕輕一陣風就能引發劇痛。第三個最經典，是醫師 Beecher 在二戰的觀察：前線重傷士兵的傷口比平民開刀嚴重得多，但要求止痛藥的比例卻只有 32%，遠低於平民的 83%。因為對士兵來說，受傷意味著活下來可以回家；對平民來說，開刀卻是人生危機的開始。這直接證明了心理意義對痛覺的巨大影響。",
    "apa_citation": "Sarafino & Smith (2017), pp. 293–294; Beecher (1956); Melzack & Katz (2004)"
  },
  {
    "slide_no": 8,
    "unit_id": "unit_2",
    "unit_badge": "單元二 · 早期理論與誘痛實驗",
    "action_title": "早期機械論忽略心理調節，標準化誘痛實驗開啟了實證檢驗之路",
    "bullets": [
      "早期理論瓶頸：特定論（Specificity Theory）解剖結構不符；模式論（Pattern Theory）要求強刺激，無法解釋微弱觸碰誘發神經痛或催眠減痛。",
      "冷壓測驗（Cold-Pressor）：2°C 循環冰水；唯有理解正向自我陳述「控制原理」者痛感才顯著下降（Girodo & Wood, 1979）。",
      "肌肉缺血（Muscle-Ischemia，240 mm Hg）：聽喜劇或放鬆可使痛閾提高 50%（Cogan et al., 1987），且不同疼痛類型的痛閾幾乎無相關（Janal et al., 1994）。",
      "研究倫理：須確保無實質傷害、完整知情同意，並保障受試者隨時無壓力退出。"
    ],
    "asset_path": "raw/assets/sarafino-ch11-nature-symptoms-of-pain/fig11-1-cold-pressor.png",
    "asset_caption": "圖 11-1：冷壓測驗（Cold-Pressor Procedure）標準化實驗裝置（原文 p. 296）",
    "sticker": "ice",
    "theme_tint": "mint",
    "est_minutes": 1.5,
    "speaker_notes": "進入第二單元：疼痛理論。二十世紀初的特定論跟模式論都非常機械化，完全沒辦法解釋為什麼催眠能讓人真的感覺不那麼痛，也沒辦法解釋為什麼微弱刺激會觸發灼痛。要研究心理因素如何影響疼痛，研究者在實驗室發展出兩種安全的標準化誘痛法：右邊這張課本原圖就是冷壓測驗裝置，把手臂放進 2 度循環冰水；另一種是肌肉缺血法，用血壓計綁帶加壓到 240 毫米汞柱。很有意思的是，實驗發現聽喜劇錄音或做放鬆練習，可以讓受試者的痛閾直接提高 50%！",
    "apa_citation": "Sarafino & Smith (2017), pp. 295–296; Girodo & Wood (1979); Cogan et al. (1987)"
  },
  {
    "slide_no": 9,
    "unit_id": "unit_2",
    "unit_badge": "單元二 · 門控理論",
    "action_title": "門控理論以脊髓背角膠質層解釋心理因素如何即時調控痛覺上傳",
    "bullets": [
      "理論核心（Melzack & Wall, 1965, 1982）：脊髓背角灰質的膠質層（substantia gelatinosa）具神經「閘門」，調控傳遞細胞（transmission cells）輸出量。",
      "1. 疼痛纖維（A-delta、C）活動：傷害刺激越強，越傾向打開閘門。",
      "2. 其他周邊纖維（A-beta）活動：輕觸、按摩、熱敷等無害刺激傾向關閉閘門。",
      "3. 大腦下行訊號：腦幹與皮質透過傳出路徑，將焦慮、分心或催眠轉化為實質的開關閘訊號。"
    ],
    "asset_path": "raw/assets/sarafino-ch11-nature-symptoms-of-pain/fig11-2-gate-control.png",
    "asset_caption": "圖 11-2：門控理論開閘（高痛覺）與關閘（低痛覺）示意圖（原文 p. 297）",
    "sticker": "brain",
    "theme_tint": "lavender",
    "est_minutes": 1.5,
    "speaker_notes": "為了彌補早期理論的不足，Melzack 與 Wall 在 1960 年代提出了非常經典的門控理論。大家可以參考右邊這張課本圖 11-2：疼痛訊號進到脊髓背角膠質層時，會經過一道神經閘門。左半邊是閘門打開的狀態，除了疼痛纖維訊號強，加上大腦傳來像焦慮這樣的刺激，傳遞細胞就會把強烈痛覺送往大腦；右半邊則是閘門關閉，當我們搓揉痛處啟動 A-beta 纖維，或者大腦透過分心、放鬆送出抑制訊號，最後上傳的痛覺就會大幅減弱。",
    "apa_citation": "Sarafino & Smith (2017), pp. 297–298; Melzack & Wall (1965, 1982)"
  },
  {
    "slide_no": 10,
    "unit_id": "unit_2",
    "unit_badge": "單元二 · 開關閘與神經矩陣",
    "action_title": "情緒與注意力即時決定閘門開關，神經矩陣則解釋無刺激痛覺",
    "table": {
      "headers": [
        "生活條件（Table 11.1）",
        "打開閘門（加劇疼痛）",
        "關閉閘門（減輕疼痛）"
      ],
      "rows": [
        [
          "生理條件",
          "組織損傷程度、不當活動量",
          "止痛藥、反刺激（熱敷、按摩）"
        ],
        [
          "情緒條件",
          "焦慮、擔憂、緊繃、憂鬱",
          "正向情緒（愉悅、樂觀）、放鬆、休息"
        ],
        [
          "認知條件",
          "專注於疼痛、無聊、缺乏生活投入",
          "高度專注或分心、投入感興趣的活動"
        ]
      ]
    },
    "bullets": [
      "神經矩陣（Neuromatrix）：大腦整合感官、認知、情緒與壓力調節之網絡，即使無傷害刺激仍可產生幻肢痛（Melzack & Katz, 2004）。",
      "經典支持證據：Reynolds（1969）電刺激大鼠中腦導水管周圍灰質（PAG），使其在清醒狀態下無痛完成腹部手術。"
    ],
    "sticker": "neuron",
    "theme_tint": "lemon",
    "est_minutes": 1.5,
    "speaker_notes": "這張表整理了日常生活中哪些條件會把閘門打開或關上：生理上按摩和熱敷能關閘；情緒上焦慮、憂鬱會開閘，而放鬆、正向情緒能關閘；認知上如果一直盯著痛處看會越痛，投入感興趣的事則有助關閘。這套理論獲得很有力的實驗支持，像 Reynolds 在 1969 年電刺激大鼠中腦的 PAG 區域，結果大鼠在清醒開刀時竟然完全沒有痛覺反應！後來 Melzack 又進一步提出神經矩陣概念，解釋大腦網絡本身就能產生痛覺脈衝，成功補足幻肢痛的謎團。",
    "apa_citation": "Sarafino & Smith (2017), p. 298; Reynolds (1969); Melzack & Katz (2004)"
  },
  {
    "slide_no": 11,
    "unit_id": "unit_2",
    "unit_badge": "單元二 · 神經化學止痛",
    "action_title": "SPA 透過血清素與內生性鴉片抑制 P 物質，為人體內建的天然止痛系統",
    "bullets": [
      "SPA 神經化學鏈：刺激 PAG → 下行血清素（serotonin）活化脊髓抑制性中間神經元 → 釋放腦內啡（endorphin）→ 抑制疼痛纖維釋放 P 物質（substance P）。",
      "內生性鴉片受損：慢性痛患者常呈內生性鴉片系統功能受損，具家族慢性痛史者更顯著（Bruehl & Chung, 2006）。",
      "Naloxone 驗證與複雜性：鴉片拮抗劑 naloxone 可阻斷 SPA 與拔牙止痛（Akil et al., 1976; Levine et al., 1978），但非總能阻斷，且嗎啡對短痛易耐受卻對長期癌痛少見耐受。",
      "適應功能：心理壓力可觸發內生性鴉片，解釋受傷運動員或士兵在緊急時刻能暫時忽略痛覺。"
    ],
    "asset_path": "raw/assets/sarafino-ch11-nature-symptoms-of-pain/fig11-3-spa-pathway.png",
    "asset_caption": "圖 11-3：刺激誘發止痛（SPA）神經化學路徑示意圖（原文 p. 299）",
    "sticker": "capsule",
    "theme_tint": "mint",
    "est_minutes": 1.5,
    "speaker_notes": "為什麼電刺激中腦 PAG 就能止痛呢？右邊這張課本圖 11-3 清楚畫出了刺激誘發止痛的神經化學接力賽：PAG 送出訊號往下走，透過血清素活化脊髓的抑制性中間神經元，接著釋放出天然的腦內啡，擋住疼痛纖維釋放 P 物質，痛覺訊號就上不去了。科學家用鴉片拮抗劑 naloxone 實驗，發現一打下去止痛效果就消失，證明這是內生性鴉片系統在運作。這套系統在極端壓力下——像是戰場上的士兵或比賽中受傷的運動員——都能幫人暫時屏蔽痛覺來求生。",
    "apa_citation": "Sarafino & Smith (2017), pp. 299–300; Akil et al. (1976); Bruehl & Chung (2006)"
  },
  {
    "slide_no": 12,
    "unit_id": "unit_2",
    "unit_badge": "單元二 · 安慰劑止痛",
    "action_title": "安慰劑止痛透過預期與制約觸發內生性鴉片，緩解人數達真實藥物一半",
    "highlight_stats": [
      {
        "value": "約 1/2",
        "label": "顯著減痛人數約為真實止痛藥（aspirin/morphine）一半"
      },
      {
        "value": "近 40%",
        "label": "膝關節炎假手術與真手術組皆自評減痛與活動改善 (Moseley et al., 2002)"
      }
    ],
    "bullets": [
      "強化療效三大條件：較大劑量／大顆膠囊 > 小劑量、注射 > 口服、醫師明確強力背書（但重複使用效果會遞減）。",
      "生理實證：預期（expectancies）與古典制約可促使體內分泌內生性鴉片；雙盲施打 naloxone 會使安慰劑組痛感回升（Benedetti et al., 2003）。",
      "臨床倫理兩難：既然安慰劑具實質止痛效果，醫療人員在何種情境下使用安慰劑才符合專業倫理？"
    ],
    "sticker": "capsule",
    "theme_tint": "pink",
    "est_minutes": 1.5,
    "speaker_notes": "談完內生性鴉片，就一定要提安慰劑效應。安慰劑可不是沒效的糖丸而已，在疼痛治療上，能產生顯著緩解的人數大約是阿斯匹靈或嗎啡的一半！甚至有實驗把膝關節炎患者分成真開刀跟假開刀，結果兩組都有將近四成覺得比較不痛、活動變好。而且如果用注射的、劑量看起來大一點、醫師語氣更篤定，效果會更好。雙盲實驗加上 naloxone 證實，預期跟古典制約真的會讓大腦分泌內生性鴉片來止痛。不過這也帶來很重要的倫理問題：醫師到底該不該、什麼時候可以用安慰劑？",
    "apa_citation": "Sarafino & Smith (2017), p. 301; Moseley et al. (2002); Benedetti et al. (2003)"
  },
  {
    "slide_no": 13,
    "unit_id": "unit_3",
    "unit_badge": "單元三 · 學習與疼痛行為",
    "action_title": "疼痛行為常在無意識下受制約與次級獲益強化，甚至反饋拉高痛感",
    "bullets": [
      "古典制約：偏頭痛前驅暈眩或疼痛詞彙（如 throbbing、excruciating）本身即可誘發痛覺生理激發與腦區活化（Jamner & Tursky, 1987; Richter et al., 2010）。",
      "操作制約與次級獲益（Secondary Gains）：免除討厭家務／工作或殘障給付，常在未察覺下強化病人角色並延長復原。",
      "表情反饋與習慣固化：強化痛苦表情會使主觀痛感評分同步上升（Kunz et al., 2011）；慢性化後即便痛度波動，疼痛行為仍高度穩定（Martel et al., 2010）。"
    ],
    "table": {
      "headers": [
        "四大疼痛行為（Turk, Wack, & Kerns, 1985）",
        "具體日常表現"
      ],
      "rows": [
        [
          "1. 臉部或聲音痛苦表達",
          "咬牙、呻吟、皺眉扭曲表情"
        ],
        [
          "2. 步態或姿勢改變",
          "保護性移動、彎腰行走、搓揉或按住痛處"
        ],
        [
          "3. 負向情感",
          "易怒、情緒低落"
        ],
        [
          "4. 活動逃避",
          "日間頻繁躺床、請假、避免費力活動"
        ]
      ]
    },
    "sticker": "bandaid",
    "theme_tint": "peach",
    "est_minutes": 1.5,
    "speaker_notes": "接下來進入第三單元：個人與社會經驗如何影響疼痛。首先是學習歷程。透過古典制約，偏頭痛患者光看到搏動、刺痛這些詞，生理反應就會比一般人強烈。另外，人在痛的時候會出現四類外顯的疼痛行為：表情呻吟、保護性姿勢、易怒和逃避活動。這些行為常在當事人沒察覺的情況下，因為不用做討厭的事或領取補償而受到操作制約強化。更驚人的是，研究發現當痛苦表情被強化時，連當事人自己評的疼痛分數都會跟著變高！",
    "apa_citation": "Sarafino & Smith (2017), pp. 300–301; Turk et al. (1985); Kunz et al. (2011)"
  },
  {
    "slide_no": 14,
    "unit_id": "unit_3",
    "unit_badge": "單元三 · 家庭與社會文化",
    "action_title": "配偶過度關切會無意間強化失能，而性別與社經背景亦形塑疼痛經驗",
    "bullets": [
      "配偶單面鏡實驗（Block et al., 1980）：認為配偶高度關切（solicitous）者，在配偶觀看時報告更多疼痛；認為配偶不關切者則報告更少疼痛。",
      "親子互動：父母關注皮膚病童抓癢反使抓癢增加（Gil et al., 1988）；採分心引導則減少疼痛行為（Walker et al., 2006）。",
      "情緒支持 vs. 過度保護：溫暖情緒支持可降壓減痛（Roberts et al., 2015），但缺乏鼓勵健康活動的過度保護會削弱自我效能、造成肌肉萎縮。",
      "性別與社經文化：男女痛閾相近，但女性冷壓評分、日常頭痛與骨骼肌肉痛盛行率及干擾較高；低社經族群疼痛較多，但族群差異對個別臨床治療參考有限（Korol & Craig, 2001）。"
    ],
    "sticker": "heart_chat",
    "theme_tint": "pink",
    "est_minutes": 1.5,
    "speaker_notes": "家人的反應也是非常強大的社會強化來源。有一個很經典的單面鏡實驗：慢性痛患者知道外面正在看他的是配偶還是醫院職員，結果覺得配偶平常很溺愛、過度關切的人，在配偶看的時候報告的疼痛明顯變高。我們當然要關心痛中的家人，單純的情緒支持確實能減痛；但如果變成什麼事都幫他做、不鼓勵他慢慢恢復活動，反而會讓患者越來越依賴、覺得自己控制不了疼痛。至於性別與文化方面，男女開始覺得痛的痛閾差不多，但女性在日常頭痛與生活干擾上比例較高；社經地位較低者也承受較多疼痛，不過臨床上還是要看個別病人，不能套用刻板印象。",
    "apa_citation": "Sarafino & Smith (2017), pp. 301–302; Block et al. (1980); Roberts et al. (2015)"
  },
  {
    "slide_no": 15,
    "unit_id": "unit_3",
    "unit_badge": "單元三 · 情緒與壓力",
    "action_title": "高焦慮使疼痛記憶放大為實際四倍，且實驗證實壓力能直接誘發頭痛",
    "highlight_stats": [
      {
        "value": "4 倍 vs. < 2 倍",
        "label": "高 vs. 低牙科焦慮者預期與 3 個月後回憶痛感 (Kent, 1985)"
      },
      {
        "value": "> 2/3 vs. 1/4",
        "label": "1 小時壓力算術誘發慢性 vs. 偶發頭痛比例 (Gannon et al., 1987)"
      }
    ],
    "bullets": [
      "焦慮主導記憶：高牙科焦慮患者的疼痛記憶由「預期」而非「實際體驗」決定（Kent, 1985; Gedney & Logan, 2006）。",
      "壓力誘發頭痛：壓力作業引發的緊張型頭痛前皆伴隨持續生理激發，於安靜休息後緩解（Gannon et al., 1987）。",
      "情緒雙向影響：正向情緒（如大笑）有助減痛（Finan & Garland, 2015）；慢性痛合併憂鬱／焦慮者，2 年後持續情緒障礙風險隨痛度、部位數與病程上升（Gerrits et al., 2012）。"
    ],
    "sticker": "bell",
    "theme_tint": "lemon",
    "est_minutes": 1.5,
    "speaker_notes": "情緒跟疼痛的連結有多深？來看兩個讓人印象深刻的實驗。第一個是看牙醫的研究：高牙科焦慮的患者，不管是看診前預期、還是三個月後回想，都覺得痛是實際經驗的四倍；低焦慮的人則不到兩倍，說明焦慮會徹底改寫我們的疼痛記憶。第二個實驗讓受試者做一小時很折磨人的心算壓力測驗，結果超過三分之二的慢性頭痛患者當場就痛起來了，直接證實壓力真的可以引發緊張型頭痛。",
    "apa_citation": "Sarafino & Smith (2017), pp. 303–304; Kent (1985); Gannon et al. (1987)"
  },
  {
    "slide_no": 16,
    "unit_id": "unit_3",
    "unit_badge": "單元三 · 因應、MMPI 與接納",
    "action_title": "慢性痛易現 MMPI 神經質三合症與災難化，但疼痛接納能翻轉適應",
    "bullets": [
      "MMPI 神經質三合症（Hs 慮病、D 憂鬱、Hy 歇斯底里）：≥ 70 僅見於 < 5% 一般人口；慢性痛患者（不論有無器質病因）三量表均飆高，其餘 7 量表正常；急性痛整體落於常模。",
      "因果方向：慢性痛通常先於適應不良（痛消失後心理困擾即顯著下降，Hilderink et al., 2012）。",
      "災難化（Catastrophizing）：頻繁放大負向想法，推動急性痛轉為慢性痛與憂鬱失能（Wade et al., 2012）。",
      "疼痛接納（Pain Acceptance）：帶著痛仍投入生活活動 → 自我效能較高、功能更佳、止痛藥用更少（Cook et al., 2015）。"
    ],
    "asset_path": "raw/assets/sarafino-ch11-nature-symptoms-of-pain/fig11-4-mmpi-profiles.png",
    "asset_caption": "圖 11-4：慢性痛 vs. 急性痛患者 MMPI 剖面比較（原文 p. 305）",
    "sticker": "sunflower",
    "theme_tint": "lavender",
    "est_minutes": 1.5,
    "speaker_notes": "要評估慢性痛患者的因應困難，心理師常用 MMPI。看右邊這張課本圖 11-4 非常清楚：慢性痛患者在慮病、憂鬱、歇斯底里這三個神經質三合症量表上平均飆破 70 分，也就是前 5% 的臨床顯著線，但其他七個量表都很正常；急性痛患者則幾乎都在正常範圍。這反映的是看不到盡頭的痛帶來的無助與災難化思考。不過也不是所有慢性痛患者都會適應不良，研究發現適應得很好的人通常具備高度疼痛接納——他們不再把全部力氣花在消滅疼痛，而是帶著痛繼續過自己重視的生活，結果反而功能更好、止痛藥吃得更少。",
    "apa_citation": "Sarafino & Smith (2017), pp. 304–305; Cox et al. (1978); Rosen et al. (1987); Cook et al. (2015)"
  },
  {
    "slide_no": 17,
    "unit_id": "unit_4",
    "unit_badge": "單元四 · 自陳評估量表",
    "action_title": "建議併用至少兩種評估技術，並從臨床訪談與簡易強度量表起步",
    "bullets": [
      "多方法評估原則：結合自陳法、行為評估與心理生理指標中至少兩種工具，以提升準確度（Bradley, 1994）。",
      "慢性痛訪談七大焦點：病史演變、前後情緒適應、原生活型態、目前工作人際衝擊、家庭發作情境、誘發／加劇因子、典型因應。",
      "視覺類比量表（VAS）：兩端標註無痛與最劇烈痛之線段，直覺易用，可適用低至 5 歲兒童（Karoly, 1985）。",
      "方格／數字量表（Box / NRS）與口語評分量表（VRS）：分別透過 0–10 數字或形容詞快速量化強度。"
    ],
    "asset_path": "raw/assets/sarafino-ch11-nature-symptoms-of-pain/fig11-5-pain-rating-scales.png",
    "asset_caption": "圖 11-5：視覺類比（VAS）、方格數字（Box）與口語評分（VRS）量表（原文 p. 306）",
    "sticker": "faces_scale",
    "theme_tint": "mint",
    "est_minutes": 1.0,
    "speaker_notes": "進入第四單元：既然疼痛這麼主觀，我們到底要怎麼評估？專家建議在臨床和研究上最好同時搭配兩種以上的方法，主要分為自陳法、行為評估和心理生理測量三大類。自陳法最基本的就是詳細的臨床訪談，了解疼痛的歷史、生活影響跟家人反應；再搭配右邊這張圖 11-5 的三種簡易強度量表——線段式的 VAS、0 到 10 的數字方格量表，還有口語量表。其中 VAS 非常直覺，連五歲小朋友都能用。",
    "apa_citation": "Sarafino & Smith (2017), pp. 305–306; Bradley (1994); Karoly (1985)"
  },
  {
    "slide_no": 18,
    "unit_id": "unit_4",
    "unit_badge": "單元四 · 疼痛日誌",
    "action_title": "重複評分與疼痛日誌能還原日常波動，並有效矯正家屬對疼痛的誤判",
    "bullets": [
      "跨時平均效度更高：連續兩週清醒時每小時評分並取平均，比單次詢問更能精準反映患者一般疼痛水準（Jensen & McFarland, 1993）。",
      "疼痛日誌要素：記錄時間、疼痛評分與部位、發作前活動、用藥種類與劑量、服藥 1–2 小時後評分及伴隨困擾（如失眠）。",
      "臨床翻轉案例：妻子誤認丈夫全天候劇痛難耐而禁止其做家事，夫妻憂鬱 4 年；透過每小時紀錄證實丈夫多半僅中度疼痛且渴望參與日常，成功改變互動（Turk et al., 1983）。"
    ],
    "asset_path": "raw/assets/sarafino-ch11-nature-symptoms-of-pain/fig11-6-pain-diary.png",
    "asset_caption": "圖 11-6：慢性疼痛每日疼痛日誌（Pain Diary）範例（原文 p. 307）",
    "sticker": "sleep_cloud",
    "theme_tint": "peach",
    "est_minutes": 1.0,
    "speaker_notes": "因為簡易量表填起來很快，臨床上很常請病人做重複測量，或像右邊這張圖 11-6 一樣寫每日疼痛日誌，記錄幾點痛、當時在做什麼、吃了什麼藥、一兩小時後有沒有改善。這除了能幫醫師抓出疼痛發作的規律，還能改善家庭關係。課本舉了一個很動人的案例：一位太太以為先生每天無時無刻都痛到無法動彈，四年來什麼家事都不讓他碰，兩人越來越憂鬱；後來靠著每小時評分紀錄，太太才發現先生大多數時候只是中度疼痛、而且其實很想幫忙做點事，這才成功打破了過度保護的僵局。",
    "apa_citation": "Sarafino & Smith (2017), pp. 306–307; Jensen & McFarland (1993); Turk et al. (1983)"
  },
  {
    "slide_no": 19,
    "unit_id": "unit_4",
    "unit_badge": "單元四 · McGill 疼痛問卷",
    "action_title": "McGill 疼痛問卷（MPQ）從感覺、情感與評價三維度刻畫疼痛全貌",
    "bullets": [
      "三大維度（Melzack & Torgerson, 1971; Melzack, 1975）：感覺（hot → searing）、情感動機（fearful → terrifying）與評價（annoying → unbearable）。",
      "核心分數：Part 2 的 20 組詞彙加總得 Pain Rating Index（PRI）；Part 4 當下強度得 Present Pain Intensity（PPI）。",
      "優勢：不同痛症（牙痛、關節炎、癌症、幻肢痛）呈現具區辨力之選詞型態。",
      "限制與替代：需較高英文詞彙力（如 taut、lancinating），對語言受限者與 12 歲以下兒童適用性有限；替代工具如 Multidimensional Pain Inventory（MPI）。"
    ],
    "asset_path": "raw/assets/sarafino-ch11-nature-symptoms-of-pain/fig11-7-mpq.png",
    "asset_caption": "圖 11-7：McGill 疼痛問卷（MPQ）四部分完整結構（原文 p. 308）",
    "sticker": "brain",
    "theme_tint": "pink",
    "est_minutes": 1.5,
    "speaker_notes": "光知道幾分痛還不夠，因為灼熱的痛跟抽痛感受完全不同。Melzack 透過跟幻肢痛患者訪談，發展出最著名的多維度問卷——McGill 疼痛問卷，簡稱 MPQ。右邊這張圖 11-7 包含四個部分：標記部位、從 20 組形容詞裡選最貼切的字來計算疼痛評分指數 PRI、時間型態，以及當下強度 PPI。它最厲害的地方是涵蓋了感覺、情感跟評價三個維度，不同疾病的人選出的詞彙組合真的會不一樣。不過它也有明顯限制，就是裡頭有不少冷僻的英文單字，對語言能力受限或 12 歲以下的孩子比較不適用。",
    "apa_citation": "Sarafino & Smith (2017), pp. 307–309; Melzack (1975); Karoly (1985)"
  },
  {
    "slide_no": 20,
    "unit_id": "unit_4",
    "unit_badge": "單元四 · 行為與心理生理評估",
    "action_title": "行為觀察與 EEG 誘發電位效度佳，自主神經指標專一性偏低宜作輔助",
    "bullets": [
      "結構化臨床觀察：護理師使用 UAB Pain Behavior Scale（10 項 3 點計分）或錄影評分標準動作（走路、撿物、脫鞋），信效度高且與自評高度相關（Kleinke & Spangler, 1988）。",
      "日常觀察：Pain Behaviors Self Report（20 題）或訓練配偶依 Fordyce（1976）記錄 5–10 項疼痛行為與旁人反應。"
    ],
    "table": {
      "headers": [
        "心理生理指標",
        "與疼痛之實證關聯",
        "臨床應用限制"
      ],
      "rows": [
        [
          "肌電圖（EMG）",
          "壓力下患部肌張力高於無痛對照組（Flor, 2001）",
          "靜止無穩定差異；須長時間測量才反映痛度"
        ],
        [
          "自主神經（心率／膚電）",
          "反映一般生理激發",
          "與痛刺激強度關聯弱、易受壓力混淆，實用性低"
        ],
        [
          "EEG 誘發電位",
          "振幅隨痛刺激增減、服止痛藥下降且與自評相關",
          "仍受注意力、飲食與壓力影響，宜輔助自陳與行為法"
        ]
      ]
    },
    "sticker": "neuron",
    "theme_tint": "lavender",
    "est_minutes": 1.5,
    "speaker_notes": "除了讓病人自己填問卷，我們也能用行為觀察和生理儀器來輔助。行為評估分成兩種：在醫院裡可以用 UAB 量表或請病人做撿東西、脫鞋等標準動作錄影評分；在日常生活中則可訓練家屬觀察並記錄發作情境。至於心理生理指標，大家可以看下方表格：肌電圖 EMG 必須長時間測量才跟疼痛強度有關；心率和膚電因為太容易被單純的緊張干擾，其實不太適合拿來測痛；表現最好的是腦電圖誘發電位，它的波幅會隨刺激變強而升高、吃止痛藥後下降。不過這三者都容易受注意力或壓力影響，臨床上最適合作為自陳與行為評估的補充。",
    "apa_citation": "Sarafino & Smith (2017), pp. 309–310; Richards et al. (1982); Flor (2001); Chapman et al. (1985)"
  },
  {
    "slide_no": 21,
    "unit_id": "unit_5",
    "unit_badge": "單元五 · 兒童疼痛與發展",
    "action_title": "胎兒產前數週即具痛覺，兒童疼痛評估須配合年齡與語言發展調整",
    "highlight_stats": [
      {
        "value": "11%–38%",
        "label": "跨國兒童青少年慢性／復發痛平均盛行率 (King et al., 2011)"
      },
      {
        "value": "約 26 詞",
        "label": "兒童至 13 歲累積之疼痛描述詞彙量 (Jeans, 1983)"
      }
    ],
    "bullets": [
      "破除嬰兒無痛迷思：胎兒在出生前最後數週即能感受疼痛（Fabrizi et al., 2011）；新生兒采血會呈現典型痛覺表情（擠眼、皺眉、張口）與高頻急迫哭聲。",
      "< 5 歲評估：因語言多限於 hurt/ouch/ow，以行為觀察與哭聲／表情為主（兒科護理師準確度高於父母，Boerner et al., 2013）。",
      "≥ 5 歲評估：可使用 VAS、搭配臉譜之 VRS，以及 Pediatric Pain Questionnaire 等多維兒童問卷；另須留意父母在旁災難化易促使中止孩子活動（Caes et al., 2011）。"
    ],
    "sticker": "faces_scale",
    "theme_tint": "lemon",
    "est_minutes": 1.5,
    "speaker_notes": "最後一個單元聚焦在兒童疼痛。大家可能會驚訝，其實兒童青少年慢性或復發性疼痛的盛行率高達 11% 到 38%。早期醫界曾誤以為嬰兒神經還沒發育好、不太會痛，甚至連割包皮都不上麻醉；但現代研究已經證實，胎兒在出生前最後幾週就能感受到疼痛，新生兒也會做出跟成人類似的痛苦表情與高頻急迫哭聲。因為小小孩語言能力有限，五歲以下主要靠觀察行為和表情，五歲以上就可以搭配臉譜量表或兒童專用多維問卷。另外，父母若在旁邊過度災難化，也會影響孩子面對疼痛時的活動參與。",
    "apa_citation": "Sarafino & Smith (2017), pp. 310–312; King et al. (2011); Fabrizi et al. (2011); Caes et al. (2011)"
  },
  {
    "slide_no": 22,
    "unit_id": "summary",
    "unit_badge": "全章總結與參考文獻",
    "action_title": "整合生物心理社會視角與多維度評估，才能真正理解並協助疼痛患者",
    "bullets": [
      "1. 本質與神經機制：疼痛是生理與心理連續體；門控理論、神經矩陣與內生性鴉片系統解釋了認知與情緒如何實質調節痛覺。",
      "2. 惡性循環與保護因子：睡眠剝奪、過度關切與災難化推升慢性失能；溫暖支持與「疼痛接納」則是復原關鍵。",
      "3. 臨床評估原則：併用自陳、行為與心理生理多方法評估，並隨年齡調整工具。",
      "主要參考文獻（APA 7th）：Sarafino, E. P., & Smith, T. W. (2017). The nature and symptoms of pain. In Health psychology: Biopsychosocial interactions (9th ed., pp. 288–313). Wiley."
    ],
    "wiki_gap_note": "[Wiki 缺口: 本簡報 100% 依據已收錄之 Sarafino & Smith (2017) 第 11 章撰寫，後續可持續匯入原始實證期刊論文以進行跨篇比較]",
    "sticker": "sunflower",
    "theme_tint": "pink",
    "est_minutes": 1.0,
    "speaker_notes": "最後幫大家做個三點總結：第一，疼痛絕對不只是組織受傷，透過門控理論和內生性鴉片系統，我們的認知、預期和情緒都在即時調控痛覺；第二，在慢性痛裡，睡眠剝奪、家人過度關切和災難化思考容易形成惡性循環，而疼痛接納與適當支持是幫助患者重回生活的關鍵；第三，臨床上應該結合自陳、行為與心理生理的多元評估，並照顧到不同年齡層的需求。以上是今天的分享，謝謝大家，歡迎提問與指教！",
    "apa_citation": "Sarafino & Smith (2017), pp. 288–313"
  }
]
