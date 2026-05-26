<!-- Dev specification skeleton for the project. Fill sections with details later. -->
# Developer Specification (DEV_SPEC)

> 鐗堟湰锛?.1 鈥?鏂囨。缁撴瀯鑽夋

## 鐩綍

- 椤圭洰姒傝堪
- 鏍稿績鐗圭偣
- 鎶€鏈€夊瀷
- 娴嬭瘯鏂规
- 绯荤粺鏋舵瀯涓庢ā鍧楄璁?
- 椤圭洰鎺掓湡
- 鍙墿灞曟€т笌鏈潵灞曟湜

---

## 1. 椤圭洰姒傝堪
鏈」鐩熀浜庡闃舵妫€绱㈠寮虹敓鎴愶紙RAG, Retrieval-Augmented Generation锛変笌妯″瀷涓婁笅鏂囧崗璁紙MCP, Model Context Protocol锛夎璁★紝鐩爣鏄惌寤轰竴涓彲鎵╁睍銆侀珮鍙娴嬨€佹槗杩唬鐨勬櫤鑳介棶绛斾笌鐭ヨ瘑妫€绱㈡鏋躲€?

### 璁捐鐞嗗康 (Design Philosophy)

> **鏍稿績瀹氫綅锛氳嚜瀛︿笌鏁欏鍚屾 (Learning by Teaching)**
> 
> 鏈」鐩槸鎴戜釜浜烘妧鏈涔犮€佷赴瀵岀畝鍘嗐€佸鎴橀潰璇曠殑瀹炴垬鍘嗙▼锛屽悓鏃朵篃鏄竴浠藉悓姝ユ暀瀛︾殑寮€婧愯祫婧愩€傛垜鐩镐俊"**鏁欐槸鏈€濂界殑瀛?*"鈥斺€斿湪鏁寸悊浠ｇ爜銆佹挵鍐欐枃妗ｃ€佸綍鍒惰棰戠殑杩囩▼涓紝鎴戣嚜宸卞 RAG 鐨勭悊瑙ｄ篃鍦ㄤ笉鏂繁鍖栥€傚笇鏈涜繖浠?杈瑰杈规暀"鐨勬垚鏋滆兘澶熷府鍔╁埌鏇村鍚屾牱鍦ㄦ眰鑱岃矾涓婄殑鏈嬪弸銆?

鏈」鐩笉浠呮槸涓€涓姛鑳藉畬澶囩殑鏅鸿兘闂瓟妗嗘灦锛屾洿鏄竴涓笓涓?**RAG 鎶€鏈涔犱笌闈㈣瘯姹傝亴** 璁捐鐨勫疄鎴樺钩鍙帮細

#### 1锔忊儯 瀹炴垬椹卞姩瀛︿範 (Learn by Doing)
椤圭洰鏋舵瀯鏈韩灏辨槸 RAG 闈㈣瘯棰樼殑"**娲讳綋绛旀**"銆傛垜浠皢缁忓吀闈㈣瘯鑰冪偣鐩存帴铻嶅叆浠ｇ爜璁捐锛岄€氳繃鍔ㄦ墜瀹炶返鏉ュ珐鍥虹悊璁虹煡璇嗭細
- 鍒嗗眰妫€绱?(Hierarchical Retrieval)
- Hybrid Search (BM25 + Dense Embedding)
- Rerank 閲嶆帓搴忔満鍒?
- Embedding 绛栫暐涓庝紭鍖?
- RAG 鎬ц兘璇勬祴 (Ragas/DeepEval)

#### 2锔忊儯 寮€绠卞嵆鐢ㄤ笌娣卞害鎵╁睍骞堕噸 (Plug-and-Play & Extensible)
- **寮€绠卞嵆鐢?*锛氭彁渚?MCP 鏍囧噯鎺ュ彛锛屽彲鐩存帴瀵规帴 Copilot/Claude锛屾嬁鍒伴」鐩嵆鍙繍琛屼綋楠屻€?
- **娣卞害鎵╁睍**锛氫繚鐣欏畬鍏ㄦā鍧楀寲鐨勫唴閮ㄧ粨鏋勶紝鏂逛究寮€鍙戣€呮浛鎹㈢粍浠躲€侀瓟鏀圭畻娉曪紝浣滀负鍏峰娣卞害鐨勪釜浜虹畝鍘嗛」鐩€?
- **鎵╁睍鎸囧紩**锛氭枃妗ｄ腑浼氭槑纭寚鍑哄悇妯″潡鐨勬墿灞曟柟鍚戜笌寤鸿锛屽府鍔╀綘鍦ㄦ帉鎻″熀纭€鍚庣户缁繁鍏ヨ凯浠ｃ€?

#### 3锔忊儯 閰嶅鏁欏璧勬簮 (Comprehensive Learning Materials)
鎴戜細鎻愪緵**涓変綅涓€浣?*鐨勯厤濂楀涔犺祫婧愶紝甯姪浣犲揩閫熷悆閫忛」鐩細

| 璧勬簮绫诲瀷 | 鍐呭璇存槑 |
|---------|---------|
| 馃搫 **鎶€鏈枃妗?* | 鏋舵瀯璁捐鏂囨。銆佹妧鏈€夊瀷璇存槑銆佹ā鍧楄瑙?|
| 馃捇 **浠ｇ爜绀鸿寖** | 甯﹁缁嗘敞閲婄殑婧愮爜銆佸叧閿ā鍧楃殑 Step-by-step 瀹炵幇 |
| 馃幀 **瑙嗛璁茶В** | RAG 鏍稿績鐭ヨ瘑鐐瑰洖椤俱€佷唬鐮佺粏鑺傜簿璁层€佺幆澧冮厤缃暀绋?|

#### 4锔忊儯 瀛︿範璺嚎涓庨潰璇曟寚鍗?(Study Guide & Interview Prep)
閽堝姣忎釜妯″潡锛屾垜浼氭暣鐞嗭細
- **馃摎 鐭ヨ瘑鐐规竻鍗?*锛氳繖鍧楁秹鍙婂摢浜涚悊璁虹煡璇嗛渶瑕佹彁鍓嶅涔狅紙濡?BM25 鍘熺悊銆丗AISS 绱㈠紩绫诲瀷銆丆ross-Encoder vs Bi-Encoder锛?
- **鉂?楂橀闈㈣瘯棰?*锛氱粨鍚堥」鐩唬鐮佽瑙ｅ父瑙侀潰璇曢棶棰樺強鍙傝€冪瓟妗?
- **馃摑 绠€鍘嗘挵鍐欏缓璁?*锛氬浣曞皢鏈」鐩殑浜偣鍐欒繘绠€鍘嗭紝绐佸嚭鎶€鏈繁搴?

#### 5锔忊儯 绀惧尯浜ゆ祦涓庢寔缁凯浠?(Community & Iteration)
- **缁忛獙鍒嗕韩**锛氭垜鑷繁鐨勯潰璇曠粡鍘嗐€佸ぇ瀹朵娇鐢ㄦ湰椤圭洰闈㈣瘯鐨勫弽棣堬紝閮戒細姹囨€绘矇娣€
- **闂璁ㄨ**锛氫竴璧锋帰璁?濡備綍灏嗘湰椤圭洰鍐欒繘绠€鍘?銆?閽堝鏈」鐩殑闈㈣瘯棰樻€庝箞绛?
- **鎸佺画鏇存柊**锛氫粠浠ｇ爜 鈫?鍏偂鐭ヨ瘑 鈫?闈㈣瘯鎶€宸э紝褰㈡垚瀹屾暣鐨勬眰鑱岀煡璇嗗簱锛屽府鍔╁ぇ瀹舵洿濂藉湴鎷垮埌 Offer 馃幆

---

## 2. 鏍稿績鐗圭偣

### RAG 绛栫暐涓庤璁′寒鐐?
鏈」鐩湪 RAG 閾捐矾鐨勫叧閿幆鑺傞噰鐢ㄤ簡缁忓吀鐨勫伐绋嬪寲浼樺寲绛栫暐锛屽钩琛′簡妫€绱㈢殑鏌ュ噯鐜囦笌鏌ュ叏鐜囷紝鍏蜂綋鎬濇兂濡備笅锛?
- **鍒嗗潡绛栫暐 (Chunking Strategy)**锛氶噰鐢ㄦ櫤鑳藉垎鍧椾笌涓婁笅鏂囧寮猴紝涓洪珮璐ㄩ噺妫€绱㈡墦涓嬪熀纭€銆?
    - **鏅鸿兘鍒嗗潡**锛氭憭寮冩満姊扮殑瀹氶暱鍒囧垎锛岄噰鐢ㄨ涔夋劅鐭ョ殑鍒囧垎绛栫暐浠ヤ繚鐣欏畬鏁磋涔夛紱
    - **涓婁笅鏂囧寮?*锛氫负 Chunk 娉ㄥ叆鏂囨。鍏冩暟鎹紙鏍囬銆侀〉鐮侊級鍜屽浘鐗囨弿杩帮紙Image Caption锛夛紝纭繚妫€绱㈡椂涓嶄粎鍖归厤鏂囨湰锛岃繕鑳芥劅鐭ヤ笂涓嬫枃銆?
- **绮楁帓鍙洖 (Coarse Recall / Hybrid Search)**锛氶噰鐢?**娣峰悎妫€绱?* 绛栫暐浣滀负绗竴闃舵鍙洖锛屽揩閫熺瓫閫夊€欓€夐泦銆?
    - 缁撳悎 **绋€鐤忔绱?(Sparse Retrieval/BM25)** 鍒╃敤鍏抽敭璇嶇簿纭尮閰嶏紝瑙ｅ喅涓撴湁鍚嶈瘝鏌ユ壘闂锛?
    - 缁撳悎 **绋犲瘑妫€绱?(Dense Retrieval/Embedding)** 鍒╃敤璇箟鍚戦噺锛岃В鍐冲悓涔夎瘝涓庢ā绯婅〃杈鹃棶棰橈紱
    - 涓よ€呬簰琛ワ紝閫氳繃 RRF (Reciprocal Rank Fusion) 绠楁硶铻嶅悎锛岀‘淇濇煡鍏ㄧ巼涓庢煡鍑嗙巼鐨勫钩琛°€?
- **绮炬帓閲嶆帓 (Rerank / Fine Ranking)**锛氬湪绮楁帓鍙洖鐨勫熀纭€涓婅繘琛屾繁搴﹁涔夋帓搴忋€?
	- 閲囩敤 Cross-Encoder锛堜笓鐢ㄩ噸鎺掓ā鍨嬶級鎴?LLM Rerank锛堝彲閫夊悗绔級瀵瑰€欓€夐泦杩涜閫愪竴鎵撳垎锛岃瘑鍒粏寰殑璇箟宸紓銆?
    - 閫氳繃 **"绮楁帓(浣庢垚鏈硾鍙洖) -> 绮炬帓(楂樻垚鏈簿杩囨护)"** 鐨勪袱娈靛紡鏋舵瀯锛屽湪涓嶇壓鐗叉暣浣撳搷搴旈€熷害鐨勫墠鎻愪笅澶у箙鎻愬崌 Top-Results 鐨勭簿鍑嗗害銆?

### 鍏ㄩ摼璺彲鎻掓嫈鏋舵瀯 (Pluggable Architecture)
閴翠簬 AI 鎶€鏈殑蹇€熸紨杩涳紝鏈」鐩湪鏋舵瀯璁捐涓婅拷姹?*鏋佽嚧鐨勭伒娲绘€?*锛屾嫆缁濅笌鐗瑰畾妯″瀷鎴栦緵搴斿晢寮虹粦瀹氥€?*鏁翠釜绯荤粺**锛堜笉浠呮槸 RAG 閾捐矾锛夌殑姣忎竴涓牳蹇冪幆鑺傚潎瀹氫箟浜嗘娊璞℃帴鍙ｏ紝鏀寔"涔愰珮绉湪寮?鐨勮嚜鐢辨浛鎹笌缁勫悎锛?

- **LLM 璋冪敤灞傛彃鎷?(LLM Provider Agnostic)**锛?
    - 鏍稿績鎺ㄧ悊 LLM 閫氳繃缁熶竴鐨勬娊璞℃帴鍙ｅ皝瑁咃紝鏀寔**澶氬崗璁?*鏃犵紳鍒囨崲锛?
        - **Azure OpenAI**锛氫紒涓氱骇 Azure 浜戠鏈嶅姟锛岀鍚堝悎瑙勪笌瀹夊叏瑕佹眰锛?
        - **OpenAI API**锛氱洿鎺ュ鎺?OpenAI 瀹樻柟鎺ュ彛锛?
        - **鏈湴妯″瀷**锛氭敮鎸?Ollama銆乿LLM銆丩M Studio 绛夋湰鍦扮鏈夊寲閮ㄧ讲鏂规锛?
        - **鍏朵粬浜戞湇鍔?*锛欴eepSeek銆丄nthropic Claude 绛夌涓夋柟 API銆?
    - 閫氳繃閰嶇疆鏂囦欢涓€閿垏鎹㈠悗绔紝**闆朵唬鐮佷慨鏀?*鍗冲彲瀹屾垚 LLM 杩佺Щ锛屼究浜庢垚鏈紭鍖栥€侀殣绉佸悎瑙勬垨 A/B 娴嬭瘯銆?

- **Embedding & Rerank 妯″瀷鎻掓嫈 (Model Agnostic)**锛?
    - Embedding 妯″瀷涓?Rerank 妯″瀷鍚屾牱閲囩敤缁熶竴鎺ュ彛灏佽锛?
    - 鏀寔浜戠鏈嶅姟锛圤penAI Embedding, Cohere Rerank锛変笌鏈湴妯″瀷锛圫entence-Transformers, BGE锛夎嚜鐢卞垏鎹€?

- **RAG Pipeline 缁勪欢鎻掓嫈**锛?
    - **Loader锛堣В鏋愬櫒锛?*锛氭敮鎸?PDF銆丮arkdown銆丆ode 绛夊绉嶆枃妗ｈВ鏋愬櫒鐙珛鏇挎崲锛?
    - **Smart Splitter锛堝垏鍒嗙瓥鐣ワ級**锛氳涔夊垏鍒嗐€佸畾闀垮垏鍒嗐€侀€掑綊鍒囧垎绛夌瓥鐣ュ彲閰嶇疆锛?
    - **Transformation锛堝厓鏁版嵁/鍥炬枃澧炲己閫昏緫锛?*锛歄CR銆両mage Captioning 绛夊寮烘ā鍧楀彲鐙珛閰嶇疆銆?

- **妫€绱㈢瓥鐣ユ彃鎷?(Retrieval Strategy)**锛?
    - 鏀寔鍔ㄦ€侀厤缃函鍚戦噺銆佺函鍏抽敭璇嶆垨娣峰悎妫€绱㈡ā寮忥紱
    - 鏀寔鐏垫椿鏇存崲鍚戦噺鏁版嵁搴撳悗绔紙濡備粠 Chroma 杩佺Щ鑷?Qdrant銆丮ilvus锛夈€?

- **璇勪及浣撶郴鎻掓嫈 (Evaluation Framework)**锛?
    - 璇勪及妯″潡涓嶉攣瀹氬崟涓€鎸囨爣锛屾敮鎸佹寕杞戒笉鍚岀殑 Evaluator锛堝 Ragas, DeepEval锛変互閫傚簲涓嶅悓鐨勪笟鍔¤€冩牳缁村害銆?

杩欑璁捐纭繚寮€鍙戣€呭彲浠?*闆朵唬鐮佷慨鏀?*鍗冲彲杩涜 A/B 娴嬭瘯銆佹垚鏈紭鍖栨垨闅愮杩佺Щ锛屼娇绯荤粺鍏峰鏋佸己鐨勭敓鍛藉姏涓庣幆澧冮€傚簲鎬с€?

### MCP 鐢熸€侀泦鎴?(Copilot / ReSearch)
鏈」鐩殑鏍稿績璁捐瀹屽叏閬靛惊 Model Context Protocol (MCP) 鏍囧噯锛岃繖浣垮緱瀹冧笉浠呮槸涓€涓嫭绔嬬殑闂瓟鏈嶅姟锛屾洿鏄竴涓嵆鎻掑嵆鐢ㄧ殑鐭ヨ瘑涓婁笅鏂囨彁渚涜€呫€?

- **宸ヤ綔鍘熺悊**锛?
    - 鎴戜滑鐨?Server 浣滀负涓€涓?**MCP Server** 杩愯锛屾毚闇蹭竴缁勬爣鍑嗙殑 `tools` 鍜?`resources` 鎺ュ彛銆?
    - **MCP Clients**锛堝 GitHub Copilot, ReSearch Agent, Claude Desktop 绛夛級鍙互鐩存帴杩炴帴鍒拌繖涓?Server銆?
    - **鏃犵紳鎺ュ叆**锛氬綋浣犲湪 GitHub Copilot 涓彁闂椂锛孋opilot 浣滀负涓€涓?MCP Host锛岃兘澶熻嚜鍔ㄥ彂鐜板苟璋冪敤鎴戜滑鐨?Server 鎻愪緵鐨勫伐鍏凤紙濡?`search_documentation`锛夛紝鑾峰彇鎴戜滑鍐呯疆鐨勭鏈夋枃妗ｇ煡璇嗭紝鐒跺悗缁撳悎杩欎簺涓婁笅鏂囨潵鍥炵瓟浣犵殑闂銆?
- **浼樺娍**锛?
    - **闆跺墠绔紑鍙?*锛氭棤闇€涓虹煡璇嗗簱寮€鍙戜笓闂ㄧ殑 Chat UI锛岀洿鎺ュ鐢ㄥ紑鍙戣€呭凡鏈夌殑缂栬緫鍣紙VS Code锛夊拰 AI 鍔╂墜銆?
    - **涓婁笅鏂囦簰閫?*锛欳opilot 鍙互鍚屾椂鐪嬪埌浣犵殑浠ｇ爜鏂囦欢鍜屾垜浠殑鐭ヨ瘑搴撳唴瀹癸紝杩涜鏇存繁搴︾殑鎺ㄧ悊銆?
    - **鏍囧噯鍏煎**锛氫换浣曟敮鎸?MCP 鐨?AI Agent锛堜笉浠呮槸 Copilot锛夐兘鍙互鍗冲埢鎺ュ叆鎴戜滑鐨勭煡璇嗗簱锛屼竴娆″紑鍙戯紝澶勫鍙敤銆?

### 澶氭ā鎬佸浘鍍忓鐞?(Multimodal Image Processing)
鏈」鐩噰鐢ㄤ簡缁忓吀鐨?**"Image-to-Text" (鍥捐浆鏂?** 绛栫暐鏉ュ鐞嗘枃妗ｄ腑鐨勫浘鍍忓唴瀹癸紝瀹炵幇浜嗕綆鎴愭湰涓旈珮鏁堢殑澶氭ā鎬佹绱細
- **鍥惧儚鎻忚堪鐢熸垚 (Captioning)**锛氬埄鐢?LLM 鐨勮瑙夎兘鍔涳紝鑷姩鎻愬彇鏂囨。涓彃鍥剧殑鏍稿績淇℃伅锛屽苟鐢熸垚璇︾粏鐨勬枃瀛楁弿杩帮紙Caption锛夈€?
- **缁熶竴鍚戦噺绌洪棿**锛氬皢鐢熸垚鐨勫浘鍍忔弿杩版枃瀛楃洿鎺ュ祵鍏ュ埌鏂囨。鏂囨湰鍧楋紙Chunk锛変腑杩涜鍚戦噺鍖栥€?
- **浼樺娍**锛?
    - **鏋舵瀯缁熶竴**锛氭棤闇€寮曞叆澶嶆潅鐨?CLIP 绛夊妯℃€佸悜閲忓簱锛屽鐢ㄧ幇鏈夌殑绾枃鏈?RAG 妫€绱㈤摼璺嵆鍙疄鐜扳€滄悳鏂囧瓧鍑哄浘鈥濄€?
    - **璇箟瀵归綈**锛氶€氳繃 LLM 灏嗗浘鍍忕殑瑙嗚鐗瑰緛杞寲涓鸿涔夌悊瑙ｏ紝浣跨敤鎴疯兘閫氳繃鑷劧璇█绮惧噯妫€绱㈠埌鍥捐〃銆佹祦绋嬪浘绛夎瑙変俊鎭€?

### 鍙娴嬫€с€佸彲瑙嗗寲绠＄悊涓庤瘎浼颁綋绯?(Observability, Visual Management & Evaluation)
閽堝 RAG 绯荤粺甯歌鐨勨€滈粦鐩掆€濋棶棰橈紝鏈」鐩嚧鍔涗簬璁╂瘡涓€娆＄敓鎴愯繃绋嬮兘**閫忔槑鍙**涓?*鍙噺鍖?*锛屽苟鎻愪緵瀹屾暣鐨?*鏈湴鍙鍖栫鐞嗗钩鍙?*锛?
- **鍏ㄩ摼璺櫧鐩掑寲 (White-box Tracing)**锛?
    - 璁板綍骞跺彲瑙嗗寲 RAG 娴佹按绾跨殑姣忎竴涓腑闂寸姸鎬侊細瑕嗙洊 Ingestion锛堝姞杞解啋鍒囧垎鈫掑寮衡啋缂栫爜鈫掑瓨鍌級涓?Query锛堟煡璇㈤澶勭悊鈫扗ense/Sparse 鍙洖鈫掕瀺鍚堚啋閲嶆帓鈫掑搷搴旀瀯寤猴級涓ゆ潯瀹屾暣閾捐矾銆?
    - 寮€鍙戣€呭彲浠ユ竻鏅扮湅鍒扳€滅郴缁熶负浠€涔堥€変簡杩欎釜鏂囨。鈥濅互鍙娾€淩erank 璧蜂簡浠€涔堜綔鐢ㄢ€濓紝浠庤€岀簿鍑嗗畾浣嶅潖 Case銆?
- **鍙鍖栫鐞嗗钩鍙?(Visual Management Dashboard)**锛?
    - 鍩轰簬 Streamlit 鐨勬湰鍦?Web 绠＄悊闈㈡澘锛屾彁渚涘叚澶у姛鑳介〉闈細
        - **绯荤粺鎬昏**锛氬睍绀哄綋鍓嶅彲鎻掓嫈缁勪欢閰嶇疆锛圠LM/Embedding/Splitter/Reranker锛変笌鏁版嵁璧勪骇缁熻銆?
        - **鏁版嵁娴忚鍣?*锛氭煡鐪嬪凡绱㈠紩鐨勬枃妗ｅ垪琛ㄣ€丆hunk 璇︽儏锛堝師鏂囥€乵etadata 鍚勫瓧娈点€佸叧鑱斿浘鐗囷級锛屾敮鎸佹悳绱㈣繃婊ゃ€?
        - **Ingestion 绠＄悊**锛氶€氳繃鐣岄潰閫夋嫨鏂囦欢瑙﹀彂鎽勫彇銆佸疄鏃跺睍绀哄悇闃舵杩涘害銆佹敮鎸佸垹闄ゅ凡鎽勫叆鏂囨。锛堣法 4 涓瓨鍌ㄧ殑鍗忚皟鍒犻櫎锛夈€?
        - **Query 杩借釜**锛氭煡璇㈠巻鍙插垪琛紝鑰楁椂鐎戝竷鍥撅紝Dense/Sparse 鍙洖瀵规瘮锛孯erank 鍓嶅悗鎺掑悕鍙樺寲銆?
        - **Ingestion 杩借釜**锛氭憚鍙栧巻鍙插垪琛紝鍚勯樁娈佃€楁椂涓庡鐞嗚鎯呫€?
        - **璇勪及闈㈡澘**锛氳繍琛岃瘎浼颁换鍔°€佹煡鐪嬪悇椤规寚鏍囥€佸巻鍙茶秼鍔垮姣斻€?
    - 鎵€鏈夐〉闈㈠熀浜?Trace 涓殑 `method`/`provider` 瀛楁**鍔ㄦ€佹覆鏌?*锛屾洿鎹㈠彲鎻掓嫈缁勪欢鍚?Dashboard 鑷姩閫傞厤锛屾棤闇€淇敼浠ｇ爜銆?
- **鑷姩鍖栬瘎浼伴棴鐜?(Automated Evaluation)**锛?
    - 闆嗘垚 Ragas 绛夎瘎浼版鏋讹紙鍙彃鎷旓級锛屼负姣忎竴娆℃绱㈠拰鐢熸垚璁＄畻鈥滀綋妫€鎶ュ憡鈥濓紙濡傚彫鍥炵巼 Hit Rate銆佸噯纭€?Faithfulness 绛夋寚鏍囷級銆?
    - 鎷掔粷鈥滃嚟鎰熻鈥濊皟浼橈紝寤虹珛鍩轰簬鏁版嵁鐨勮凯浠ｅ弽棣堝洖璺紝纭繚姣忎竴娆＄瓥鐣ヨ皟鏁达紙濡備慨鏀?Chunk Size 鎴栨洿鎹?Reranker锛夐兘鏈夐噺鍖栫殑鍒嗘暟鏀拺銆?

### 涓氬姟鍙墿灞曟€?(Extensibility for Your Own Projects)
鏈」鐩噰鐢?*閫氱敤鍖栨灦鏋勮璁?*锛屼笉浠呮槸涓€涓紑绠卞嵆鐢ㄧ殑鐭ヨ瘑闂瓟绯荤粺锛屾洿鏄竴涓彲浠ュ揩閫熼€傞厤鍚勭被涓氬姟鍦烘櫙鐨?*鎵╁睍鍩哄骇**锛?

- **Agent 瀹㈡埛绔墿灞?(Build Your Own Agent Client)**锛?
    - 鏈」鐩殑 MCP Server 澶╃劧鏀寔琚悇绫?Agent 璋冪敤锛屼綘鍙互鍩轰簬姝ゆ瀯寤哄睘浜庤嚜宸辩殑 Agent 瀹㈡埛绔細
        - **瀛︿範 Agent 寮€鍙?*锛氶€氳繃瀹炵幇涓€涓皟鐢ㄦ湰 Server 鐨?Agent锛屾繁鍏ョ悊瑙?Agent 鐨勬牳蹇冩蹇碉紙Tool Calling銆丆hain of Thought銆丷eAct 妯″紡绛夛級锛?
        - **瀹氬埗涓氬姟 Agent**锛氱粨鍚堜綘鐨勫叿浣撲笟鍔￠渶姹傦紝寮€鍙戜笓灞炵殑鏅鸿兘鍔╂墜锛堝浠ｇ爜瀹℃煡 Agent銆佹枃妗ｅ啓浣?Agent銆佸鏈嶉棶绛?Agent锛夛紱
        - **澶?Agent 鍗忎綔**锛氬皢鏈?Server 浣滀负鐭ヨ瘑妫€绱?Agent锛屼笌鍏朵粬鍔熻兘 Agent锛堝浠ｇ爜鐢熸垚銆佷换鍔¤鍒掞級缁勫悎锛屾瀯寤哄鏉傜殑 Multi-Agent 绯荤粺銆?

- **涓氬姟鍦烘櫙蹇€熼€傞厤 (Adapt to Your Domain)**锛?
    - **鏁版嵁灞傛墿灞?*锛氬彧闇€鏇挎崲鏁版嵁婧愶紙鎺ュ叆浣犺嚜宸辩殑鏂囨。銆佹暟鎹簱銆丄PI锛夛紝鍗冲彲灏嗘湰绯荤粺鏀归€犱负浣犵殑绉佹湁鐭ヨ瘑搴擄紱
    - **妫€绱㈤€昏緫瀹氬埗**锛氬熀浜庡彲鎻掓嫈鏋舵瀯锛岃交鏉捐皟鏁存绱㈢瓥鐣ヤ互閫傞厤涓嶅悓涓氬姟鐗圭偣锛堝鐢靛晢鎼滅储鍋忛噸鍏抽敭璇嶃€佹硶寰嬫枃妗ｅ亸閲嶈涔夛級锛?
    - **Prompt 妯℃澘瀹氬埗**锛氫慨鏀圭郴缁?Prompt 鍜岃緭鍑烘牸寮忥紝浣垮叾绗﹀悎浣犵殑涓氬姟椋庢牸涓庝笓涓氭湳璇€?

- **瀛︿範涓庡疄鎴樺苟閲?(Learn While Building)**锛?
    - 閫氳繃鎵╁睍鏈」鐩紝浣犲皢鍚屾鎺屾彙锛?
        - **Agent 鏋舵瀯璁捐**锛欶unction Calling銆乀ool Use銆丮emory 绠＄悊绛夋牳蹇冩蹇碉紱
        - **LLM 搴旂敤宸ョ▼鍖?*锛歅rompt Engineering銆乀oken 浼樺寲銆佹祦寮忚緭鍑虹瓑瀹炴垬鎶€鑳斤紱
        - **绯荤粺闆嗘垚鑳藉姏**锛氬浣曞皢 AI 鑳藉姏宓屽叆鐜版湁涓氬姟绯荤粺锛屾瀯寤虹鍒扮鐨勬櫤鑳藉簲鐢ㄣ€?

杩欑璁捐璁╂湰椤圭洰涓嶄粎鏄?瀛﹀畬鍗冲純"鐨?Demo锛岃€屾槸鍙互**鎸佺画杩唬銆佺湡姝ｈ惤鍦?*鐨勫伐绋嬪寲妯℃澘锛屽府鍔╀綘灏嗗鍒扮殑鐭ヨ瘑杞寲涓哄疄闄呴」鐩粡楠屻€?


## 3. 鎶€鏈€夊瀷

### 3.1 RAG 鏍稿績娴佹按绾胯璁?

#### 3.1.1 鏁版嵁鎽勫彇娴佹按绾?

**鐩爣锛?* 鏋勫缓缁熶竴銆佸彲閰嶇疆涓斿彲瑙傛祴鐨勬暟鎹憚鍙栨祦姘寸嚎锛岃鐩栨枃妗ｅ姞杞姐€佹牸寮忚В鏋愩€佽涔夊垏鍒嗐€佸妯℃€佸寮恒€佸祵鍏ヨ绠椼€佸幓閲嶄笌鎵归噺涓婅浇鍒板悜閲忓瓨鍌ㄣ€傝鑳藉姏搴旀槸鍙噸鐢ㄧ殑搴撴ā鍧楋紝渚夸簬鍦?`ingest.py`銆丏ashboard 绠＄悊闈㈡澘銆佺绾挎壒澶勭悊鍜屾祴璇曚腑璋冪敤銆?

- **鑷爺 Pipeline 妗嗘灦锛堣璁＄伒鎰熷弬鑰?LlamaIndex 鍒嗗眰鎬濇兂锛屼絾涓嶄緷璧?LlamaIndex 搴擄級锛?*
	- 閲囩敤鑷畾涔夋娊璞℃帴鍙ｏ紙`BaseLoader`/`BaseSplitter`/`BaseTransform`/`BaseEmbedding`/`BaseVectorStore`锛夛紝瀹炵幇瀹屽叏鍙帶鐨勫彲鎻掓嫈鏋舵瀯銆?
	- 鏀寔鍙粍鍚堢殑 Loader -> Splitter -> Transform -> Embed -> Upsert 娴佺▼锛屼究浜庡疄鐜板彲瑙傛祴鐨勬祦姘寸嚎銆?
	- 涓庝富娴?embedding provider 鏈夎壇濂介€傞厤锛屾灦鏋勪腑缁熶竴浣跨敤 Chroma 浣滀负鍚戦噺瀛樺偍銆?


璁捐瑕佺偣锛?
- **鏄庣‘鍒嗗眰鑱岃矗**锛?
  - Loader锛氳礋璐ｆ妸鍘熷鏂囦欢瑙ｆ瀽涓虹粺涓€鐨?`Document` 瀵硅薄锛坄text` + `metadata`锛涚被鍨嬪畾涔夐泦涓湪 `src/core/types.py`锛夈€?*鍦ㄥ綋鍓嶉樁娈碉紝浠呭疄鐜?PDF 鏍煎紡鐨?Loader銆?*
		- 缁熶竴杈撳嚭鏍煎紡閲囩敤瑙勮寖鍖?Markdown浣滀负 `Document.text`锛氳繖鏍峰彲浠ユ洿濂界殑閰嶅悎鍚庨潰鐨凷plitte锛圠angchain RecursiveCharacterTextSplitte锛夛級鏂规硶浜у嚭楂樿川閲忓垏鍧椼€?
		- Loader 鍚屾椂鎶藉彇/琛ラ綈鍩虹 metadata锛堝 `source_path`, `doc_type=pdf`, `page`, `title/heading_outline`, `images` 寮曠敤鍒楄〃绛夛級锛屼负瀹氫綅銆佸洖婧笌鍚庣画 Transform 鎻愪緵渚濇嵁銆?
	- Splitter锛氬熀浜?Markdown 缁撴瀯锛堟爣棰?娈佃惤/浠ｇ爜鍧楃瓑锛変笌鍙傛暟閰嶇疆鎶?`Document` 鍒囦负鑻ュ共 Chunk锛屼繚鐣欏師濮嬩綅缃笌涓婁笅鏂囧紩鐢ㄣ€?
	- Transform锛氬彲鎻掑叆鐨勫鐞嗘楠わ紙ImageCaptioning銆丱CR銆乧ode-block normalization銆乭tml-to-text cleanup 绛夛級锛孴ransform 鍙互閫夋嫨鎶婇澶栦俊鎭拷鍔犲埌 chunk.text 鎴栨斁鍏?chunk.metadata锛堟帹鑽愰粯璁よ拷鍔犲埌 text 浠ヤ繚璇佹绱㈣鐩栵級銆?
	- Embed & Upsert锛氭寜鎵规璁＄畻 embedding锛屽苟涓婅浇鍒板悜閲忓瓨鍌紱鏀寔鍚戦噺 + metadata 涓婅浇锛屽苟鎻愪緵骞傜瓑 upsert 绛栫暐锛堝熀浜?id/hash锛夈€?
	- Dedup & Normalize锛氬湪涓婅浇鍓嶈繍琛屽悜閲?鏂囨湰鍘婚噸涓庡搱甯岃繃婊わ紝閬垮厤閲嶅绱㈠紩銆?

鍏抽敭瀹炵幇瑕佺礌锛?

- Loader锛堢粺涓€鏍煎紡涓庡厓鏁版嵁锛?
	- **鍓嶇疆鍘婚噸 (Early Exit / File Integrity Check)**锛?
		- 鏈哄埗锛氬湪瑙ｆ瀽鏂囦欢鍓嶏紝璁＄畻鍘熷鏂囦欢鐨?SHA256 鍝堝笇鎸囩汗銆?
		- 鍔ㄤ綔锛氭绱?`ingestion_history` 琛紝鑻ュ彂鐜扮浉鍚?Hash 涓旂姸鎬佷负 `success` 鐨勮褰曪紝鍒欒瀹氳鏂囦欢鏈彂鐢熷彉鏇达紝鐩存帴璺宠繃鍚庣画鎵€鏈夊鐞嗭紙瑙ｆ瀽銆佸垏鍒嗐€丩LM閲嶅啓锛夛紝瀹炵幇**闆舵垚鏈?(Zero-Cost)** 鐨勫閲忔洿鏂般€?
		- **瀛樺偍鏂规**锛堝垵鏈熷疄鐜帮紝鍙彃鎷旓級锛?
			- **榛樿閫夋嫨锛歋QLite**锛屽瓨鍌ㄤ簬 `data/db/ingestion_history.db`
			- **琛ㄧ粨鏋?*锛?
				```sql
				CREATE TABLE ingestion_history (
				    file_hash TEXT PRIMARY KEY,
				    file_path TEXT NOT NULL,
				    file_size INTEGER,
				    status TEXT NOT NULL CHECK(status IN ('success', 'failed', 'processing')),
				    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
				    error_msg TEXT,
				    chunk_count INTEGER
				);
				CREATE INDEX idx_status ON ingestion_history(status);
				CREATE INDEX idx_processed_at ON ingestion_history(processed_at);
				```
			- **鏌ヨ閫昏緫**锛歚SELECT status FROM ingestion_history WHERE file_hash = ? AND status = 'success'`
			- **鏇挎崲璺緞**锛氬悗缁彲鍗囩骇涓?Redis锛堝垎甯冨紡缂撳瓨锛夋垨 PostgreSQL锛堜紒涓氱骇涓績鍖栧瓨鍌級
	
	> **馃搶 鎸佷箙鍖栧瓨鍌ㄦ灦鏋勭粺涓€璇存槑**
	> 
	> 鏈」鐩湪澶氫釜鏍稿績妯″潡涓噰鐢?**SQLite** 浣滀负杞婚噺绾ф寔涔呭寲瀛樺偍鏂规锛岄伩鍏嶅紩鍏ラ噸閲忕骇鏁版嵁搴撲緷璧栵紝淇濇寔鏈湴浼樺厛锛圠ocal-First锛夌殑璁捐鐞嗗康锛?
	> 
	> | 瀛樺偍妯″潡 | 鏁版嵁搴撴枃浠?| 鐢ㄩ€?| 琛ㄧ粨鏋勫叧閿瓧娈?|
	> |---------|-----------|------|---------------|
	> | **鏂囦欢瀹屾暣鎬ф鏌?* | `data/db/ingestion_history.db` | 璁板綍宸插鐞嗘枃浠剁殑 SHA256 鍝堝笇锛屽疄鐜板閲忔憚鍙?| `file_hash`, `status`, `processed_at` |
	> | **鍥剧墖绱㈠紩鏄犲皠** | `data/db/image_index.db` | 璁板綍 image_id 鈫?鏂囦欢璺緞鏄犲皠锛屾敮鎸佸浘鐗囨绱笌寮曠敤 | `image_id`, `file_path`, `collection` |
	> | **BM25 绱㈠紩鍏冩暟鎹?* | `data/db/bm25/` | 瀛樺偍鍊掓帓绱㈠紩鍜?IDF 缁熻淇℃伅锛堟湭鏉ュ彲鎵╁睍鐢?SQLite锛?| 褰撳墠浣跨敤 pickle锛屽彲杩佺Щ鑷?SQLite |
	> 
	> **璁捐浼樺娍**锛?
	> - **闆朵緷璧栭儴缃?*锛氭棤闇€瀹夎 MySQL/PostgreSQL 绛夋暟鎹簱鏈嶅姟锛宍pip install` 鍗冲彲杩愯
	> - **骞跺彂瀹夊叏**锛歐AL (Write-Ahead Logging) 妯″紡鏀寔澶氳繘绋嬪畨鍏ㄨ鍐?
	> - **鎸佷箙鍖栦繚璇?*锛氭憚鍙栧巻鍙插拰绱㈠紩鏄犲皠鍦ㄨ繘绋嬮噸鍚悗鑷姩鎭㈠锛岄伩鍏嶉噸澶嶈绠?
	> - **鏋舵瀯涓€鑷存€?*锛氭墍鏈?SQLite 妯″潡閬靛惊鐩稿悓鐨勫垵濮嬪寲銆佹煡璇笌閿欒澶勭悊妯″紡锛屼究浜庣淮鎶や笌鎵╁睍
	> 
	> **鍗囩骇璺緞**锛氬綋绯荤粺瑙勬ā鎵╁睍鑷冲垎甯冨紡鍦烘櫙鏃讹紝鍙€氳繃缁熶竴鐨勬娊璞℃帴鍙ｅ皢 SQLite 鏇挎崲涓?PostgreSQL 鎴?Redis锛屾棤闇€淇敼涓婂眰涓氬姟閫昏緫銆?
	
	- **瑙ｆ瀽涓庢爣鍑嗗寲**锛?
		- 褰撳墠鑼冨洿锛?*浠呭疄鐜?PDF -> canonical Markdown 瀛愰泦** 鐨勮浆鎹€?
	- 鎶€鏈€夊瀷锛圥ython PDF -> Markdown锛夛細
		- **棣栭€夛細MarkItDown**锛堜綔涓洪粯璁?PDF 瑙ｆ瀽/杞崲寮曟搸锛夈€備紭鐐规槸鐩存帴浜у嚭 Markdown 褰㈡€佹枃鏈紝渚夸簬涓庡悗缁?`RecursiveCharacterTextSplitter` 鐨?separators 閰嶅悎銆?
	- 杈撳嚭鏍囧噯 `Document`锛歚id|source|text(markdown)|metadata`銆俶etadata 鑷冲皯鍖呭惈 `source_path`, `doc_type`, `title/heading_outline`, `page/slide`锛堝閫傜敤锛? `images`锛堝浘鐗囧紩鐢ㄥ垪琛級銆?
	- Loader 涓嶈礋璐ｅ垏鍒嗭細鍙仛鈥滄牸寮忕粺涓€ + 缁撴瀯鎶藉彇 + 寮曠敤鏀堕泦鈥濓紝纭繚鍒囧垎绛栫暐鍙嫭绔嬭凯浠ｄ笌搴﹂噺銆?

- Splitter锛圠angChain 璐熻矗鍒囧垎锛涚嫭绔嬨€佸彲鎺э級
	- **瀹炵幇鏂规锛氫娇鐢?LangChain 鐨?`RecursiveCharacterTextSplitter` 杩涜鍒囧垎銆?*
		- 浼樺娍锛氳鏂规硶瀵?Markdown 鏂囨。鐨勭粨鏋勶紙鏍囬銆佹钀姐€佸垪琛ㄣ€佷唬鐮佸潡锛夋湁澶╃劧鐨勯€傞厤鎬э紝鑳藉閫氳繃閰嶇疆璇箟鏂偣锛圫eparators锛夊疄鐜伴珮璐ㄩ噺銆佽涔夊畬鏁寸殑鍒囧潡銆?
	- Splitter 杈撳叆锛歀oader 浜у嚭鐨?Markdown `Document`銆?
	- Splitter 杈撳嚭锛氳嫢骞?`Chunk`锛堟垨 Document-like chunks锛夛紝姣忎釜 chunk 蹇呴』鎼哄甫绋冲畾鐨勫畾浣嶄俊鎭笌鏉ユ簮淇℃伅锛歚source`, `chunk_index`, `start_offset/end_offset`锛堟垨绛変环瀹氫綅瀛楁锛夈€?

- Transform & Enrichment锛堢粨鏋勮浆鎹笌娣卞害澧炲己锛?
	鏈樁娈垫槸 ETL 绠￠亾鐨勬牳蹇冣€滄櫤鍔涒€濈幆鑺傦紝璐熻矗灏?Splitter 浜у嚭鐨勯潪缁撴瀯鍖栨枃鏈潡杞寲涓虹粨鏋勫寲銆佸瘜璇箟鐨勬櫤鑳藉垏鐗囷紙Smart Chunk锛夈€?
	- **缁撴瀯杞崲 (Structure Transformation)**锛氬皢鍘熷鐨?`String` 绫诲瀷鏁版嵁杞寲涓哄己绫诲瀷鐨?`Record/Object`锛屼负涓嬫父妫€绱㈡彁渚涘瓧娈电骇鏀寔銆?
	- **鏍稿績澧炲己绛栫暐**锛?
		1. **鏅鸿兘閲嶇粍 (Smart Chunking & Refinement)**锛?
			- 绛栫暐锛氬埄鐢?LLM 鐨勮涔夌悊瑙ｈ兘鍔涳紝瀵逛笂涓€闃舵鈥滅矖鍒囧垎鈥濈殑鐗囨杩涜浜屾鍔犲伐銆?
			- 鍔ㄤ綔锛氬悎骞跺湪閫昏緫涓婄揣瀵嗙浉鍏充絾琚墿鐞嗗垏鏂殑娈佃惤锛屽墧闄ゆ棤鎰忎箟鐨勯〉鐪夐〉鑴氭垨涔辩爜锛堝幓鍣級锛岀‘淇濇瘡涓?Chunk 鏄嚜鍖呭惈锛圫elf-contained锛夌殑璇箟鍗曞厓銆?
		2. **璇箟鍏冩暟鎹敞鍏?(Semantic Metadata Enrichment)**锛?
			- 绛栫暐锛氬湪鍩虹鍏冩暟鎹紙璺緞銆侀〉鐮侊級涔嬩笂锛屽埄鐢?LLM 鎻愬彇楂樼淮璇箟鐗瑰緛銆?
			- 浜у嚭锛氫负姣忎釜 Chunk 鑷姩鐢熸垚 `Title`锛堢簿鍑嗗皬鏍囬锛夈€乣Summary`锛堝唴瀹规憳瑕侊級鍜?`Tags`锛堜富棰樻爣绛撅級锛屽苟灏嗗叾娉ㄥ叆鍒?Metadata 瀛楁涓紝鏀寔鍚庣画鐨勬贩鍚堟绱笌绮剧‘杩囨护銆?
		3. **澶氭ā鎬佸寮?(Multimodal Enrichment / Image Captioning)**锛?
			- 绛栫暐锛氭壂鎻忔枃妗ｇ墖娈典腑鐨勫浘鍍忓紩鐢紝璋冪敤 Vision LLM锛堝 GPT-4o锛夎繘琛岃瑙夌悊瑙ｃ€?
			- 鍔ㄤ綔锛氱敓鎴愰珮淇濈湡鐨勬枃鏈弿杩帮紙Caption锛夛紝鎻忚堪鍥捐〃閫昏緫鎴栨彁鍙栨埅鍥炬枃瀛椼€?
			- 瀛樺偍锛氬皢 Caption 鏂囨湰鈥滅紳鍚堚€濊繘 Chunk 鐨勬鏂囨垨 Metadata 涓紝鎵撻€氭ā鎬侀殧闃傦紝瀹炵幇鈥滄悳鏂囧嚭鍥锯€濄€?
	- **宸ョ▼鐗规€?*锛歍ransform 姝ラ璁捐涓哄師瀛愬寲涓庡箓绛夋搷浣滐紝鏀寔閽堝鐗瑰畾 Chunk 鐨勭嫭绔嬮噸璇曚笌澧為噺鏇存柊锛岄伩鍏嶅洜 LLM 璋冪敤澶辫触瀵艰嚧鏁翠釜鏂囨。澶勭悊涓柇銆?

- **Embedding (鍙岃矾鍚戦噺鍖?**
	- **宸噺璁＄畻 (Incremental Embedding / Cost Optimization)**锛?
		- 绛栫暐锛氬湪璋冪敤鏄傝吹鐨?Embedding API 涔嬪墠锛岃绠?Chunk 鐨勫唴瀹瑰搱甯岋紙Content Hash锛夈€備粎閽堝鏁版嵁搴撲腑涓嶅瓨鍦ㄧ殑鏂板唴瀹瑰搱甯屾墽琛屽悜閲忓寲璁＄畻锛屽浜庢枃浠跺悕鍙樻洿浣嗗唴瀹规湭鍙樼殑鐗囨锛岀洿鎺ュ鐢ㄥ凡鏈夊悜閲忥紝鏄捐憲闄嶄綆 API 璋冪敤鎴愭湰銆?
	- **鏍稿績绛栫暐**锛氫负浜嗘敮鎸侀珮绮惧害鐨勬贩鍚堟绱紙Hybrid Search锛夛紝绯荤粺瀵规瘡涓?Chunk 骞惰鎵ц鍙岃矾缂栫爜璁＄畻銆?
		- **Dense Embeddings锛堣涔夊悜閲忥級**锛氳皟鐢?Embedding 妯″瀷锛堝 OpenAI text-embedding-3 鎴?BGE锛夌敓鎴愰珮缁存诞鐐瑰悜閲忥紝鎹曟崏鏂囨湰鐨勬繁灞傝涔夊叧鑱旓紝瑙ｅ喅鈥滆瘝涓嶅悓鎰忓悓鈥濈殑妫€绱㈤毦棰樸€?
		- **Sparse Embeddings锛堢█鐤忓悜閲忥級**锛氬埄鐢?BM25 缂栫爜鍣ㄦ垨 SPLADE 妯″瀷鐢熸垚绋€鐤忓悜閲忥紙Keyword Weights锛夛紝鎹曟崏绮剧‘鐨勫叧閿瘝鍖归厤淇℃伅锛岃В鍐充笓鏈夊悕璇嶆煡鎵鹃棶棰樸€?
	- **鎵瑰鐞嗕紭鍖?*锛氭墍鏈夎绠楀潎閲囩敤 `batch_size` 椹卞姩鐨勬壒澶勭悊妯″紡锛屾渶澶у寲 CPU 鍒╃敤鐜囧苟鍑忓皯缃戠粶 RTT銆?

- **Upsert & Storage (绱㈠紩瀛樺偍)**
	- **瀛樺偍鍚庣**锛氱粺涓€浣跨敤鍚戦噺鏁版嵁搴擄紙濡?Chroma/Qdrant锛変綔涓哄瓨鍌ㄥ紩鎿庯紝鍚屾椂鎸佷箙鍖栧瓨鍌?Dense Vector銆丼parse Vector 浠ュ強 Transform 闃舵鐢熸垚鐨勫瘜 Metadata銆?
	- **All-in-One 瀛樺偍绛栫暐**锛氭墽琛屽師瀛愬寲瀛樺偍锛屾瘡鏉¤褰曞悓鏃跺寘鍚細
		1. **Index Data**: 鐢ㄤ簬璁＄畻鐩镐技搴︾殑 Dense Vector 鍜?Sparse Vector銆?
		2. **Payload Data**: 瀹屾暣鐨?Chunk 鍘熷鏂囨湰 (Content) 鍙?Metadata銆?
		**鏈哄埗浼樺娍**锛氱‘淇濇绱㈠懡涓?ID 鍚庤兘绔嬪嵆鍙栧洖瀵瑰簲鐨勬鏂囧唴瀹癸紝鏃犻渶棰濆鐨勬煡搴撴搷浣?(Lookup)锛屼繚闅滀簡 Retrieve 闃舵鐨勬绉掔骇鍝嶅簲銆?
- **骞傜瓑鎬ц璁?(Idempotency)**锛?
		- 涓烘瘡涓?Chunk 鐢熸垚鍏ㄥ眬鍞竴鐨?`chunk_id`锛岀敓鎴愮畻娉曢噰鐢ㄧ‘瀹氱殑鍝堝笇缁勫悎锛歚hash(source_path + section_path + content_hash)`銆?
		- 鍐欏叆鏃堕噰鐢?"Upsert"锛堟洿鏂版垨鎻掑叆锛夎涔夛紝纭繚鍚屼竴鏂囨。鍗充娇琚娆″鐞嗭紝鏁版嵁搴撲腑涔熸案杩滃彧鏈変竴浠芥渶鏂板壇鏈紝褰诲簳閬垮厤閲嶅绱㈠紩闂銆?
	- **鍘熷瓙鎬т繚璇?*锛氫互 Batch 涓哄崟浣嶈繘琛屼簨鍔℃€у啓鍏ワ紝纭繚绱㈠紩鐘舵€佺殑涓€鑷存€с€?

- **鏂囨。鐢熷懡鍛ㄦ湡绠＄悊 (Document Lifecycle Management)**

	涓烘敮鎸?Dashboard 绠＄悊闈㈡澘涓殑鏂囨。娴忚涓庡垹闄ゅ姛鑳斤紝Ingestion 灞傞渶瑕佹彁渚涘畬鏁寸殑鏂囨。鐢熷懡鍛ㄦ湡绠＄悊鑳藉姏锛?

	- **DocumentManager锛堟枃妗ｇ鐞嗗櫒锛?*锛氱嫭绔嬩簬 Pipeline 鐨勬枃妗ｇ鐞嗘ā鍧楋紙`src/ingestion/document_manager.py`锛夛紝璐熻矗璺ㄥ瓨鍌ㄧ殑鍗忚皟鎿嶄綔锛?
		- `list_documents(collection?) -> List[DocumentInfo]`锛氬垪鍑哄凡鎽勫叆鏂囨。鍙婂叾缁熻淇℃伅锛坈hunk 鏁般€佸浘鐗囨暟銆佹憚鍏ユ椂闂达級銆?
		- `get_document_detail(doc_id) -> DocumentDetail`锛氳幏鍙栧崟涓枃妗ｇ殑璇︾粏淇℃伅锛堟墍鏈?chunk 鍐呭銆乵etadata銆佸叧鑱斿浘鐗囷級銆?
		- `delete_document(source_path, collection) -> DeleteResult`锛氬崗璋冨垹闄よ法 4 涓瓨鍌ㄧ殑鍏宠仈鏁版嵁锛?
			1. **Chroma** 鈥?鎸?`metadata.source` 鍒犻櫎鎵€鏈?chunk 鍚戦噺
			2. **BM25 Indexer** 鈥?绉婚櫎瀵瑰簲鏂囨。鐨勫€掓帓绱㈠紩鏉＄洰
			3. **ImageStorage** 鈥?鍒犻櫎璇ユ枃妗ｅ叧鑱旂殑鎵€鏈夊浘鐗囨枃浠?
			4. **FileIntegrity** 鈥?绉婚櫎澶勭悊璁板綍锛屼娇鏂囦欢鍙噸鏂版憚鍏?
		- `get_collection_stats(collection?) -> CollectionStats`锛氳繑鍥為泦鍚堢骇缁熻锛堟枃妗ｆ暟銆乧hunk 鏁般€佸瓨鍌ㄥぇ灏忕瓑锛夈€?

	- **Pipeline 杩涘害鍥炶皟 (Progress Callback)**锛氬湪 `IngestionPipeline.run()` 鏂规硶涓柊澧炲彲閫?`on_progress` 鍙傛暟锛?
		```python
		def run(self, source_path: str, collection: str = "default",
		        on_progress: Callable[[str, int, int], None] | None = None) -> IngestionResult:
		```
		- 鍥炶皟绛惧悕锛歚on_progress(stage_name: str, current: int, total: int)`
		- 鍚勯樁娈碉紙load / split / transform / embed / upsert锛夊湪澶勭悊姣忎釜 batch 鏃惰皟鐢ㄥ洖璋冿紝Dashboard 鎹灞曠ず瀹炴椂杩涘害鏉°€?
		- `on_progress` 涓?`None` 鏃惰涓轰笌褰撳墠瀹屽叏涓€鑷达紝涓嶅奖鍝?CLI 鍜屾祴璇曞満鏅€?

	- **瀛樺偍灞傛帴鍙ｆ墿灞?*锛氫负鏀寔 DocumentManager 鐨勫垹闄ゆ搷浣滐紝闇€鎵╁睍浠ヤ笅瀛樺偍鎺ュ彛锛?
		- `BaseVectorStore` 鏂板 `delete_by_metadata(filter: dict) -> int` 鈥?鎸?metadata 鏉′欢鎵归噺鍒犻櫎
		- `BM25Indexer` 鏂板 `remove_document(source: str) -> None` 鈥?绉婚櫎鎸囧畾鏂囨。鐨勭储寮曟潯鐩?
		- `FileIntegrityChecker` 鏂板 `remove_record(file_hash: str) -> None` 鍜?`list_processed() -> List[dict]`

#### 3.1.2 妫€绱㈡祦姘寸嚎


鏈ā鍧楀疄鐜版牳蹇冪殑 RAG 妫€绱㈠紩鎿庯紝閲囩敤 **鈥滃闃舵杩囨护 (Multi-stage Filtering)鈥?* 鏋舵瀯锛岃礋璐ｆ帴鏀跺凡娑堟鐨勭嫭绔嬫煡璇紙Standalone Query锛夛紝骞剁簿鍑嗗彫鍥?Top-K 鏈€鐩稿叧鐗囨銆?

- **Query Processing (鏌ヨ棰勫鐞?**
	- **鏍稿績鍋囪**锛氳緭鍏?Query 宸茬敱涓婃父锛圕lient/MCP Host锛夊畬鎴愪細璇濅笂涓嬫枃琛ュ叏锛圖e-referencing锛夛紝涓嶄粎濡傛锛岃繕杩涜浜嗘寚浠ｆ秷姝с€?
	- **鏌ヨ杞崲 (Transformation) 涓庢墿寮犵瓥鐣?(Expansion Strategy)**锛?
		- **Keyword Extraction**锛氬埄鐢?NLP 宸ュ叿鎻愬彇 Query 涓殑鍏抽敭瀹炰綋涓庡姩璇嶏紙鍘诲仠鐢ㄨ瘝锛夛紝鐢熸垚鐢ㄤ簬绋€鐤忔绱㈢殑 Token 鍒楄〃銆?
		- **Query Expansion **锛?
			- 绯荤粺鍙仛 Synonym/Alias Expansion锛堝悓涔夎瘝/鍒悕/缂╁啓鎵╁睍锛夛紝榛樿绛栫暐閲囩敤鈥?*鎵╁睍铻嶅叆绋€鐤忔绱€佺瀵嗘绱繚鎸佸崟娆?*鈥濅互鎺у埗鎴愭湰涓庡鏉傚害銆?
			- **Sparse Route (BM25)**锛氬皢鈥滃叧閿瘝 + 鍚屼箟璇?鍒悕鈥濆悎骞朵负涓€涓煡璇㈣〃杈惧紡锛堥€昏緫涓婃寜 `OR` 鎵╁睍锛夛紝**鍙墽琛屼竴娆＄█鐤忔绱?*銆傚師濮嬪叧閿瘝鍙祴浜堟洿楂樻潈閲嶄互鎶戝埗璇箟婕傜Щ銆?
			- **Dense Route (Embedding)**锛氫娇鐢ㄥ師濮?query锛堟垨杞诲害鏀瑰啓鍚庣殑璇箟 query锛夌敓鎴?embedding锛?*鍙墽琛屼竴娆＄瀵嗘绱?*锛涢粯璁や笉涓烘瘡涓悓涔夎瘝鍗曠嫭瑙﹀彂棰濆鐨勫悜閲忔绱㈣姹傘€?

- **Hybrid Search Execution (鍙岃矾娣峰悎妫€绱?**
	- **骞惰鍙洖 (Parallel Execution)**锛?
		- **Dense Route**锛氳绠?Query Embedding -> 妫€绱㈠悜閲忓簱锛圕osine Similarity锛?> 杩斿洖 Top-N 璇箟鍊欓€夈€?
		- **Sparse Route**锛氫娇鐢?BM25 绠楁硶 -> 妫€绱㈠€掓帓绱㈠紩 -> 杩斿洖 Top-N 鍏抽敭璇嶅€欓€夈€?
	- **缁撴灉铻嶅悎 (Fusion)**锛?
		- 閲囩敤 **RRF (Reciprocal Rank Fusion)** 绠楁硶锛屼笉渚濊禆鍚勮矾鍒嗘暟鐨勭粷瀵瑰€硷紝鑰屾槸鍩轰簬鎺掑悕鐨勫€掓暟杩涜鍔犳潈铻嶅悎銆?
		- 鍏紡绛栫暐锛歚Score = 1 / (k + Rank_Dense) + 1 / (k + Rank_Sparse)`锛屽钩婊戝洜鍗曚竴妯℃€佺己闄峰鑷寸殑婕忓彫鍥炪€?

- **Filtering & Reranking (绮剧‘杩囨护涓庨噸鎺?**
	- **Metadata Filtering Strategy (閫氱敤杩囨护绛栫暐)**锛?
		- **鍘熷垯锛氬厛瑙ｆ瀽銆佽兘鍓嶇疆鍒欏墠缃€佹棤娉曞墠缃垯鍚庣疆鍏滃簳銆?*
		- Query Processing 闃舵搴斿皢缁撴瀯鍖栫害鏉熻В鏋愪负閫氱敤 `filters`锛堜緥濡?`collection`/`doc_type`/`language`/`time_range`/`access_level` 绛夛級銆?
		- 鑻ュ簳灞傜储寮曟敮鎸佷笖灞炰簬纭害鏉燂紙Hard Filter锛夛紝鍒欏湪 Dense/Sparse 妫€绱㈤樁娈靛仛 Pre-filter 浠ョ缉灏忓€欓€夐泦銆侀檷浣庢垚鏈€?
		- 鏃犳硶鍓嶇疆鐨勮繃婊わ紙绱㈠紩涓嶆敮鎸佹垨瀛楁缂哄け/璐ㄩ噺涓嶇ǔ锛夊湪 Rerank 鍓嶇粺涓€鍋?Post-filter 浣滀负 safety net锛涘缂哄け瀛楁榛樿閲囧彇鈥滃鏉惧寘鍚€?missing->include) 浠ラ伩鍏嶈鏉€鍙洖銆?
		- 杞亸濂斤紙Soft Preference锛屼緥濡傗€滄洿杩戞湡鏇村ソ鈥濓級涓嶅簲纭繃婊わ紝鑰屽簲浣滀负鎺掑簭淇″彿鍦ㄨ瀺鍚?閲嶆帓闃舵鍔犳潈銆?
	- **Rerank Backend (鍙彃鎷旂簿鎺掑悗绔?**锛?
		- **鐩爣**锛氬湪 Top-M 鍊欓€変笂杩涜楂樼簿搴︽帓搴?杩囨护锛涜妯″潡蹇呴』鍙叧闂紝骞舵彁渚涚ǔ瀹氬洖閫€绛栫暐銆?
		- **鍚庣閫夐」**锛?
			1. **None (鍏抽棴绮炬帓)**锛氱洿鎺ヨ繑鍥炶瀺鍚堝悗鐨?Top-K锛圧RF 鎺掑悕浣滀负鏈€缁堢粨鏋滐級銆?
			2. **Cross-Encoder Rerank (鏈湴/鎵樼妯″瀷)**锛氳緭鍏ヤ负 `[Query, Chunk]` 瀵癸紝杈撳嚭鐩稿叧鎬у垎鏁板苟鎺掑簭锛涢€傚悎绋冲畾銆佺粨鏋勫寲杈撳嚭銆侰PU 鐜涓嬪缓璁粯璁や粎瀵硅緝灏忕殑 Top-M 鎵ц锛堜緥濡?M=10~30锛夛紝骞舵彁渚涜秴鏃跺洖閫€銆?
			3. **LLM Rerank (鍙€?**锛氫娇鐢?LLM 瀵瑰€欓€夐泦鎺掑簭/閫夋嫨锛涢€傚悎闇€瑕佹洿寮烘寚浠ょ悊瑙ｆ垨鏃犳湰鍦版ā鍨嬬幆澧冩椂銆備负鎺у埗鎴愭湰涓庣ǔ瀹氭€э紝鍊欓€夋暟搴旀洿灏忥紙渚嬪 M<=20锛夛紝骞惰姹傝緭鍑轰弗鏍肩粨鏋勫寲鏍煎紡锛堝 JSON 鐨?ranked ids锛夈€?
		- **榛樿涓庡洖閫€ (Fallback)**锛?
			- 榛樿绛栫暐闈㈠悜閫氱敤妗嗘灦涓?CPU 鐜锛氫紭鍏堜繚璇佲€滃彲鐢ㄤ笌鍙帶鈥濓紝Cross-Encoder/LLM 鍧囦负鍙€夊寮恒€?
			- 褰撶簿鎺掍笉鍙敤/瓒呮椂/澶辫触鏃讹紝蹇呴』鍥為€€鍒拌瀺鍚堥樁娈电殑鎺掑簭锛圧RF Top-K锛夛紝纭繚绯荤粺鍙敤鎬т笌缁撴灉绋冲畾鎬с€?

### 3.2 MCP 鏈嶅姟璁捐 (MCP Service Design)

**鐩爣锛?* 璁捐骞跺疄鐜颁竴涓鍚?Model Context Protocol (MCP) 瑙勮寖鐨?Server锛屼娇鍏惰兘澶熶綔涓虹煡璇嗕笂涓嬫枃鎻愪緵鑰咃紝鏃犵紳瀵规帴涓绘祦 MCP Clients锛堝 GitHub Copilot銆丆laude Desktop 绛夛級锛岃鐢ㄦ埛閫氳繃鐜版湁 AI 鍔╂墜鍗冲彲鏌ヨ绉佹湁鐭ヨ瘑搴撱€?

#### 3.2.1 鏍稿績璁捐鐞嗗康

- **鍗忚浼樺厛 (Protocol-First)**锛氫弗鏍奸伒寰?MCP 瀹樻柟瑙勮寖锛圝SON-RPC 2.0锛夛紝纭繚涓庝换浣曞悎瑙?Client 鐨勪簰鎿嶄綔鎬с€?
- **寮€绠卞嵆鐢?(Zero-Config for Clients)**锛欳lient 绔棤闇€浠讳綍鐗规畩閰嶇疆锛屽彧闇€鍦ㄩ厤缃枃浠朵腑娣诲姞 Server 杩炴帴淇℃伅鍗冲彲浣跨敤鍏ㄩ儴鍔熻兘銆?
- **寮曠敤閫忔槑 (Citation Transparency)**锛氭墍鏈夋绱㈢粨鏋滃繀椤绘惡甯﹀畬鏁寸殑鏉ユ簮淇℃伅锛屾敮鎸?Client 绔睍绀?鍥炵瓟渚濇嵁"锛屽寮虹敤鎴峰 AI 杈撳嚭鐨勪俊浠汇€?
- **澶氭ā鎬佸弸濂?(Multimodal-Ready)**锛氳繑鍥炴牸寮忓簲鏀寔鏂囨湰涓庡浘鍍忕瓑澶氱鍐呭绫诲瀷锛屼负鏈潵鐨勫瘜濯掍綋灞曠ず棰勭暀鎵╁睍绌洪棿銆?

#### 3.2.2 浼犺緭鍗忚锛歋tdio 鏈湴閫氫俊

鏈」鐩噰鐢?**Stdio Transport** 浣滀负鍞竴閫氫俊妯″紡銆?

- **宸ヤ綔鏂瑰紡**锛欳lient锛圴S Code Copilot銆丆laude Desktop锛変互瀛愯繘绋嬫柟寮忓惎鍔ㄦ垜浠殑 Server锛屽弻鏂归€氳繃鏍囧噯杈撳叆/杈撳嚭浜ゆ崲 JSON-RPC 娑堟伅銆?
- **閫夊瀷鐞嗙敱**锛?
	- **闆堕厤缃?*锛氭棤闇€缃戠粶绔彛銆佹棤闇€閴存潈锛岀敤鎴峰彧闇€鍦?Client 閰嶇疆鏂囦欢涓寚瀹氬惎鍔ㄥ懡浠ゅ嵆鍙娇鐢ㄣ€?
	- **闅愮瀹夊叏**锛氭暟鎹笉缁忚繃缃戠粶锛屽ぉ鐒堕€傚悎澶勭悊绉佹湁鐭ヨ瘑搴撲笌鏁忔劅涓氬姟鏁版嵁銆?
	- **濂戝悎瀹氫綅**锛歋tdio 瀹岀編閫傞厤寮€鍙戣€呮湰鍦板伐浣滄祦锛屾弧瓒崇鏈夌煡璇嗙鐞嗕笌蹇€熷師鍨嬮獙璇侀渶姹傘€?
- **瀹炵幇绾︽潫**锛?
	- `stdout` 浠呰緭鍑哄悎娉?MCP 娑堟伅锛岀姝㈡贩鍏ヤ换浣曟棩蹇楁垨璋冭瘯淇℃伅銆?
	- 鏃ュ織缁熶竴杈撳嚭鑷?`stderr`锛岄伩鍏嶆薄鏌撻€氫俊閫氶亾銆?

#### 3.2.3 SDK 涓庡疄鐜板簱閫夊瀷

- **棣栭€夛細Python 瀹樻柟 MCP SDK (`mcp`)**
	- **浼樺娍**锛?
		- 瀹樻柟缁存姢锛屼笌鍗忚瑙勮寖鍚屾鏇存柊锛屼繚璇佹渶鏂扮壒鎬ф敮鎸侊紙濡?`outputSchema`銆乣annotations` 绛夛級銆?
		- 鎻愪緵 `@server.tool()` 绛夎楗板櫒锛屽０鏄庡紡瀹氫箟 Tools/Resources/Prompts锛屼唬鐮佺畝娲併€?
		- 鍐呯疆 Stdio 涓?HTTP Transport 鏀寔锛屾棤闇€鎵嬪姩澶勭悊 JSON-RPC 搴忓垪鍖栦笌鐢熷懡鍛ㄦ湡绠＄悊銆?
	- **閫傜敤**锛氭湰椤圭洰鐨勯粯璁ゅ疄鐜版柟妗堛€?

- **澶囬€夛細FastAPI + 鑷畾涔夊崗璁眰**
	- **鍦烘櫙**锛氶渶瑕佹繁搴﹀畾鍒?HTTP 琛屼负锛堝鑷畾涔変腑闂翠欢銆佸鏉傞壌鏉冩祦绋嬶級鎴栧笇鏈涘涔?MCP 鍗忚搴曞眰缁嗚妭鏃跺彲鑰冭檻銆?
	- **鏉冭　**锛氬紑鍙戞垚鏈洿楂橈紝闇€鑷瀹炵幇鑳藉姏鍗忓晢 (Capability Negotiation)銆侀敊璇爜鏄犲皠绛夛紝涓旈渶鎸佺画璺熻繘鍗忚鐗堟湰鏇存柊銆?

- **鍗忚鐗堟湰**锛氳窡韪?MCP 鏈€鏂扮ǔ瀹氱増鏈紙濡?`2025-06-18`锛夛紝鍦?`initialize` 闃舵杩涜鐗堟湰鍗忓晢锛岀‘淇?Client/Server 鍏煎鎬с€?

#### 3.2.4 瀵瑰鏆撮湶鐨勫伐鍏峰嚱鏁拌璁?(Tools Design)

Server 閫氳繃 `tools/list` 鍚?Client 娉ㄥ唽鍙皟鐢ㄧ殑宸ュ叿鍑芥暟銆傚伐鍏疯璁″簲閬靛惊"鍗曚竴鑱岃矗銆佸弬鏁版槑纭€佽緭鍑轰赴瀵?鍘熷垯銆?

- **鏍稿績宸ュ叿闆?*锛?

| 宸ュ叿鍚嶇О | 鍔熻兘鎻忚堪 | 鍏稿瀷杈撳叆鍙傛暟 | 杈撳嚭鐗圭偣 |
|---------|---------|-------------|---------|
| `query_knowledge_hub` | 涓绘绱㈠叆鍙ｏ紝鎵ц娣峰悎妫€绱?+ Rerank锛岃繑鍥炴渶鐩稿叧鐗囨 | `query: string`, `top_k?: int`, `collection?: string` | 杩斿洖甯﹀紩鐢ㄧ殑缁撴瀯鍖栫粨鏋?|
| `list_collections` | 鍒椾妇鐭ヨ瘑搴撲腑鍙敤鐨勬枃妗ｉ泦鍚?| 鏃?| 闆嗗悎鍚嶇О銆佹弿杩般€佹枃妗ｆ暟閲?|
| `get_document_summary` | 鑾峰彇鎸囧畾鏂囨。鐨勬憳瑕佷笌鍏冧俊鎭?| `doc_id: string` | 鏍囬銆佹憳瑕併€佸垱寤烘椂闂淬€佹爣绛?|

- **鎵╁睍宸ュ叿锛圓gentic 婕旇繘鏂瑰悜锛?*锛?
	- `search_by_keyword` / `search_by_semantic`锛氭媶鍒嗙嫭绔嬬殑妫€绱㈢瓥鐣ワ紝渚?Agent 鑷富閫夋嫨銆?
	- `verify_answer`锛氫簨瀹炴牳鏌ュ伐鍏凤紝妫€娴嬬敓鎴愬唴瀹规槸鍚︽湁渚濇嵁鏀拺銆?
	- `list_document_sections`锛氭祻瑙堟枃妗ｇ洰褰曠粨鏋勶紝鏀寔澶氭瀵艰埅寮忔绱€?

#### 3.2.5 杩斿洖鍐呭涓庡紩鐢ㄩ€忔槑璁捐 (Response & Citation Design)

MCP 鍗忚鐨?Tool 杩斿洖鏍煎紡鏀寔澶氱鍐呭绫诲瀷锛坄content` 鏁扮粍锛夛紝鏈」鐩皢鍏呭垎鍒╃敤杩欎竴鐗规€у疄鐜?鍙函婧?鐨勫洖绛旓細

- **缁撴瀯鍖栧紩鐢ㄨ璁?*锛?
	- 姣忎釜妫€绱㈢粨鏋滅墖娈靛簲鍖呭惈瀹屾暣鐨勫畾浣嶄俊鎭細`source_file`锛堟枃浠跺悕/璺緞锛夈€乣page`锛堥〉鐮侊紝濡傞€傜敤锛夈€乣chunk_id`锛堢墖娈垫爣璇嗭級銆乣score`锛堢浉鍏虫€у垎鏁帮級銆?
	- 鎺ㄨ崘鍦ㄨ繑鍥炵殑 `structuredContent` 涓噰鐢ㄧ粺涓€鐨?Citation 鏍煎紡锛?
		```
		{
		  "answer": "...",
		  "citations": [
		    { "id": 1, "source": "xxx.pdf", "page": 5, "text": "鍘熸枃鐗囨...", "score": 0.92 },
		    ...
		  ]
		}
		```
	- 鍚屾椂鍦?`content` 鏁扮粍涓互 Markdown 鏍煎紡鍛堢幇浜虹被鍙鐨勫甫寮曠敤鍥炵瓟锛坄[1]` 鏍囨敞锛夛紝淇濊瘉 Client 鏃犺鏄惁瑙ｆ瀽缁撴瀯鍖栧唴瀹归兘鑳藉睍绀哄紩鐢ㄣ€?

- **澶氭ā鎬佸唴瀹硅繑鍥?*锛?
	- **鏂囨湰鍐呭 (TextContent)**锛氶粯璁よ繑鍥炵被鍨嬶紝Markdown 鏍煎紡锛屾敮鎸佷唬鐮佸潡銆佸垪琛ㄧ瓑瀵屾枃鏈€?
	- **鍥惧儚鍐呭 (ImageContent)**锛氬綋妫€绱㈢粨鏋滃叧鑱斿浘鍍忔椂锛孲erver 璇诲彇鏈湴鍥剧墖鏂囦欢骞剁紪鐮佷负 Base64 杩斿洖銆?
		- **鏍煎紡**锛歚{ "type": "image", "data": "<base64>", "mimeType": "image/png" }`
		- **宸ヤ綔娴佺▼**锛氭暟鎹憚鍙栭樁娈靛瓨鍌ㄥ浘鐗囨湰鍦拌矾寰?鈫?妫€绱㈠懡涓悗 Server 鍔ㄦ€佽鍙?鈫?缂栫爜涓?Base64 鈫?宓屽叆杩斿洖娑堟伅銆?
		- **Client 鍏煎鎬?*锛氬浘鍍忓睍绀鸿兘鍔涘彇鍐充簬 Client 瀹炵幇锛孏itHub Copilot 鍙兘闄嶇骇澶勭悊锛孋laude Desktop 鏀寔瀹屾暣娓叉煋銆係erver 绔粺涓€杩斿洖 Base64 鏍煎紡锛岀敱 Client 鍐冲畾濡備綍娓叉煋銆?

- **Client 閫傞厤绛栫暐**锛?
	- **GitHub Copilot (VS Code)**锛氬綋鍓嶅 MCP 鐨勬敮鎸侀泦涓湪 Tools 璋冪敤锛岃繑鍥炵殑 `content` 涓殑鏂囨湰浼氬睍绀虹粰鐢ㄦ埛銆傚缓璁互娓呮櫚鐨?Markdown 鏂囨湰锛堝惈寮曠敤鏍囨敞锛変负涓伙紝鍥惧儚浣滀负琛ュ厖銆?
	- **Claude Desktop**锛氬 MCP Tools/Resources 鏈夊畬鏁存敮鎸侊紝鍥惧儚涓庤祫婧愰摼鎺ュ彲鐩存帴娓叉煋銆傚彲鏇存縺杩涘湴浣跨敤澶氭ā鎬佽繑鍥炪€?
	- **閫氱敤鍏煎鍘熷垯**锛氬缁堝湪 `content` 鏁扮粍绗竴椤规彁渚涚函鏂囨湰/Markdown 鐗堟湰鐨勭瓟妗堬紝纭繚鏈€浣庡吋瀹规€э紱灏嗙粨鏋勫寲鏁版嵁銆佸浘鍍忕瓑鏀惧湪鍚庣画椤规垨 `structuredContent` 涓紝渚涢珮绾?Client 瑙ｆ瀽銆?

### 3.3 鍙彃鎷旀灦鏋勮璁?(Pluggable Architecture Design)

**鐩爣锛?* 瀹氫箟娓呮櫚鐨勬娊璞″眰涓庢帴鍙ｅ绾︼紝浣?RAG 閾捐矾鐨勬瘡涓牳蹇冪粍浠堕兘鑳藉鐙珛鏇挎崲涓庡崌绾э紝閬垮厤鎶€鏈攣瀹氾紝鏀寔浣庢垚鏈殑 A/B 娴嬭瘯涓庣幆澧冭縼绉汇€?

> **鏈璇存槑**锛氭湰鑺備腑鐨?鎻愪緵鑰?(Provider)"銆?瀹炵幇 (Implementation)"鎸囩殑鏄畬鎴愭煇椤瑰姛鑳界殑**鍏蜂綋鎶€鏈柟妗?*锛岃€岄潪浼犵粺 Web 鏋舵瀯涓殑"鍚庣鏈嶅姟鍣?銆備緥濡傦紝LLM 鎻愪緵鑰呭彲浠ユ槸杩滅▼鐨?Azure OpenAI API锛屼篃鍙互鏄湰鍦拌繍琛岀殑 Ollama锛涘悜閲忓瓨鍌ㄥ彲浠ユ槸鏈湴宓屽叆寮忕殑 Chroma锛屼篃鍙互鏄簯绔墭绠＄殑 Pinecone銆傛湰椤圭洰浣滀负鏈湴 MCP Server锛岄€氳繃缁熶竴鎺ュ彛瀵规帴杩欎簺涓嶅悓鐨勬彁渚涜€咃紝瀹炵幇鐏垫椿鍒囨崲銆?

#### 3.3.1 璁捐鍘熷垯

- **鎺ュ彛闅旂 (Interface Segregation)**锛氫负姣忕被缁勪欢瀹氫箟鏈€灏忓寲鐨勬娊璞℃帴鍙ｏ紝涓婂眰涓氬姟閫昏緫浠呬緷璧栨帴鍙ｈ€岄潪鍏蜂綋瀹炵幇銆?
- **閰嶇疆椹卞姩 (Configuration-Driven)**锛氶€氳繃缁熶竴閰嶇疆鏂囦欢锛堝 `settings.yaml`锛夋寚瀹氬悇缁勪欢鐨勫叿浣撳悗绔紝浠ｇ爜鏃犻渶淇敼鍗冲彲鍒囨崲瀹炵幇銆?
- **宸ュ巶妯″紡 (Factory Pattern)**锛氫娇鐢ㄥ伐鍘傚嚱鏁版牴鎹厤缃姩鎬佸疄渚嬪寲瀵瑰簲鐨勫疄鐜扮被锛屽疄鐜?涓€澶勯厤缃紝澶勫鐢熸晥"銆?
- **浼橀泤闄嶇骇 (Graceful Fallback)**锛氬綋棣栭€夊悗绔笉鍙敤鏃讹紝绯荤粺搴旇嚜鍔ㄥ洖閫€鍒板閫夋柟妗堟垨瀹夊叏榛樿鍊硷紝淇濋殰鍙敤鎬с€?

**閫氱敤缁撴瀯绀烘剰锛堥€傜敤浜?3.3.2 / 3.3.3 / 3.3.4 绛夊彲鎻掓嫈缁勪欢锛?*锛?

```
涓氬姟浠ｇ爜
  鈹?
  鈻?
<Component>Factory.get_xxx()  鈫?璇诲彇閰嶇疆锛屽喅瀹氱敤鍝釜瀹炵幇
  鈹?
  鈹溾攢鈫?ImplementationA()
  鈹溾攢鈫?ImplementationB()  
  鈹斺攢鈫?ImplementationC()
      鈹?
      鈻?
    閮藉疄鐜颁簡缁熶竴鐨勬娊璞℃帴鍙?
```

#### 3.3.2 LLM 涓?Embedding 鎻愪緵鑰呮娊璞?

杩欐槸鍙彃鎷旇璁＄殑鏍稿績鐜妭锛屽洜涓烘ā鍨嬫彁渚涜€呯殑閫夋嫨鐩存帴褰卞搷鎴愭湰銆佹€ц兘涓庨殣绉佸悎瑙勩€?

- **缁熶竴鎺ュ彛灞?(Unified API Abstraction)**锛?
	- **璁捐鎬濊矾**锛氭棤璁哄簳灞備娇鐢?Azure OpenAI銆丱penAI 鍘熺敓 API銆丏eepSeek 杩樻槸鏈湴 Ollama锛屼笂灞傝皟鐢ㄤ唬鐮佸簲淇濇寔涓€鑷淬€?
	- **鍏抽敭鎶借薄**锛?
		- `LLMClient`锛氭毚闇?`chat(messages) -> response` 鏂规硶锛屽睆钄戒笉鍚?Provider 鐨勮璇佹柟寮忎笌璇锋眰鏍煎紡宸紓銆?
		- `EmbeddingClient`锛氭毚闇?`embed(texts) -> vectors` 鏂规硶锛岀粺涓€澶勭悊鎵归噺璇锋眰涓庣淮搴﹀綊涓€鍖栥€?

- **鎻愪緵鑰呴€夐」涓庡垏鎹㈠満鏅?*锛?

| 鎻愪緵鑰呯被鍨?| 鍏稿瀷鍦烘櫙 | 閰嶇疆鍒囨崲鐐?|
|---------|---------|-----------|
| **Azure OpenAI** | 浼佷笟鍚堣銆佺鏈変簯閮ㄧ讲銆佸尯鍩熸暟鎹┗鐣?| `provider: azure`, `endpoint`, `api_key`, `deployment_name` |
| **OpenAI 鍘熺敓** | 閫氱敤寮€鍙戙€佹渶鏂版ā鍨嬪皾椴?| `provider: openai`, `api_key`, `model` |
| **DeepSeek / 鍏朵粬浜戠** | 鎴愭湰浼樺寲銆佺壒瀹氳瑷€浼樺寲 | `provider: deepseek`, `api_key`, `model` |
| **Ollama / vLLM (鏈湴)** | 瀹屽叏绂荤嚎銆侀殣绉佹晱鎰熴€佹棤 API 鎴愭湰 | `provider: ollama`, `base_url`, `model` |

- **鎶€鏈€夊瀷寤鸿**锛?
	- 鏈」鐩噰鐢ㄨ嚜鐮旂殑 `BaseLLM` / `BaseEmbedding` 鎶借薄鍩虹被锛岄厤鍚堝伐鍘傛ā寮忥紙`llm_factory.py` / `embedding_factory.py`锛夊疄鐜扮粺涓€璋冪敤鎺ュ彛銆傚凡鍐呯疆 Azure OpenAI銆丱penAI銆丱llama銆丏eepSeek 鍥涚 Provider 閫傞厤銆?
	- 瀵逛簬鍏朵粬 Provider锛屽彲閫氳繃 **OpenAI-Compatible 妯″紡**鎺ュ叆锛堣缃嚜瀹氫箟 `api_base`锛夛紝鎴栧疄鐜?`BaseLLM` 鎺ュ彛骞跺湪宸ュ巶涓敞鍐屻€?

	- 瀵逛簬浼佷笟绾ч渶姹傦紝鍙湪鍏跺熀纭€涓婂鍔犵粺涓€鐨?**閲嶈瘯銆侀檺娴併€佹棩蹇?* 涓棿灞傦紝鎻愬崌鐢熶骇鍙潬鎬э紝浣嗘湰椤圭洰鏆備笉瀹炵幇锛岃繖閲屼粎鎻愪緵鎬濊矾銆?
	- **Vision LLM 鎵╁睍**锛氶拡瀵瑰浘鍍忔弿杩扮敓鎴愶紙Image Captioning锛夐渶姹傦紝绯荤粺鎵╁睍浜?`BaseVisionLLM` 鎺ュ彛锛屾敮鎸佹枃鏈?鍥剧墖鐨勫妯℃€佽緭鍏ャ€傚綋鍓嶅疄鐜帮細
		- **Azure OpenAI Vision**锛圙PT-4o/GPT-4-Vision锛夛細浼佷笟绾у悎瑙勯儴缃诧紝鏀寔澶嶆潅鍥捐〃瑙ｆ瀽锛屼笌 Azure 鐢熸€佹繁搴﹂泦鎴愩€?

#### 3.3.3 妫€绱㈢瓥鐣ユ娊璞?

妫€绱㈠眰鐨勫彲鎻掓嫈鎬у喅瀹氫簡绯荤粺鍦ㄤ笉鍚屾暟鎹妯′笌鏌ヨ妯″紡涓嬬殑閫傚簲鑳藉姏銆?

**璁捐妯″紡锛氭娊璞″伐鍘傛ā寮?*

涓?3.3.2 鑺傜殑 LLM 鎶借薄绫讳技锛屾绱㈠眰鍚勭粍浠剁殑鍙彃鎷旀€у悓鏍蜂緷璧栦袱灞傝璁★細

1. **鑷爺鐨勭粺涓€鎶借薄鎺ュ彛**锛氭湰椤圭洰涓哄悜閲忔暟鎹簱锛坄BaseVectorStore`锛夈€丒mbedding锛坄BaseEmbedding`锛夈€佸垎鍧楋紙`BaseSplitter`锛夌瓑鏍稿績缁勪欢瀹氫箟浜嗙粺涓€鐨勬娊璞″熀绫伙紝涓嶅悓瀹炵幇鍙渶閬靛惊鐩稿悓鎺ュ彛鍗冲彲鏃犵紳鏇挎崲銆?

2. **宸ュ巶鍑芥暟璺敱**锛氭瘡涓娊璞″眰閰嶅宸ュ巶鍑芥暟锛堝 `embedding_factory.py`銆乣splitter_factory.py`锛夛紝鏍规嵁 `settings.yaml` 涓殑閰嶇疆瀛楁鑷姩瀹炰緥鍖栧搴斿疄鐜帮紝瀹炵幇"鏀归厤缃笉鏀逛唬鐮?鐨勫垏鎹綋楠屻€?


閫氱敤鐨勨€滈厤缃┍鍔?+ 宸ュ巶璺敱鈥濈粨鏋勭ず鎰忚 3.3.1 鑺傘€?

涓嬮潰鍒嗗埆璇存槑鍚勭粍浠跺浣曞簲鐢ㄨ繖涓€妯″紡锛?

---

**1. 鍒嗗潡绛栫暐 (Chunking Strategy)**

鍒嗗潡鏄?Ingestion Pipeline 鐨勬牳蹇冪幆鑺備箣涓€锛屽喅瀹氫簡鏂囨。濡備綍琚垏鍒嗕负閫傚悎妫€绱㈢殑璇箟鍗曞厓銆傛湰椤圭洰鐨?Splitter 灞傞噰鐢ㄥ彲鎻掓嫈璁捐锛圔aseSplitter 鎶借薄鎺ュ彛 + SplitterFactory 宸ュ巶锛夛紝涓嶅悓鍒嗗潡瀹炵幇鍙渶閬靛惊鐩稿悓鎺ュ彛鍗冲彲鏃犵紳鏇挎崲銆?

甯歌鐨勫垎鍧楃瓥鐣ュ寘鎷細
- **鍥哄畾闀垮害鍒囧垎**锛氭寜瀛楃鏁版垨 Token 鏁板垏鍒嗭紝绠€鍗曚絾鍙兘鐮村潖璇箟瀹屾暣鎬с€?
- **閫掑綊瀛楃鍒囧垎**锛氭寜灞傜骇鍒嗛殧绗︼紙娈佃惤鈫掑彞瀛愨啋瀛楃锛夐€掑綊鍒囧垎锛屽湪闀垮害闄愬埗鍐呭敖閲忎繚鎸佽涔夎竟鐣屻€?
- **璇箟鍒囧垎**锛氬埄鐢?Embedding 鐩镐技搴︽娴嬭涔夋柇鐐癸紝纭繚姣忎釜 Chunk 鏄嚜鍖呭惈鐨勮涔夊崟鍏冦€?
- **缁撴瀯鎰熺煡鍒囧垎**锛氭牴鎹枃妗ｇ粨鏋勶紙Markdown 鏍囬銆佷唬鐮佸潡銆佸垪琛ㄧ瓑锛夎繘琛屽垏鍒嗐€?

鏈」鐩綋鍓嶉噰鐢?**LangChain 鐨?`RecursiveCharacterTextSplitter`** 杩涜鍒囧垎锛岃鏂规硶瀵?Markdown 鏂囨。鐨勭粨鏋勶紙鏍囬銆佹钀姐€佸垪琛ㄣ€佷唬鐮佸潡锛夋湁澶╃劧鐨勯€傞厤鎬э紝鑳藉閫氳繃閰嶇疆璇箟鏂偣锛圫eparators锛夊疄鐜伴珮璐ㄩ噺銆佽涔夊畬鏁寸殑鍒囧潡銆?

> **褰撳墠瀹炵幇璇存槑**锛氱洰鍓嶇郴缁熶娇鐢?LangChain RecursiveCharacterTextSplitter銆傛灦鏋勮璁′笂棰勭暀浜嗗垏鎹㈣兘鍔涳紝濡傞渶鍒囨崲涓?SentenceSplitter銆丼emanticSplitter 鎴栬嚜瀹氫箟鍒囧垎鍣紝鍙渶瀹炵幇 BaseSplitter 鎺ュ彛骞跺湪閰嶇疆涓寚瀹氬嵆鍙€?

---

**2. 鍚戦噺鏁版嵁搴?(Vector Store)**

鏈」鐩嚜瀹氫箟浜嗙粺涓€鐨?BaseVectorStore 鎶借薄鎺ュ彛锛屾毚闇?.add()銆?query()銆?delete() 绛夋柟娉曘€傛墍鏈夊悜閲忔暟鎹簱鍚庣锛圕hroma銆丵drant銆丳inecone 绛夛級鍙渶瀹炵幇璇ユ帴鍙ｅ嵆鍙彃鎷旀浛鎹紝閫氳繃 VectorStoreFactory 鏍规嵁閰嶇疆鑷姩閫夋嫨鍏蜂綋瀹炵幇銆?

鏈」鐩€夌敤 **Chroma** 浣滀负鍚戦噺鏁版嵁搴撱€傜浉姣?Qdrant銆丮ilvus銆乄eaviate 绛夐渶瑕?Docker 瀹瑰櫒鎴栧垎甯冨紡鏋舵瀯鏀拺鐨勬柟妗堬紝Chroma 閲囩敤宓屽叆寮忚璁★紝`pip install chromadb` 鍗冲彲浣跨敤锛屾棤闇€棰濆閮ㄧ讲鏁版嵁搴撴湇鍔★紝闈炲父閫傚悎鏈湴寮€鍙戜笌蹇€熷師鍨嬮獙璇併€傚悓鏃?ChromaStore 閫傞厤鍣紙src/libs/vector_store/chroma_store.py锛夛紝涓?Pipeline 鏃犵紳闆嗘垚銆?

> **褰撳墠瀹炵幇璇存槑**锛氱洰鍓嶇郴缁熶粎瀹炵幇浜?Chroma 鍚庣銆傝櫧鐒舵灦鏋勮璁′笂棰勭暀浜嗗伐鍘傛ā寮忎互鏀寔鏈潵鎵╁睍锛屼絾褰撳墠鐗堟湰灏氭湭瀹炵幇鍏朵粬鍚戦噺鏁版嵁搴撶殑閫傞厤鍣ㄣ€?

---

**3. 鍚戦噺缂栫爜绛栫暐 (Embedding Strategy)**

鍚戦噺缂栫爜鏄?Ingestion Pipeline 鐨勫叧閿幆鑺傦紝鍐冲畾浜?Chunk 濡備綍琚浆鎹负鍙绱㈢殑鍚戦噺琛ㄧず銆傛湰椤圭洰鑷畾涔変簡 BaseEmbedding 鎶借薄鎺ュ彛锛坰rc/libs/embedding/base.py锛夛紝鏀寔涓嶅悓 Embedding 妯″瀷鐨勫彲鎻掓嫈鏇挎崲銆?

甯歌鐨勭紪鐮佺瓥鐣ュ寘鎷細
- **绾瀵嗙紪鐮侊紙Dense Only锛?*锛氫粎鐢熸垚璇箟鍚戦噺锛岄€傚悎閫氱敤鍦烘櫙銆?
- **绾█鐤忕紪鐮侊紙Sparse Only锛?*锛氫粎鐢熸垚鍏抽敭璇嶆潈閲嶅悜閲忥紝閫傚悎绮剧‘鍖归厤鍦烘櫙銆?
- **鍙岃矾缂栫爜锛圖ense + Sparse锛?*锛氬悓鏃剁敓鎴愮瀵嗗悜閲忓拰绋€鐤忓悜閲忥紝涓烘贩鍚堟绱㈡彁渚涙暟鎹熀纭€銆?

鏈」鐩綋鍓嶉噰鐢?**鍙岃矾缂栫爜锛圖ense + Sparse锛?* 绛栫暐锛?
- **Dense Embeddings锛堣涔夊悜閲忥級**锛氳皟鐢?Embedding 妯″瀷锛堝 OpenAI text-embedding-3锛夌敓鎴愰珮缁存诞鐐瑰悜閲忥紝鎹曟崏鏂囨湰鐨勬繁灞傝涔夊叧鑱斻€?
- **Sparse Embeddings锛堢█鐤忓悜閲忥級**锛氬埄鐢?BM25 缂栫爜鍣ㄧ敓鎴愮█鐤忓悜閲忥紙Keyword Weights锛夛紝鎹曟崏绮剧‘鐨勫叧閿瘝鍖归厤淇℃伅銆?

瀛樺偍鏃讹紝Dense Vector 鍜?Sparse Vector 涓?Chunk 鍘熸枃銆丮etadata 涓€璧峰師瀛愬寲鍐欏叆鍚戦噺鏁版嵁搴擄紝纭繚妫€绱㈡椂鍙悓鏃跺埄鐢ㄤ袱绉嶅悜閲忋€?

> **褰撳墠瀹炵幇璇存槑**锛氱洰鍓嶇郴缁熷疄鐜颁簡 Dense + Sparse 鍙岃矾缂栫爜銆傛灦鏋勮璁′笂棰勭暀浜嗗垏鎹㈣兘鍔涳紝濡傞渶浣跨敤鍏朵粬 Embedding 妯″瀷锛堝 BGE銆丱llama 鏈湴妯″瀷锛夋垨璋冩暣缂栫爜绛栫暐锛屽彲鍦?Pipeline 涓浛鎹㈢浉搴旂粍浠躲€?

---

**4. 鍙洖绛栫暐 (Retrieval Strategy)**

鍙洖绛栫暐鍐冲畾浜嗘煡璇㈤樁娈靛浣曚粠鐭ヨ瘑搴撲腑妫€绱㈢浉鍏冲唴瀹广€傚熀浜?Ingestion 闃舵瀛樺偍鐨勫悜閲忕被鍨嬶紝鍙噰鐢ㄤ笉鍚岀殑鍙洖鏂规锛?
- **绾瀵嗗彫鍥烇紙Dense Only锛?*锛氫粎浣跨敤璇箟鍚戦噺杩涜鐩镐技搴﹀尮閰嶃€?
- **绾█鐤忓彫鍥烇紙Sparse Only锛?*锛氫粎浣跨敤 BM25 杩涜鍏抽敭璇嶅尮閰嶃€?
- **娣峰悎鍙洖锛圚ybrid锛?*锛氬苟琛屾墽琛岀瀵嗗拰绋€鐤忎袱璺彫鍥烇紝鍐嶉€氳繃铻嶅悎绠楁硶鍚堝苟缁撴灉銆?
- **娣峰悎鍙洖 + 绮炬帓锛圚ybrid + Rerank锛?*锛氬湪娣峰悎鍙洖鍩虹涓婏紝澧炲姞绮炬帓姝ラ杩涗竴姝ユ彁鍗囩浉鍏虫€с€?

鏈」鐩綋鍓嶉噰鐢?**娣峰悎鍙洖 + 绮炬帓锛圚ybrid + Rerank锛?* 绛栫暐锛?
- **绋犲瘑鍙洖锛圖ense Route锛?*锛氳绠?Query Embedding锛屽湪鍚戦噺搴撲腑杩涜 Cosine Similarity 妫€绱紝杩斿洖 Top-N 璇箟鍊欓€夈€?
- **绋€鐤忓彫鍥烇紙Sparse Route锛?*锛氫娇鐢?BM25 绠楁硶妫€绱㈠€掓帓绱㈠紩锛岃繑鍥?Top-N 鍏抽敭璇嶅€欓€夈€?
- **铻嶅悎锛團usion锛?*锛氫娇鐢?RRF (Reciprocal Rank Fusion) 绠楁硶灏嗕袱璺粨鏋滃悎骞舵帓搴忋€?
- **绮炬帓锛圧erank锛?*锛氬铻嶅悎鍚庣殑鍊欓€夐泦杩涜閲嶆帓搴忥紝鏀寔 None / Cross-Encoder / LLM Rerank 涓夌妯″紡銆?

> **褰撳墠瀹炵幇璇存槑**锛氱洰鍓嶇郴缁熷疄鐜颁簡 Hybrid + Rerank 绛栫暐銆傛灦鏋勮璁′笂棰勭暀浜嗙瓥鐣ュ垏鎹㈣兘鍔涳紝濡傞渶浣跨敤绾瀵嗘垨绾█鐤忓彫鍥烇紝鍙€氳繃閰嶇疆鍒囨崲锛涜瀺鍚堢畻娉曞拰 Reranker 鍚屾牱鏀寔鏇挎崲銆?

#### 3.3.4 璇勪及妗嗘灦鎶借薄

璇勪及浣撶郴鐨勫彲鎻掓嫈鎬х‘淇濆洟闃熷彲浠ユ牴鎹笟鍔＄洰鏍囩伒娲婚€夋嫨鎴栫粍鍚堜笉鍚岀殑璐ㄩ噺搴﹂噺缁村害銆?

- **璁捐鎬濊矾**锛?
	- 瀹氫箟缁熶竴鐨?`Evaluator` 鎺ュ彛锛屾毚闇?`evaluate(query, retrieved_chunks, generated_answer, ground_truth) -> metrics` 鏂规硶銆?
	- 鍚勮瘎浼版鏋跺疄鐜拌鎺ュ彛锛岃緭鍑烘爣鍑嗗寲鐨勬寚鏍囧瓧鍏搞€?

- **鍙€夎瘎浼版鏋?*锛?

| 妗嗘灦 | 鐗圭偣 | 閫傜敤鍦烘櫙 |
|-----|------|---------|
| **Ragas** | RAG 涓撶敤銆佹寚鏍囦赴瀵岋紙Faithfulness, Answer Relevancy, Context Precision 绛夛級 | 鍏ㄩ潰璇勪及 RAG 璐ㄩ噺銆佸鏈姣?|
| **DeepEval** | LLM-as-Judge 妯″紡銆佹敮鎸佽嚜瀹氫箟璇勪及鏍囧噯 | 闇€瑕佷富瑙傝川閲忓垽鏂€佸鏉備笟鍔¤鍒?|
| **鑷畾涔夋寚鏍?* | Hit Rate, MRR, Latency P99 绛夊熀纭€宸ョ▼鎸囨爣 | 蹇€熷洖褰掓祴璇曘€佷笂绾垮墠 Sanity Check |

- **缁勫悎涓庢墿灞?*锛?
	- 璇勪及妯″潡璁捐涓?*缁勫悎妯″紡**锛屽彲鍚屾椂鎸傝浇澶氫釜 Evaluator锛岀敓鎴愮患鍚堟姤鍛娿€?
	- 閰嶇疆绀轰緥锛歚evaluation.backends: [ragas, custom_metrics]`锛岀郴缁熷苟琛屾墽琛屽苟姹囨€荤粨鏋溿€?

#### 3.3.5 閰嶇疆绠＄悊涓庡垏鎹㈡祦绋?

- **閰嶇疆鏂囦欢缁撴瀯绀轰緥** (`config/settings.yaml`)锛?
	```yaml
	llm:
	  provider: azure  # azure | openai | ollama | deepseek
	  model: gpt-4o
	  # provider-specific configs...
	
	embedding:
	  provider: openai
	  model: text-embedding-3-small
	
	vector_store:
	  backend: chroma  # chroma | qdrant | pinecone
	
	retrieval:
	  sparse_backend: bm25  # bm25 | elasticsearch
	  fusion_algorithm: rrf  # rrf | weighted_sum
	  rerank_backend: cross_encoder  # none | cross_encoder | llm
	
	evaluation:
	  backends: [ragas, custom_metrics]
	
	dashboard:
	  enabled: true
	  port: 8501
	  traces_dir: ./logs
	```

- **鍒囨崲娴佺▼**锛?

	1. 淇敼 `settings.yaml` 涓搴旂粍浠剁殑 `backend` / `provider` 瀛楁銆?
	2. 纭繚鏂板悗绔殑渚濊禆宸插畨瑁呫€佸嚟鎹凡閰嶇疆銆?
	3. 閲嶅惎鏈嶅姟锛屽伐鍘傚嚱鏁拌嚜鍔ㄥ姞杞芥柊瀹炵幇锛屾棤闇€淇敼涓氬姟浠ｇ爜銆?

### 3.4 鍙娴嬫€т笌鍙鍖栫鐞嗗钩鍙拌璁?(Observability & Visual Management Platform Design)

**鐩爣锛?* 閽堝 RAG 绯荤粺甯歌鐨?榛戠洅"闂锛岃璁″叏閾捐矾鍙娴嬬殑杩借釜浣撶郴涓庡畬鏁寸殑鍙鍖栫鐞嗗钩鍙般€傝鐩?**Ingestion锛堟憚鍙栭摼璺級** 涓?**Query锛堟煡璇㈤摼璺級** 涓ゆ潯瀹屾暣娴佹按绾跨殑杩借釜璁板綍锛屽悓鏃舵彁渚涙暟鎹祻瑙堛€佹枃妗ｇ鐞嗐€佺粍浠舵瑙堢瓑绠＄悊鍔熻兘锛屼娇鏁翠釜绯荤粺**閫忔槑鍙**銆?*鍙鐞?*涓?*鍙噺鍖?*銆?

#### 3.4.1 璁捐鐞嗗康

- **鍙岄摼璺叏瑕嗙洊杩借釜 (Dual-Pipeline Tracing)**锛?
    - **Ingestion Trace**锛氫互 `trace_id` 涓烘牳蹇冿紝璁板綍涓€娆℃憚鍙栦粠鏂囦欢鍔犺浇鍒板瓨鍌ㄥ畬鎴愮殑鍏ㄨ繃绋嬶紙load 鈫?split 鈫?transform 鈫?embed 鈫?upsert锛夛紝鍖呭惈鍚勯樁娈佃€楁椂銆佸鐞嗙殑 chunk 鏁伴噺銆佽烦杩?澶辫触璇︽儏銆?
    - **Query Trace**锛氫互 `trace_id` 涓烘牳蹇冿紝璁板綍涓€娆℃煡璇粠 Query 杈撳叆鍒?Response 杈撳嚭鐨勫叏杩囩▼锛坬uery_processing 鈫?dense 鈫?sparse 鈫?fusion 鈫?rerank锛夛紝鍖呭惈鍚勯樁娈靛€欓€夋暟閲忋€佸垎鏁板垎甯冧笌鑰楁椂銆?
- **閫忔槑鍙洖婧?(Transparent & Traceable)**锛氭瘡涓樁娈电殑涓棿鐘舵€侀兘琚褰曪紝寮€鍙戣€呭彲浠ユ竻鏅扮湅鍒?绯荤粺涓轰粈涔堝彫鍥炰簡杩欎簺鏂囨。"銆?Rerank 鍓嶅悗鎺掑悕濡備綍鍙樺寲"锛屼粠鑰岀簿鍑嗗畾浣嶉棶棰樸€?
- **浣庝镜鍏ユ€?(Low Intrusiveness)**锛氳拷韪€昏緫涓庝笟鍔￠€昏緫瑙ｈ€︼紝閫氳繃 `TraceContext` 鏄惧紡璋冪敤妯″紡娉ㄥ叆锛岄伩鍏嶆薄鏌撴牳蹇冧唬鐮併€?
- **杞婚噺鏈湴鍖?(Lightweight & Local)**锛氶噰鐢ㄧ粨鏋勫寲鏃ュ織 + 鏈湴 Dashboard 鐨勬柟妗堬紝闆跺閮ㄤ緷璧栵紝寮€绠卞嵆鐢ㄣ€?
- **鍔ㄦ€佺粍浠舵劅鐭?(Dynamic Component Awareness)**锛欴ashboard 鍩轰簬 Trace 涓殑 `method`/`provider`/`details` 瀛楁鍔ㄦ€佹覆鏌擄紝鏇存崲鍙彃鎷旂粍浠跺悗鑷姩閫傞厤灞曠ず鍐呭锛屾棤闇€淇敼 Dashboard 浠ｇ爜銆?


#### 3.4.2 杩借釜鏁版嵁缁撴瀯

绯荤粺瀹氫箟涓ょ被 Trace 璁板綍锛屽垎鍒鐩栨煡璇笌鎽勫彇涓ゆ潯閾捐矾锛?

**A. Query Trace锛堟煡璇㈣拷韪級**

姣忔鏌ヨ璇锋眰鐢熸垚鍞竴鐨?`trace_id`锛岃褰曚粠 Query 杈撳叆鍒?Response 杈撳嚭鐨勫叏杩囩▼锛?

**鍩虹淇℃伅**锛?
- `trace_id`锛氳姹傚敮涓€鏍囪瘑
- `trace_type`锛歚"query"`
- `timestamp`锛氳姹傛椂闂存埑
- `user_query`锛氱敤鎴峰師濮嬫煡璇?
- `collection`锛氭绱㈢殑鐭ヨ瘑搴撻泦鍚?

**鍚勯樁娈佃鎯?(Stages)**锛?

| 闃舵 | 璁板綍鍐呭 |
|-----|---------|
| **Query Processing** | 鍘熷 Query銆佹敼鍐欏悗 Query锛堣嫢鏈夛級銆佹彁鍙栫殑鍏抽敭璇嶃€乵ethod銆佽€楁椂 |
| **Dense Retrieval** | 杩斿洖鐨?Top-N 鍊欓€夊強鐩镐技搴﹀垎鏁般€乸rovider銆佽€楁椂 |
| **Sparse Retrieval** | 杩斿洖鐨?Top-N 鍊欓€夊強 BM25 鍒嗘暟銆乵ethod銆佽€楁椂 |
| **Fusion** | 铻嶅悎鍚庣殑缁熶竴鎺掑悕銆乤lgorithm銆佽€楁椂 |
| **Rerank** | 閲嶆帓鍚庣殑鏈€缁堟帓鍚嶅強鍒嗘暟銆乥ackend銆佹槸鍚﹁Е鍙?Fallback銆佽€楁椂 |

**姹囨€绘寚鏍?*锛?
- `total_latency`锛氱鍒扮鎬昏€楁椂
- `top_k_results`锛氭渶缁堣繑鍥炵殑 Top-K 鏂囨。 ID
- `error`锛氬紓甯镐俊鎭紙鑻ユ湁锛?

**璇勪及鎸囨爣 (Evaluation Metrics)**锛?
- `context_relevance`锛氬彫鍥炴枃妗ｄ笌 Query 鐨勭浉鍏虫€у垎鏁?
- `answer_faithfulness`锛氱敓鎴愮瓟妗堜笌鍙洖鏂囨。鐨勪竴鑷存€у垎鏁帮紙鑻ユ湁鐢熸垚鐜妭锛?

**B. Ingestion Trace锛堟憚鍙栬拷韪級**

姣忔鏂囨。鎽勫彇鐢熸垚鍞竴鐨?`trace_id`锛岃褰曚粠鏂囦欢鍔犺浇鍒板瓨鍌ㄥ畬鎴愮殑鍏ㄨ繃绋嬶細

**鍩虹淇℃伅**锛?
- `trace_id`锛氭憚鍙栧敮涓€鏍囪瘑
- `trace_type`锛歚"ingestion"`
- `timestamp`锛氭憚鍙栧紑濮嬫椂闂?
- `source_path`锛氭簮鏂囦欢璺緞
- `collection`锛氱洰鏍囬泦鍚堝悕绉?

**鍚勯樁娈佃鎯?(Stages)**锛?

| 闃舵 | 璁板綍鍐呭 |
|-----|---------|
| **Load** | 鏂囦欢澶у皬銆佽В鏋愬櫒锛坢ethod: markitdown锛夈€佹彁鍙栫殑鍥剧墖鏁般€佽€楁椂 |
| **Split** | splitter 绫诲瀷锛坢ethod锛夈€佷骇鍑?chunk 鏁般€佸钩鍧?chunk 闀垮害銆佽€楁椂 |
| **Transform** | 鍚?transform 鍚嶇О涓庡鐞嗚鎯咃紙refined/enriched/captioned 鏁伴噺锛夈€丩LM provider銆佽€楁椂 |
| **Embed** | embedding provider銆乥atch 鏁般€佸悜閲忕淮搴︺€乨ense + sparse 缂栫爜鑰楁椂 |
| **Upsert** | 瀛樺偍鍚庣锛坢ethod: chroma锛夈€乽psert 鏁伴噺銆丅M25 绱㈠紩鏇存柊銆佸浘鐗囧瓨鍌ㄣ€佽€楁椂 |

**姹囨€绘寚鏍?*锛?
- `total_latency`锛氱鍒扮鎬昏€楁椂
- `total_chunks`锛氭渶缁堝瓨鍌ㄧ殑 chunk 鏁伴噺
- `total_images`锛氬鐞嗙殑鍥剧墖鏁伴噺
- `skipped`锛氳烦杩囩殑鏂囦欢/chunk 鏁帮紙宸插瓨鍦ㄣ€佹湭鍙樻洿绛夛級
- `error`锛氬紓甯镐俊鎭紙鑻ユ湁锛?


#### 3.4.3 鎶€鏈柟妗堬細缁撴瀯鍖栨棩蹇?+ 鏈湴 Web Dashboard

鏈」鐩噰鐢?**"缁撴瀯鍖栨棩蹇?+ 鏈湴 Web Dashboard"** 浣滀负鍙娴嬫€х殑瀹炵幇鏂规銆?

**閫夊瀷鐞嗙敱**锛?
- **闆跺閮ㄤ緷璧?*锛氫笉渚濊禆 LangSmith銆丩angFuse 绛夌涓夋柟骞冲彴锛屾棤闇€缃戠粶杩炴帴涓庤处鍙锋敞鍐岋紝瀹屽叏鏈湴鍖栬繍琛屻€?
- **杞婚噺鏄撻儴缃?*锛氫粎闇€ Python 鏍囧噯搴?+ 涓€涓交閲?Web 妗嗘灦锛堝 Streamlit锛夛紝`pip install` 鍗冲彲浣跨敤锛屾棤闇€ Docker 鎴栨暟鎹簱鏈嶅姟銆?
- **瀛︿範鎴愭湰浣?*锛氱粨鏋勫寲鏃ュ織鏄€氱敤鎶€鑳斤紝璋冭瘯鏃跺彲鐩存帴鐢?`jq`銆乣grep` 绛夊懡浠よ宸ュ叿鏌ヨ锛汥ashboard 浠ｇ爜绠€鍗曠洿瑙傦紝渚夸簬鐞嗚В涓庝簩娆″紑鍙戙€?
- **濂戝悎椤圭洰瀹氫綅**锛氭湰椤圭洰闈㈠悜鏈湴 MCP Server 鍦烘櫙锛屽崟鐢ㄦ埛銆佸崟鏈鸿繍琛岋紝鏃犻渶鍒嗗竷寮忚拷韪垨澶氱鎴烽殧绂荤瓑浼佷笟绾ц兘鍔涖€?

**瀹炵幇鏋舵瀯**锛?

```
RAG Pipeline
    鈹?
    鈻?
Trace Collector (瑁呴グ鍣?鍥炶皟)
    鈹?
    鈻?
JSON Lines 鏃ュ織鏂囦欢 (logs/traces.jsonl)
    鈹?
    鈻?
鏈湴 Web Dashboard (Streamlit)
    鈹?
    鈻?
鎸?trace_id 鏌ョ湅鍚勯樁娈佃鎯呬笌鎬ц兘鎸囨爣
```

**鏍稿績缁勪欢**锛?
- **缁撴瀯鍖栨棩蹇楀眰**锛氬熀浜?Python `logging` + JSON Formatter锛屽皢姣忔璇锋眰鐨?Trace 鏁版嵁浠?JSON Lines 鏍煎紡杩藉姞鍐欏叆鏈湴鏂囦欢銆傛瘡琛屼竴鏉″畬鏁寸殑璇锋眰璁板綍锛屽寘鍚?`trace_id`銆佸悇闃舵璇︽儏涓庤€楁椂銆?
- **鏈湴 Web Dashboard**锛氬熀浜?Streamlit 鏋勫缓鐨勮交閲忕骇 Web UI锛岃鍙栨棩蹇楁枃浠跺苟鎻愪緵浜や簰寮忓彲瑙嗗寲銆傛牳蹇冨姛鑳芥槸鎸?`trace_id` 妫€绱㈠苟灞曠ず鍗曟璇锋眰鐨勫畬鏁磋拷韪摼璺€?

#### 3.4.4 杩借釜鏈哄埗瀹炵幇

涓虹‘淇濆悇 RAG 闃舵锛堝彲鏇挎崲銆佸彲鑷畾涔夛級閮借兘杈撳嚭缁熶竴鏍煎紡鐨勮拷韪棩蹇楋紝绯荤粺閲囩敤 **TraceContext锛堣拷韪笂涓嬫枃锛?* 浣滀负鏍稿績鏈哄埗銆?

**宸ヤ綔鍘熺悊**锛?

1. **璇锋眰寮€濮?*锛歅ipeline 鍏ュ彛鍒涘缓涓€涓?`TraceContext` 瀹炰緥锛岀敓鎴愬敮涓€ `trace_id`锛岃褰曡姹傚熀纭€淇℃伅锛圦uery銆丆ollection 绛夛級銆?

2. **闃舵璁板綍**锛歚TraceContext` 鎻愪緵 `record_stage()` 鏂规硶锛屽悇闃舵鎵ц瀹屾瘯鍚庤皟鐢ㄨ鏂规硶锛屼紶鍏ラ樁娈靛悕绉般€佽€楁椂銆佽緭鍏ヨ緭鍑虹瓑鏁版嵁銆?

3. **璇锋眰缁撴潫**锛氳皟鐢?`trace.finish()`锛宍TraceContext` 灏嗘敹闆嗙殑瀹屾暣鏁版嵁搴忓垪鍖栦负 JSON锛岃拷鍔犲啓鍏ユ棩蹇楁枃浠躲€?

**涓庡彲鎻掓嫈缁勪欢鐨勯厤鍚?*锛?
- 鍚勯樁娈电粍浠讹紙Retriever銆丷eranker 绛夛級鐨勬帴鍙ｇ害瀹氫腑鍖呭惈 `TraceContext` 鍙傛暟銆?
- 缁勪欢瀹炵幇鑰呭湪鎵ц鏍稿績閫昏緫鍚庯紝璋冪敤 `trace.record_stage()` 璁板綍鏈樁娈电殑鍏抽敭淇℃伅銆?
- 杩欐槸**鏄惧紡璋冪敤**妯″紡锛氫笉寮哄埗銆佷笉浼氬洜鏈皟鐢ㄨ€屾姤閿欙紝浣嗕緷璧栧紑鍙戣€呬富鍔ㄨ褰曘€傚ソ澶勬槸浠ｇ爜閫忔槑锛屽紑鍙戣€呮竻妤氱煡閬撳摢浜涙暟鎹璁板綍锛涗唬浠锋槸闇€瑕佸紑鍙戣€呰嚜瑙夐伒瀹堢害瀹氥€?

**闃舵鍒掑垎鍘熷垯**锛?
- **Stage 鏄浐瀹氱殑閫氱敤澶х被**锛歚retrieval`锛堟绱級銆乣rerank`锛堥噸鎺掞級銆乣generation`锛堢敓鎴愶級绛夛紝涓嶉殢鍏蜂綋瀹炵幇鏂规鍙樺寲銆?
- **鍏蜂綋瀹炵幇鏄樁娈靛唴閮ㄧ殑缁嗚妭**锛氬湪 `record_stage()` 涓€氳繃 `method` 瀛楁璁板綍閲囩敤鐨勫叿浣撴柟娉曪紙濡?`bm25`銆乣hybrid`锛夛紝閫氳繃 `details` 瀛楁璁板綍鏂规硶鐩稿叧鐨勭粏鑺傛暟鎹€?
- 杩欐牱鏃犺搴曞眰鏂规鎬庝箞鏇挎崲锛岄樁娈电粨鏋勪繚鎸佺ǔ瀹氾紝Dashboard 灞曠ず閫昏緫鏃犻渶璋冩暣銆?

#### 3.4.5 Dashboard 鍔熻兘璁捐锛堝叚椤甸潰鏋舵瀯锛?

Dashboard 鍩轰簬 Streamlit 鏋勫缓澶氶〉闈㈠簲鐢紙`st.navigation`锛夛紝鎻愪緵鍏ぇ鍔熻兘椤甸潰锛?

**椤甸潰 1锛氱郴缁熸€昏 (Overview)**
- **缁勪欢閰嶇疆鍗＄墖**锛氳鍙?`Settings`锛屽睍绀哄綋鍓嶅彲鎻掓嫈缁勪欢鐨勯厤缃姸鎬侊細
    - LLM锛歱rovider + model锛堝 `azure / gpt-4o`锛?
    - Embedding锛歱rovider + model + 缁村害
    - Splitter锛氱被鍨?+ chunk_size + overlap
    - Reranker锛歜ackend + model锛堟垨 None锛?
    - Evaluator锛氬凡鍚敤鐨?backends 鍒楄〃
- **鏁版嵁璧勪骇缁熻**锛氳皟鐢?`DocumentManager.get_collection_stats()` 灞曠ず鍚勯泦鍚堢殑鏂囨。鏁般€乧hunk 鏁般€佸浘鐗囨暟銆?
- **绯荤粺鍋ュ悍鎸囨爣**锛氭渶杩戜竴娆?Ingestion/Query trace 鐨勬椂闂翠笌鑰楁椂銆?

**椤甸潰 2锛氭暟鎹祻瑙堝櫒 (Data Browser)**
- **鏂囨。鍒楄〃瑙嗗浘**锛氬睍绀哄凡鎽勫叆鐨勬枃妗ｏ紙source_path銆侀泦鍚堛€乧hunk 鏁般€佹憚鍏ユ椂闂达級锛屾敮鎸佹寜闆嗗悎绛涢€変笌鍏抽敭璇嶆悳绱€?
- **Chunk 璇︽儏瑙嗗浘**锛氱偣鍑绘枃妗ｅ睍寮€鍏舵墍鏈?chunk锛屾瘡涓?chunk 鏄剧ず锛?
    - 鍘熸枃鍐呭锛堝彲鎶樺彔闀挎枃鏈級
    - Metadata 鍚勫瓧娈碉紙title銆乻ummary銆乼ags銆乸age銆乮mage_refs 绛夛級
    - 鍏宠仈鍥剧墖棰勮锛堜粠 ImageStorage 璇诲彇骞跺睍绀虹缉鐣ュ浘锛?
- **鏁版嵁鏉ユ簮**锛氶€氳繃 `ChromaStore.get_all()` 鎴?`get_by_metadata()` 璇诲彇 chunk 鏁版嵁銆?

**椤甸潰 3锛欼ngestion 绠＄悊 (Ingestion Manager)**
- **鏂囦欢閫夋嫨涓庢憚鍙栬Е鍙?*锛?
    - 鏂囦欢涓婁紶缁勪欢锛坄st.file_uploader`锛夋垨鐩綍璺緞杈撳叆
    - 閫夋嫨鐩爣闆嗗悎锛堜笅鎷夐€夋嫨鎴栨柊寤猴級
    - 鐐瑰嚮"寮€濮嬫憚鍙?鎸夐挳瑙﹀彂 `IngestionPipeline.run()`
    - 鍒╃敤 `on_progress` 鍥炶皟椹卞姩 Streamlit 杩涘害鏉★紙`st.progress`锛夛紝瀹炴椂鏄剧ず褰撳墠闃舵涓庡鐞嗚繘搴?
- **鏂囨。鍒犻櫎**锛?
    - 鍦ㄦ枃妗ｅ垪琛ㄤ腑鎻愪緵"鍒犻櫎"鎸夐挳
    - 璋冪敤 `DocumentManager.delete_document()` 鍗忚皟璺ㄥ瓨鍌ㄥ垹闄?
    - 鍒犻櫎瀹屾垚鍚庡埛鏂板垪琛?
- **娉ㄦ剰**锛歅ipeline 鎵ц涓哄悓姝ラ樆濉炴搷浣滐紝Streamlit 鐨?rerun 鏈哄埗澶╃劧鏀寔锛堣繘搴︽潯鍦ㄥ悓涓€ request 涓洿鏂帮級銆?

**椤甸潰 4锛欼ngestion 杩借釜 (Ingestion Traces)**
- **鎽勫彇鍘嗗彶鍒楄〃**锛氭寜鏃堕棿鍊掑簭灞曠ず `trace_type == "ingestion"` 鐨勫巻鍙茶褰曪紝鏄剧ず鏂囦欢鍚嶃€侀泦鍚堛€佹€昏€楁椂銆佺姸鎬侊紙鎴愬姛/澶辫触锛夈€?
- **鍗曟鎽勫彇璇︽儏**锛?
    - **闃舵鑰楁椂鐎戝竷鍥?*锛氭í鍚戞潯褰㈠浘灞曠ず load/split/transform/embed/upsert 鍚勯樁娈垫椂闂村垎甯冦€?
    - **澶勭悊缁熻**锛歝hunk 鏁般€佸浘鐗囨暟銆佽烦杩囨暟銆佸け璐ユ暟銆?
    - **鍚勯樁娈佃鎯呭睍寮€**锛氱偣鍑绘煡鐪?method/provider銆佽緭鍏ヨ緭鍑烘牱鏈€?

**椤甸潰 5锛歈uery 杩借釜 (Query Traces)**
- **鏌ヨ鍘嗗彶鍒楄〃**锛氭寜鏃堕棿鍊掑簭灞曠ず `trace_type == "query"` 鐨勫巻鍙茶褰曪紝鏀寔鎸?Query 鍏抽敭璇嶇瓫閫夈€?
- **鍗曟鏌ヨ璇︽儏**锛?
    - **鑰楁椂鐎戝竷鍥?*锛氬睍绀?query_processing/dense/sparse/fusion/rerank 鍚勯樁娈垫椂闂村垎甯冦€?
    - **Dense vs Sparse 瀵规瘮**锛氬苟鍒楀睍绀轰袱璺彫鍥炵粨鏋滅殑 Top-N 鏂囨。 ID 涓庡垎鏁般€?
    - **Rerank 鍓嶅悗瀵规瘮**锛氬睍绀鸿瀺鍚堟帓鍚嶄笌绮炬帓鍚庢帓鍚嶇殑鍙樺寲锛堟帓鍚嶈穬鍗?涓嬮檷鏍囪锛夈€?
    - **鏈€缁堢粨鏋滆〃**锛氬睍绀?Top-K 鍊欓€夋枃妗ｇ殑鏍囬銆佸垎鏁般€佹潵婧愩€?

**椤甸潰 6锛氳瘎浼伴潰鏉?(Evaluation Panel)**
- **璇勪及杩愯**锛氶€夋嫨璇勪及鍚庣锛圧agas / Custom / All锛変笌 golden test set锛岀偣鍑昏繍琛屻€?
- **鎸囨爣灞曠ず**锛氫互琛ㄦ牸鍜屽浘琛ㄥ睍绀?hit_rate銆乵rr銆乫aithfulness 绛夋寚鏍囥€?
- **鍘嗗彶瓒嬪娍**锛氬姣斾笉鍚屾椂闂寸殑璇勪及缁撴灉锛岃瀵熺瓥鐣ヨ皟鏁寸殑鏁堟灉銆?
- **娉ㄦ剰**锛氳瘎浼伴潰鏉垮湪 Phase H 瀹炵幇锛孭hase G 瀹屾垚鍚庤椤甸潰鏄剧ず"璇勪及妯″潡灏氭湭鍚敤"鐨勫崰浣嶆彁绀恒€?

**Dashboard 鎶€鏈灦鏋?*锛?

```
src/observability/dashboard/
鈹溾攢鈹€ app.py                    # Streamlit 鍏ュ彛锛岄〉闈㈠鑸敞鍐?
鈹溾攢鈹€ pages/
鈹?  鈹溾攢鈹€ overview.py           # 椤甸潰 1锛氱郴缁熸€昏
鈹?  鈹溾攢鈹€ data_browser.py       # 椤甸潰 2锛氭暟鎹祻瑙堝櫒
鈹?  鈹溾攢鈹€ ingestion_manager.py  # 椤甸潰 3锛欼ngestion 绠＄悊
鈹?  鈹溾攢鈹€ ingestion_traces.py   # 椤甸潰 4锛欼ngestion 杩借釜
鈹?  鈹溾攢鈹€ query_traces.py       # 椤甸潰 5锛歈uery 杩借釜
鈹?  鈹斺攢鈹€ evaluation_panel.py   # 椤甸潰 6锛氳瘎浼伴潰鏉?
鈹斺攢鈹€ services/
    鈹溾攢鈹€ trace_service.py      # Trace 鏁版嵁璇诲彇鏈嶅姟锛堣В鏋?traces.jsonl锛?
    鈹溾攢鈹€ data_service.py       # 鏁版嵁娴忚鏈嶅姟锛堝皝瑁?ChromaStore/ImageStorage 璇诲彇锛?
    鈹斺攢鈹€ config_service.py     # 閰嶇疆璇诲彇鏈嶅姟锛堝皝瑁?Settings 璇诲彇涓庡睍绀猴級
```

**Dashboard 涓?Trace 鐨勬暟鎹叧绯?*锛?
- Dashboard 椤甸潰 4/5 璇诲彇 `logs/traces.jsonl`锛堥€氳繃 `TraceService`锛夛紝鎸?`trace_type` 鍒嗙被灞曠ず銆?
- Dashboard 椤甸潰 1/2/3 鐩存帴璇诲彇瀛樺偍灞傦紙閫氳繃 `DataService` 灏佽 ChromaStore/ImageStorage/FileIntegrity锛夛紝涓嶄緷璧?Trace銆?
- 鎵€鏈夐〉闈㈠熀浜?Trace 涓?`method`/`provider` 瀛楁鍔ㄦ€佹覆鏌撴爣绛撅紝鏇存崲缁勪欢鍚庤嚜鍔ㄩ€傞厤銆?


#### 3.4.6 閰嶇疆绀轰緥

```yaml
observability:
  enabled: true
  
  # 鏃ュ織閰嶇疆
  logging:
    log_file: logs/traces.jsonl  # JSON Lines 鏍煎紡鏃ュ織鏂囦欢
    log_level: INFO  # DEBUG | INFO | WARNING
  
  # 杩借釜绮掑害鎺у埗
  detail_level: standard  # minimal | standard | verbose

# Dashboard 绠＄悊骞冲彴閰嶇疆
dashboard:
  enabled: true
  port: 8501                     # Streamlit 鏈嶅姟绔彛
  traces_dir: ./logs             # Trace 鏃ュ織鏂囦欢鐩綍
  auto_refresh: true             # 鏄惁鑷姩鍒锋柊锛堣疆璇㈡柊 trace锛?
  refresh_interval: 5            # 鑷姩鍒锋柊闂撮殧锛堢锛?
```


### 3.5 澶氭ā鎬佸浘鐗囧鐞嗚璁?(Multimodal Image Processing Design)

**鐩爣锛?* 璁捐涓€濂楀畬鏁寸殑鍥剧墖澶勭悊鏂规锛屼娇 RAG 绯荤粺鑳藉鐞嗚В銆佺储寮曞苟妫€绱㈡枃妗ｄ腑鐨勫浘鐗囧唴瀹癸紝瀹炵幇"鐢ㄨ嚜鐒惰瑷€鎼滅储鍥剧墖"鐨勮兘鍔涳紝鍚屾椂淇濇寔鏋舵瀯鐨勭畝娲佹€т笌鍙墿灞曟€с€?

#### 3.5.1 璁捐鐞嗗康涓庣瓥鐣ラ€夊瀷

澶氭ā鎬?RAG 鐨勬牳蹇冩寫鎴樺湪浜庯細**濡備綍璁╃函鏂囨湰鐨勬绱㈢郴缁?鐪嬫噦"鍥剧墖**銆備笟鐣屼富瑕佹湁涓ょ鎶€鏈矾绾匡細

| 绛栫暐 | 鏍稿績鎬濊矾 | 浼樺娍 | 鍔ｅ娍 |
|-----|---------|------|------|
| **Image-to-Text (鍥捐浆鏂?** | 鍒╃敤 Vision LLM 灏嗗浘鐗囪浆鍖栦负鏂囨湰鎻忚堪锛屽鐢ㄧ函鏂囨湰 RAG 閾捐矾 | 鏋舵瀯缁熶竴銆佸疄鐜扮畝鍗曘€佹垚鏈彲鎺?| 鎻忚堪璐ㄩ噺渚濊禆 LLM 鑳藉姏锛屽彲鑳戒涪澶辫瑙夌粏鑺?|
| **Multi-Embedding (澶氭ā鎬佸悜閲?** | 浣跨敤 CLIP 绛夋ā鍨嬪皢鍥炬枃缁熶竴鏄犲皠鍒板悓涓€鍚戦噺绌洪棿 | 淇濈暀鍘熷瑙嗚鐗瑰緛锛屾敮鎸佸浘鎼滃浘 | 闇€寮曞叆棰濆鍚戦噺搴擄紝鏋舵瀯澶嶆潅搴﹂珮 |

**鏈」鐩€夊瀷锛欼mage-to-Text锛堝浘杞枃锛夌瓥鐣?*

閫夊瀷鐞嗙敱锛?
- **鏋舵瀯缁熶竴**锛氭棤闇€寮曞叆 CLIP 绛夊妯℃€?Embedding 妯″瀷锛屾棤闇€缁存姢鐙珛鐨勫浘鍍忓悜閲忓簱锛屽畬鍏ㄥ鐢ㄧ幇鏈夌殑鏂囨湰 RAG 閾捐矾锛圛ngestion 鈫?Hybrid Search 鈫?Rerank锛夈€?
- **璇箟瀵归綈**锛氶€氳繃 LLM 灏嗗浘鐗囩殑瑙嗚淇℃伅杞寲涓鸿嚜鐒惰瑷€鎻忚堪锛屽ぉ鐒朵笌鐢ㄦ埛鐨勬枃鏈煡璇㈠湪鍚屼竴璇箟绌洪棿锛屾绱㈡晥鏋滃彲棰勬湡銆?
- **鎴愭湰鍙帶**锛氫粎鍦ㄦ暟鎹憚鍙栭樁娈典竴娆℃€ц皟鐢?Vision LLM锛屾绱㈤樁娈垫棤棰濆鎴愭湰銆?
- **娓愯繘澧炲己**锛氭湭鏉ュ闇€鏀寔"鍥炬悳鍥?绛夐珮绾ц兘鍔涳紝鍙湪姝ゅ熀纭€涓婂彔鍔?CLIP Embedding锛屾棤闇€閲嶆瀯鏍稿績閾捐矾銆?

#### 3.5.2 鍥剧墖澶勭悊鍏ㄦ祦绋嬭璁?

鍥剧墖澶勭悊璐┛ Ingestion Pipeline 鐨勫涓樁娈碉紝鏁翠綋娴佺▼濡備笅锛?

```
鍘熷鏂囨。 (PDF/PPT/Markdown)
    鈹?
    鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹? Loader 闃舵锛氬浘鐗囨彁鍙栦笌寮曠敤鏀堕泦                           鈹?
鈹? - 瑙ｆ瀽鏂囨。锛岃瘑鍒苟鎻愬彇宓屽叆鐨勫浘鐗囪祫婧?                       鈹?
鈹? - 涓烘瘡寮犲浘鐗囩敓鎴愬敮涓€鏍囪瘑 (image_id)                       鈹?
鈹? - 鍦ㄦ枃妗ｆ枃鏈腑鎻掑叆鍥剧墖鍗犱綅绗?寮曠敤鏍囪                       鈹?
鈹? - 杈撳嚭锛欴ocument (text + metadata.images[])             鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
    鈹?
    鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹? Splitter 闃舵锛氫繚鎸佸浘鏂囧叧鑱?                              鈹?
鈹? - 鍒囧垎鏃朵繚鐣欏浘鐗囧紩鐢ㄦ爣璁板湪瀵瑰簲 Chunk 涓?                    鈹?
鈹? - 纭繚鍥剧墖涓庡叾涓婁笅鏂囨钀戒繚鎸佸叧鑱?                           鈹?
鈹? - 杈撳嚭锛欳hunks (鍚勮嚜鎼哄甫鍏宠仈鐨?image_refs)                鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
    鈹?
    鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹? Transform 闃舵锛氬浘鐗囩悊瑙ｄ笌鎻忚堪鐢熸垚                         鈹?
鈹? - 璋冪敤 Vision LLM 瀵规瘡寮犲浘鐗囩敓鎴愮粨鏋勫寲鎻忚堪                  鈹?
鈹? - 灏嗘弿杩版枃鏈敞鍏ュ埌鍏宠仈 Chunk 鐨勬鏂囨垨 Metadata 涓?          鈹?
鈹? - 杈撳嚭锛欵nriched Chunks (鍚浘鐗囪涔変俊鎭?                  鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
    鈹?
    鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹? Storage 闃舵锛氬弻杞ㄥ瓨鍌?                                   鈹?
鈹? - 鍚戦噺搴擄細瀛樺偍澧炲己鍚庣殑 Chunk (鍚浘鐗囨弿杩? 鐢ㄤ簬妫€绱?          鈹?
鈹? - 鏂囦欢绯荤粺/Blob锛氬瓨鍌ㄥ師濮嬪浘鐗囨枃浠剁敤浜庤繑鍥炲睍绀?               鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
```

#### 3.5.3 鍚勯樁娈垫妧鏈鐐?

**1. Loader 闃舵锛氬浘鐗囨彁鍙栦笌寮曠敤鏀堕泦**

- **鎻愬彇绛栫暐**锛?
  - 瑙ｆ瀽鏂囨。鏃惰瘑鍒祵鍏ョ殑鍥剧墖璧勬簮锛圥DF 涓殑 XObject銆丳PT 涓殑濯掍綋鏂囦欢銆丮arkdown 涓殑 `![]()` 寮曠敤锛夈€?
  - 涓烘瘡寮犲浘鐗囩敓鎴愬叏灞€鍞竴鐨?`image_id`锛堝缓璁牸寮忥細`{doc_hash}_{page}_{seq}`锛夈€?
  - 灏嗗浘鐗囦簩杩涘埗鏁版嵁鎻愬彇骞舵殏瀛橈紝璁板綍鍏跺湪鍘熸枃妗ｄ腑鐨勪綅缃俊鎭€?

- **寮曠敤鏍囪**锛?
  - 鍦ㄨ浆鎹㈠悗鐨?Markdown 鏂囨湰涓紝浜庡浘鐗囧師濮嬩綅缃彃鍏ュ崰浣嶇锛堝 `[IMAGE: {image_id}]`锛夈€?
  - 鍦?Document 鐨?Metadata 涓淮鎶?`images` 鍒楄〃锛岃褰曟瘡寮犲浘鐗囩殑 `image_id`銆佸師濮嬭矾寰勩€侀〉鐮併€佸昂瀵哥瓑鍩虹淇℃伅銆?

- **瀛樺偍鍘熷鍥剧墖**锛?
  - 灏嗘彁鍙栫殑鍥剧墖淇濆瓨鑷虫湰鍦版枃浠剁郴缁熺殑绾﹀畾鐩綍锛堝 `data/images/{collection}/{image_id}.png`锛夈€?
  - 浠呬繚瀛橀渶瑕佺殑鍥剧墖鏍煎紡锛堟帹鑽愮粺涓€杞崲涓?PNG/JPEG锛夛紝鎺у埗瀛樺偍浣撶Н銆?

**2. Splitter 闃舵锛氫繚鎸佸浘鏂囧叧鑱?*

- **鍏宠仈淇濇寔鍘熷垯**锛?
  - 鍥剧墖寮曠敤鏍囪搴斾笌鍏惰鏄庢€ф枃瀛楋紙Caption銆佸墠鍚庢钀斤級灏介噺淇濇寔鍦ㄥ悓涓€ Chunk 涓€?
  - 鑻ュ浘鐗囧嚭鐜板湪绔犺妭寮€澶存垨缁撳熬锛屽垏鍒嗘椂搴斿皢鍏跺綊鍏ヨ涔変笂鏈€鐩稿叧鐨?Chunk銆?

- **Chunk Metadata 鎵╁睍**锛?
  - 姣忎釜 Chunk 鐨?Metadata 涓鍔?`image_refs: List[image_id]` 瀛楁锛岃褰曡 Chunk 鍏宠仈鐨勫浘鐗囧垪琛ㄣ€?
  - 姝ゅ瓧娈电敤浜庡悗缁?Transform 闃舵瀹氫綅闇€瑕佸鐞嗙殑鍥剧墖锛屼互鍙婃绱㈠懡涓悗瀹氫綅闇€瑕佽繑鍥炵殑鍥剧墖銆?

**3. Transform 闃舵锛氬浘鐗囩悊瑙ｄ笌鎻忚堪鐢熸垚**

杩欐槸澶氭ā鎬佸鐞嗙殑鏍稿績鐜妭锛岃礋璐ｅ皢瑙嗚淇℃伅杞寲涓哄彲妫€绱㈢殑鏂囨湰璇箟銆?

- **Vision LLM 閫夊瀷**锛?

| 妯″瀷 | 鎻愪緵鍟?| 鐗圭偣 | 閫傜敤鍦烘櫙 | 鎺ㄨ崘鎸囨暟 |
|-----|--------|------|---------|---------|
| **GPT-4o** | OpenAI / Azure | 鐞嗚В鑳藉姏寮猴紝鏀寔澶嶆潅鍥捐〃瑙ｈ锛岃嫳鏂囨枃妗ｈ〃鐜颁紭寮?| 楂樿川閲忛渶姹傘€佸鏉備笟鍔℃枃妗ｃ€佸浗闄呭寲鍦烘櫙 | 猸愨瓙猸愨瓙猸?|
| **Qwen-VL-Max** | 闃块噷浜?(DashScope) | 涓枃鐞嗚В鑳藉姏鍑鸿壊锛屾€т环姣旈珮锛屽涓枃鍥捐〃/鏂囨。鏀寔濂?| 涓枃鏂囨。銆佸浗鍐呴儴缃层€佹垚鏈晱鎰熷満鏅?| 猸愨瓙猸愨瓙猸?|
| **Qwen-VL-Plus** | 闃块噷浜?(DashScope) | 閫熷害鏇村揩锛屾垚鏈洿浣庯紝閫傚悎澶ф壒閲忓鐞?| 澶ф壒閲忎腑鏂囨枃妗ｃ€佸揩閫熻凯浠ｅ満鏅?| 猸愨瓙猸愨瓙 |
| **Claude 3.5 Sonnet** | Anthropic | 澶氭ā鎬佸師鐢熸敮鎸侊紝闀夸笂涓嬫枃 | 闇€瑕佺粨鍚堝ぇ娈垫枃瀛楃悊瑙ｅ浘鐗?| 猸愨瓙猸愨瓙 |
| **Gemini Pro Vision** | Google | 鎴愭湰杈冧綆锛岄€熷害杈冨揩 | 澶ф壒閲忓鐞嗐€佹垚鏈晱鎰熷満鏅?| 猸愨瓙猸?|
| **GLM-4V** | 鏅鸿氨 AI (ZhipuAI) | 鍥藉唴鑰佺墝锛岀ǔ瀹氭€уソ锛屼腑鏂囨敮鎸佷匠 | 鍥藉唴閮ㄧ讲澶囬€夈€佷紒涓氱骇搴旂敤 | 猸愨瓙猸愨瓙 |

**鍙屾ā鍨嬮€夊瀷绛栫暐锛堟帹鑽愶級**锛?

鏈」鐩噰鐢?*鍥藉唴 + 鍥藉鍙屾ā鍨?*鏂规锛岄€氳繃閰嶇疆鍒囨崲锛屽吋椤句笉鍚岄儴缃茬幆澧冨拰鏂囨。绫诲瀷锛?

| 閮ㄧ讲鐜 | 涓婚€夋ā鍨?| 澶囬€夋ā鍨?| 璇存槑 |
|---------|---------|---------|------|
| **鍥介檯鍖?/ Azure 鐜** | GPT-4o (Azure) | Qwen-VL-Max | 鑻辨枃鏂囨。浼樺厛鐢?GPT-4o锛屼腑鏂囨枃妗ｅ彲鍒囨崲 Qwen-VL |
| **鍥藉唴閮ㄧ讲 / 绾腑鏂囧満鏅?* | Qwen-VL-Max | GPT-4o | 涓枃鍥捐〃鐞嗚В鐢?Qwen-VL锛岀壒娈婇渶姹傚彲鍒囨崲 GPT-4o |
| **鎴愭湰鏁忔劅 / 澶ф壒閲?* | Qwen-VL-Plus | Gemini Pro Vision | 鐗虹壊閮ㄥ垎璐ㄩ噺鎹㈠彇閫熷害鍜屾垚鏈?|

**閫夊瀷鐞嗙敱**锛?

1. **GPT-4o (鍥藉棣栭€?**锛?
   - 瑙嗚鐞嗚В鑳藉姏涓氱晫棰嗗厛锛屽鏉傚浘琛ㄨВ璇诲噯纭巼楂?
   - Azure 閮ㄧ讲鍙弧瓒充紒涓氬悎瑙勮姹?
   - 鑻辨枃鎶€鏈枃妗ｇ悊瑙ｆ晥鏋滄渶浣?

2. **Qwen-VL-Max (鍥藉唴棣栭€?**锛?
   - 涓枃鍦烘櫙涓嬭〃鐜颁笌 GPT-4o 鎺ヨ繎锛岄儴鍒嗕腑鏂囧浘琛ㄤ换鍔＄敋鑷虫洿浼?
   - 閫氳繃闃块噷浜?DashScope API 璋冪敤锛屽浗鍐呰闂ǔ瀹氥€佸欢杩熶綆
   - 浠锋牸绾︿负 GPT-4o 鐨?1/3 ~ 1/5锛屾€т环姣旀瀬楂?
   - 鍘熺敓鏀寔涓枃 OCR锛屽涓枃鎴浘銆佽〃鏍艰瘑鍒洿鍑嗙‘

- **鎻忚堪鐢熸垚绛栫暐**锛?
  - **缁撴瀯鍖?Prompt**锛氳璁′笓鐢ㄧ殑鍥剧墖鐞嗚В Prompt锛屽紩瀵?LLM 杈撳嚭缁撴瀯鍖栨弿杩帮紝鑰岄潪鑷敱鍙戞尌銆?
  - **涓婁笅鏂囨劅鐭?*锛氬皢鍥剧墖鐨勫墠鍚庢枃鏈钀戒竴骞朵紶鍏?Vision LLM锛屽府鍔╁叾鐞嗚В鍥剧墖鍦ㄦ枃妗ｄ腑鐨勮澧冧笌浣滅敤銆?
  - **鍒嗙被鍨嬪鐞?*锛氶拡瀵逛笉鍚岀被鍨嬬殑鍥剧墖閲囩敤宸紓鍖栫殑鐞嗚В绛栫暐锛?

| 鍥剧墖绫诲瀷 | 鐞嗚В閲嶇偣 | Prompt 寮曞鏂瑰悜 |
|---------|---------|----------------|
| **娴佺▼鍥?鏋舵瀯鍥?* | 鑺傜偣銆佽繛鎺ュ叧绯汇€佹祦绋嬮€昏緫 | "鎻忚堪杩欏紶鍥剧殑缁撴瀯鍜屾祦绋嬫楠? |
| **鏁版嵁鍥捐〃** | 鏁版嵁瓒嬪娍銆佸叧閿暟鍊笺€佸姣斿叧绯?| "鎻愬彇鍥捐〃涓殑鍏抽敭鏁版嵁鍜岀粨璁? |
| **鎴浘/UI** | 鐣岄潰鍏冪礌銆佹搷浣滄寚寮曘€佺姸鎬佷俊鎭?| "鎻忚堪鎴浘涓殑鐣岄潰鍐呭鍜屽叧閿俊鎭? |
| **鐓х墖/鎻掑浘** | 涓讳綋瀵硅薄銆佸満鏅€佽瑙夌壒寰?| "鎻忚堪鍥剧墖涓殑涓昏鍐呭" |

- **鎻忚堪娉ㄥ叆鏂瑰紡**锛?
  - **鎺ㄨ崘锛氭敞鍏ユ鏂?*锛氬皢鐢熸垚鐨勬弿杩扮洿鎺ユ浛鎹㈡垨杩藉姞鍒?Chunk 姝ｆ枃涓殑鍥剧墖鍗犱綅绗︿綅缃紝鏍煎紡濡?`[鍥剧墖鎻忚堪: {caption}]`銆傝繖鏍锋弿杩颁細琚?Embedding 瑕嗙洊锛屽彲琚洿鎺ユ绱€?
  - **澶囬€夛細娉ㄥ叆 Metadata**锛氬皢鎻忚堪瀛樺叆 `chunk.metadata.image_captions` 瀛楁銆傞渶纭繚妫€绱㈡椂璇ュ瓧娈典篃琚储寮曘€?

- **骞傜瓑涓庡閲忓鐞?*锛?
  - 涓烘瘡寮犲浘鐗囩殑鎻忚堪璁＄畻鍐呭鍝堝笇锛屽瓨鍏?`processing_cache` 琛ㄣ€?
  - 閲嶅澶勭悊鏃讹紝鑻ュ浘鐗囧唴瀹规湭鍙樹笖 Prompt 鐗堟湰涓€鑷达紝鐩存帴澶嶇敤缂撳瓨鐨勬弿杩帮紝閬垮厤閲嶅璋冪敤 Vision LLM銆?

**4. Storage 闃舵锛氬弻杞ㄥ瓨鍌?*

- **鍚戦噺搴撳瓨鍌紙鐢ㄤ簬妫€绱級**锛?
  - 瀛樺偍澧炲己鍚庣殑 Chunk锛屽叾姝ｆ枃宸插寘鍚浘鐗囨弿杩帮紝Metadata 鍖呭惈 `image_refs` 鍒楄〃銆?
  - 妫€绱㈡椂閫氳繃鏂囨湰鐩镐技搴﹀嵆鍙懡涓寘鍚浉鍏冲浘鐗囨弿杩扮殑 Chunk銆?

- **鍘熷鍥剧墖瀛樺偍锛堢敤浜庤繑鍥烇級**锛?
  - 鍥剧墖鏂囦欢瀛樺偍浜庢湰鍦版枃浠剁郴缁燂紝璺緞璁板綍鍦ㄧ嫭绔嬬殑 `images` 绱㈠紩琛ㄤ腑銆?
  - 绱㈠紩琛ㄥ瓧娈碉細`image_id`, `file_path`, `source_doc`, `page`, `width`, `height`, `mime_type`銆?
  - 妫€绱㈠懡涓悗锛屾牴鎹?Chunk 鐨?`image_refs` 鏌ヨ绱㈠紩琛紝鑾峰彇鍥剧墖鏂囦欢璺緞鐢ㄤ簬杩斿洖銆?

#### 3.5.4 妫€绱笌杩斿洖娴佺▼

褰撶敤鎴锋煡璇㈠懡涓寘鍚浘鐗囩殑 Chunk 鏃讹紝绯荤粺闇€瑕佸皢鍥剧墖涓庢枃鏈竴骞惰繑鍥烇細

```
鐢ㄦ埛鏌ヨ: "绯荤粺鏋舵瀯鏄粈涔堟牱鐨勶紵"
    鈹?
    鈻?
Hybrid Search 鍛戒腑 Chunk锛堟鏂囧惈 "[鍥剧墖鎻忚堪: 绯荤粺閲囩敤涓夊眰鏋舵瀯...]"锛?
    鈹?
    鈻?
浠?Chunk.metadata.image_refs 鑾峰彇鍏宠仈鐨?image_id 鍒楄〃
    鈹?
    鈻?
鏌ヨ images 绱㈠紩琛紝鑾峰彇鍥剧墖鏂囦欢璺緞
    鈹?
    鈻?
璇诲彇鍥剧墖鏂囦欢锛岀紪鐮佷负 Base64
    鈹?
    鈻?
鏋勯€?MCP 鍝嶅簲锛屽寘鍚?TextContent + ImageContent
```

**MCP 鍝嶅簲鏍煎紡**锛?

```json
{
  "content": [
    {
      "type": "text",
      "text": "鏍规嵁鏂囨。锛岀郴缁熸灦鏋勫涓嬶細...\n\n[1] 鏉ユ簮: architecture.pdf, 绗?椤?
    },
    {
      "type": "image",
      "data": "<base64-encoded-image>",
      "mimeType": "image/png"
    }
  ]
}
```

#### 3.5.5 璐ㄩ噺淇濋殰涓庤竟鐣屽鐞?

- **鎻忚堪璐ㄩ噺妫€娴?*锛?
  - 瀵圭敓鎴愮殑鎻忚堪杩涜鍩虹璐ㄩ噺妫€鏌ワ紙闀垮害銆佹槸鍚﹀寘鍚叧閿俊鎭級銆?
  - 鑻ユ弿杩拌繃鐭垨 LLM 杩斿洖"鏃犳硶璇嗗埆"锛屾爣璁拌鍥剧墖涓?`low_quality`锛屽彲閫夋嫨浜哄伐澶嶆牳鎴栬烦杩囩储寮曘€?

- **澶у昂瀵?鐗规畩鍥剧墖澶勭悊**锛?
  - 瓒呭ぇ鍥剧墖鍦ㄤ紶鍏?Vision LLM 鍓嶈繘琛屽帇缂╋紙淇濇寔瀹介珮姣旓紝闄愬埗鏈€澶ц竟闀匡級銆?
  - 瀵逛簬绾楗版€у浘鐗囷紙濡傚垎闅旂嚎銆佽儗鏅浘锛夛紝鍙€氳繃灏哄鎴栦綅缃鍒欒繃婊わ紝涓嶈繘鍏ユ弿杩扮敓鎴愭祦绋嬨€?

- **鎵归噺澶勭悊浼樺寲**锛?
  - 鍥剧墖鎻忚堪鐢熸垚鏀寔鎵归噺寮傛璋冪敤锛屾彁楂樺悶鍚愰噺銆?
  - 鍗曚釜鏂囨。澶勭悊澶辫触鏃讹紝璁板綍澶辫触鐨勫浘鐗?ID锛屼笉褰卞搷鍏朵粬鍥剧墖鐨勫鐞嗚繘搴︺€?

- **闄嶇骇绛栫暐**锛?
  - 褰?Vision LLM 涓嶅彲鐢ㄦ椂锛岀郴缁熷洖閫€鍒?浠呬繚鐣欏浘鐗囧崰浣嶇"妯″紡锛屽浘鐗囦笉鍙備笌妫€绱絾涓嶉樆濉?Ingestion 娴佺▼銆?
  - 鍦?Chunk 涓爣璁?`has_unprocessed_images: true`锛屽悗缁彲澧為噺琛ュ厖鎻忚堪銆?

## 4. 娴嬭瘯鏂规

### 4.1 璁捐鐞嗗康锛氭祴璇曢┍鍔ㄥ紑鍙?(TDD)

鏈」鐩噰鐢?*娴嬭瘯椹卞姩寮€鍙戯紙Test-Driven Development锛?*浣滀负鏍稿績寮€鍙戣寖寮忥紝纭繚姣忎釜缁勪欢鍦ㄥ疄鐜板墠灏卞凡鏄庣‘鍏堕鏈熻涓猴紝閫氳繃鑷姩鍖栨祴璇曟寔缁獙璇佺郴缁熻川閲忋€?

**鏍稿績鍘熷垯**锛?
- **鏃╂祴璇曘€佸父娴嬭瘯**锛氭瘡涓姛鑳芥ā鍧楀疄鐜扮殑鍚屾椂灏辩紪鍐欏搴旂殑鍗曞厓娴嬭瘯锛岃€岄潪浜嬪悗琛ユ祴銆?
- **娴嬭瘯鍗虫枃妗?*锛氭祴璇曠敤渚嬫湰韬氨鏄渶鍑嗙‘鐨勮涓鸿鑼冿紝鏂板姞鍏ョ殑寮€鍙戣€呭彲閫氳繃闃呰娴嬭瘯蹇€熺悊瑙ｅ悇妯″潡鍔熻兘銆?
- **蹇€熷弽棣堝惊鐜?*锛氬崟鍏冩祴璇曞簲鍦ㄧ绾у畬鎴愶紝鏀寔寮€鍙戣€呴珮棰戞墽琛岋紝绔嬪嵆鍙戠幇寮曞叆鐨勯棶棰樸€?
- **鍒嗗眰娴嬭瘯閲戝瓧濉?*锛氬ぇ閲忓揩閫熺殑鍗曞厓娴嬭瘯浣滀负鍩哄骇锛屽皯閲忓叧閿矾寰勭殑闆嗘垚娴嬭瘯浣滀负淇濋殰锛屾瀬灏戞暟绔埌绔祴璇曢獙璇佸畬鏁存祦绋嬨€?

```
        /\
       /E2E\         <- 灏戦噺锛岄獙璇佸叧閿笟鍔℃祦绋?
      /------\
     /Integration\   <- 涓噺锛岄獙璇佹ā鍧楀崗浣?
    /------------\
   /  Unit Tests  \  <- 澶ч噺锛岄獙璇佸崟涓嚱鏁?绫?
  /________________\
```

### 4.2 娴嬭瘯鍒嗗眰绛栫暐

#### 4.2.1 鍗曞厓娴嬭瘯 (Unit Tests)

**鐩爣**锛氶獙璇佹瘡涓嫭绔嬬粍浠剁殑鍐呴儴閫昏緫姝ｇ‘鎬э紝闅旂澶栭儴渚濊禆銆?

**瑕嗙洊鑼冨洿**锛?

| 妯″潡 | 娴嬭瘯閲嶇偣 | 鍏稿瀷娴嬭瘯鐢ㄤ緥 |
|-----|---------|------------|
| **Loader (鏂囨。瑙ｆ瀽鍣?** | 鏍煎紡瑙ｆ瀽銆佸厓鏁版嵁鎻愬彇銆佸浘鐗囧紩鐢ㄦ敹闆?| - 娴嬭瘯瑙ｆ瀽鍗曢〉/澶氶〉 PDF<br>- 楠岃瘉 Markdown 鏍囬灞傜骇鎻愬彇<br>- 妫€鏌ュ浘鐗囧崰浣嶇鎻掑叆浣嶇疆 |
| **Splitter (鍒囧垎鍣?** | 鍒囧垎杈圭晫銆佷笂涓嬫枃淇濈暀銆佸厓鏁版嵁浼犻€?| - 楠岃瘉鎸夋爣棰樺垏鍒嗕笉鐮村潖娈佃惤<br>- 娴嬭瘯瓒呴暱鏂囨湰鐨勯€掑綊鍒囧垎<br>- 妫€鏌?Chunk 鐨?`source` 瀛楁姝ｇ‘鎬?|
| **Transform (澧炲己鍣?** | 鍥剧墖鎻忚堪鐢熸垚銆佸厓鏁版嵁娉ㄥ叆 | - Mock Vision LLM锛岄獙璇佹弿杩版敞鍏ラ€昏緫<br>- 娴嬭瘯鏃犲浘鐗囨椂鐨勯檷绾ц涓?br>- 楠岃瘉骞傜瓑鎬э紙閲嶅澶勭悊鐩稿悓杈撳叆锛?|
| **Embedding (鍚戦噺鍖?** | 鎵瑰鐞嗐€佸樊閲忚绠椼€佸悜閲忕淮搴?| - 楠岃瘉鐩稿悓鏂囨湰鐢熸垚鐩稿悓鍚戦噺<br>- 娴嬭瘯鎵归噺璇锋眰鐨勬媶鍒嗕笌鍚堝苟<br>- 妫€鏌ョ紦瀛樺懡涓€昏緫 |
| **BM25 (绋€鐤忕紪鐮?** | 鍏抽敭璇嶆彁鍙栥€佹潈閲嶈绠?| - 楠岃瘉鍋滅敤璇嶈繃婊?br>- 娴嬭瘯 IDF 璁＄畻鍑嗙‘鎬?br>- 妫€鏌ョ█鐤忓悜閲忔牸寮?|
| **Retrieval (妫€绱㈠櫒)** | 鍙洖绮惧害銆佽瀺鍚堢畻娉?| - 娴嬭瘯绾?Dense/Sparse/Hybrid 涓夌妯″紡<br>- 楠岃瘉 RRF 铻嶅悎鍒嗘暟璁＄畻<br>- 妫€鏌?Top-K 缁撴灉鎺掑簭 |
| **Reranker (閲嶆帓鍣?** | 鍒嗘暟褰掍竴鍖栥€侀檷绾у洖閫€ | - Mock Cross-Encoder锛岄獙璇佸垎鏁伴噸鎺?br>- 娴嬭瘯瓒呮椂鍚庣殑 Fallback 閫昏緫<br>- 楠岃瘉绌哄€欓€夐泦澶勭悊 |

**鎶€鏈€夊瀷**锛?
- **娴嬭瘯妗嗘灦**锛歚pytest`锛圥ython 鏍囧噯閫夋嫨锛屾敮鎸佸弬鏁板寲娴嬭瘯銆丗ixture 鏈哄埗锛?
- **Mock 宸ュ叿**锛歚unittest.mock` / `pytest-mock`锛堥殧绂诲閮ㄤ緷璧栵紝濡?LLM API锛?
- **鏂█澧炲己**锛歚pytest-check`锛堟敮鎸佸鏂█涓嶄腑鏂墽琛岋級

#### 4.2.2 闆嗘垚娴嬭瘯 (Integration Tests)

**鐩爣**锛氶獙璇佸涓粍浠跺崗浣滄椂鐨勬暟鎹祦杞笌鎺ュ彛鍏煎鎬с€?

**瑕嗙洊鑼冨洿**锛?

| 娴嬭瘯鍦烘櫙 | 楠岃瘉瑕佺偣 | 娴嬭瘯绛栫暐 |
|---------|---------|---------|
| **Ingestion Pipeline** | Loader 鈫?Splitter 鈫?Transform 鈫?Storage 鐨勫畬鏁存祦绋?| - 浣跨敤鐪熷疄鐨勬祴璇?PDF 鏂囦欢<br>- 楠岃瘉鏈€缁堝瓨鍏ュ悜閲忓簱鐨勬暟鎹畬鏁存€?br>- 妫€鏌ヤ腑闂翠骇鐗╋紙濡備复鏃跺浘鐗囨枃浠讹級鏄惁姝ｇ‘娓呯悊 |
| **Hybrid Search** | Dense + Sparse 鍙洖鐨勮瀺鍚堢粨鏋?| - 鍑嗗宸茬煡绛旀鐨勬煡璇?鏂囨。瀵?br>- 楠岃瘉铻嶅悎鍚庣殑 Top-1 鏄惁鍛戒腑姝ｇ‘鏂囨。<br>- 娴嬭瘯鏋佺鎯呭喌锛堟煇涓€璺棤缁撴灉锛?|
| **Rerank Pipeline** | 鍙洖 鈫?杩囨护 鈫?閲嶆帓鐨勭粍鍚?| - 楠岃瘉 Metadata 杩囨护鍚庣殑鍊欓€夐泦姝ｇ‘鎬?br>- 妫€鏌?Reranker 鏄惁鏀瑰彉浜?Top-1 缁撴灉<br>- 娴嬭瘯 Reranker 澶辫触鏃剁殑鍥為€€ |
| **MCP Server** | 宸ュ叿璋冪敤鐨勭鍒扮娴佺▼ | - 妯℃嫙 MCP Client 鍙戦€?JSON-RPC 璇锋眰<br>- 楠岃瘉杩斿洖鐨?`content` 鏍煎紡绗﹀悎鍗忚<br>- 娴嬭瘯閿欒澶勭悊锛堝鏌ヨ璇硶閿欒锛?|

**鎶€鏈€夊瀷**锛?
- **鏁版嵁闅旂**锛氭瘡涓祴璇曚娇鐢ㄧ嫭绔嬬殑涓存椂鏁版嵁搴?鍚戦噺搴擄紙`pytest-tempdir`锛?
- **寮傛娴嬭瘯**锛歚pytest-asyncio`锛堣嫢 MCP Server 閲囩敤寮傛瀹炵幇锛?
- **濂戠害娴嬭瘯**锛氬畾涔夊悇妯″潡闂寸殑 Schema锛岀‘淇濇帴鍙ｄ笉婕傜Щ

#### 4.2.3 绔埌绔祴璇?(End-to-End Tests)

**鐩爣**锛氭ā鎷熺湡瀹炵敤鎴锋搷浣滐紝楠岃瘉瀹屾暣涓氬姟娴佺▼鐨勫彲鐢ㄦ€с€?

**鏍稿績鍦烘櫙**锛?

**鍦烘櫙 1锛氭暟鎹噯澶囷紙绂荤嚎鎽勫彇锛?*
- **娴嬭瘯鐩爣**锛氶獙璇佹枃妗ｆ憚鍙栨祦绋嬬殑瀹屾暣鎬т笌姝ｇ‘鎬?
- **娴嬭瘯姝ラ**锛?
  - 鍑嗗娴嬭瘯鏂囨。锛圥DF 鏂囦欢锛屽寘鍚枃鏈€佸浘鐗囥€佽〃鏍肩瓑澶氱鍏冪礌锛?
  - 鎵ц绂荤嚎鎽勫彇鑴氭湰锛屽皢鏂囨。瀵煎叆鐭ヨ瘑搴?
  - 楠岃瘉鎽勫彇缁撴灉锛氭鏌ョ敓鎴愮殑 Chunk 鏁伴噺銆佸厓鏁版嵁瀹屾暣鎬с€佸浘鐗囨弿杩扮敓鎴?
  - 楠岃瘉瀛樺偍鐘舵€侊細纭鍚戦噺搴撳拰 BM25 绱㈠紩姝ｇ‘鍒涘缓
  - 楠岃瘉骞傜瓑鎬э細閲嶅鎽勫彇鍚屼竴鏂囨。锛岀‘淇濅笉浜х敓閲嶅鏁版嵁
- **楠岃瘉瑕佺偣**锛?
  - Chunk 鐨勫垏鍒嗚川閲忥紙璇箟瀹屾暣鎬с€佷笂涓嬫枃淇濈暀锛?
  - 鍏冩暟鎹瓧娈靛畬鏁存€э紙source銆乸age銆乼itle銆乼ags 绛夛級
  - 鍥剧墖澶勭悊缁撴灉锛圕aption 鐢熸垚銆丅ase64 缂栫爜瀛樺偍锛?
  - 鍚戦噺涓庣█鐤忕储寮曠殑姝ｇ‘鎬?

**鍦烘櫙 2锛氬彫鍥炴祴璇?*
- **娴嬭瘯鐩爣**锛氶獙璇佹绱㈢郴缁熺殑鍙洖绮惧害涓庢帓搴忚川閲?
- **娴嬭瘯姝ラ**锛?
  - 鍩轰簬宸叉憚鍙栫殑鐭ヨ瘑搴擄紝鍑嗗涓€缁勬祴璇曟煡璇紙鍖呭惈涓嶅悓闅惧害涓庣被鍨嬶級
  - 鎵ц娣峰悎妫€绱紙Dense + Sparse + Rerank锛?
  - 楠岃瘉鍙洖缁撴灉锛氭鏌?Top-K 鏂囨。鏄惁鍖呭惈棰勬湡鏉ユ簮
  - 瀵规瘮涓嶅悓妫€绱㈢瓥鐣ョ殑鏁堟灉锛堢函 Dense銆佺函 Sparse銆丠ybrid锛?
  - 楠岃瘉 Rerank 鐨勫奖鍝嶏細瀵规瘮閲嶆帓鍓嶅悗鐨勭粨鏋滃彉鍖?
- **楠岃瘉瑕佺偣**锛?
  - Hit Rate@K锛歍op-K 缁撴灉鍛戒腑鐜囨槸鍚﹁揪鏍?
  - 鎺掑簭璐ㄩ噺锛氭纭瓟妗堟槸鍚︽帓鍦ㄥ墠鍒楋紙MRR銆丯DCG锛?
  - 杈圭晫鎯呭喌澶勭悊锛氱┖鏌ヨ銆佹棤缁撴灉鏌ヨ銆佽秴闀挎煡璇?
  - 澶氭ā鎬佸彫鍥烇細鍖呭惈鍥剧墖鐨勬枃妗ｆ槸鍚﹁兘閫氳繃鏂囨湰鏌ヨ鍙洖

**鍦烘櫙 3锛歁CP Client 鍔熻兘娴嬭瘯**
- **娴嬭瘯鐩爣**锛氶獙璇?MCP Server 涓?Client锛堝 GitHub Copilot锛夌殑鍗忚鍏煎鎬т笌鍔熻兘瀹屾暣鎬?
- **娴嬭瘯姝ラ**锛?
  - 鍚姩 MCP Server锛圫tdio Transport 妯″紡锛?
  - 妯℃嫙 MCP Client 鍙戦€佸悇绫?JSON-RPC 璇锋眰
  - 娴嬭瘯宸ュ叿璋冪敤锛歚query_knowledge_hub`銆乣list_collections` 绛?
  - 楠岃瘉杩斿洖鏍煎紡锛氱鍚?MCP 鍗忚瑙勮寖锛坈ontent 鏁扮粍銆乻tructuredContent锛?
  - 娴嬭瘯寮曠敤閫忔槑鎬э細杩斿洖缁撴灉鍖呭惈瀹屾暣鐨?Citation 淇℃伅
  - 娴嬭瘯澶氭ā鎬佽繑鍥烇細鍖呭惈鍥剧墖鐨勫搷搴旀纭紪鐮佷负 Base64
- **楠岃瘉瑕佺偣**锛?
  - 鍗忚鍚堣鎬э細JSON-RPC 2.0 鏍煎紡銆侀敊璇爜鏄犲皠
  - 宸ュ叿娉ㄥ唽锛歚tools/list` 杩斿洖鎵€鏈夊彲鐢ㄥ伐鍏峰強鍏?Schema
  - 鍝嶅簲鏍煎紡锛歍extContent 涓?ImageContent 鐨勬纭粍鍚?
  - 閿欒澶勭悊锛氭棤鏁堝弬鏁般€佽秴鏃躲€佹湇鍔′笉鍙敤绛夊紓甯稿満鏅?
  - 鎬ц兘鎸囨爣锛氬崟娆¤姹傜殑绔埌绔欢杩燂紙鍚绱€侀噸鎺掋€佹牸寮忓寲锛?

**娴嬭瘯宸ュ叿**锛?
- **BDD 妗嗘灦**锛歚behave` 鎴?`pytest-bdd`锛堜互 Gherkin 璇硶鎻忚堪鍦烘櫙锛?
- **鐜鍑嗗**锛?
  - 涓存椂娴嬭瘯鍚戦噺搴擄紙鐙珛浜庣敓浜ф暟鎹級
  - 棰勭疆鐨勬爣鍑嗘祴璇曟枃妗ｉ泦
  - 鏈湴 MCP Server 杩涚▼锛圫tdio Transport锛?

### 4.3 RAG 璐ㄩ噺璇勪及娴嬭瘯

**鐩爣**锛氶獙璇佸凡璁捐鐨勮瘎浼颁綋绯伙紙瑙?3.3.4 璇勪及妗嗘灦鎶借薄锛夋槸鍚︽纭疄鐜帮紝骞惰兘鏈夋晥璇勪及 RAG 绯荤粺鐨勫彫鍥炰笌鐢熸垚璐ㄩ噺銆?

**娴嬭瘯瑕佺偣**锛?

1. **榛勯噾娴嬭瘯闆嗗噯澶?*
   - 鏋勫缓鏍囧噯鐨?闂-绛旀-鏉ユ簮鏂囨。"娴嬭瘯闆嗭紙JSON 鏍煎紡锛?
   - 鍒濇湡浜哄伐鏍囨敞鏍稿績鍦烘櫙锛屽悗鏈熸寔缁Н绱潖 Case

2. **璇勪及妗嗘灦瀹炵幇楠岃瘉**
   - 楠岃瘉 Ragas/DeepEval 绛夎瘎浼版鏋剁殑姝ｇ‘闆嗘垚
   - 纭璇勪及鎺ュ彛鑳借緭鍑烘爣鍑嗗寲鐨勬寚鏍囧瓧鍏?
   - 娴嬭瘯澶氳瘎浼板櫒骞惰鎵ц涓庣粨鏋滄眹鎬?

3. **鍏抽敭鎸囨爣杈炬爣楠岃瘉**
   - 妫€绱㈡寚鏍囷細Hit Rate@K 鈮?90%銆丮RR 鈮?0.8銆丯DCG@K 鈮?0.85
   - 鐢熸垚鎸囨爣锛欶aithfulness 鈮?0.9銆丄nswer Relevancy 鈮?0.85
   - 瀹氭湡杩愯璇勪及锛岀洃鎺ф寚鏍囨槸鍚﹀洖褰?

**璇存槑**锛氭湰鑺傞噸鐐规槸楠岃瘉璇勪及浣撶郴鐨勫伐绋嬪疄鐜帮紝鑰岄潪閲嶆柊璁捐璇勪及鏂规硶锛堣瘎浼版柟娉曠殑璁捐瑙佺 3 绔犳妧鏈€夊瀷锛夈€?

### 4.4 鎬ц兘涓庡帇鍔涙祴璇曪紙鍙€夛級

> **璇存槑**锛氭湰椤圭洰瀹氫綅涓烘湰鍦?MCP Server锛屽崟鐢ㄦ埛寮€鍙戠幆澧冿紝閲囩敤 Stdio Transport 閫氫俊鏂瑰紡銆傛€ц兘涓庡帇鍔涙祴璇曞湪褰撳墠闃舵**涓嶆槸蹇呴渶鐨?*锛屾澶勫垪鍑轰富瑕佺敤浜庯細
> 1. **鏋舵瀯瀹屾暣鎬?*锛氬睍绀哄畬鏁寸殑宸ョ▼鍖栨祴璇曚綋绯伙紝浣撶幇绯荤粺璁捐鐨勪笓涓氭€?
> 2. **鏈潵鎵╁睍鎬?*锛氳嫢鍚庣画闇€瑕佷簯绔儴缃叉垨澶氱敤鎴锋敮鎸侊紝鍙洿鎺ュ弬鑰冩鏂规
> 3. **鎬ц兘鍩哄噯寤虹珛**锛氶€氳繃鍩虹鎬ц兘娴嬭瘯浜嗚В绯荤粺鐡堕锛屼负浼樺寲鎻愪緵鏁版嵁鏀拺

**鍙€夋祴璇曞満鏅?*锛?

| 娴嬭瘯绫诲瀷 | 楠岃瘉鐐?| 宸ュ叿 | 浼樺厛绾?|
|---------|-------|------|-------|
| **寤惰繜娴嬭瘯** | 鍗曟鏌ヨ鐨?P50/P95/P99 寤惰繜 | `pytest-benchmark` | 涓紙鍙府鍔╄瘑鍒參鏌ヨ锛?|
| **鍚炲悙閲忔祴璇?* | 骞跺彂鏌ヨ鏃剁殑 QPS 涓婇檺 | `locust` | 浣庯紙鏈湴鍗曠敤鎴锋棤闇€姹傦級 |
| **鍐呭瓨娉勬紡妫€娴?* | 闀挎椂闂磋繍琛屽悗鐨勫唴瀛樺崰鐢?| `memory_profiler` | 浣庯紙鐭湡杩愯鏃犲奖鍝嶏級 |
| **鍚戦噺搴撴€ц兘** | 涓嶅悓鏁版嵁瑙勬ā涓嬬殑鏌ヨ閫熷害 | 鑷畾涔?Benchmark | 涓紙楠岃瘉鎵╁睍鎬э級 |

### 4.5 娴嬭瘯宸ュ叿閾句笌 CI/CD 闆嗘垚

**鏈湴寮€鍙戝伐浣滄祦**锛?
- **蹇€熼獙璇?*锛氫粎杩愯鍗曞厓娴嬭瘯锛岀绾у弽棣?
- **瀹屾暣楠岃瘉**锛氬崟鍏冩祴璇?+ 闆嗘垚娴嬭瘯锛岀敓鎴愯鐩栫巼鎶ュ憡
- **璐ㄩ噺璇勪及**锛氬畾鏈熸墽琛?RAG 璐ㄩ噺娴嬭瘯锛岀洃鎺ф寚鏍囧彉鍖?

**CI/CD Pipeline 璁捐**锛堝彲閫夛級锛?
> **璇存槑**锛氭湰鍦伴」鐩笉寮哄埗瑕佹眰 CI/CD锛屼絾閰嶇疆鑷姩鍖栨祴璇曟祦绋嬫湁鍔╀簬浠ｇ爜璐ㄩ噺淇濋殰涓庢寔缁泦鎴愬疄璺点€?

- **鍗曞厓娴嬭瘯闃舵**锛氭瘡娆℃彁浜よ嚜鍔ㄨЕ鍙戯紝楠岃瘉鍩虹鍔熻兘锛岀敓鎴愯鐩栫巼鎶ュ憡
- **闆嗘垚娴嬭瘯闃舵**锛氬崟鍏冩祴璇曢€氳繃鍚庢墽琛岋紝楠岃瘉妯″潡鍗忎綔
- **璐ㄩ噺璇勪及闃舵**锛歅R 瑙﹀彂锛岃繍琛屽畬鏁寸殑 RAG 璐ㄩ噺娴嬭瘯锛屽彂甯冭瘎浼版姤鍛?

**娴嬭瘯瑕嗙洊鐜囩洰鏍?*锛?
- **鍗曞厓娴嬭瘯**锛氭牳蹇冮€昏緫瑕嗙洊鐜?鈮?80%
- **闆嗘垚娴嬭瘯**锛氬叧閿矾寰勮鐩栫巼 100%锛堝 Ingestion銆丠ybrid Search锛?
- **E2E 娴嬭瘯**锛氭牳蹇冪敤鎴峰満鏅鐩栫巼 100%锛堣嚦灏?3 涓叧閿祦绋嬶級


## 5. 绯荤粺鏋舵瀯涓庢ā鍧楄璁?

### 5.1 鏁翠綋鏋舵瀯鍥?

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?                                    MCP Clients (澶栭儴璋冪敤灞?                                  鈹?
鈹?                                                                                            鈹?
鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                       鈹?
鈹?   鈹? GitHub Copilot 鈹?   鈹? Claude Desktop 鈹?   鈹? 鍏朵粬 MCP Agent 鈹?                       鈹?
鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                       鈹?
鈹?            鈹?                     鈹?                     鈹?                                鈹?
鈹?            鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                                鈹?
鈹?                                   鈹? JSON-RPC 2.0 (Stdio Transport)                       鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
                                     鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?                                  MCP Server 灞?(鎺ュ彛灞?                                     鈹?
鈹?                                                                                            鈹?
鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?     鈹?
鈹?   鈹?                             MCP Protocol Handler                               鈹?     鈹?
鈹?   鈹?                   (tools/list, tools/call, resources/*)                        鈹?     鈹?
鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?     鈹?
鈹?                                          鈹?                                                鈹?
鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?         鈹?
鈹?   鈻?                     鈻?              鈻?              鈻?                     鈻?         鈹?
鈹?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹?
鈹?鈹俼uery_knowledge鈹?鈹俵ist_collections鈹?鈹俫et_document_ 鈹? 鈹俿earch_by_    鈹? 鈹? 鍏朵粬鎵╁睍    鈹?   鈹?
鈹?鈹?   _hub      鈹? 鈹?             鈹? 鈹?  summary    鈹? 鈹? keyword     鈹? 鈹?  宸ュ叿...    鈹?   鈹?
鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
                                         鈹?
                                         鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?                                  Core 灞?(鏍稿績涓氬姟閫昏緫)                                     鈹?
鈹?                                                                                            鈹?
鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹?
鈹? 鈹?                           Query Engine (鏌ヨ寮曟搸)                                   鈹?   鈹?
鈹? 鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹?   鈹?
鈹? 鈹? 鈹?                        Query Processor (鏌ヨ棰勫鐞?                         鈹?   鈹?   鈹?
鈹? 鈹? 鈹?           鍏抽敭璇嶆彁鍙?| 鏌ヨ鎵╁睍 (鍚屼箟璇?鍒悕) | Metadata 瑙ｆ瀽               鈹?   鈹?   鈹?
鈹? 鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹?   鈹?
鈹? 鈹?                                      鈹?                                            鈹?   鈹?
鈹? 鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈹?   鈹?
鈹? 鈹? 鈹?                    Hybrid Search Engine (娣峰悎妫€绱㈠紩鎿?                  鈹?       鈹?   鈹?
鈹? 鈹? 鈹?                                   鈹?                                   鈹?       鈹?   鈹?
鈹? 鈹? 鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹粹攢鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹?       鈹?   鈹?
鈹? 鈹? 鈹?   鈹?  Dense Route     鈹?   鈹?  Fusion    鈹?   鈹?  Sparse Route    鈹?   鈹?       鈹?   鈹?
鈹? 鈹? 鈹?   鈹?(Embedding 璇箟)  鈹傗梽鈹€鈹€鈹€鈹?   (RRF)    鈹溾攢鈹€鈹€鈻衡攤   (BM25 鍏抽敭璇?   鈹?   鈹?       鈹?   鈹?
鈹? 鈹? 鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹?       鈹?   鈹?
鈹? 鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈹?   鈹?
鈹? 鈹?                                      鈹?                                            鈹?   鈹?
鈹? 鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹?   鈹?
鈹? 鈹? 鈹?                       Reranker (閲嶆帓搴忔ā鍧? [鍙€塢                          鈹?   鈹?   鈹?
鈹? 鈹? 鈹?         None (鍏抽棴) | Cross-Encoder (鏈湴妯″瀷) | LLM Rerank               鈹?   鈹?   鈹?
鈹? 鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹?   鈹?
鈹? 鈹?                                      鈹?                                            鈹?   鈹?
鈹? 鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹?   鈹?
鈹? 鈹? 鈹?                     Response Builder (鍝嶅簲鏋勫缓鍣?                           鈹?   鈹?   鈹?
鈹? 鈹? 鈹?           寮曠敤鐢熸垚 (Citation) | 澶氭ā鎬佸唴瀹圭粍瑁?(Text + Image)               鈹?   鈹?   鈹?
鈹? 鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹?   鈹?
鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹?
鈹?                                                                                            鈹?
鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹?
鈹? 鈹?                         Trace Collector (杩借釜鏀堕泦鍣?                                鈹?   鈹?
鈹? 鈹?                  trace_id 鐢熸垚 | 鍚勯樁娈佃€楁椂璁板綍 | JSON Lines 杈撳嚭                  鈹?   鈹?
鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
                                         鈹?
                                         鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?                                  Storage 灞?(瀛樺偍灞?                                        鈹?
鈹?                                                                                            鈹?
鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?     鈹?
鈹?   鈹?                            Vector Store (鍚戦噺瀛樺偍)                              鈹?     鈹?
鈹?   鈹?                                                                                鈹?     鈹?
鈹?   鈹?    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹?     鈹?
鈹?   鈹?    鈹?                        Chroma DB                                   鈹?    鈹?     鈹?
鈹?   鈹?    鈹?   Dense Vector | Sparse Vector | Chunk Content | Metadata          鈹?    鈹?     鈹?
鈹?   鈹?    鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹?     鈹?
鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?     鈹?
鈹?                                                                                            鈹?
鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?            鈹?
鈹?   鈹?      BM25 Index (绋€鐤忕储寮?       鈹?   鈹?      Image Store (鍥剧墖瀛樺偍)     鈹?            鈹?
鈹?   鈹?       鍊掓帓绱㈠紩 | IDF 缁熻        鈹?   鈹?   鏈湴鏂囦欢绯荤粺 | Base64 缂栫爜     鈹?            鈹?
鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?            鈹?
鈹?                                                                                            鈹?
鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?            鈹?
鈹?   鈹?    Trace Logs (杩借釜鏃ュ織)         鈹?   鈹?  Processing Cache (澶勭悊缂撳瓨)    鈹?            鈹?
鈹?   鈹?    JSON Lines 鏍煎紡鏂囦欢           鈹?   鈹?  鏂囦欢鍝堝笇 | Chunk 鍝堝笇 | 鐘舵€?  鈹?            鈹?
鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?            鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?

鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?                             Ingestion Pipeline (绂荤嚎鏁版嵁鎽勫彇)                               鈹?
鈹?                                                                                            鈹?
鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?
鈹?   鈹?  Loader   鈹傗攢鈹€鈹€鈻衡攤  Splitter  鈹傗攢鈹€鈹€鈻衡攤 Transform  鈹傗攢鈹€鈹€鈻衡攤  Embedding 鈹傗攢鈹€鈹€鈻衡攤   Upsert   鈹?  鈹?
鈹?   鈹?(鏂囨。瑙ｆ瀽) 鈹?   鈹? (鍒囧垎鍣?  鈹?   鈹?(澧炲己澶勭悊) 鈹?   鈹? (鍚戦噺鍖?  鈹?   鈹? (瀛樺偍)    鈹?  鈹?
鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?
鈹?        鈹?                 鈹?                 鈹?                 鈹?               鈹?        鈹?
鈹?        鈻?                 鈻?                 鈻?                 鈻?               鈻?        鈹?
鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?
鈹?   鈹侻arkItDown 鈹?   鈹俁ecursive   鈹?   鈹侺LM閲嶅啓     鈹?   鈹侱ense:      鈹?   鈹侰hroma      鈹?  鈹?
鈹?   鈹侾DF鈫扢D     鈹?   鈹侰haracter   鈹?   鈹侷mage       鈹?   鈹侽penAI/BGE  鈹?   鈹俇psert      鈹?  鈹?
鈹?   鈹傚厓鏁版嵁鎻愬彇 鈹?   鈹俆extSplitter鈹?   鈹侰aptioning  鈹?   鈹係parse:BM25 鈹?   鈹傚箓绛夊啓鍏?   鈹?  鈹?
鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?

鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?                               Libs 灞?(鍙彃鎷旀娊璞″眰)                                        鈹?
鈹?                                                                                            鈹?
鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?      鈹?
鈹?   鈹?                           Factory Pattern (宸ュ巶妯″紡)                           鈹?      鈹?
鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?      鈹?
鈹?                                          鈹?                                                鈹?
鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹?
鈹? 鈹?LLM Client 鈹?鈹?Embedding  鈹?鈹? Splitter  鈹?鈹俈ectorStore 鈹?鈹? Reranker  鈹?鈹?Evaluator  鈹? 鈹?
鈹? 鈹? Factory   鈹?鈹? Factory   鈹?鈹? Factory   鈹?鈹? Factory   鈹?鈹? Factory   鈹?鈹? Factory   鈹? 鈹?
鈹? 鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹?
鈹? 鈹?路 Azure    鈹?鈹?路 OpenAI   鈹?鈹?路 Recursive鈹?鈹?路 Chroma   鈹?鈹?路 None     鈹?鈹?路 Ragas    鈹? 鈹?
鈹? 鈹?路 OpenAI   鈹?鈹?路 BGE      鈹?鈹?路 Semantic 鈹?鈹?路 Qdrant   鈹?鈹?路 CrossEnc 鈹?鈹?路 DeepEval 鈹? 鈹?
鈹? 鈹?路 Ollama   鈹?鈹?路 Ollama   鈹?鈹?路 FixedLen 鈹?鈹?路 Pinecone 鈹?鈹?路 LLM      鈹?鈹?路 Custom   鈹? 鈹?
鈹? 鈹?路 DeepSeek 鈹?鈹?路 ...      鈹?鈹?路 ...      鈹?鈹?路 ...      鈹?鈹?           鈹?鈹?           鈹? 鈹?
鈹? 鈹?路 Vision鉁?鈹?鈹?           鈹?鈹?           鈹?鈹?           鈹?鈹?           鈹?鈹?           鈹? 鈹?
鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?

鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?                            Observability 灞?(鍙娴嬫€?                                      鈹?
鈹?                                                                                            鈹?
鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹?
鈹?   鈹?         Trace Context               鈹?   鈹?        Web Dashboard                鈹?    鈹?
鈹?   鈹?  trace_id | stages[] | metrics      鈹?   鈹?       (Streamlit)                   鈹?    鈹?
鈹?   鈹?  record_stage() | finish()          鈹?   鈹?   璇锋眰鍒楄〃 | 鑰楁椂鐎戝竷鍥?| 璇︽儏灞曞紑   鈹?    鈹?
鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹?
鈹?                                                                                            鈹?
鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹?
鈹?   鈹?         Evaluation Module           鈹?   鈹?        Structured Logger            鈹?    鈹?
鈹?   鈹?  Hit Rate | MRR | Faithfulness      鈹?   鈹?   JSON Formatter | File Handler     鈹?    鈹?
鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
```

### 5.2 鐩綍缁撴瀯

```
smart-knowledge-hub/
鈹?
鈹溾攢鈹€ config/                              # 閰嶇疆鏂囦欢鐩綍
鈹?  鈹溾攢鈹€ settings.yaml                    # 涓婚厤缃枃浠?(LLM/Embedding/VectorStore 閰嶇疆)
鈹?  鈹斺攢鈹€ prompts/                         # Prompt 妯℃澘鐩綍
鈹?      鈹溾攢鈹€ image_captioning.txt         # 鍥剧墖鎻忚堪鐢熸垚 Prompt
鈹?      鈹溾攢鈹€ chunk_refinement.txt         # Chunk 閲嶅啓 Prompt
鈹?      鈹斺攢鈹€ rerank.txt                   # LLM Rerank Prompt
鈹?
鈹溾攢鈹€ src/                                 # 婧愪唬鐮佷富鐩綍
鈹?  鈹?
鈹?  鈹溾攢鈹€ mcp_server/                      # MCP Server 灞?(鎺ュ彛灞?
鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹溾攢鈹€ server.py                    # MCP Server 鍏ュ彛 (Stdio Transport)
鈹?  鈹?  鈹溾攢鈹€ protocol_handler.py          # JSON-RPC 鍗忚澶勭悊
鈹?  鈹?  鈹斺攢鈹€ tools/                       # MCP Tools 瀹氫箟
鈹?  鈹?      鈹溾攢鈹€ __init__.py
鈹?  鈹?      鈹溾攢鈹€ query_knowledge_hub.py   # 涓绘绱㈠伐鍏?
鈹?  鈹?      鈹溾攢鈹€ list_collections.py      # 鍒楀嚭闆嗗悎宸ュ叿
鈹?  鈹?      鈹斺攢鈹€ get_document_summary.py  # 鏂囨。鎽樿宸ュ叿
鈹?  鈹?
鈹?  鈹溾攢鈹€ core/                            # Core 灞?(鏍稿績涓氬姟閫昏緫)
鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹溾攢鈹€ settings.py                   # 閰嶇疆鍔犺浇涓庢牎楠?(Settings锛歭oad_settings/validate_settings)
鈹?  鈹?  鈹溾攢鈹€ types.py                      # 鏍稿績鏁版嵁绫诲瀷/濂戠害锛圖ocument/Chunk/ChunkRecord锛夛紝渚?ingestion/retrieval/mcp 澶嶇敤
鈹?  鈹?  鈹?
鈹?  鈹?  鈹溾攢鈹€ query_engine/                # 鏌ヨ寮曟搸妯″潡
鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ query_processor.py       # 鏌ヨ棰勫鐞?(鍏抽敭璇嶆彁鍙?鏌ヨ鎵╁睍)
鈹?  鈹?  鈹?  鈹溾攢鈹€ hybrid_search.py         # 娣峰悎妫€绱㈠紩鎿?(Dense + Sparse + RRF)
鈹?  鈹?  鈹?  鈹溾攢鈹€ dense_retriever.py       # 绋犲瘑鍚戦噺妫€绱?
鈹?  鈹?  鈹?  鈹溾攢鈹€ sparse_retriever.py      # 绋€鐤忔绱?(BM25)
鈹?  鈹?  鈹?  鈹溾攢鈹€ fusion.py                # 缁撴灉铻嶅悎 (RRF 绠楁硶)
鈹?  鈹?  鈹?  鈹斺攢鈹€ reranker.py              # 閲嶆帓搴忔ā鍧?(None/CrossEncoder/LLM)
鈹?  鈹?  鈹?
鈹?  鈹?  鈹溾攢鈹€ response/                    # 鍝嶅簲鏋勫缓妯″潡
鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ response_builder.py      # 鍝嶅簲鏋勫缓鍣?
鈹?  鈹?  鈹?  鈹溾攢鈹€ citation_generator.py    # 寮曠敤鐢熸垚鍣?
鈹?  鈹?  鈹?  鈹斺攢鈹€ multimodal_assembler.py  # 澶氭ā鎬佸唴瀹圭粍瑁?(Text + Image)
鈹?  鈹?  鈹?
鈹?  鈹?  鈹斺攢鈹€ trace/                       # 杩借釜妯″潡
鈹?  鈹?      鈹溾攢鈹€ __init__.py
鈹?  鈹?      鈹溾攢鈹€ trace_context.py         # 杩借釜涓婁笅鏂?(trace_id/stages)
鈹?  鈹?      鈹斺攢鈹€ trace_collector.py       # 杩借釜鏀堕泦鍣?
鈹?  鈹?
鈹?  鈹溾攢鈹€ ingestion/                       # Ingestion Pipeline (绂荤嚎鏁版嵁鎽勫彇)
鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹溾攢鈹€ pipeline.py                  # Pipeline 涓绘祦绋嬬紪鎺?(鏀寔 on_progress 鍥炶皟)
鈹?  鈹?  鈹溾攢鈹€ document_manager.py          # 鏂囨。鐢熷懡鍛ㄦ湡绠＄悊 (list/delete/stats)
鈹?  鈹?  鈹?
鈹?  鈹?  鈹溾攢鈹€ chunking/                    # Chunking 妯″潡 (鏂囨。鍒囧垎)
鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹斺攢鈹€ document_chunker.py      # Document 鈫?Chunks 杞崲锛堣皟鐢?libs.splitter锛?
鈹?  鈹?  鈹?
鈹?  鈹?  鈹溾攢鈹€ transform/                   # Transform 妯″潡 (澧炲己澶勭悊)
鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ base_transform.py        # Transform 鎶借薄鍩虹被
鈹?  鈹?  鈹?  鈹溾攢鈹€ chunk_refiner.py         # Chunk 鏅鸿兘閲嶇粍/鍘诲櫔
鈹?  鈹?  鈹?  鈹溾攢鈹€ metadata_enricher.py     # 璇箟鍏冩暟鎹敞鍏?(Title/Summary/Tags)
鈹?  鈹?  鈹?  鈹斺攢鈹€ image_captioner.py       # 鍥剧墖鎻忚堪鐢熸垚 (Vision LLM)
鈹?  鈹?  鈹?
鈹?  鈹?  鈹溾攢鈹€ embedding/                   # Embedding 妯″潡 (鍚戦噺鍖?
鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ dense_encoder.py         # 绋犲瘑鍚戦噺缂栫爜
鈹?  鈹?  鈹?  鈹溾攢鈹€ sparse_encoder.py        # 绋€鐤忓悜閲忕紪鐮?(BM25)
鈹?  鈹?  鈹?  鈹斺攢鈹€ batch_processor.py       # 鎵瑰鐞嗕紭鍖?
鈹?  鈹?  鈹?
鈹?  鈹?  鈹斺攢鈹€ storage/                     # Storage 妯″潡 (瀛樺偍)
鈹?  鈹?      鈹溾攢鈹€ __init__.py
鈹?  鈹?      鈹溾攢鈹€ vector_upserter.py       # 鍚戦噺搴?Upsert
鈹?  鈹?      鈹溾攢鈹€ bm25_indexer.py          # BM25 绱㈠紩鏋勫缓
鈹?  鈹?      鈹斺攢鈹€ image_storage.py         # 鍥剧墖鏂囦欢瀛樺偍
鈹?  鈹?
鈹?  鈹溾攢鈹€ libs/                            # Libs 灞?(鍙彃鎷旀娊璞″眰)
鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?
鈹?  鈹?  鈹溾攢鈹€ loader/                      # Loader 鎶借薄 (鏂囨。鍔犺浇)
鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ base_loader.py           # Loader 鎶借薄鍩虹被
鈹?  鈹?  鈹?  鈹溾攢鈹€ pdf_loader.py            # PDF Loader (MarkItDown)
鈹?  鈹?  鈹?  鈹斺攢鈹€ file_integrity.py        # 鏂囦欢瀹屾暣鎬ф鏌?(SHA256 鍝堝笇)
鈹?  鈹?  鈹?
鈹?  鈹?  鈹溾攢鈹€ llm/                         # LLM 鎶借薄
鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ base_llm.py              # LLM 鎶借薄鍩虹被
鈹?  鈹?  鈹?  鈹溾攢鈹€ llm_factory.py           # LLM 宸ュ巶
鈹?  鈹?  鈹?  鈹溾攢鈹€ azure_llm.py             # Azure OpenAI 瀹炵幇
鈹?  鈹?  鈹?  鈹溾攢鈹€ openai_llm.py            # OpenAI 瀹炵幇
鈹?  鈹?  鈹?  鈹溾攢鈹€ ollama_llm.py            # Ollama 鏈湴妯″瀷瀹炵幇
鈹?  鈹?  鈹?  鈹溾攢鈹€ deepseek_llm.py          # DeepSeek 瀹炵幇
鈹?  鈹?  鈹?  鈹溾攢鈹€ base_vision_llm.py       # Vision LLM 鎶借薄鍩虹被锛堟敮鎸佸浘鍍忚緭鍏ワ級
鈹?  鈹?  鈹?  鈹斺攢鈹€ azure_vision_llm.py      # Azure Vision 瀹炵幇 (GPT-4o/GPT-4-Vision)
鈹?  鈹?  鈹?
鈹?  鈹?  鈹溾攢鈹€ embedding/                   # Embedding 鎶借薄
鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ base_embedding.py        # Embedding 鎶借薄鍩虹被
鈹?  鈹?  鈹?  鈹溾攢鈹€ embedding_factory.py     # Embedding 宸ュ巶
鈹?  鈹?  鈹?  鈹溾攢鈹€ openai_embedding.py      # OpenAI Embedding 瀹炵幇
鈹?  鈹?  鈹?  鈹溾攢鈹€ azure_embedding.py       # Azure Embedding 瀹炵幇
鈹?  鈹?  鈹?  鈹斺攢鈹€ ollama_embedding.py      # Ollama 鏈湴妯″瀷瀹炵幇
鈹?  鈹?  鈹?
鈹?  鈹?  鈹溾攢鈹€ splitter/                    # Splitter 鎶借薄 (鍒囧垎绛栫暐)
鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ base_splitter.py         # Splitter 鎶借薄鍩虹被
鈹?  鈹?  鈹?  鈹溾攢鈹€ splitter_factory.py      # Splitter 宸ュ巶
鈹?  鈹?  鈹?  鈹溾攢鈹€ recursive_splitter.py    # RecursiveCharacterTextSplitter 瀹炵幇
鈹?  鈹?  鈹?  鈹溾攢鈹€ semantic_splitter.py     # 璇箟鍒囧垎瀹炵幇
鈹?  鈹?  鈹?  鈹斺攢鈹€ fixed_length_splitter.py # 瀹氶暱鍒囧垎瀹炵幇
鈹?  鈹?  鈹?
鈹?  鈹?  鈹溾攢鈹€ vector_store/                # VectorStore 鎶借薄
鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ base_vector_store.py     # VectorStore 鎶借薄鍩虹被
鈹?  鈹?  鈹?  鈹溾攢鈹€ vector_store_factory.py  # VectorStore 宸ュ巶
鈹?  鈹?  鈹?  鈹斺攢鈹€ chroma_store.py          # Chroma 瀹炵幇
鈹?  鈹?  鈹?
鈹?  鈹?  鈹溾攢鈹€ reranker/                    # Reranker 鎶借薄
鈹?  鈹?  鈹?  鈹溾攢鈹€ __init__.py
鈹?  鈹?  鈹?  鈹溾攢鈹€ base_reranker.py         # Reranker 鎶借薄鍩虹被
鈹?  鈹?  鈹?  鈹溾攢鈹€ reranker_factory.py      # Reranker 宸ュ巶
鈹?  鈹?  鈹?  鈹溾攢鈹€ cross_encoder_reranker.py# CrossEncoder 瀹炵幇
鈹?  鈹?  鈹?  鈹斺攢鈹€ llm_reranker.py          # LLM Rerank 瀹炵幇
鈹?  鈹?  鈹?
鈹?  鈹?  鈹斺攢鈹€ evaluator/                   # Evaluator 鎶借薄
鈹?  鈹?      鈹溾攢鈹€ __init__.py
鈹?  鈹?      鈹溾攢鈹€ base_evaluator.py        # Evaluator 鎶借薄鍩虹被
鈹?  鈹?      鈹溾攢鈹€ evaluator_factory.py     # Evaluator 宸ュ巶
鈹?  鈹?      鈹溾攢鈹€ ragas_evaluator.py       # Ragas 瀹炵幇
鈹?  鈹?      鈹斺攢鈹€ custom_evaluator.py      # 鑷畾涔夋寚鏍囧疄鐜?
鈹?  鈹?
鈹?  鈹斺攢鈹€ observability/                   # Observability 灞?(鍙娴嬫€?
鈹?      鈹溾攢鈹€ __init__.py
鈹?      鈹溾攢鈹€ logger.py                    # 缁撴瀯鍖栨棩蹇?(JSON Formatter)
鈹?      鈹溾攢鈹€ dashboard/                   # Web Dashboard (鍙鍖栫鐞嗗钩鍙?
鈹?      鈹?  鈹溾攢鈹€ __init__.py
鈹?      鈹?  鈹溾攢鈹€ app.py                   # Streamlit 鍏ュ彛 (椤甸潰瀵艰埅娉ㄥ唽)
鈹?      鈹?  鈹溾攢鈹€ pages/                   # 鍏ぇ鍔熻兘椤甸潰
鈹?      鈹?  鈹?  鈹溾攢鈹€ overview.py          # 绯荤粺鎬昏 (缁勪欢閰嶇疆 + 鏁版嵁缁熻)
鈹?      鈹?  鈹?  鈹溾攢鈹€ data_browser.py      # 鏁版嵁娴忚鍣?(鏂囨。/Chunk/鍥剧墖鏌ョ湅)
鈹?      鈹?  鈹?  鈹溾攢鈹€ ingestion_manager.py # Ingestion 绠＄悊 (瑙﹀彂鎽勫彇/鍒犻櫎鏂囨。)
鈹?      鈹?  鈹?  鈹溾攢鈹€ ingestion_traces.py  # Ingestion 杩借釜 (鎽勫彇鍘嗗彶涓庤鎯?
鈹?      鈹?  鈹?  鈹溾攢鈹€ query_traces.py      # Query 杩借釜 (鏌ヨ鍘嗗彶涓庤鎯?
鈹?      鈹?  鈹?  鈹斺攢鈹€ evaluation_panel.py  # 璇勪及闈㈡澘 (杩愯璇勪及/鏌ョ湅鎸囨爣)
鈹?      鈹?  鈹斺攢鈹€ services/                # Dashboard 鏁版嵁鏈嶅姟灞?
鈹?      鈹?      鈹溾攢鈹€ trace_service.py     # Trace 璇诲彇鏈嶅姟 (瑙ｆ瀽 traces.jsonl)
鈹?      鈹?      鈹溾攢鈹€ data_service.py      # 鏁版嵁娴忚鏈嶅姟 (ChromaStore/ImageStorage)
鈹?      鈹?      鈹斺攢鈹€ config_service.py    # 閰嶇疆璇诲彇鏈嶅姟 (Settings 灞曠ず)
鈹?      鈹斺攢鈹€ evaluation/                  # 璇勪及妯″潡
鈹?          鈹溾攢鈹€ __init__.py
鈹?          鈹溾攢鈹€ eval_runner.py           # 璇勪及鎵ц鍣?
鈹?          鈹溾攢鈹€ ragas_evaluator.py       # Ragas 璇勪及瀹炵幇
鈹?          鈹斺攢鈹€ composite_evaluator.py   # 缁勫悎璇勪及鍣?(澶氬悗绔苟琛?

鈹?
鈹溾攢鈹€ data/                                # 鏁版嵁鐩綍
鈹?  鈹溾攢鈹€ documents/                       # 鍘熷鏂囨。瀛樻斁
鈹?  鈹?  鈹斺攢鈹€ {collection}/                # 鎸夐泦鍚堝垎绫?
鈹?  鈹溾攢鈹€ images/                          # 鎻愬彇鐨勫浘鐗囧瓨鏀?
鈹?  鈹?  鈹斺攢鈹€ {collection}/                # 鎸夐泦鍚堝垎绫伙紙瀹為檯瀛樺偍鍦?{doc_hash}/ 瀛愮洰褰曚笅锛?
鈹?  鈹斺攢鈹€ db/                              # 鏁版嵁搴撲笌绱㈠紩鏂囦欢鐩綍
鈹?      鈹溾攢鈹€ ingestion_history.db         # 鏂囦欢瀹屾暣鎬у巻鍙茶褰?(SQLite)
鈹?      鈹?                               # 琛ㄧ粨鏋勶細file_hash, file_path, status, processed_at, error_msg
鈹?      鈹?                               # 鐢ㄩ€旓細澧為噺鎽勫彇锛岄伩鍏嶉噸澶嶅鐞嗘湭鍙樻洿鏂囦欢
鈹?      鈹溾攢鈹€ image_index.db               # 鍥剧墖绱㈠紩鏄犲皠 (SQLite)
鈹?      鈹?                               # 琛ㄧ粨鏋勶細image_id, file_path, collection, doc_hash, page_num
鈹?      鈹?                               # 鐢ㄩ€旓細蹇€熸煡璇?image_id 鈫?鏈湴鏂囦欢璺緞锛屾敮鎸佸浘鐗囨绱笌寮曠敤
鈹?      鈹溾攢鈹€ chroma/                      # Chroma 鍚戦噺搴撶洰褰?
鈹?      鈹?                               # 瀛樺偍 Dense Vector銆丼parse Vector 涓?Chunk Metadata
鈹?      鈹斺攢鈹€ bm25/                        # BM25 绱㈠紩鐩綍
鈹?                                       # 瀛樺偍鍊掓帓绱㈠紩涓?IDF 缁熻淇℃伅锛堝綋鍓嶄娇鐢?pickle锛?
鈹?
鈹溾攢鈹€ cache/                               # 缂撳瓨鐩綍
鈹?  鈹溾攢鈹€ embeddings/                      # Embedding 缂撳瓨 (鎸夊唴瀹瑰搱甯?
鈹?  鈹溾攢鈹€ captions/                        # 鍥剧墖鎻忚堪缂撳瓨
鈹?  鈹斺攢鈹€ processing/                      # 澶勭悊鐘舵€佺紦瀛?(鏂囦欢鍝堝笇/Chunk 鍝堝笇)
鈹?
鈹溾攢鈹€ logs/                                # 鏃ュ織鐩綍
鈹?  鈹溾攢鈹€ traces.jsonl                     # 杩借釜鏃ュ織 (JSON Lines)
鈹?  鈹斺攢鈹€ app.log                          # 搴旂敤鏃ュ織
鈹?
鈹溾攢鈹€ tests/                               # 娴嬭瘯鐩綍
鈹?  鈹溾攢鈹€ unit/                            # 鍗曞厓娴嬭瘯
鈹?  鈹?  鈹溾攢鈹€ test_dense_retriever.py      # D2: 绋犲瘑妫€绱㈠櫒娴嬭瘯
鈹?  鈹?  鈹溾攢鈹€ test_sparse_retriever.py     # D3: 绋€鐤忔绱㈠櫒娴嬭瘯
鈹?  鈹?  鈹溾攢鈹€ test_fusion_rrf.py           # D4: RRF 铻嶅悎娴嬭瘯
鈹?  鈹?  鈹溾攢鈹€ test_reranker_fallback.py    # D6: Reranker 鍥為€€娴嬭瘯
鈹?  鈹?  鈹溾攢鈹€ test_protocol_handler.py     # E2: 鍗忚澶勭悊鍣ㄦ祴璇?
鈹?  鈹?  鈹溾攢鈹€ test_response_builder.py     # E3: 鍝嶅簲鏋勫缓鍣ㄦ祴璇?
鈹?  鈹?  鈹溾攢鈹€ test_list_collections.py     # E4: 闆嗗悎鍒楄〃宸ュ叿娴嬭瘯
鈹?  鈹?  鈹溾攢鈹€ test_get_document_summary.py # E5: 鏂囨。鎽樿宸ュ叿娴嬭瘯
鈹?  鈹?  鈹溾攢鈹€ test_trace_context.py        # F1: 杩借釜涓婁笅鏂囨祴璇?
鈹?  鈹?  鈹溾攢鈹€ test_jsonl_logger.py         # F2: JSON Lines 鏃ュ織娴嬭瘯
鈹?  鈹?  鈹斺攢鈹€ ...                          # 鍏朵粬宸叉湁鍗曞厓娴嬭瘯
鈹?  鈹溾攢鈹€ integration/                     # 闆嗘垚娴嬭瘯
鈹?  鈹?  鈹溾攢鈹€ test_ingestion_pipeline.py
鈹?  鈹?  鈹溾攢鈹€ test_hybrid_search.py        # D5: 娣峰悎妫€绱㈤泦鎴愭祴璇?
鈹?  鈹?  鈹斺攢鈹€ test_mcp_server.py           # E1-E6: MCP 鏈嶅姟鍣ㄩ泦鎴愭祴璇?
鈹?  鈹溾攢鈹€ e2e/                             # 绔埌绔祴璇?
鈹?  鈹?  鈹溾攢鈹€ test_data_ingestion.py
鈹?  鈹?  鈹溾攢鈹€ test_recall.py               # G2: 鍙洖鍥炲綊娴嬭瘯
鈹?  鈹?  鈹斺攢鈹€ test_mcp_client.py           # G1: MCP Client 妯℃嫙娴嬭瘯
鈹?  鈹斺攢鈹€ fixtures/                        # 娴嬭瘯鏁版嵁
鈹?      鈹溾攢鈹€ sample_documents/
鈹?      鈹斺攢鈹€ golden_test_set.json         # F5/G2: 榛勯噾娴嬭瘯闆?
鈹?
鈹溾攢鈹€ scripts/                             # 鑴氭湰鐩綍
鈹?  鈹溾攢鈹€ ingest.py                        # 鏁版嵁鎽勫彇鑴氭湰锛堢绾挎憚鍙栧叆鍙ｏ級
鈹?  鈹溾攢鈹€ query.py                         # 鏌ヨ娴嬭瘯鑴氭湰锛堝湪绾挎煡璇㈠叆鍙ｏ級
鈹?  鈹溾攢鈹€ evaluate.py                      # 璇勪及杩愯鑴氭湰
鈹?  鈹斺攢鈹€ start_dashboard.py               # Dashboard 鍚姩鑴氭湰
鈹?
鈹溾攢鈹€ main.py                              # MCP Server 鍚姩鍏ュ彛
鈹溾攢鈹€ pyproject.toml                       # Python 椤圭洰閰嶇疆
鈹溾攢鈹€ requirements.txt                     # 渚濊禆鍒楄〃
鈹斺攢鈹€ README.md                            # 椤圭洰璇存槑
```

### 5.3 妯″潡璇存槑

#### 5.3.1 MCP Server 灞?

| 妯″潡 | 鑱岃矗 | 鍏抽敭鎶€鏈偣 |
|-----|-----|----------|
| `server.py` | MCP Server 涓诲叆鍙ｏ紝澶勭悊 Stdio Transport 閫氫俊 | Python MCP SDK锛孞SON-RPC 2.0 |
| `protocol_handler.py` | 鍗忚瑙ｆ瀽涓庤兘鍔涘崗鍟?| `initialize`銆乣tools/list`銆乣tools/call` |
| `tools/*` | 瀵瑰鏆撮湶鐨勫伐鍏峰嚱鏁板疄鐜?| 瑁呴グ鍣ㄥ畾涔夛紝鍙傛暟鏍￠獙锛屽搷搴旀牸寮忓寲 |

#### 5.3.2 Core 灞?

| 妯″潡 | 鑱岃矗 | 鍏抽敭鎶€鏈偣 |
|-----|-----|----------|
| `settings.py` | 閰嶇疆鍔犺浇涓庢牎楠?| 璇诲彇 `config/settings.yaml`锛岃В鏋愪负 `Settings`锛屽繀濉瓧娈垫牎楠岋紙fail-fast锛?|
| `types.py` | 鏍稿績鏁版嵁绫诲瀷/濂戠害锛堝叏閾捐矾澶嶇敤锛?| 瀹氫箟 `Document/Chunk/ChunkRecord/ProcessedQuery/RetrievalResult`锛涘簭鍒楀寲绋冲畾锛涗綔涓?ingestion/retrieval/mcp 鐨勬暟鎹绾︿腑蹇?|
| `query_processor.py` | 鏌ヨ棰勫鐞?| 鍏抽敭璇嶆彁鍙栥€佸悓涔夎瘝鎵╁睍銆丮etadata 瑙ｆ瀽 |
| `hybrid_search.py` | 娣峰悎妫€绱㈢紪鎺?| 骞惰 Dense/Sparse 鍙洖锛岀粨鏋滆瀺鍚堬紝Metadata 杩囨护 |
| `dense_retriever.py` | 璇箟鍚戦噺妫€绱?| Query Embedding + VectorStore 妫€绱紝Cosine Similarity |
| `sparse_retriever.py` | BM25 鍏抽敭璇嶆绱?| 鍊掓帓绱㈠紩鏌ヨ锛孴F-IDF 鎵撳垎 |
| `fusion.py` | 缁撴灉铻嶅悎 | RRF 绠楁硶锛屾帓鍚嶅€掓暟鍔犳潈 |
| `reranker.py` | 绮炬帓閲嶆帓 | CrossEncoder / LLM Rerank / Fallback 鍥為€€ |
| `response_builder.py` | 鍝嶅簲鏋勫缓 | MCP 鍝嶅簲鏍煎紡鍖栵紝Markdown 鐢熸垚 |
| `citation_generator.py` | 寮曠敤鐢熸垚 | 浠庢绱㈢粨鏋滅敓鎴愮粨鏋勫寲寮曠敤鍒楄〃 |
| `multimodal_assembler.py` | 澶氭ā鎬佺粍瑁?| Text + Image Base64 缂栫爜锛孧CP 澶氬唴瀹圭被鍨?|
| `trace_context.py` | 杩借釜涓婁笅鏂?| trace_id 鐢熸垚锛岄樁娈佃褰曪紝finish 姹囨€?|
| `trace_collector.py` | 杩借釜鏀堕泦鍣?| 鏀堕泦 trace 骞惰Е鍙戞寔涔呭寲鍒?JSON Lines |

#### 5.3.3 Scripts 灞傦紙鍛戒护琛屽叆鍙ｏ級

| 鑴氭湰 | 鑱岃矗 | 鍏抽敭鎶€鏈偣 |
|-----|-----|----------|
| `ingest.py` | 绂荤嚎鏁版嵁鎽勫彇鍏ュ彛 | CLI 鍙傛暟瑙ｆ瀽锛岃皟鐢?Ingestion Pipeline锛屾敮鎸?`--collection`/`--path`/`--force` |
| `query.py` | 鍦ㄧ嚎鏌ヨ娴嬭瘯鍏ュ彛 | CLI 鍙傛暟瑙ｆ瀽锛岃皟鐢?HybridSearch + Reranker锛屾敮鎸?`--query`/`--top-k`/`--verbose` |
| `evaluate.py` | 璇勪及杩愯鍏ュ彛 | 鍔犺浇 golden_test_set锛岃繍琛岃瘎浼帮紝杈撳嚭 metrics |
| `start_dashboard.py` | Dashboard 鍚姩鍏ュ彛 | Streamlit 搴旂敤鍚姩 |

#### 5.3.4 Ingestion Pipeline 灞?

| 妯″潡 | 鑱岃矗 | 鍏抽敭鎶€鏈偣 |
|-----|-----|----------|
| `pipeline.py` | Pipeline 娴佺▼缂栨帓 | 涓茶鎵ц锛堟垨鍒嗛樁娈靛彲瑙傛祴锛夛紝寮傚父澶勭悊锛屽閲忔洿鏂帮紱鏀寔 `on_progress` 鍥炶皟锛涚粺涓€浣跨敤 `core/types.py` 鐨勬暟鎹绾?|
| `document_manager.py` | 鏂囨。鐢熷懡鍛ㄦ湡绠＄悊 | list/delete/stats 鎿嶄綔锛涜法 4 涓瓨鍌紙Chroma/BM25/ImageStorage/FileIntegrity锛夌殑鍗忚皟鍒犻櫎锛涗緵 Dashboard 涓?CLI 璋冪敤 |

| `chunking/document_chunker.py` | Document鈫扖hunks 杞崲 | 璋冪敤 `libs.splitter` 杩涜鏂囨湰鍒囧垎锛涚敓鎴愮ǔ瀹?Chunk ID锛堟牸寮忥細`{doc_id}_{index:04d}_{hash}`锛夛紱缁ф壙 metadata锛涘缓绔?source_ref 婧簮閾炬帴 |
| `transform/base_transform.py` | Transform 鎶借薄 | 鍘熷瓙鍖栥€佸箓绛夛紱鍙嫭绔嬮噸璇曪紱澶辫触闄嶇骇涓嶉樆濉?|
| `transform/chunk_refiner.py` | Chunk 鏅鸿兘閲嶇粍 | 瑙勫垯鍘诲櫔 + 鍙€?LLM 浜屾鍔犲伐锛涘彲鍥為€€ |
| `transform/metadata_enricher.py` | 鍏冩暟鎹寮?| Title/Summary/Tags 瑙勫垯鐢熸垚 + 鍙€?LLM 澧炲己 |
| `transform/image_captioner.py` | 鍥剧墖鎻忚堪鐢熸垚 | Vision LLM锛涘啓鍥?metadata/text锛涚鐢?澶辫触闄嶇骇 |
| `embedding/dense_encoder.py` | 绋犲瘑鍚戦噺缂栫爜 | 閫氳繃 `libs.embedding` 璋冪敤鍏蜂綋 provider锛涙壒澶勭悊 |
| `embedding/sparse_encoder.py` | 绋€鐤忓悜閲忕紪鐮?| BM25 缂栫爜/缁熻锛堟垨鏇挎崲瀹炵幇锛夛紱鎵瑰鐞?|
| `storage/vector_upserter.py` | 鍚戦噺瀛樺偍鍐欏叆 | 閫氳繃 `libs.vector_store` Upsert锛涘箓绛夛紱metadata 瀹屾暣 |

#### 5.3.5 Libs 灞?(鍙彃鎷旀娊璞?

| 鎶借薄鎺ュ彛 | 褰撳墠榛樿瀹炵幇 | 鍙浛鎹㈤€夐」 |
|---------|------------|----------|
| `LLMClient` | Azure OpenAI | OpenAI / Ollama / DeepSeek |
| `VisionLLMClient` | Azure OpenAI Vision (GPT-4o) | OpenAI Vision / Ollama Vision (LLaVA) |
| `EmbeddingClient` | OpenAI text-embedding-3 | BGE / Ollama 鏈湴妯″瀷 |
| `Loader` | PDF Loader锛圡arkItDown锛?| Markdown/HTML/Code Loader 绛?|
| `FileIntegrity` | SQLite (`data/db/ingestion_history.db`) | Redis锛堝垎甯冨紡锛? PostgreSQL锛堜紒涓氱骇锛? JSON鏂囦欢锛堟祴璇曪級 |
| `Splitter` | RecursiveCharacterTextSplitter | Semantic / FixedLen |
| `VectorStore` | Chroma | Qdrant / Pinecone / Milvus |
| `Reranker` | CrossEncoder | LLM Rerank / None (鍏抽棴) |
| `Evaluator` | Ragas | DeepEval / 鑷畾涔夋寚鏍?|

#### 5.3.6 Observability 灞?

| 妯″潡 | 鑱岃矗 | 鍏抽敭鎶€鏈偣 |
|-----|-----|----------|
| `logger.py` | 缁撴瀯鍖栨棩蹇?| JSON Formatter锛孞SON Lines 杈撳嚭 |
| `trace_context.py` | 璇锋眰绾ц拷韪?| trace_id锛宼race_type锛坬uery/ingestion锛夛紝闃舵鑰楁椂璁板綍锛宍finish()` + `to_dict()` 搴忓垪鍖?|
| `trace_collector.py` | 杩借釜鏀堕泦鍣?| 鏀堕泦 trace 骞惰Е鍙戞寔涔呭寲鍒?JSON Lines |
| `dashboard/app.py` | Dashboard 鍏ュ彛 | Streamlit 澶氶〉闈㈠簲鐢紝`st.navigation` 椤甸潰娉ㄥ唽 |
| `dashboard/pages/overview.py` | 绯荤粺鎬昏 | 缁勪欢閰嶇疆鍗＄墖锛屾暟鎹祫浜х粺璁?|
| `dashboard/pages/data_browser.py` | 鏁版嵁娴忚鍣?| 鏂囨。鍒楄〃锛孋hunk 璇︽儏锛屽浘鐗囬瑙?|
| `dashboard/pages/ingestion_manager.py` | Ingestion 绠＄悊 | 鏂囦欢涓婁紶锛屾憚鍙栬Е鍙戯紙杩涘害鏉★級锛屾枃妗ｅ垹闄?|
| `dashboard/pages/ingestion_traces.py` | Ingestion 杩借釜 | 鎽勫彇鍘嗗彶锛岄樁娈佃€楁椂鐎戝竷鍥?|
| `dashboard/pages/query_traces.py` | Query 杩借釜 | 鏌ヨ鍘嗗彶锛孌ense/Sparse 瀵规瘮锛孯erank 鍙樺寲 |
| `dashboard/pages/evaluation_panel.py` | 璇勪及闈㈡澘 | 杩愯璇勪及锛屾寚鏍囧睍绀猴紝鍘嗗彶瓒嬪娍锛圥hase H 瀹炵幇锛?|
| `dashboard/services/trace_service.py` | Trace 鏁版嵁鏈嶅姟 | 瑙ｆ瀽 traces.jsonl锛屾寜 trace_type 鍒嗙被 |
| `dashboard/services/data_service.py` | 鏁版嵁娴忚鏈嶅姟 | 灏佽 ChromaStore/ImageStorage 璇诲彇 |
| `dashboard/services/config_service.py` | 閰嶇疆璇诲彇鏈嶅姟 | 灏佽 Settings 灞曠ず |
| `evaluation/eval_runner.py` | 璇勪及鎵ц | 榛勯噾娴嬭瘯闆嗭紝鎸囨爣璁＄畻锛屾姤鍛婄敓鎴?|
| `evaluation/ragas_evaluator.py` | Ragas 璇勪及 | Faithfulness, Answer Relevancy, Context Precision |
| `evaluation/composite_evaluator.py` | 缁勫悎璇勪及鍣?| 澶氬悗绔苟琛屾墽琛岋紝缁撴灉姹囨€?|


### 5.4 鏁版嵁娴佽鏄?

#### 5.4.1 绂荤嚎鏁版嵁鎽勫彇娴?(Ingestion Flow)

```
鍘熷鏂囨。 (PDF)
      鈹?
      鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鏈彉鏇村垯璺宠繃
鈹?File Integrity  鈹傗攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈻?缁撴潫
鈹?  (SHA256)      鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
         鈹?鏂版枃浠?宸插彉鏇?
         鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?    Loader      鈹? PDF 鈫?Markdown + 鍥剧墖鎻愬彇 + 鍏冩暟鎹敹闆?
鈹?  (MarkItDown)  鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
         鈹?Document (text + metadata.images)
         鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?   Splitter     鈹? 鎸夎涔夎竟鐣屽垏鍒嗭紝淇濈暀鍥剧墖寮曠敤
鈹?(Recursive)     鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
         鈹?Chunks[] (with image_refs)
         鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?  Transform     鈹? LLM 閲嶅啓 + 鍏冩暟鎹敞鍏?+ 鍥剧墖鎻忚堪鐢熸垚
鈹?(Enrichment)    鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
         鈹?Enriched Chunks[] (with captions in text)
         鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?  Embedding     鈹? Dense (OpenAI) + Sparse (BM25) 鍙岃矾缂栫爜
鈹? (Dual Path)    鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
         鈹?Vectors + Chunks + Metadata
         鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?   Upsert       鈹? Chroma Upsert (骞傜瓑) + BM25 Index + 鍥剧墖瀛樺偍
鈹?  (Storage)     鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
```

#### 5.4.2 鍦ㄧ嚎鏌ヨ娴?(Query Flow)

```
鐢ㄦ埛鏌ヨ (via MCP Client)
      鈹?
      鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹? MCP Server     鈹? JSON-RPC 瑙ｆ瀽锛屽伐鍏疯矾鐢?
鈹?(Stdio Transport)鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
         鈹?query + params
         鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?Query Processor 鈹? 鍏抽敭璇嶆彁鍙?+ 鍚屼箟璇嶆墿灞?+ Metadata 瑙ｆ瀽
鈹?                鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
         鈹?processed_query + filters
         鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?             Hybrid Search                  鈹?
鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?         鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?
鈹? 鈹侱ense Retrieval鈹? 骞惰   鈹係parse Retrieval鈹?  鈹?
鈹? 鈹?(Embedding)  鈹傗梽鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈻衡攤  (BM25)     鈹?  鈹?
鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹?         鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹?  鈹?
鈹?        鈹?                       鈹?         鈹?
鈹?        鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?         鈹?
鈹?                 鈻?                         鈹?
鈹?        鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                    鈹?
鈹?        鈹?  Fusion    鈹? RRF 铻嶅悎           鈹?
鈹?        鈹?  (RRF)     鈹?                    鈹?
鈹?        鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹?                    鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
                 鈹?Top-M 鍊欓€?
                 鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?   Reranker     鈹? CrossEncoder / LLM / None
鈹?  (Optional)    鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
         鈹?Top-K 绮炬帓缁撴灉
         鈻?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹?Response Builder鈹? 寮曠敤鐢熸垚 + 鍥剧墖 Base64 缂栫爜 + MCP 鏍煎紡鍖?
鈹?                鈹?
鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
         鈹?MCP Response (TextContent + ImageContent)
         鈻?
杩斿洖缁?MCP Client (Copilot / Claude Desktop)
```

#### 5.4.3 绠＄悊鎿嶄綔娴?(Management Flow)

```
Dashboard (Streamlit UI)
      鈹?
      鈹溾攢鈹€鈹€ 鏁版嵁娴忚 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
      鈹?                                                      鈹?
      鈹?   DataService                                        鈹?
      鈹?   鈹溾攢鈹€ ChromaStore.get_by_metadata(source=...)        鈹?
      鈹?   鈹溾攢鈹€ ImageStorage.list_images(collection, doc_hash) 鈹?
      鈹?   鈹斺攢鈹€ 杩斿洖鏂囨。鍒楄〃 / Chunk 璇︽儏 / 鍥剧墖棰勮            鈹?
      鈹?                                                      鈹?
      鈹溾攢鈹€鈹€ Ingestion 绠＄悊 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
      鈹?                                                      鈹?
      鈹?   瑙﹀彂鎽勫彇锛?                                         鈹?
      鈹?   鈹溾攢鈹€ IngestionPipeline.run(path, collection,        鈹?
      鈹?   鈹?                        on_progress=callback)    鈹?
      鈹?   鈹斺攢鈹€ st.progress() 瀹炴椂鏇存柊杩涘害                      鈹?
      鈹?                                                      鈹?
      鈹?   鍒犻櫎鏂囨。锛?                                         鈹?
      鈹?   鈹溾攢鈹€ DocumentManager.delete_document(source, col)   鈹?
      鈹?   鈹?  鈹溾攢鈹€ ChromaStore.delete_by_metadata(source=...) 鈹?
      鈹?   鈹?  鈹溾攢鈹€ BM25Indexer.remove_document(source=...)    鈹?
      鈹?   鈹?  鈹溾攢鈹€ ImageStorage.delete_images(col, doc_hash)  鈹?
      鈹?   鈹?  鈹斺攢鈹€ FileIntegrity.remove_record(file_hash)     鈹?
      鈹?   鈹斺攢鈹€ 鍒锋柊鏂囨。鍒楄〃                                    鈹?
      鈹?                                                      鈹?
      鈹斺攢鈹€鈹€ Trace 鏌ョ湅 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
           鈹?
           TraceService
           鈹溾攢鈹€ 璇诲彇 logs/traces.jsonl
           鈹溾攢鈹€ 鎸?trace_type 鍒嗙被 (query / ingestion)
           鈹斺攢鈹€ 杩斿洖 Trace 鍒楄〃涓庤鎯?
```

### 5.5 閰嶇疆椹卞姩璁捐


绯荤粺閫氳繃 `config/settings.yaml` 缁熶竴閰嶇疆鍚勭粍浠跺疄鐜帮紝鏀寔闆朵唬鐮佸垏鎹細

```yaml
# config/settings.yaml 绀轰緥

# LLM 閰嶇疆
llm:
  provider: azure           # azure | openai | ollama | deepseek
  model: gpt-4o
  azure_endpoint: "..."
  api_key: "${AZURE_API_KEY}"

# Embedding 閰嶇疆
embedding:
  provider: openai          # openai | azure | ollama (鏈湴)
  model: text-embedding-3-small
  
# Vision LLM 閰嶇疆 (鍥剧墖鎻忚堪)
vision_llm:
  provider: azure           # azure | dashscope (Qwen-VL)
  model: gpt-4o
  
# 鍚戦噺瀛樺偍閰嶇疆
vector_store:
  backend: chroma           # chroma | qdrant | pinecone
  persist_path: ./data/db/chroma

# 妫€绱㈤厤缃?
retrieval:
  sparse_backend: bm25      # bm25 | elasticsearch
  fusion_algorithm: rrf     # rrf | weighted_sum
  top_k_dense: 20
  top_k_sparse: 20
  top_k_final: 10

# 閲嶆帓閰嶇疆
rerank:
  backend: cross_encoder    # none | cross_encoder | llm
  model: cross-encoder/ms-marco-MiniLM-L-6-v2
  top_m: 30

# 璇勪及閰嶇疆
evaluation:
  backends: [ragas, custom]
  golden_test_set: ./tests/fixtures/golden_test_set.json

# 鍙娴嬫€ч厤缃?
observability:
  enabled: true
  log_file: ./logs/traces.jsonl

# Dashboard 绠＄悊骞冲彴閰嶇疆
dashboard:
  enabled: true
  port: 8501                     # Streamlit 鏈嶅姟绔彛
  traces_dir: ./logs             # Trace 鏃ュ織鏂囦欢鐩綍
  auto_refresh: true             # 鏄惁鑷姩鍒锋柊锛堣疆璇㈡柊 trace锛?
  refresh_interval: 5            # 鑷姩鍒锋柊闂撮殧锛堢锛?
```

### 5.6 鎵╁睍鎬ц璁¤鐐?


1. **鏂板 LLM Provider**锛氬疄鐜?`BaseLLM` 鎺ュ彛锛屽湪 `llm_factory.py` 娉ㄥ唽锛岄厤缃枃浠舵寚瀹?`provider` 鍗冲彲
2. **鏂板鏂囨。鏍煎紡**锛氬疄鐜?`BaseLoader` 鎺ュ彛锛屽湪 Pipeline 涓敞鍐屽搴旀枃浠舵墿灞曞悕鐨勫鐞嗗櫒
3. **鏂板妫€绱㈢瓥鐣?*锛氬疄鐜版绱㈡帴鍙ｏ紝鍦?`hybrid_search.py` 涓粍鍚堣皟鐢?
4. **鏂板璇勪及鎸囨爣**锛氬疄鐜?`BaseEvaluator` 鎺ュ彛锛屽湪閰嶇疆涓坊鍔犲埌 `backends` 鍒楄〃


## 6. 椤圭洰鎺掓湡

> **鎺掓湡鍘熷垯锛堜弗鏍煎榻愭湰 DEV_SPEC 鐨勬灦鏋勫垎灞備笌鐩綍缁撴瀯锛?*
> 
> - **鍙寜鏈枃妗ｈ璁¤惤鍦?*锛氫互绗?5.2 鑺傜洰褰曟爲涓衡€滀氦浠樻竻鍗曗€濓紝姣忎竴姝ラ兘瑕佸湪鏂囦欢绯荤粺涓婁骇鐢熷彲瑙佸彉鍖栥€?
> - **1 灏忔椂涓€涓彲楠屾敹澧為噺**锛氭瘡涓皬闃舵锛堚増1h锛夐兘蹇呴』鍚屾椂缁欏嚭鈥滈獙鏀舵爣鍑?+ 娴嬭瘯鏂规硶鈥濓紝灏介噺鍋氬埌 TDD銆?
> - **鍏堟墦閫氫富闂幆锛屽啀琛ラ綈榛樿瀹炵幇**锛氫紭鍏堝仛鈥滃彲璺戦€氱殑绔埌绔矾寰勶紙Ingestion 鈫?Retrieval 鈫?MCP Tool锛夆€濓紝骞跺湪 Libs 灞傝ˉ榻愬彲杩愯鐨勯粯璁ゅ悗绔疄鐜帮紝閬垮厤鍑虹幇鈥滃彧鏈夋帴鍙ｆ病鏈夊疄鐜扳€濈殑绌鸿浆銆?
> - **澶栭儴渚濊禆鍙浛鎹?鍙?Mock**锛歀LM/Embedding/Vision/VectorStore 鐨勭湡瀹炶皟鐢ㄥ湪鍗曞厓娴嬭瘯涓竴寰嬬敤 Fake/Mock锛岄泦鎴愭祴璇曞啀寮€鐪熷疄鍚庣锛堝彲閫夛級銆?

### 闃舵鎬昏锛堝ぇ闃舵 鈫?鐩殑锛?

1. **闃舵 A锛氬伐绋嬮鏋朵笌娴嬭瘯鍩哄骇**
   - 鐩殑锛氬缓绔嬪彲杩愯銆佸彲閰嶇疆銆佸彲娴嬭瘯鐨勫伐绋嬮鏋讹紱鍚庣画鎵€鏈夋ā鍧楅兘鑳戒互 TDD 鏂瑰紡钀藉湴銆?
2. **闃舵 B锛歀ibs 鍙彃鎷斿眰锛團actory + Base 鎺ュ彛 + 榛樿鍙繍琛屽疄鐜帮級**
  - 鐩殑锛氭妸鈥滃彲鏇挎崲鈥濆彉鎴愪唬鐮佷簨瀹烇紱骞惰ˉ榻愬彲杩愯鐨勯粯璁ゅ悗绔疄鐜帮紝纭繚 Core / Ingestion 涓嶄粎鈥滃彲缂栬瘧鈥濓紝杩樺彲鍦ㄧ湡瀹炵幆澧冭窇閫氥€?
3. **闃舵 C锛欼ngestion Pipeline锛圥DF鈫扢D鈫扖hunk鈫扙mbedding鈫扷psert锛?*
  - 鐩殑锛氱绾挎憚鍙栭摼璺窇閫氾紝鑳芥妸鏍蜂緥鏂囨。鍐欏叆鍚戦噺搴?BM25 绱㈠紩骞舵敮鎸佸閲忋€?
4. **闃舵 D锛歊etrieval锛圖ense + Sparse + RRF + 鍙€?Rerank锛?*
  - 鐩殑锛氬湪绾挎煡璇㈤摼璺窇閫氾紝寰楀埌 Top-K chunks锛堝惈寮曠敤淇℃伅锛夛紝骞跺叿澶囩ǔ瀹氬洖閫€绛栫暐銆?
5. **闃舵 E锛歁CP Server 灞備笌 Tools 钀藉湴**
   - 鐩殑锛氭寜 MCP 鏍囧噯鏆撮湶 tools锛岃 Copilot/Claude 鍙洿鎺ヨ皟鐢ㄦ煡璇㈣兘鍔涖€?
6. **闃舵 F锛歍race 鍩虹璁炬柦涓庢墦鐐?*
   - 鐩殑锛氬寮?TraceContext锛屽疄鐜扮粨鏋勫寲鏃ュ織鎸佷箙鍖栵紝鍦?Ingestion + Query 鍙岄摼璺墦鐐癸紝娣诲姞 Pipeline 杩涘害鍥炶皟銆?
7. **闃舵 G锛氬彲瑙嗗寲绠＄悊骞冲彴 Dashboard**
   - 鐩殑锛氭惌寤?Streamlit 鍏〉闈㈢鐞嗗钩鍙帮紙绯荤粺鎬昏 / 鏁版嵁娴忚 / Ingestion 绠＄悊 / Ingestion 杩借釜 / Query 杩借釜 / 璇勪及鍗犱綅锛夛紝瀹炵幇 DocumentManager 璺ㄥ瓨鍌ㄥ崗璋冦€?
8. **闃舵 H锛氳瘎浼颁綋绯?*
   - 鐩殑锛氬疄鐜?RagasEvaluator + CompositeEvaluator + EvalRunner锛屽惎鐢ㄨ瘎浼伴潰鏉块〉闈紝寤虹珛 golden test set 鍥炲綊鍩虹嚎銆?
9. **闃舵 I锛氱鍒扮楠屾敹涓庢枃妗ｆ敹鍙?*
   - 鐩殑锛氳ˉ榻?E2E 娴嬭瘯锛圡CP Client 妯℃嫙 + Dashboard 鍐掔儫锛夛紝瀹屽杽 README锛屽叏閾捐矾楠屾敹锛岀‘淇濃€滃紑绠卞嵆鐢?+ 鍙鐜扳€濄€?


---

### 馃搳 杩涘害璺熻釜琛?(Progress Tracking)

> **鐘舵€佽鏄?*锛歚[ ]` 鏈紑濮?| `[~]` 杩涜涓?| `[x]` 宸插畬鎴?
> 
> **鏇存柊鏃堕棿**锛氭瘡瀹屾垚涓€涓瓙浠诲姟鍚庢洿鏂板搴旂姸鎬?

#### 闃舵 A锛氬伐绋嬮鏋朵笌娴嬭瘯鍩哄骇

| 浠诲姟缂栧彿 | 浠诲姟鍚嶇О | 鐘舵€?| 瀹屾垚鏃ユ湡 | 澶囨敞 |
|---------|---------|------|---------|------|
| A1 | 鍒濆鍖栫洰褰曟爲涓庢渶灏忓彲杩愯鍏ュ彛 | [x] | 2026-04-20 | 宸插畬鎴愰鏋躲€佸崰浣嶆ā鍧椾笌瀵煎叆楠岃瘉 |
| A2 | 寮曞叆 pytest 骞跺缓绔嬫祴璇曠洰褰曠害瀹?| [x] | 2026-04-20 | 宸插缓绔?pytest 鍩哄骇銆乫ixture 鍗犱綅涓庡鍏ュ啋鐑熸祴璇?|
| A3 | 閰嶇疆鍔犺浇涓庢牎楠岋紙Settings锛?| [x] | 2026-04-20 | 宸插疄鐜?YAML 鍔犺浇銆佸瓧娈垫牎楠屻€佸惎鍔ㄦ牎楠屼笌鍗曟祴 |

#### 闃舵 B锛歀ibs 鍙彃鎷斿眰

| 浠诲姟缂栧彿 | 浠诲姟鍚嶇О | 鐘舵€?| 瀹屾垚鏃ユ湡 | 澶囨敞 |
|---------|---------|------|---------|------|
| B1 | LLM 鎶借薄鎺ュ彛涓庡伐鍘?| [x] | 2026-04-21 | 宸插疄鐜?BaseLLM銆丆hatMessage銆丩LMFactory 娉ㄥ唽/鍒涘缓涓庡崟娴?|
| B2 | Embedding 鎶借薄鎺ュ彛涓庡伐鍘?| [x] | 2026-04-21 | 宸插疄鐜?BaseEmbedding銆丒mbeddingFactory 娉ㄥ唽/鍒涘缓涓庡崟娴?|
| B3 | Splitter 鎶借薄鎺ュ彛涓庡伐鍘?| [x] | 2026-04-21 | 宸插疄鐜?BaseSplitter銆丼plitterFactory 娉ㄥ唽/鍒涘缓銆佸弬鏁板墠缃牎楠屼笌琛ュ厖鍗曟祴 |
| B4 | VectorStore 鎶借薄鎺ュ彛涓庡伐鍘?| [x] | 2026-04-22 | 宸插疄鐜?BaseVectorStore銆乂ectorStoreFactory 涓庡绾︽祴璇?|
| B5 | Reranker 鎶借薄鎺ュ彛涓庡伐鍘傦紙鍚?None 鍥為€€锛?| [x] | 2026-04-22 | 宸插疄鐜?BaseReranker銆丷erankerFactory銆丯oneReranker 涓庡崟娴?|
| B6 | Evaluator 鎶借薄鎺ュ彛涓庡伐鍘?| [x] | 2026-04-22 | 宸插疄鐜?BaseEvaluator銆丒valuatorFactory銆丆ustomEvaluator(hit_rate/mrr) 涓庡崟娴?|
| B7.1 | OpenAI-Compatible LLM 瀹炵幇 | [x] | 2026-04-22 | 宸插疄鐜?OpenAI/Azure/DeepSeek provider銆佸伐鍘傝矾鐢变笌 smoke 鍗曟祴锛涘鏌ラ€氳繃锛堝惈 Azure base_url alias 淇锛?|
| B7.2 | Ollama LLM 瀹炵幇 | [x] | 2026-04-22 | 宸插疄鐜?OllamaLLM銆佸伐鍘傝矾鐢变笌杩炴帴澶辫触/瓒呮椂 smoke 鍗曟祴 |
| B7.3 | OpenAI & Azure Embedding 瀹炵幇 | [x] | 2026-04-22 | 宸插疄鐜?OpenAI/Azure Embedding provider銆佸伐鍘傝矾鐢变笌 smoke 鍗曟祴 |
| B7.4 | Ollama Embedding 瀹炵幇 | [x] | 2026-04-22 | 宸插疄鐜?OllamaEmbedding銆佸伐鍘傝矾鐢变笌杩炴帴澶辫触/瓒呮椂 smoke 鍗曟祴 |
| B7.5 | Recursive Splitter 榛樿瀹炵幇 | [x] | 2026-04-22 | 宸插疄鐜?RecursiveSplitter銆佸伐鍘傚唴缃矾鐢变笌 markdown 鍒囧垎鍗曟祴锛涘鏌ラ€氳繃锛堝惈 custom separators 淇锛?|
| B7.6 | ChromaStore 榛樿瀹炵幇 | [x] | 2026-04-22 | 宸插疄鐜?ChromaStore 鎸佷箙鍖栥€佸伐鍘傚唴缃矾鐢便€乺oundtrip 闆嗘垚娴嬭瘯涓?embedding signature 涓€鑷存€ф満鍒?|
| B7.7 | LLM Reranker 瀹炵幇 | [x] | 2026-04-22 | 宸插疄鐜?LLMReranker锛坧rompt 鏂囦欢璇诲彇銆佷弗鏍?ranked_ids schema 瑙ｆ瀽锛夈€佸伐鍘?llm 鍐呯疆璺敱锛涗慨澶嶇┖/缂哄け id 涓庨噸澶?id 鍊欓€変涪澶遍棶棰樺苟琛ラ綈缁煎悎鍗曟祴 |
| B7.8 | Cross-Encoder Reranker 瀹炵幇 | [x] | 2026-04-28 | 宸插疄鐜?CrossEncoderReranker锛圱op-M 閲嶆帓銆佸彲娉ㄥ叆 scorer銆侀粯璁ゅ彲杩愯鎵撳垎锛夈€佸伐鍘?cross_encoder 鍐呯疆璺敱涓庤秴鏃?澶辫触鍥為€€淇″彿 |
| B8 | Vision LLM 鎶借薄鎺ュ彛涓庡伐鍘傞泦鎴?| [x] | 2026-04-30 | 宸插疄鐜?BaseVisionLLM/ChatResponse銆丩LMFactory.create_vision_llm/register_vision 璺敱鑳藉姏涓?vision 宸ュ巶鍗曟祴 |
| B9 | Azure Vision LLM 瀹炵幇 | [x] | 2026-04-30 | 宸插疄鐜?AzureVisionLLM锛堣矾寰?base64 杈撳叆銆乵ax_image_size 鍘嬬缉閽╁瓙銆丄zure 閿欒鐮佸寘瑁咃級锛屽苟鎺ュ叆 vision 宸ュ巶鍐呯疆 azure 璺敱 |

#### 闃舵 C锛欼ngestion Pipeline MVP

| 浠诲姟缂栧彿 | 浠诲姟鍚嶇О | 鐘舵€?| 瀹屾垚鏃ユ湡 | 澶囨敞 |
|---------|---------|------|---------|------|
| C1 | 瀹氫箟鏍稿績鏁版嵁绫诲瀷/濂戠害锛圖ocument/Chunk/ChunkRecord锛?| [x] | 2026-05-25 | 宸插疄鐜?Document/Chunk/ChunkRecord 濂戠害銆乵etadata.images 缁撴瀯鏍￠獙銆佸浘鐗囧崰浣嶇瑙勮寖涓庡簭鍒楀寲鍗曟祴 |
| C2 | 鏂囦欢瀹屾暣鎬ф鏌ワ紙SHA256锛?| [x] | 2026-05-25 | 宸插疄鐜?FileIntegrityChecker 鎶借薄涓?SQLiteIntegrityChecker锛圵AL銆乭ash 鍘婚噸鍒ゅ畾銆乻uccess/failed 鏍囪锛夊強鍗曟祴 |
| C3 | Loader 鎶借薄鍩虹被涓?PDF Loader | [x] | 2026-05-25 | 宸插疄鐜?BaseLoader 鎶借薄鎺ュ彛銆丳dfLoader 鏈€灏忚涓猴紙Document 濂戠害銆佸浘鐗囧崰浣嶇鍚堝苟銆佸浘鐗囨彁鍙栧け璐ラ檷绾э級鍙婂绾﹀崟娴?|
| C4 | Splitter integration (via Libs) | [x] | 2026-05-25 | Implemented `DocumentChunker` adapter and added C4 unit/contract tests; included in unified C4/C5 regression run. |
| C5 | Transform base + ChunkRefiner | [x] | 2026-05-25 | Implemented `BaseTransform` + `ChunkRefiner` (rule cleanup, optional LLM refine, graceful fallback); unified run result: unit 26 passed, integration 2 skipped (missing OPENAI_API_KEY). |
| C6 | MetadataEnricher | [x] | 2026-05-25 | Implemented `MetadataEnricher` (rule-based metadata + optional LLM enrichment + graceful fallback); review recheck passed (unit 10 passed, fallback_count repro fixed). |
| C7 | ImageCaptioner | [x] | 2026-05-25 | Implemented `ImageCaptioner` (optional vision LLM captioning + graceful fallback for disabled/unavailable/error paths); C7 review passed with `tests/unit/test_image_captioner_fallback.py` (6 passed). |
| C8 | DenseEncoder | [x] | 2026-05-26 | Implemented `DenseEncoder` (batch embedding via `libs.embedding`, `ChunkRecord` output, configurable `batch_size`, trace metrics); C8 review passed with `tests/unit/test_dense_encoder.py` (7 passed). |
| C9 | SparseEncoder | [x] | 2026-05-26 | Implemented `SparseEncoder` (BM25-style sparse term weights, configurable `k1/b/min_token_length/remove_stopwords`, trace metrics); C9 review passed with `tests/unit/test_sparse_encoder.py` (7 passed). |
| C10 | BatchProcessor | [x] | 2026-05-26 | Implemented `BatchProcessor` (batch orchestration for dense/sparse encoders, per-batch elapsed metrics, merge validation); recheck passed with extended C8/C9/C10 suite (`28 passed`). |
| C11 | BM25Indexer锛堝€掓帓绱㈠紩+IDF璁＄畻锛?| [ ] | | |
| C12 | VectorUpserter锛堝箓绛塽psert锛?| [ ] | | |
| C13 | ImageStorage锛堝浘鐗囧瓨鍌?SQLite绱㈠紩锛?| [ ] | | |
| C14 | Pipeline 缂栨帓锛圡VP 涓茶捣鏉ワ級 | [ ] | | |
| C15 | 鑴氭湰鍏ュ彛 ingest.py | [ ] | | |

#### 闃舵 D锛歊etrieval MVP

| 浠诲姟缂栧彿 | 浠诲姟鍚嶇О | 鐘舵€?| 瀹屾垚鏃ユ湡 | 澶囨敞 |
|---------|---------|------|---------|------|
| D1 | QueryProcessor锛堝叧閿瘝鎻愬彇 + filters锛?| [ ] | | |
| D2 | DenseRetriever锛堣皟鐢?VectorStore.query锛?| [ ] | | |
| D3 | SparseRetriever锛圔M25 鏌ヨ锛?| [ ] | | |
| D4 | RRF Fusion | [ ] | | |
| D5 | HybridSearch 缂栨帓 | [ ] | | |
| D6 | Reranker锛圕ore 灞傜紪鎺?+ Fallback锛?| [ ] | | |
| D7 | 鑴氭湰鍏ュ彛 query.py锛堟煡璇㈠彲鐢級 | [ ] | | |

#### 闃舵 E锛歁CP Server 灞備笌 Tools

| 浠诲姟缂栧彿 | 浠诲姟鍚嶇О | 鐘舵€?| 瀹屾垚鏃ユ湡 | 澶囨敞 |
|---------|---------|------|---------|------|
| E1 | MCP Server 鍏ュ彛涓?Stdio 绾︽潫 | [ ] | | |
| E2 | Protocol Handler 鍗忚瑙ｆ瀽涓庤兘鍔涘崗鍟?| [ ] | | |
| E3 | query_knowledge_hub Tool | [ ] | | |
| E4 | list_collections Tool | [ ] | | |
| E5 | get_document_summary Tool | [ ] | | |
| E6 | 澶氭ā鎬佽繑鍥炵粍瑁咃紙Text + Image锛?| [ ] | | |

#### 闃舵 F锛歍race 鍩虹璁炬柦涓庢墦鐐?

| 浠诲姟缂栧彿 | 浠诲姟鍚嶇О | 鐘舵€?| 瀹屾垚鏃ユ湡 | 澶囨敞 |
|---------|---------|------|---------|------|
| F1 | TraceContext 澧炲己锛坒inish + 鑰楁椂缁熻 + trace_type锛?| [ ] | | |
| F2 | 缁撴瀯鍖栨棩蹇?logger锛圝SON Lines锛?| [ ] | | |
| F3 | 鍦?Query 閾捐矾鎵撶偣 | [ ] | | |
| F4 | 鍦?Ingestion 閾捐矾鎵撶偣 | [ ] | | |
| F5 | Pipeline 杩涘害鍥炶皟 (on_progress) | [ ] | | |

#### 闃舵 G锛氬彲瑙嗗寲绠＄悊骞冲彴 Dashboard

| 浠诲姟缂栧彿 | 浠诲姟鍚嶇О | 鐘舵€?| 瀹屾垚鏃ユ湡 | 澶囨敞 |
|---------|---------|------|---------|------|
| G1 | Dashboard 鍩虹鏋舵瀯涓庣郴缁熸€昏椤?| [ ] | | |
| G2 | DocumentManager 瀹炵幇 | [ ] | | |
| G3 | 鏁版嵁娴忚鍣ㄩ〉闈?| [ ] | | |
| G4 | Ingestion 绠＄悊椤甸潰 | [ ] | | |
| G5 | Ingestion 杩借釜椤甸潰 | [ ] | | |
| G6 | Query 杩借釜椤甸潰 | [ ] | | |

#### 闃舵 H锛氳瘎浼颁綋绯?

| 浠诲姟缂栧彿 | 浠诲姟鍚嶇О | 鐘舵€?| 瀹屾垚鏃ユ湡 | 澶囨敞 |
|---------|---------|------|---------|------|
| H1 | RagasEvaluator 瀹炵幇 | [ ] | | |
| H2 | CompositeEvaluator 瀹炵幇 | [ ] | | |
| H3 | EvalRunner + Golden Test Set | [ ] | | |
| H4 | 璇勪及闈㈡澘椤甸潰 | [ ] | | |
| H5 | Recall 鍥炲綊娴嬭瘯锛圗2E锛?| [ ] | | |

#### 闃舵 I锛氱鍒扮楠屾敹涓庢枃妗ｆ敹鍙?

| 浠诲姟缂栧彿 | 浠诲姟鍚嶇О | 鐘舵€?| 瀹屾垚鏃ユ湡 | 澶囨敞 |
|---------|---------|------|---------|------|
| I1 | E2E锛歁CP Client 渚ц皟鐢ㄦā鎷?| [ ] | | |
| I2 | E2E锛欴ashboard 鍐掔儫娴嬭瘯 | [ ] | | |
| I3 | 瀹屽杽 README锛堣繍琛岃鏄?+ MCP + Dashboard锛?| [ ] | | |
| I4 | 娓呯悊鎺ュ彛涓€鑷存€э紙濂戠害娴嬭瘯琛ラ綈锛?| [ ] | | |
| I5 | 鍏ㄩ摼璺?E2E 楠屾敹 | [ ] | | |

---

### 馃搱 鎬讳綋杩涘害

| 闃舵 | 鎬讳换鍔℃暟 | 宸插畬鎴?| 杩涘害 |
|------|---------|--------|------|
| 闃舵 A | 3 | 3 | 100% |
| 闃舵 B | 16 | 16 | 100% |
| 闃舵 C | 15 | 3 | 20% |
| 闃舵 D | 7 | 0 | 0% |
| 闃舵 E | 6 | 0 | 0% |
| 闃舵 F | 5 | 0 | 0% |
| 闃舵 G | 6 | 0 | 0% |
| 闃舵 H | 5 | 0 | 0% |
| 闃舵 I | 5 | 0 | 0% |
| **鎬昏** | **68** | **22** | **32%** |


---

## 闃舵 A锛氬伐绋嬮鏋朵笌娴嬭瘯鍩哄骇锛堢洰鏍囷細鍏堝彲瀵煎叆锛屽啀鍙祴璇曪級

### A1锛氬垵濮嬪寲鐩綍鏍戜笌鏈€灏忓彲杩愯鍏ュ彛
- **鐩爣**锛氬湪 repo 鏍圭洰褰曞垱寤虹 5.2 鑺傛墍杩扮洰褰曢鏋朵笌绌烘ā鍧楁枃浠讹紙鍙?import锛夈€?
- **淇敼鏂囦欢**锛?
  - `main.py`
  - `pyproject.toml`
  - `README.md`
  - `.gitignore`锛圥ython 椤圭洰鏍囧噯蹇界暐瑙勫垯锛歚__pycache__`銆乣.venv`銆乣.env`銆乣*.pyc`銆両DE 閰嶇疆绛夛級
  - `src/**/__init__.py`锛堟寜鐩綍鏍戣ˉ榻愶級
  - `config/settings.yaml`锛堟渶灏忓彲瑙ｆ瀽閰嶇疆锛?
  - `config/prompts/image_captioning.txt`锛堝彲鍏堟斁鍗犱綅鍐呭锛屽悗缁樁娈佃ˉ鍏?Prompt锛?
  - `config/prompts/chunk_refinement.txt`锛堝彲鍏堟斁鍗犱綅鍐呭锛屽悗缁樁娈佃ˉ鍏?Prompt锛?
  - `config/prompts/rerank.txt`锛堝彲鍏堟斁鍗犱綅鍐呭锛屽悗缁樁娈佃ˉ鍏?Prompt锛?
- **瀹炵幇绫?鍑芥暟**锛氭棤锛堜粎楠ㄦ灦锛夈€?
- **瀹炵幇绫?鍑芥暟**锛氭棤锛堜粎楠ㄦ灦锛屼笉瀹炵幇涓氬姟閫昏緫锛夈€?
- **瀹炵幇绫?鍑芥暟**锛氫负褰撳墠椤圭洰鍒涘缓涓€涓櫄鎷熺幆澧冩ā鍧椼€?
 - **楠屾敹鏍囧噯**锛?
  - 鐩綍缁撴瀯涓?DEV_SPEC 5.2 涓€鑷达紙鑷冲皯鎶婂搴旂洰褰曞垱寤哄嚭鏉ワ級銆?
  - `config/prompts/` 鐩綍瀛樺湪锛屼笖涓変釜 prompt 鏂囦欢鍙璇诲彇锛堝嵆浣垮彧鏄崰浣嶆枃鏈級銆?
  - 鑳藉鍏ュ叧閿《灞傚寘锛堜笌鐩綍缁撴瀯涓€涓€瀵瑰簲锛夛細
    - `python -c "import mcp_server; import core; import ingestion; import libs; import observability"`
  - 鍙互鍚姩铏氭嫙鐜妯″潡
- **娴嬭瘯鏂规硶**锛氳繍琛?`python -m compileall src`锛堜粎鍋氳娉?鍙鍏ユ€ф鏌ワ紱pytest 鍩哄骇鍦?A2 寤虹珛锛夈€?

### A2锛氬紩鍏?pytest 骞跺缓绔嬫祴璇曠洰褰曠害瀹?
- **鐩爣**锛氬缓绔?`tests/unit|integration|e2e|fixtures` 鐩綍涓?pytest 杩愯鍩哄骇銆?
- **淇敼鏂囦欢**锛?
  - `pyproject.toml`锛堟坊鍔?pytest 閰嶇疆锛歵estpaths銆乵arkers 绛夛級
  - `tests/unit/test_smoke_imports.py`
  - `tests/fixtures/sample_documents/`锛堟斁 1 涓渶灏忔牱渚嬫枃妗ｅ崰浣嶏級
- **瀹炵幇绫?鍑芥暟**锛氭棤銆?
- **瀹炵幇绫?鍑芥暟**锛氭棤锛堟柊澧炵殑鏄祴璇曟枃浠朵笌 pytest 閰嶇疆锛夈€?
- **楠屾敹鏍囧噯**锛?
  - `pytest -q` 鍙繍琛屽苟閫氳繃銆?
  - 鑷冲皯 1 涓啋鐑熸祴璇曪紙渚嬪 `tests/unit/test_smoke_imports.py` 鍙仛鍏抽敭鍖?import 鏍￠獙锛夈€?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_smoke_imports.py`銆?

### A3锛氶厤缃姞杞戒笌鏍￠獙锛圫ettings锛?
- **鐩爣**锛氬疄鐜拌鍙?`config/settings.yaml` 鐨勯厤缃姞杞藉櫒锛屽苟鍦ㄥ惎鍔ㄦ椂鏍￠獙鍏抽敭瀛楁瀛樺湪銆?
- **淇敼鏂囦欢**锛?
  - `main.py`锛堝惎鍔ㄦ椂璋冪敤 `load_settings()`锛岀己瀛楁鐩存帴 fail-fast 閫€鍑猴級
  - `src/observability/logger.py`锛堝厛鍗犱綅锛氭彁渚?get_logger锛宻tderr 杈撳嚭锛?
  - `src/core/settings.py`锛堟柊澧烇細闆嗕腑鏀?Settings 鏁版嵁缁撴瀯涓庡姞杞?鏍￠獙閫昏緫锛?
  - `config/settings.yaml`锛堣ˉ榻愬瓧娈碉細llm/embedding/vector_store/retrieval/rerank/evaluation/observability锛?
  - `tests/unit/test_config_loading.py`
- **瀹炵幇绫?鍑芥暟**锛?
  - `Settings`锛坉ataclass锛氬彧鍋氱粨鏋勪笌鏈€灏忔牎楠岋紱涓嶅湪杩欓噷鍋氫换浣曠綉缁?IO 鐨勨€滀笟鍔″垵濮嬪寲鈥濓級
  - `load_settings(path: str) -> Settings`锛堣鍙?YAML -> 瑙ｆ瀽涓?Settings -> 鏍￠獙蹇呭～瀛楁锛?
  - `validate_settings(settings: Settings) -> None`锛堟妸鈥滃繀濉瓧娈垫鏌モ€濋泦涓寲锛岄敊璇俊鎭寘鍚瓧娈佃矾寰勶紝渚嬪 `embedding.provider`锛?
- **楠屾敹鏍囧噯**锛?
  - `main.py` 鍚姩鏃惰兘鎴愬姛鍔犺浇 `config/settings.yaml` 骞舵嬁鍒?`Settings` 瀵硅薄銆?
  - 鍒犻櫎/缂哄け鍏抽敭瀛楁鏃讹紙渚嬪 `embedding.provider`锛夛紝鍚姩鎴?`load_settings()` 鎶涘嚭鈥滃彲璇婚敊璇€濓紙鏄庣‘鎸囧嚭缂虹殑鏄摢涓瓧娈碉級銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_config_loading.py`銆?

---

## 闃舵 B锛歀ibs 鍙彃鎷斿眰锛堢洰鏍囷細Factory 鍙伐浣滐紝涓旇嚦灏戞湁鈥滈粯璁ゅ悗绔€濆彲璺戦€氱鍒扮锛?

### B1锛歀LM 鎶借薄鎺ュ彛涓庡伐鍘?
- **鐩爣**锛氬畾涔?`BaseLLM` 涓?`LLMFactory`锛屾敮鎸佹寜閰嶇疆閫夋嫨 provider銆?
- **淇敼鏂囦欢**锛?
  - `src/libs/llm/base_llm.py`
  - `src/libs/llm/llm_factory.py`
  - `tests/unit/test_llm_factory.py`
- **瀹炵幇绫?鍑芥暟**锛?
  - `BaseLLM.chat(messages) -> str`锛堟垨缁熶竴 response 瀵硅薄锛?
  - `LLMFactory.create(settings) -> BaseLLM`
- **楠屾敹鏍囧噯**锛氬湪娴嬭瘯閲岀敤 Fake provider锛堟祴璇曞唴 stub锛夐獙璇佸伐鍘傝矾鐢遍€昏緫銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_llm_factory.py`銆?

### B2锛欵mbedding 鎶借薄鎺ュ彛涓庡伐鍘?
- **鐩爣**锛氬畾涔?`BaseEmbedding` 涓?`EmbeddingFactory`锛屾敮鎸佹壒閲?embed銆?
- **淇敼鏂囦欢**锛?
  - `src/libs/embedding/base_embedding.py`
  - `src/libs/embedding/embedding_factory.py`
  - `tests/unit/test_embedding_factory.py`
- **瀹炵幇绫?鍑芥暟**锛?
  - `BaseEmbedding.embed(texts: list[str], trace: TraceContext | None = None) -> list[list[float]]`
  - `EmbeddingFactory.create(settings) -> BaseEmbedding`
- **楠屾敹鏍囧噯**锛欶ake embedding 杩斿洖绋冲畾鍚戦噺锛屽伐鍘傛寜 provider 鍒嗘祦銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_embedding_factory.py`銆?

### B3锛歋plitter 鎶借薄鎺ュ彛涓庡伐鍘?
- **鐩爣**锛氬畾涔?`BaseSplitter` 涓?`SplitterFactory`锛屾敮鎸佷笉鍚屽垏鍒嗙瓥鐣ワ紙Recursive/Semantic/Fixed锛夈€?
- **淇敼鏂囦欢**锛?
  - `src/libs/splitter/base_splitter.py`
  - `src/libs/splitter/splitter_factory.py`
  - `tests/unit/test_splitter_factory.py`
- **瀹炵幇绫?鍑芥暟**锛?
  - `BaseSplitter.split_text(text: str, trace: TraceContext | None = None) -> List[str]`
  - `SplitterFactory.create(settings) -> BaseSplitter`
- **楠屾敹鏍囧噯**锛欶actory 鑳芥牴鎹厤缃繑鍥炰笉鍚岀被鍨嬬殑 Splitter 瀹炰緥锛堟祴璇曚腑鍙敤 Fake 瀹炵幇锛夈€?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_splitter_factory.py`銆?

### B4锛歏ectorStore 鎶借薄鎺ュ彛涓庡伐鍘傦紙鍏堝畾涔夊绾︼級
- **鐩爣**锛氬畾涔?`BaseVectorStore` 涓?`VectorStoreFactory`锛屽厛涓嶆帴鐪熷疄 DB銆?
- **淇敼鏂囦欢**锛?
  - `src/libs/vector_store/base_vector_store.py`
  - `src/libs/vector_store/vector_store_factory.py`
  - `tests/unit/test_vector_store_contract.py`
- **瀹炵幇绫?鍑芥暟**锛?
  - `BaseVectorStore.upsert(records, trace: TraceContext | None = None)`
  - `BaseVectorStore.query(vector, top_k, filters, trace: TraceContext | None = None)`
- **楠屾敹鏍囧噯**锛氬绾︽祴璇曪紙contract test锛夌害鏉熻緭鍏ヨ緭鍑?shape銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_vector_store_contract.py`銆?

### B5锛歊eranker 鎶借薄鎺ュ彛涓庡伐鍘傦紙鍚?None 鍥為€€锛?
- **鐩爣**锛氬疄鐜?`BaseReranker`銆乣RerankerFactory`锛屾彁渚?`NoneReranker` 浣滀负榛樿鍥為€€銆?
- **淇敼鏂囦欢**锛?
  - `src/libs/reranker/base_reranker.py`
  - `src/libs/reranker/reranker_factory.py`
  - `tests/unit/test_reranker_factory.py`
- **瀹炵幇绫?鍑芥暟**锛?
  - `BaseReranker.rerank(query, candidates, trace: TraceContext | None = None) -> ranked_candidates`
  - `NoneReranker`锛堜繚鎸佸師椤哄簭锛?
- **楠屾敹鏍囧噯**锛歜ackend=none 鏃朵笉浼氭敼鍙樻帓搴忥紱鏈煡 backend 鏄庣‘鎶ラ敊銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_reranker_factory.py`銆?

### B6锛欵valuator 鎶借薄鎺ュ彛涓庡伐鍘傦紙鍏堝仛鑷畾涔夎交閲忔寚鏍囷級
- **鐩爣**锛氬畾涔?`BaseEvaluator`銆乣EvaluatorFactory`锛屽疄鐜版渶灏?`CustomEvaluator`锛堜緥濡?hit_rate/mrr锛夈€?
- **淇敼鏂囦欢**锛?
  - `src/libs/evaluator/base_evaluator.py`
  - `src/libs/evaluator/evaluator_factory.py`
  - `src/libs/evaluator/custom_evaluator.py`
  - `tests/unit/test_custom_evaluator.py`
- **楠屾敹鏍囧噯**锛氳緭鍏?query + retrieved_ids + golden_ids 鑳借緭鍑虹ǔ瀹?metrics銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_custom_evaluator.py`銆?

### B7锛氳ˉ榻?Libs 榛樿瀹炵幇锛堟媶鍒嗕负鈮?h鍙獙鏀跺閲忥級

> 璇存槑锛欱7 鍙ˉ榻愪笌绔埌绔富閾捐矾寮虹浉鍏崇殑榛樿瀹炵幇锛圠LM/Embedding/Splitter/VectorStore/Reranker锛夈€傚叾浣欏彲閫夋墿灞曪紙渚嬪棰濆 splitter 绛栫暐銆佹洿澶?vector store 鍚庣銆佹洿澶?evaluator 鍚庣绛夛級淇濇寔鍘熸帓鏈熶笉鎻愬墠銆?

### B7.1锛歄penAI-Compatible LLM锛圤penAI/Azure/DeepSeek锛?
- **鐩爣**锛氳ˉ榻?OpenAI-compatible 鐨?LLM 瀹炵幇锛岀‘淇濋€氳繃 `LLMFactory` 鍙垱寤哄苟鍙 mock 娴嬭瘯銆?
- **淇敼鏂囦欢**锛?
  - `src/libs/llm/openai_llm.py`
  - `src/libs/llm/azure_llm.py`
  - `src/libs/llm/deepseek_llm.py`
  - `tests/unit/test_llm_providers_smoke.py`锛坢ock HTTP锛屼笉璧扮湡瀹炵綉缁滐級
- **楠屾敹鏍囧噯**锛?
  - 閰嶇疆涓嶅悓 `provider` 鏃跺伐鍘傝矾鐢辨纭€?
  - `chat(messages)` 瀵硅緭鍏?shape 鏍￠獙娓呮櫚锛屽紓甯镐俊鎭彲璇伙紙鍖呭惈 provider 涓庨敊璇被鍨嬶級銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_llm_providers_smoke.py`銆?

### B7.2锛歄llama LLM锛堟湰鍦板悗绔級
- **鐩爣**锛氳ˉ榻?`ollama_llm.py`锛屾敮鎸佹湰鍦?HTTP endpoint锛堥粯璁?`base_url` + `model`锛夛紝骞跺彲琚?mock 娴嬭瘯銆?
- **淇敼鏂囦欢**锛?
  - `src/libs/llm/ollama_llm.py`
  - `tests/unit/test_ollama_llm.py`锛坢ock HTTP锛?
- **楠屾敹鏍囧噯**锛?
  - provider=ollama 鏃跺彲鐢?`LLMFactory` 鍒涘缓銆?
  - 鍦ㄨ繛鎺ュけ璐?瓒呮椂绛夊満鏅笅锛屾姏鍑哄彲璇婚敊璇笖涓嶆硠闇叉晱鎰熼厤缃€?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_ollama_llm.py`銆?

### B7.3锛歄penAI & Azure Embedding 瀹炵幇
- **鐩爣**锛氳ˉ榻?`openai_embedding.py` 鍜?`azure_embedding.py`锛屾敮鎸?OpenAI 瀹樻柟 API 鍜?Azure OpenAI 鏈嶅姟鐨?Embedding 璋冪敤锛屾敮鎸佹壒閲?`embed(texts)`锛屽苟鍙 mock 娴嬭瘯銆?
- **淇敼鏂囦欢**锛?
  - `src/libs/embedding/openai_embedding.py`
  - `src/libs/embedding/azure_embedding.py`
  - `tests/unit/test_embedding_providers_smoke.py`锛坢ock HTTP锛屽寘鍚?OpenAI 鍜?Azure 娴嬭瘯鐢ㄤ緥锛?
- **楠屾敹鏍囧噯**锛?
  - provider=openai 鏃?`EmbeddingFactory` 鍙垱寤猴紝鏀寔 OpenAI 瀹樻柟 API 鐨?text-embedding-3-small/large 绛夋ā鍨嬨€?
  - provider=azure 鏃?`EmbeddingFactory` 鍙垱寤猴紝姝ｇ‘澶勭悊 Azure 鐗规湁鐨?endpoint銆乤pi-version銆乤pi-key 閰嶇疆锛屾敮鎸?Azure 閮ㄧ讲鐨?text-embedding-ada-002 绛夋ā鍨嬨€?
  - 绌鸿緭鍏ャ€佽秴闀胯緭鍏ユ湁鏄庣‘琛屼负锛堟姤閿欐垨鎴柇绛栫暐鐢遍厤缃喅瀹氾級銆?
  - Azure 瀹炵幇澶嶇敤 OpenAI Embedding 鐨勬牳蹇冮€昏緫锛屼繚鎸佽涓轰竴鑷存€с€?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_embedding_providers_smoke.py`銆?

### B7.4锛歄llama Embedding 瀹炵幇
- **鐩爣**锛氳ˉ榻?`ollama_embedding.py`锛屾敮鎸侀€氳繃 Ollama HTTP API 璋冪敤鏈湴閮ㄧ讲鐨?Embedding 妯″瀷锛堝 `nomic-embed-text`銆乣mxbai-embed-large` 绛夛級锛屽疄鐜?`embed(texts)` 鎵归噺鍚戦噺鍖栧姛鑳姐€?
- **淇敼鏂囦欢**锛?
  - `src/libs/embedding/ollama_embedding.py`
  - `tests/unit/test_ollama_embedding.py`锛堝寘鍚?mock HTTP 娴嬭瘯锛?
- **楠屾敹鏍囧噯**锛?
  - provider=ollama 鏃?`EmbeddingFactory` 鍙垱寤恒€?
  - 鏀寔閰嶇疆 Ollama 鏈嶅姟鍦板潃锛堥粯璁?http://localhost:11434锛夊拰妯″瀷鍚嶇О銆?
  - 杈撳嚭鍚戦噺缁村害鐢辨ā鍨嬪喅瀹氾紙濡?nomic-embed-text 涓?768 缁达級锛屾弧瓒?ingestion/retrieval 鐨勬帴鍙ｅ绾︺€?
  - 鏀寔鎵归噺 `embed(texts)` 璋冪敤锛屽唴閮ㄥ鐞嗗崟鏉?鎵归噺璇锋眰閫昏緫銆?
  - 绌鸿緭鍏ャ€佽秴闀胯緭鍏ユ湁鏄庣‘琛屼负锛堟姤閿欐垨鎴柇绛栫暐锛夈€?
  - mock 娴嬭瘯瑕嗙洊姝ｅ父鍝嶅簲銆佽繛鎺ュけ璐ャ€佽秴鏃剁瓑鍦烘櫙銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_ollama_embedding.py`銆?

### B7.5锛歊ecursive Splitter 榛樿瀹炵幇
- **鐩爣**锛氳ˉ榻?`recursive_splitter.py`锛屽皝瑁?LangChain 鐨勫垏鍒嗛€昏緫锛屼綔涓洪粯璁ゅ垏鍒嗗櫒銆?
- **淇敼鏂囦欢**锛?
  - `src/libs/splitter/recursive_splitter.py`
  - `tests/unit/test_recursive_splitter_lib.py`
- **楠屾敹鏍囧噯**锛?
  - provider=recursive 鏃?`SplitterFactory` 鍙垱寤恒€?
  - `split_text` 鑳芥纭鐞?Markdown 缁撴瀯锛堟爣棰?浠ｇ爜鍧椾笉琚墦鏂級銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_recursive_splitter_lib.py`銆?

### B7.6锛欳hromaStore锛圴ectorStore 榛樿鍚庣锛?
- **鐩爣**锛氳ˉ榻?`chroma_store.py`锛屾敮鎸佹渶灏?`upsert(records)` 涓?`query(vector, top_k, filters)`锛屽苟鏀寔鏈湴鎸佷箙鍖栫洰褰曪紙渚嬪 `data/db/chroma/`锛夈€?
- **淇敼鏂囦欢**锛?
  - `src/libs/vector_store/chroma_store.py`
  - `tests/integration/test_chroma_store_roundtrip.py`
- **楠屾敹鏍囧噯**锛?
  - provider=chroma 鏃?`VectorStoreFactory` 鍙垱寤恒€?
  - **蹇呴』瀹屾垚瀹屾暣鐨?upsert鈫抭uery roundtrip 娴嬭瘯**锛氫娇鐢?mock 鏁版嵁瀹屾垚鐪熷疄鐨勫瓨鍌ㄥ拰妫€绱㈡祦绋嬶紝楠岃瘉杩斿洖缁撴灉鐨勭‘瀹氭€у拰姝ｇ‘鎬с€?
  - 娴嬭瘯搴旇鐩栵細鍩烘湰 upsert銆佸悜閲忔煡璇€乼op_k 鍙傛暟銆乵etadata filters锛堝鏀寔锛夈€?
  - 浣跨敤涓存椂鐩綍杩涜鎸佷箙鍖栨祴璇曪紝娴嬭瘯缁撴潫鍚庢竻鐞嗐€?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/integration/test_chroma_store_roundtrip.py`

### B7.7锛歀LM Reranker锛堣鍙?rerank prompt锛?
- **鐩爣**锛氳ˉ榻?`llm_reranker.py`锛岃鍙?`config/prompts/rerank.txt` 鏋勯€?prompt锛堟祴璇曚腑鍙敞鍏ユ浛浠ｆ枃鏈級锛屽苟鍙湪澶辫触鏃惰繑鍥炲彲鍥為€€淇″彿銆?
- **淇敼鏂囦欢**锛?
  - `src/libs/reranker/llm_reranker.py`
  - `tests/unit/test_llm_reranker.py`锛坢ock LLM锛?
  - `tests/unit/test_llm_reranker_b77_comprehensive.py`锛堢┖/缂哄け id銆侀噸澶?id銆佸伐鍘傞厤缃竟鐣岋級
- **楠屾敹鏍囧噯**锛?
  - backend=llm 鏃?`RerankerFactory` 鍙垱寤恒€?
  - 杈撳嚭涓ユ牸缁撴瀯鍖栵紙渚嬪 ranked ids锛夛紝涓嶆弧瓒?schema 鏃舵姏鍑哄彲璇婚敊璇€?
  - 鍊欓€夐噸鎺掍笉涓㈡暟鎹細绌?缂哄け `id` 涓庨噸澶?`id` 鐨勫€欓€夊潎闇€瀹屾暣淇濈暀锛堜粎閲嶆帓锛屼笉瑁佸壀锛夈€?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_llm_reranker.py tests/unit/test_llm_reranker_b77_comprehensive.py`銆?

### B7.8锛欳ross-Encoder Reranker锛堟湰鍦?鎵樼妯″瀷锛屽崰浣嶅彲璺戯級
- **鐩爣**锛氳ˉ榻?`cross_encoder_reranker.py`锛屾敮鎸佸 Top-M candidates 鎵撳垎鎺掑簭锛涙祴璇曚腑鐢?mock scorer 淇濊瘉 deterministic銆?
- **淇敼鏂囦欢**锛?
  - `src/libs/reranker/cross_encoder_reranker.py`
  - `src/libs/reranker/reranker_factory.py`
  - `src/libs/reranker/__init__.py`
  - `tests/unit/test_cross_encoder_reranker.py`锛坢ock scorer锛?
  - `tests/unit/test_reranker_factory.py`锛坧rovider=cross_encoder 璺敱锛?
- **楠屾敹鏍囧噯**锛?
  - backend=cross_encoder 鏃?`RerankerFactory` 鍙垱寤恒€?
  - 鎻愪緵瓒呮椂/澶辫触鍥為€€淇″彿锛堜緵 Core 灞?`D6` fallback 浣跨敤锛夈€?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_cross_encoder_reranker.py tests/unit/test_reranker_factory.py`銆?

### B8锛歏ision LLM 鎶借薄鎺ュ彛涓庡伐鍘傞泦鎴?
- **鐩爣**锛氬畾涔?`BaseVisionLLM` 鎶借薄鎺ュ彛锛屾墿灞?`LLMFactory` 鏀寔 Vision LLM 鍒涘缓锛屼负 C7 鐨?ImageCaptioner 鎻愪緵搴曞眰鎶借薄銆?
- **淇敼鏂囦欢**锛?
  - `src/libs/llm/base_vision_llm.py`
  - `src/libs/llm/llm_factory.py`锛堟墿灞?`create_vision_llm` 鏂规硶锛?
  - `src/libs/llm/__init__.py`
  - `tests/unit/test_vision_llm_factory.py`
- **瀹炵幇绫?鍑芥暟**锛?
  - `BaseVisionLLM.chat_with_image(text: str, image_path: str | bytes, trace: TraceContext | None = None) -> ChatResponse`
  - `LLMFactory.create_vision_llm(settings) -> BaseVisionLLM`
- **楠屾敹鏍囧噯**锛?
  - 鎶借薄鎺ュ彛娓呮櫚瀹氫箟澶氭ā鎬佽緭鍏ワ紙鏂囨湰+鍥剧墖璺緞/base64锛夈€?
  - 宸ュ巶鏂规硶 `create_vision_llm` 鑳芥牴鎹厤缃矾鐢卞埌涓嶅悓 provider锛堟祴璇曚腑鐢?Fake Vision LLM 楠岃瘉锛夈€?
  - 鎺ュ彛璁捐鏀寔鍥剧墖棰勫鐞嗭紙鍘嬬缉銆佹牸寮忚浆鎹級鐨勬墿灞曠偣銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_vision_llm_factory.py`銆?

### B9锛欰zure Vision LLM 瀹炵幇
- **鐩爣**锛氬疄鐜?`AzureVisionLLM`锛屾敮鎸侀€氳繃 Azure OpenAI 璋冪敤 GPT-4o/GPT-4-Vision-Preview 杩涜鍥惧儚鐞嗚В銆?
- **淇敼鏂囦欢**锛?
  - `src/libs/llm/azure_vision_llm.py`
  - `src/libs/llm/llm_factory.py`
  - `src/libs/llm/__init__.py`
  - `tests/unit/test_azure_vision_llm.py`锛坢ock HTTP锛屼笉璧扮湡瀹?API锛?
  - `tests/unit/test_vision_llm_factory.py`锛坴ision_llm.provider=azure 璺敱楠岃瘉锛?
- **瀹炵幇绫?鍑芥暟**锛?
  - `AzureVisionLLM(BaseVisionLLM)`锛氬疄鐜?`chat_with_image` 鏂规硶
  - 鏀寔 Azure 鐗规湁閰嶇疆锛歚azure_endpoint`, `api_version`, `deployment_name`, `api_key`
- **楠屾敹鏍囧噯**锛?
  - provider=azure 涓旈厤缃?vision_llm 鏃讹紝`LLMFactory.create_vision_llm()` 鍙垱寤?Azure Vision LLM 瀹炰緥銆?
  - 鏀寔鍥剧墖璺緞鍜?base64 涓ょ杈撳叆鏂瑰紡銆?
  - 鍥剧墖杩囧ぇ鏃惰嚜鍔ㄥ帇缂╄嚦 `max_image_size` 閰嶇疆鐨勫昂瀵革紙榛樿2048px锛夈€?
  - API 璋冪敤澶辫触鏃舵姏鍑烘竻鏅伴敊璇紝鍖呭惈 Azure 鐗规湁閿欒鐮併€?
  - mock 娴嬭瘯瑕嗙洊锛氭甯歌皟鐢ㄣ€佸浘鐗囧帇缂┿€佽秴鏃躲€佽璇佸け璐ョ瓑鍦烘櫙銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_azure_vision_llm.py tests/unit/test_vision_llm_factory.py`銆?

---

## 闃舵 C锛欼ngestion Pipeline MVP锛堢洰鏍囷細鑳芥妸 PDF 鏍蜂緥鎽勫彇鍒版湰鍦板瓨鍌級

> 娉細鏈樁娈典弗鏍兼寜 5.4.1 鐨勭绾挎暟鎹祦钀藉湴锛屽苟浼樺厛瀹炵幇鈥滃閲忚烦杩囷紙SHA256锛夆€濄€?

### C1锛氬畾涔夋牳蹇冩暟鎹被鍨?濂戠害锛圖ocument/Chunk/ChunkRecord锛?
- **鐩爣**锛氬畾涔夊叏閾捐矾锛坕ngestion 鈫?retrieval 鈫?mcp tools锛夊叡鐢ㄧ殑鏁版嵁缁撴瀯/濂戠害锛岄伩鍏嶆暎钀藉湪鍚勫瓙妯″潡鍐呭鑷寸殑鑰﹀悎涓庨噸澶嶃€?
- **淇敼鏂囦欢**锛?
  - `src/core/types.py`
  - `src/core/__init__.py`锛堝彲閫夛細缁熶竴 re-export 浠ョ畝鍖栧鍏ヨ矾寰勶級
  - `tests/unit/test_core_types.py`
- **瀹炵幇绫?鍑芥暟**锛堝缓璁級锛?
  - `Document(id, text, metadata)`
  - `Chunk(id, text, metadata, start_offset, end_offset, source_ref?)`
  - `ChunkRecord(id, text, metadata, dense_vector?, sparse_vector?)`锛堢敤浜庡瓨鍌?妫€绱㈣浇浣擄紱瀛楁鎸夊悗缁?C8~C12 婕旇繘锛?
- **楠屾敹鏍囧噯**锛?
  - 绫诲瀷鍙簭鍒楀寲锛坉ict/json锛変笖瀛楁绋冲畾锛堝崟鍏冩祴璇曟柇瑷€锛夈€?
  - `metadata` 绾﹀畾鏈€灏戝寘鍚?`source_path`锛屽叾浣欏瓧娈靛厑璁稿閲忔墿灞曚絾涓嶅緱鐮村潖鍏煎銆?
  - **`metadata.images` 瀛楁瑙勮寖**锛堢敤浜庡妯℃€佹敮鎸侊級锛?
    - 缁撴瀯锛歚List[{"id": str, "path": str, "page": int, "text_offset": int, "text_length": int, "position": dict}]`
    - `id`锛氬叏灞€鍞竴鍥剧墖鏍囪瘑绗︼紙寤鸿鏍煎紡锛歚{doc_hash}_{page}_{seq}`锛?
    - `path`锛氬浘鐗囨枃浠跺瓨鍌ㄨ矾寰勶紙绾﹀畾锛歚data/images/{collection}/{image_id}.png`锛?
    - `page`锛氬浘鐗囧湪鍘熸枃妗ｄ腑鐨勯〉鐮侊紙鍙€夛紝閫傜敤浜嶱DF绛夊垎椤垫枃妗ｏ級
    - `text_offset`锛氬崰浣嶇鍦?`Document.text` 涓殑璧峰瀛楃浣嶇疆锛堜粠0寮€濮嬭鏁帮級
    - `text_length`锛氬崰浣嶇鐨勫瓧绗﹂暱搴︼紙閫氬父涓?`len("[IMAGE: {image_id}]")`锛?
    - `position`锛氬浘鐗囧湪鍘熸枃妗ｄ腑鐨勭墿鐞嗕綅缃俊鎭紙鍙€夛紝濡侾DF鍧愭爣銆佸儚绱犱綅缃€佸昂瀵哥瓑锛?
    - 璇存槑锛氶€氳繃 `text_offset` 鍜?`text_length` 鍙簿纭畾浣嶅浘鐗囧湪鏂囨湰涓殑浣嶇疆锛屾敮鎸佸悓涓€鍥剧墖澶氭鍑虹幇鐨勫満鏅?
  - **鏂囨湰涓浘鐗囧崰浣嶇瑙勮寖**锛氬湪 `Document.text` 涓紝鍥剧墖浣嶇疆浣跨敤 `[IMAGE: {image_id}]` 鏍煎紡鏍囪銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_core_types.py`銆?

### C2锛氭枃浠跺畬鏁存€ф鏌ワ紙SHA256锛?
- **鐩爣**锛氬湪Libs涓疄鐜?`file_integrity.py`锛氳绠楁枃浠?hash锛屽苟鎻愪緵鈥滄槸鍚﹁烦杩団€濈殑鍒ゅ畾鎺ュ彛锛堜娇鐢?SQLite 浣滀负榛樿瀛樺偍锛屾敮鎸佸悗缁浛鎹负 Redis/PostgreSQL锛夈€?
- **淇敼鏂囦欢**锛?
  - `src/libs/loader/file_integrity.py`
  - `tests/unit/test_file_integrity.py`
  - 鏁版嵁搴撴枃浠讹細`data/db/ingestion_history.db`锛堣嚜鍔ㄥ垱寤猴級
- **瀹炵幇绫?鍑芥暟**锛?
  - `FileIntegrityChecker` 绫伙紙鎶借薄鎺ュ彛锛?
  - `SQLiteIntegrityChecker(FileIntegrityChecker)` 绫伙紙榛樿瀹炵幇锛?
    - `compute_sha256(path: str) -> str`
    - `should_skip(file_hash: str) -> bool`
    - `mark_success(file_hash: str, file_path: str, ...)`
    - `mark_failed(file_hash: str, error_msg: str)`
- **楠屾敹鏍囧噯**锛?
  - 鍚屼竴鏂囦欢澶氭璁＄畻hash缁撴灉涓€鑷?
  - 鏍囪 success 鍚庯紝`should_skip` 杩斿洖 `True`
  - 鏁版嵁搴撴枃浠舵纭垱寤哄湪 `data/db/ingestion_history.db`
  - 鏀寔骞跺彂鍐欏叆锛圫QLite WAL妯″紡锛?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_file_integrity.py`銆?

### C3锛歀oader 鎶借薄鍩虹被涓?PDF Loader 澹冲瓙
- **鐩爣**锛氬湪Libs涓畾涔?`BaseLoader`锛屽苟瀹炵幇 `PdfLoader` 鐨勬渶灏忚涓恒€?
- **淇敼鏂囦欢**锛?
  - `src/libs/loader/base_loader.py`
  - `src/libs/loader/pdf_loader.py`
  - `tests/unit/test_loader_pdf_contract.py`
- **瀹炵幇绫?鍑芥暟**锛?
  - `BaseLoader.load(path) -> Document`
  - `PdfLoader.load(path)`
- **楠屾敹鏍囧噯**锛?
  - **鍩虹瑕佹眰**锛氬 sample PDF锛坒ixtures锛夎兘浜у嚭 Document锛宮etadata 鑷冲皯鍚?`source_path`銆?
  - **鍥剧墖澶勭悊瑕佹眰**锛堥伒寰?C1 瀹氫箟鐨勫绾︼級锛?
    - 鑻?PDF 鍖呭惈鍥剧墖锛屽簲鎻愬彇鍥剧墖骞朵繚瀛樺埌 `data/images/{doc_hash}/` 鐩綍
    - 鍦?`Document.text` 涓紝鍥剧墖浣嶇疆鎻掑叆鍗犱綅绗︼細`[IMAGE: {image_id}]`
    - 鍦?`metadata.images` 涓褰曞浘鐗囦俊鎭紙鏍煎紡瑙?C1 瑙勮寖锛?
    - 鑻?PDF 鏃犲浘鐗囷紝`metadata.images` 鍙负绌哄垪琛ㄦ垨鐪佺暐璇ュ瓧娈?
  - **闄嶇骇琛屼负**锛氬浘鐗囨彁鍙栧け璐ヤ笉搴旈樆濉炴枃鏈В鏋愶紝鍙湪鏃ュ織涓褰曡鍛娿€?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_loader_pdf_contract.py`銆?
- **娴嬭瘯寤鸿**锛?
  - 鍑嗗涓や釜娴嬭瘯鏂囦欢锛歚simple.pdf`锛堢函鏂囨湰锛夊拰 `with_images.pdf`锛堝寘鍚浘鐗囷級
  - 楠岃瘉绾枃鏈琍DF鑳芥甯歌В鏋?
  - 楠岃瘉甯﹀浘鐗嘝DF鑳芥彁鍙栧浘鐗囧苟姝ｇ‘鎻掑叆鍗犱綅绗?

### C4锛歋plitter 闆嗘垚锛堣皟鐢?Libs锛?
- **鐩爣**锛氬疄鐜?Chunking 妯″潡浣滀负 `libs.splitter` 鍜?Ingestion Pipeline 涔嬮棿鐨?*閫傞厤鍣ㄥ眰**锛屽畬鎴?Document鈫扖hunks 鐨勪笟鍔″璞¤浆鎹€?
- **鏍稿績鑱岃矗锛圖ocumentChunker 鐩告瘮 libs.splitter 鐨勫鍊硷級**锛?
  - **鑱岃矗杈圭晫璇存槑**锛?
    - `libs.splitter`锛氱函鏂囨湰鍒囧垎宸ュ叿锛坄str 鈫?List[str]`锛夛紝涓嶆秹鍙婁笟鍔″璞?
    - `DocumentChunker`锛氫笟鍔￠€傞厤鍣紙`Document瀵硅薄 鈫?List[Chunk瀵硅薄]`锛夛紝娣诲姞涓氬姟閫昏緫
  - **6 涓鍊煎姛鑳?*锛?
    1. **Chunk ID 鐢熸垚**锛氫负姣忎釜鏂囨湰鐗囨鐢熸垚鍞竴涓旂‘瀹氭€х殑 ID锛堟牸寮忥細`{doc_id}_{index:04d}_{hash_8chars}`锛?
    2. **鍏冩暟鎹户鎵?*锛氬皢 Document.metadata 澶嶅埗鍒版瘡涓?Chunk.metadata锛坰ource_path, doc_type, title 绛夛級
    3. **娣诲姞 chunk_index**锛氳褰?chunk 鍦ㄦ枃妗ｄ腑鐨勫簭鍙凤紙浠?0 寮€濮嬶級锛岀敤浜庢帓搴忓拰瀹氫綅
    4. **寤虹珛 source_ref**锛氳褰?Chunk.source_ref 鎸囧悜鐖?Document.id锛屾敮鎸佹函婧?
    5. **鍥剧墖寮曠敤鎸夐渶鍒嗗彂**锛氭壂鎻忔瘡涓?chunk 鏂囨湰涓殑 `[IMAGE: {id}]` 鍗犱綅绗︼紝浠?`Document.metadata["images"]` 涓彁鍙栬 chunk 瀹為檯寮曠敤鐨?ImageRef锛屽啓鍏?`chunk.metadata["images"]`锛堜粎鍚 chunk 寮曠敤鐨勫瓙闆嗭級鍜?`chunk.metadata["image_refs"]`锛坕mage_id 鍒楄〃锛夈€傛棤鍗犱綅绗︾殑 chunk 涓嶅惈 `images` 瀛楁銆傗殸锔?涓嶅彲绠€鍗曟暣浣撶户鎵挎垨涓㈠純鏂囨。绾?`images`锛屽惁鍒欎笅娓?C7 ImageCaptioner 灏嗘棤娉曞畾浣嶅浘鐗囪矾寰勩€?
    6. **绫诲瀷杞崲**锛氬皢 libs.splitter 鐨?`List[str]` 杞崲涓虹鍚?core.types 濂戠害鐨?`List[Chunk]` 瀵硅薄
- **淇敼鏂囦欢**锛?
  - `src/ingestion/chunking/document_chunker.py`
  - `src/ingestion/chunking/__init__.py`
  - `tests/unit/test_document_chunker.py`
- **瀹炵幇绫?鍑芥暟**锛?
  - `DocumentChunker` 绫?
  - `__init__(settings: Settings)`锛氶€氳繃 SplitterFactory 鑾峰彇閰嶇疆鐨?splitter 瀹炰緥
  - `split_document(document: Document) -> List[Chunk]`锛氬畬鏁寸殑杞崲娴佺▼
  - `_generate_chunk_id(doc_id: str, index: int, text: str) -> str`锛氱敓鎴愮ǔ瀹?Chunk ID
  - `_inherit_metadata(document: Document, chunk_index: int, chunk_text: str) -> dict`锛氬厓鏁版嵁缁ф壙 + 鍥剧墖寮曠敤鎸夐渶鍒嗗彂閫昏緫锛堥渶瑕?chunk_text 鏉ユ壂鎻?`[IMAGE: id]` 鍗犱綅绗︼級
- **楠屾敹鏍囧噯**锛?
  - **閰嶇疆椹卞姩**锛氶€氳繃淇敼 settings.yaml 涓殑 splitter 閰嶇疆锛堝 chunk_size锛夛紝浜у嚭鐨?chunk 鏁伴噺鍜岄暱搴﹀彂鐢熺浉搴斿彉鍖?
  - **ID 鍞竴鎬?*锛氭瘡涓?Chunk 鐨?ID 鍦ㄦ暣涓枃妗ｄ腑鍞竴
  - **ID 纭畾鎬?*锛氬悓涓€ Document 瀵硅薄閲嶅鍒囧垎浜х敓鐩稿悓鐨?Chunk ID 搴忓垪
  - **鍏冩暟鎹畬鏁存€?*锛欳hunk.metadata 鍖呭惈鎵€鏈?Document.metadata 瀛楁 + chunk_index 瀛楁
  - **鍥剧墖鍒嗗彂姝ｇ‘鎬?*锛氬惈 `[IMAGE: id]` 鍗犱綅绗︾殑 chunk 鍏?`metadata["images"]` 浠呭寘鍚 chunk 寮曠敤鐨勫浘鐗囧瓙闆嗭紱涓嶅惈鍗犱綅绗︾殑 chunk 鏃?`images` 瀛楁锛沗metadata["image_refs"]` 鍒楄〃涓庡崰浣嶇涓€鑷?
  - **婧簮閾炬帴**锛氭墍鏈?Chunk.source_ref 姝ｇ‘鎸囧悜鐖?Document.id
  - **绫诲瀷濂戠害**锛氳緭鍑虹殑 Chunk 瀵硅薄绗﹀悎 `core/types.py` 涓殑 Chunk 瀹氫箟锛堝彲搴忓垪鍖栥€佸瓧娈靛畬鏁达級
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_document_chunker.py`锛堜娇鐢?FakeSplitter 闅旂娴嬭瘯锛屾棤闇€鐪熷疄 LLM/澶栭儴渚濊禆锛夈€?

### C5锛歍ransform 鎶借薄鍩虹被 + ChunkRefiner锛堣鍒欏幓鍣?+ LLM 澧炲己锛?
- **鐩爣**锛氬畾涔?`BaseTransform`锛涘疄鐜?`ChunkRefiner`锛氬厛鍋氳鍒欏幓鍣紝鍐嶉€氳繃LLM杩涜鏅鸿兘澧炲己锛屽苟鎻愪緵澶辫触闄嶇骇鏈哄埗锛圠LM寮傚父鏃跺洖閫€鍒拌鍒欑粨鏋滐紝涓嶉樆濉?ingestion锛夈€?
- **鍓嶇疆鏉′欢**锛堝繀椤诲噯澶囷級锛?
  - **蹇呴』閰嶇疆LLM**锛氬湪 `config/settings.yaml` 涓厤缃彲鐢ㄧ殑LLM锛坧rovider/model/api_key锛?
  - **鐜鍙橀噺**锛氳缃搴旂殑API key鐜鍙橀噺锛坄OPENAI_API_KEY`/`OLLAMA_BASE_URL`绛夛級
  - **楠岃瘉鐩殑**锛氶€氳繃鐪熷疄LLM娴嬭瘯楠岃瘉閰嶇疆姝ｇ‘鎬у拰refinement鏁堟灉
- **淇敼鏂囦欢**锛?
  - `src/ingestion/transform/base_transform.py`锛堟柊澧烇級
  - `src/ingestion/transform/chunk_refiner.py`锛堟柊澧烇級
  - `src/core/trace/trace_context.py`锛堟柊澧烇細鏈€灏忓疄鐜帮紝Phase F 瀹屽杽锛?
  - `config/prompts/chunk_refinement.txt`锛堝凡瀛樺湪锛岄渶楠岃瘉鍐呭骞惰ˉ鍏?{text} 鍗犱綅绗︼級
  - `tests/fixtures/noisy_chunks.json`锛堟柊澧烇細8涓吀鍨嬪櫔澹板満鏅級
  - `tests/unit/test_chunk_refiner.py`锛堟柊澧烇細27涓崟鍏冩祴璇曪級
  - `tests/integration/test_chunk_refiner_llm.py`锛堟柊澧烇細鐪熷疄LLM闆嗘垚娴嬭瘯锛?
- **瀹炵幇绫?鍑芥暟**锛?
  - `BaseTransform.transform(chunks, trace) -> List[Chunk]`
  - `ChunkRefiner.__init__(settings, llm?, prompt_path?)`
  - `ChunkRefiner.transform(chunks, trace) -> List[Chunk]`
  - `ChunkRefiner._rule_based_refine(text) -> str`锛堝幓绌虹櫧/椤电湁椤佃剼/鏍煎紡鏍囪/HTML娉ㄩ噴锛?
  - `ChunkRefiner._llm_refine(text, trace) -> str | None`锛堝彲閫?LLM 閲嶅啓锛屽け璐ヨ繑鍥?None锛?
  - `ChunkRefiner._load_prompt(prompt_path?)`锛堜粠鏂囦欢鍔犺浇prompt妯℃澘锛屾敮鎸侀粯璁allback锛?
- **瀹炵幇娴佺▼寤鸿**锛?
  1. 鍏堝垱寤?`tests/fixtures/noisy_chunks.json`锛屽寘鍚?涓吀鍨嬪櫔澹板満鏅細
     - typical_noise_scenario: 缁煎悎鍣０锛堥〉鐪?椤佃剼/绌虹櫧锛?
     - ocr_errors: OCR閿欒鏂囨湰
     - page_header_footer: 椤电湁椤佃剼妯″紡
     - excessive_whitespace: 澶氫綑绌虹櫧
     - format_markers: HTML/Markdown鏍囪
     - clean_text: 骞插噣鏂囨湰锛堥獙璇佷笉杩囧害娓呯悊锛?
     - code_blocks: 浠ｇ爜鍧楋紙楠岃瘉淇濈暀鍐呴儴鏍煎紡锛?
     - mixed_noise: 鐪熷疄娣峰悎鍦烘櫙
  2. 鍒涘缓 `TraceContext` 鍗犱綅瀹炵幇锛坲uid鐢熸垚trace_id锛宺ecord_stage瀛樺偍闃舵鏁版嵁锛?
  3. 瀹炵幇 `BaseTransform` 鎶借薄鎺ュ彛
  4. 瀹炵幇 `ChunkRefiner._rule_based_refine` 瑙勫垯鍘诲櫔閫昏緫锛堟鍒欏尮閰?鍒嗘澶勭悊锛?
  5. 缂栧啓瑙勫垯妯″紡鍗曞厓娴嬭瘯锛堜娇鐢?fixtures 鏂█娓呮礂鏁堟灉锛?
  6. 瀹炵幇 `_llm_refine` 鍙€夊寮猴紙璇诲彇 prompt銆佽皟鐢?LLM銆侀敊璇鐞嗭級
  7. 缂栧啓 LLM 妯″紡鍗曞厓娴嬭瘯锛坢ock LLM 鏂█璋冪敤涓庤緭鍑猴級
  8. 缂栧啓闄嶇骇鍦烘櫙娴嬭瘯锛圠LM 澶辫触鏃跺洖閫€鍒拌鍒欑粨鏋滐紝鏍囪 metadata锛?
  9. **缂栧啓鐪熷疄LLM闆嗘垚娴嬭瘯骞舵墽琛岄獙璇?*锛堝繀椤绘墽琛岋紝楠岃瘉LLM閰嶇疆锛?
- **楠屾敹鏍囧噯**锛?
  - **鍗曞厓娴嬭瘯锛堝揩閫熷弽棣堝惊鐜級**锛?
    - 瑙勫垯妯″紡锛氬 fixtures 鍣０鏍蜂緥鑳芥纭幓鍣紙杩炵画绌虹櫧/椤电湁椤佃剼/鏍煎紡鏍囪/鍒嗛殧绾匡級
    - 淇濈暀鑳藉姏锛氫唬鐮佸潡鍐呴儴鏍煎紡涓嶈鐮村潖锛孧arkdown缁撴瀯瀹屾暣淇濈暀
    - LLM 妯″紡锛歮ock LLM 鏃惰兘姝ｇ‘璋冪敤骞惰繑鍥為噸鍐欑粨鏋滐紝metadata 鏍囪 `refined_by: "llm"`
    - 闄嶇骇琛屼负锛歀LM 澶辫触鏃跺洖閫€鍒拌鍒欑粨鏋滐紝metadata 鏍囪 `refined_by: "rule"` 鍜?fallback 鍘熷洜
    - 閰嶇疆寮€鍏筹細閫氳繃 `settings.yaml` 鐨?`ingestion.chunk_refiner.use_llm` 鎺у埗琛屼负
    - 寮傚父澶勭悊锛氬崟涓猚hunk澶勭悊寮傚父涓嶅奖鍝嶅叾浠朿hunk锛屼繚鐣欏師鏂?
  - **闆嗘垚娴嬭瘯锛堥獙鏀跺繀椤婚」锛?*锛?
    - 鉁?**蹇呴』楠岃瘉鐪熷疄LLM璋冪敤鎴愬姛**锛氫娇鐢ㄥ墠缃潯浠朵腑閰嶇疆鐨凩LM杩涜鐪熷疄refinement
    - 鉁?**蹇呴』楠岃瘉杈撳嚭璐ㄩ噺**锛歀LM refined鏂囨湰纭疄鏇村共鍑€锛堝櫔澹板噺灏戙€佸唴瀹逛繚鐣欙級
    - 鉁?**蹇呴』楠岃瘉闄嶇骇鏈哄埗**锛氭棤鏁堟ā鍨嬪悕绉版椂浼橀泤闄嶇骇鍒皉ule-based锛屼笉宕╂簝
    - 璇存槑锛氳繖鏄獙璇?鍓嶇疆鏉′欢涓噯澶囩殑LLM閰嶇疆鏄惁姝ｇ‘"鐨勫繀瑕佹楠?
- **娴嬭瘯鏂规硶**锛?
  - **闃舵1-鍗曞厓娴嬭瘯锛堝紑鍙戜腑蹇€熻凯浠ｏ級**锛?
    ```bash
    pytest tests/unit/test_chunk_refiner.py -v
    # 鉁?27涓祴璇曞叏閮ㄩ€氳繃锛屼娇鐢∕ock闅旂锛屾棤闇€鐪熷疄API
    ```
  - **闃舵2-闆嗘垚娴嬭瘯锛堥獙鏀跺繀椤绘墽琛岋級**锛?
    ```bash
    # 1. 杩愯鐪熷疄LLM闆嗘垚娴嬭瘯锛堝繀椤伙級
    pytest tests/integration/test_chunk_refiner_llm.py -v -s
    # 鉁?楠岃瘉LLM閰嶇疆姝ｇ‘锛宺efinement鏁堟灉绗﹀悎棰勬湡
    # 鈿狅笍 浼氫骇鐢熺湡瀹濧PI璋冪敤涓庤垂鐢?
    
    # 2. Review鎵撳嵃杈撳嚭锛岀‘璁ょ簿鐐艰川閲?
    # - 鍣０鏄惁琚湁鏁堝幓闄わ紵
    # - 鏈夋晥鍐呭鏄惁瀹屾暣淇濈暀锛?
    # - 闄嶇骇鏈哄埗鏄惁姝ｅ父宸ヤ綔锛?
    ```
  - **娴嬭瘯鍒嗗眰閫昏緫**锛?
    - 鍗曞厓娴嬭瘯锛氶獙璇佷唬鐮侀€昏緫姝ｇ‘
    - 闆嗘垚娴嬭瘯锛氶獙璇佺郴缁熷彲鐢ㄦ€?
    - 涓よ€呬簰琛ワ紝缂轰竴涓嶅彲

### C6锛歁etadataEnricher锛堣鍒欏寮?+ 鍙€?LLM 澧炲己 + 闄嶇骇锛?
- **鐩爣**锛氬疄鐜板厓鏁版嵁澧炲己妯″潡锛氭彁渚涜鍒欏寮虹殑榛樿瀹炵幇锛屽苟閲嶇偣鏀寔 LLM 澧炲己锛堥厤缃凡灏辩华锛孡LM 寮€鍏虫墦寮€锛夈€傚埄鐢?LLM 瀵?chunk 杩涜楂樿川閲忕殑 title 鐢熸垚銆乻ummary 鎽樿鍜?tags 鎻愬彇銆傚悓鏃朵繚鐣欏け璐ラ檷绾ф満鍒讹紝纭繚涓嶉樆濉?ingestion銆?
- **淇敼鏂囦欢**锛?
  - `src/ingestion/transform/metadata_enricher.py`
  - `tests/unit/test_metadata_enricher_contract.py`
- **楠屾敹鏍囧噯**锛?
  - 瑙勫垯妯″紡锛氫綔涓哄厹搴曢€昏緫锛岃緭鍑?metadata 蹇呴』鍖呭惈 `title/summary/tags`锛堣嚦灏戦潪绌猴級銆?
  - **LLM 妯″紡锛堟牳蹇冿級**锛氬湪 LLM 鎵撳紑鐨勬儏鍐典笅锛岀‘淇濈湡瀹炶皟鐢?LLM锛堟垨楂樿川閲?Mock锛夊苟鐢熸垚璇箟涓板瘜鐨?metadata銆傞渶楠岃瘉鍦ㄦ湁鐪熷疄 LLM 閰嶇疆涓嬬殑杩為€氭€т笌鏁堟灉銆?
  - 闄嶇骇琛屼负锛歀LM 璋冪敤澶辫触鏃跺洖閫€鍒拌鍒欐ā寮忕粨鏋滐紙鍙湪 metadata 鏍囪闄嶇骇鍘熷洜锛屼絾涓嶆姏鍑鸿嚧鍛藉紓甯革級銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_metadata_enricher_contract.py`锛屽苟纭繚鍖呭惈寮€鍚?LLM 鐨勯泦鎴愭祴璇曠敤渚嬨€?

### C7锛欼mageCaptioner锛堝彲閫夌敓鎴?caption + 闄嶇骇涓嶉樆濉烇級
- **鐩爣**锛氬疄鐜?`image_captioner.py`锛氬綋鍚敤 Vision LLM 涓斿瓨鍦?image_refs 鏃剁敓鎴?caption 骞跺啓鍥?chunk metadata锛涘綋绂佺敤/涓嶅彲鐢?寮傚父鏃惰蛋闄嶇骇璺緞锛屼笉闃诲 ingestion銆?
- **淇敼鏂囦欢**锛?
  - `src/ingestion/transform/image_captioner.py`
  - `config/prompts/image_captioning.txt`锛堜綔涓洪粯璁?prompt 鏉ユ簮锛涘彲鍦ㄦ祴璇曚腑娉ㄥ叆鏇夸唬鏂囨湰锛?
  - `tests/unit/test_image_captioner_fallback.py`
- **楠屾敹鏍囧噯**锛?
  - 鍚敤妯″紡锛氬瓨鍦?image_refs 鏃朵細鐢熸垚 caption 骞跺啓鍏?metadata锛堟祴璇曚腑鐢?mock Vision LLM 鏂█璋冪敤涓庤緭鍑猴級銆?
  - 闄嶇骇妯″紡锛氬綋閰嶇疆绂佺敤鎴栧紓甯告椂锛宑hunk 淇濈暀 image_refs锛屼絾涓嶇敓鎴?caption 涓旀爣璁?`has_unprocessed_images`銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_image_captioner_fallback.py`銆?

### C8锛欴enseEncoder锛堜緷璧?libs.embedding锛?
- **鐩爣**锛氬疄鐜?`dense_encoder.py`锛屾妸 chunks.text 鎵归噺閫佸叆 `BaseEmbedding`銆?
- **淇敼鏂囦欢**锛?
  - `src/ingestion/embedding/dense_encoder.py`
  - `tests/unit/test_dense_encoder.py`
- **楠屾敹鏍囧噯**锛歟ncoder 杈撳嚭鍚戦噺鏁伴噺涓?chunks 鏁伴噺涓€鑷达紝缁村害涓€鑷淬€?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_dense_encoder.py`銆?

### C9锛歋parseEncoder锛圔M25 缁熻涓庤緭鍑哄绾︼級
- **鐩爣**锛氬疄鐜?`sparse_encoder.py`锛氬 chunks 寤虹珛 BM25 鎵€闇€缁熻锛堝彲鍏堜粎杈撳嚭 term weights 缁撴瀯锛岀储寮曡惤鍦颁笅涓€姝ュ仛锛夈€?
- **淇敼鏂囦欢**锛?
  - `src/ingestion/embedding/sparse_encoder.py`
  - `tests/unit/test_sparse_encoder.py`
- **楠屾敹鏍囧噯**锛氳緭鍑虹粨鏋勫彲鐢ㄤ簬 bm25_indexer锛涘绌烘枃鏈湁鏄庣‘琛屼负銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_sparse_encoder.py`銆?

### C10锛欱atchProcessor锛堟壒澶勭悊缂栨帓锛?
- **鐩爣**锛氬疄鐜?`batch_processor.py`锛氬皢 chunks 鍒?batch锛岄┍鍔?dense/sparse 缂栫爜锛岃褰曟壒娆¤€楁椂锛堜负 trace 棰勭暀锛夈€?
- **淇敼鏂囦欢**锛?
  - `src/ingestion/embedding/batch_processor.py`
  - `tests/unit/test_batch_processor.py`
- **楠屾敹鏍囧噯**锛歜atch_size=2 鏃跺 5 chunks 鍒嗘垚 3 鎵癸紝涓旈『搴忕ǔ瀹氥€?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_batch_processor.py`銆?

---

**鈹佲攣鈹佲攣 瀛樺偍闃舵鍒嗙晫绾匡細浠ヤ笅浠诲姟璐熻矗灏嗙紪鐮佺粨鏋滄寔涔呭寲 鈹佲攣鈹佲攣**

> **璇存槑**锛欳8-C10瀹屾垚浜咲ense鍜孲parse鐨勭紪鐮佸伐浣滐紝C11-C13璐熻矗灏嗙紪鐮佺粨鏋滃瓨鍌ㄥ埌涓嶅悓鐨勫悗绔€?
> - **C11 (BM25Indexer)**锛氬鐞哠parse缂栫爜缁撴灉 鈫?鏋勫缓鍊掓帓绱㈠紩 鈫?瀛樺偍鍒版枃浠剁郴缁?
> - **C12 (VectorUpserter)**锛氬鐞咲ense缂栫爜缁撴灉 鈫?鐢熸垚绋冲畾ID 鈫?瀛樺偍鍒板悜閲忔暟鎹簱
> - **C13 (ImageStorage)**锛氬鐞嗗浘鐗囨暟鎹?鈫?鏂囦欢瀛樺偍 + 绱㈠紩鏄犲皠

---

### C11锛欱M25Indexer锛堝€掓帓绱㈠紩鏋勫缓涓庢寔涔呭寲锛?
- **鐩爣**锛氬疄鐜?`bm25_indexer.py`锛氭帴鏀?SparseEncoder 鐨則erm statistics杈撳嚭锛岃绠桰DF锛屾瀯寤哄€掓帓绱㈠紩锛屽苟鎸佷箙鍖栧埌 `data/db/bm25/`銆?
- **鏍稿績鍔熻兘**锛?
  - 璁＄畻 IDF (Inverse Document Frequency)锛歚IDF(term) = log((N - df + 0.5) / (df + 0.5))`
  - 鏋勫缓鍊掓帓绱㈠紩缁撴瀯锛歚{term: {idf, postings: [{chunk_id, tf, doc_length}]}}`
  - 绱㈠紩搴忓垪鍖栦笌鍔犺浇锛堟敮鎸佸閲忔洿鏂颁笌閲嶅缓锛?
- **淇敼鏂囦欢**锛?
  - `src/ingestion/storage/bm25_indexer.py`
  - `tests/unit/test_bm25_indexer_roundtrip.py`
- **楠屾敹鏍囧噯**锛?
  - build 鍚庤兘 load 骞跺鍚屼竴璇枡鏌ヨ杩斿洖绋冲畾 top ids
  - IDF璁＄畻鍑嗙‘锛堝彲鐢ㄥ凡鐭ヨ鏂欏姣旈獙璇侊級
  - 鏀寔绱㈠紩閲嶅缓涓庡閲忔洿鏂?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_bm25_indexer_roundtrip.py`銆?
- **澶囨敞**锛氭湰浠诲姟瀹屾垚Sparse璺緞鐨勬渶鍚庝竴鐜紝涓篋3 (SparseRetriever) 鎻愪緵鍙煡璇㈢殑BM25绱㈠紩銆?

### C12锛歏ectorUpserter锛堝悜閲忓瓨鍌ㄤ笌骞傜瓑鎬т繚璇侊級
- **鐩爣**锛氬疄鐜?`vector_upserter.py`锛氭帴鏀?DenseEncoder 鐨勫悜閲忚緭鍑猴紝鐢熸垚绋冲畾鐨?`chunk_id`锛屽苟璋冪敤 VectorStore 杩涜骞傜瓑鍐欏叆銆?
- **鏍稿績鍔熻兘**锛?
  - 鐢熸垚纭畾鎬?chunk_id锛歚hash(source_path + chunk_index + content_hash[:8])`
  - 璋冪敤 `BaseVectorStore.upsert()` 鍐欏叆鍚戦噺鏁版嵁搴?
  - 淇濊瘉骞傜瓑鎬э細鍚屼竴鍐呭閲嶅鍐欏叆涓嶄骇鐢熼噸澶嶈褰?
- **淇敼鏂囦欢**锛?
  - `src/ingestion/storage/vector_upserter.py`
  - `tests/unit/test_vector_upserter_idempotency.py`
- **楠屾敹鏍囧噯**锛?
  - 鍚屼竴 chunk 涓ゆ upsert 浜х敓鐩稿悓 id
  - 鍐呭鍙樻洿鏃?id 鍙樻洿
  - 鏀寔鎵归噺 upsert 涓斾繚鎸侀『搴?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_vector_upserter_idempotency.py`銆?
- **澶囨敞**锛氭湰浠诲姟瀹屾垚Dense璺緞鐨勬渶鍚庝竴鐜紝涓篋2 (DenseRetriever) 鎻愪緵鍙煡璇㈢殑鍚戦噺鏁版嵁搴撱€?

### C13锛欼mageStorage锛堝浘鐗囨枃浠跺瓨鍌ㄤ笌绱㈠紩琛ㄥ绾︼級
- **鐩爣**锛氬疄鐜?`image_storage.py`锛氫繚瀛樺浘鐗囧埌 `data/images/{collection}/`锛屽苟浣跨敤 **SQLite** 璁板綍 image_id鈫抪ath 鏄犲皠銆?
- **淇敼鏂囦欢**锛?
  - `src/ingestion/storage/image_storage.py`
  - `tests/unit/test_image_storage.py`
- **楠屾敹鏍囧噯**锛氫繚瀛樺悗鏂囦欢瀛樺湪锛涙煡鎵?image_id 杩斿洖姝ｇ‘璺緞锛涙槧灏勫叧绯绘寔涔呭寲鍦?`data/db/image_index.db`銆?
- **鎶€鏈柟妗?*锛?
  - 澶嶇敤椤圭洰宸叉湁鐨?SQLite 鏋舵瀯妯″紡锛堝弬鑰?`file_integrity.py` 鐨?`SQLiteIntegrityChecker`锛?
  - 鏁版嵁搴撹〃缁撴瀯锛?
    ```sql
    CREATE TABLE image_index (
        image_id TEXT PRIMARY KEY,
        file_path TEXT NOT NULL,
        collection TEXT,
        doc_hash TEXT,
        page_num INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX idx_collection ON image_index(collection);
    CREATE INDEX idx_doc_hash ON image_index(doc_hash);
    ```
  - 鎻愪緵骞跺彂瀹夊叏璁块棶锛圵AL 妯″紡锛?
  - 鏀寔鎸?collection 鎵归噺鏌ヨ
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_image_storage.py`銆?

### C14锛歅ipeline 缂栨帓锛圡VP 涓茶捣鏉ワ級
- **鐩爣**锛氬疄鐜?`pipeline.py`锛氫覆琛屾墽琛岋紙integrity鈫抣oad鈫抯plit鈫抰ransform鈫抏ncode鈫抯tore锛夛紝骞跺澶辫触姝ラ鍋氭竻鏅板紓甯搞€?
- **淇敼鏂囦欢**锛?
  - `src/ingestion/pipeline.py`
  - `tests/integration/test_ingestion_pipeline.py`
- **娴嬭瘯鏁版嵁**锛?
  - **涓绘祴璇曟枃妗?*锛歚tests/fixtures/sample_documents/complex_technical_doc.pdf`
    - 8绔犺妭鎶€鏈枃妗ｏ紙~21KB锛?
    - 鍖呭惈3寮犲祵鍏ュ浘鐗囷紙闇€娴嬭瘯鍥剧墖鎻愬彇鍜屾弿杩帮級
    - 鍖呭惈5涓〃鏍硷紙娴嬭瘯琛ㄦ牸鍐呭瑙ｆ瀽锛?
    - 澶氶〉澶氭钀斤紙娴嬭瘯瀹屾暣鍒嗗潡娴佺▼锛?
  - **杈呭姪娴嬭瘯**锛歚tests/fixtures/sample_documents/simple.pdf`锛堢畝鍗曞満鏅洖褰掞級
- **楠屾敹鏍囧噯**锛?
  - 瀵?`complex_technical_doc.pdf` 璺戝畬鏁?pipeline锛屾垚鍔熻緭鍑猴細
    - 鍚戦噺绱㈠紩鏂囦欢鍒?ChromaDB
    - BM25 绱㈠紩鏂囦欢鍒?`data/db/bm25/`
    - 鎻愬彇鐨勫浘鐗囧埌 `data/images/` (SHA256鍛藉悕)
  - Pipeline 鏃ュ織娓呮櫚灞曠ず鍚勯樁娈佃繘搴?
  - 澶辫触姝ラ鎶涘嚭鏄庣‘寮傚父淇℃伅
- **娴嬭瘯鏂规硶**锛歚pytest -v tests/integration/test_ingestion_pipeline.py`銆?

### C15锛氳剼鏈叆鍙?ingest.py锛堢绾垮彲鐢級
- **鐩爣**锛氬疄鐜?`scripts/ingest.py`锛屾敮鎸?`--collection`銆乣--path`銆乣--force`锛屽苟璋冪敤 pipeline銆?
- **淇敼鏂囦欢**锛?
  - `scripts/ingest.py`
  - `tests/e2e/test_data_ingestion.py`
- **楠屾敹鏍囧噯**锛氬懡浠よ鍙繍琛屽苟鍦?`data/db` 浜х敓浜х墿锛涢噸澶嶈繍琛屽湪鏈彉鏇存椂璺宠繃銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/e2e/test_data_ingestion.py`锛堝敖閲忕敤涓存椂鐩綍锛夈€?

---

## 闃舵 D锛歊etrieval MVP锛堢洰鏍囷細鑳?query 骞惰繑鍥?Top-K chunks锛?

### D1锛歈ueryProcessor锛堝叧閿瘝鎻愬彇 + filters 缁撴瀯锛?
- **鐩爣**锛氬疄鐜?`query_processor.py`锛氬叧閿瘝鎻愬彇锛堝厛瑙勫垯/鍒嗚瘝锛夛紝骞惰В鏋愰€氱敤 filters 缁撴瀯锛堝彲绌哄疄鐜帮級銆?
- **淇敼鏂囦欢**锛?
  - `src/core/query_engine/query_processor.py`
  - `tests/unit/test_query_processor.py`
- **楠屾敹鏍囧噯**锛氬杈撳叆 query 杈撳嚭 `keywords` 闈炵┖锛堝彲鏍规嵁鍋滅敤璇嶇瓥鐣ワ級锛宖ilters 涓?dict銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_query_processor.py`銆?

### D2锛欴enseRetriever锛堣皟鐢?VectorStore.query锛?
- **鐩爣**锛氬疄鐜?`dense_retriever.py`锛岀粍鍚?`EmbeddingClient`锛坬uery 鍚戦噺鍖栵級+ `VectorStore`锛堝悜閲忔绱級锛屽畬鎴愯涔夊彫鍥炪€?
- **鍓嶇疆浠诲姟**锛?
  1. 闇€鍏堝湪 `src/core/types.py` 涓畾涔?`RetrievalResult` 绫诲瀷锛堝寘鍚?`chunk_id`, `score`, `text`, `metadata` 瀛楁锛?
  2. 闇€纭 ChromaStore.query() 杩斿洖缁撴灉鍖呭惈 text锛堝綋鍓嶅瓨鍌ㄥ湪 documents 瀛楁锛岄渶琛ュ厖杩斿洖锛?
- **淇敼鏂囦欢**锛?
  - `src/core/types.py`锛堟柊澧?`RetrievalResult` 绫诲瀷锛?
  - `src/libs/vector_store/chroma_store.py`锛堜慨澶嶏細query 杩斿洖缁撴灉闇€鍖呭惈 text 瀛楁锛?
  - `src/core/query_engine/dense_retriever.py`
  - `tests/unit/test_dense_retriever.py`
- **瀹炵幇绫?鍑芥暟**锛?
  - `RetrievalResult` dataclass锛歚chunk_id: str`, `score: float`, `text: str`, `metadata: Dict`
  - `DenseRetriever.__init__(settings, embedding_client?, vector_store?)`锛氭敮鎸佷緷璧栨敞鍏ョ敤浜庢祴璇?
  - `DenseRetriever.retrieve(query: str, top_k: int, filters?: dict, trace?) -> List[RetrievalResult]`
  - 鍐呴儴娴佺▼锛歚query 鈫?embedding_client.embed([query]) 鈫?vector_store.query(vector, top_k, filters) 鈫?浠庤繑鍥炵粨鏋滄彁鍙?text 鈫?瑙勮寖鍖栫粨鏋渀
- **楠屾敹鏍囧噯**锛?
  - `RetrievalResult` 绫诲瀷宸插畾涔夊苟鍙簭鍒楀寲
  - ChromaStore.query() 杩斿洖缁撴灉鍖呭惈 `text` 瀛楁
  - 瀵硅緭鍏?query 鑳界敓鎴?embedding 骞惰皟鐢?VectorStore 妫€绱?
  - 杩斿洖缁撴灉鍖呭惈 `chunk_id`銆乣score`銆乣text`銆乣metadata`
  - mock EmbeddingClient 鍜?VectorStore 鏃惰兘姝ｇ‘缂栨帓璋冪敤
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_dense_retriever.py`锛坢ock embedding + vector store锛夈€?

### D3锛歋parseRetriever锛圔M25 鏌ヨ锛?
- **鐩爣**锛氬疄鐜?`sparse_retriever.py`锛氫粠 `data/db/bm25/` 杞藉叆绱㈠紩骞舵煡璇€?
- **鍓嶇疆浠诲姟**锛氶渶鍦?`BaseVectorStore` 鍜?`ChromaStore` 涓坊鍔?`get_by_ids()` 鏂规硶锛岀敤浜庢牴鎹?chunk_id 鎵归噺鑾峰彇 text 鍜?metadata
- **淇敼鏂囦欢**锛?
  - `src/libs/vector_store/base_vector_store.py`锛堟柊澧?`get_by_ids()` 鎶借薄鏂规硶锛?
  - `src/libs/vector_store/chroma_store.py`锛堝疄鐜?`get_by_ids()` 鏂规硶锛?
  - `src/core/query_engine/sparse_retriever.py`
  - `tests/unit/test_sparse_retriever.py`
- **瀹炵幇绫?鍑芥暟**锛?
  - `BaseVectorStore.get_by_ids(ids: List[str]) -> List[Dict]`锛氭牴鎹?ID 鎵归噺鑾峰彇璁板綍
  - `ChromaStore.get_by_ids(ids: List[str]) -> List[Dict]`锛氳皟鐢?ChromaDB 鐨?get 鏂规硶
  - `SparseRetriever.__init__(settings, bm25_indexer?, vector_store?)`锛氭敮鎸佷緷璧栨敞鍏ョ敤浜庢祴璇?
  - `SparseRetriever.retrieve(keywords: List[str], top_k: int, trace?) -> List[RetrievalResult]`
  - 鍐呴儴娴佺▼锛?
    1. `keywords 鈫?bm25_indexer.query(keywords, top_k) 鈫?[{chunk_id, score}]`
    2. `chunk_ids 鈫?vector_store.get_by_ids(chunk_ids) 鈫?[{id, text, metadata}]`
    3. 鍚堝苟 score 涓?text/metadata锛岀粍瑁呬负 `RetrievalResult` 鍒楄〃
  - 娉ㄦ剰锛歬eywords 鏉ヨ嚜 `QueryProcessor.process()` 鐨?`ProcessedQuery.keywords`
- **楠屾敹鏍囧噯**锛?
  - `BaseVectorStore.get_by_ids()` 鍜?`ChromaStore.get_by_ids()` 宸插疄鐜?
  - 瀵瑰凡鏋勫缓绱㈠紩鐨?fixtures 璇枡锛屽叧閿瘝妫€绱㈠懡涓鏈?chunk_id
  - 杩斿洖缁撴灉鍖呭惈瀹屾暣鐨?text 鍜?metadata
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_sparse_retriever.py`銆?

### D4锛欶usion锛圧RF 瀹炵幇锛?
- **鐩爣**锛氬疄鐜?`fusion.py`锛歊RF 铻嶅悎 dense/sparse 鎺掑悕骞惰緭鍑虹粺涓€鎺掑簭銆?
- **淇敼鏂囦欢**锛?
  - `src/core/query_engine/fusion.py`
  - `tests/unit/test_fusion_rrf.py`
- **楠屾敹鏍囧噯**锛氬鏋勯€犵殑鎺掑悕杈撳叆杈撳嚭 deterministic锛沰 鍙傛暟鍙厤缃€?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_fusion_rrf.py`銆?

### D5锛欻ybridSearch 缂栨帓
- **鐩爣**锛氬疄鐜?`hybrid_search.py`锛氱紪鎺?Dense + Sparse + Fusion 鐨勫畬鏁存贩鍚堟绱㈡祦绋嬶紝骞堕泦鎴?Metadata 杩囨护閫昏緫銆?
- **鍓嶇疆渚濊禆**锛欴1锛圦ueryProcessor锛夈€丏2锛圖enseRetriever锛夈€丏3锛圫parseRetriever锛夈€丏4锛團usion锛?
- **淇敼鏂囦欢**锛?
  - `src/core/query_engine/hybrid_search.py`
  - `tests/integration/test_hybrid_search.py`
- **瀹炵幇绫?鍑芥暟**锛?
  - `HybridSearch.__init__(settings, query_processor, dense_retriever, sparse_retriever, fusion)`
  - `HybridSearch.search(query: str, top_k: int, filters?: dict, trace?) -> List[RetrievalResult]`
  - `HybridSearch._apply_metadata_filters(candidates, filters) -> List[RetrievalResult]`锛氬悗缃繃婊ゅ厹搴?
  - 鍐呴儴娴佺▼锛歚query_processor.process() 鈫?骞惰(dense.retrieve + sparse.retrieve) 鈫?fusion.fuse() 鈫?metadata_filter 鈫?Top-K`
- **楠屾敹鏍囧噯**锛?
  - 瀵?fixtures 鏁版嵁锛岃兘杩斿洖 Top-K锛堝寘鍚?chunk 鏂囨湰涓?metadata锛?
  - 鏀寔 filters 鍙傛暟锛堝 `collection`銆乣doc_type`锛夎繘琛岃繃婊?
  - Dense/Sparse 浠讳竴璺緞澶辫触鏃惰兘闄嶇骇鍒板崟璺粨鏋?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/integration/test_hybrid_search.py`銆?

### D6锛歊eranker锛圕ore 灞傜紪鎺?+ fallback锛?
- **鐩爣**锛氬疄鐜?`core/query_engine/reranker.py`锛氭帴鍏?`libs.reranker` 鍚庣锛屽け璐?瓒呮椂鍥為€€ fusion 鎺掑悕銆?
- **淇敼鏂囦欢**锛?
  - `src/core/query_engine/reranker.py`
  - `config/prompts/rerank.txt`锛堜粎褰撳惎鐢?LLM Rerank 鍚庣鏃朵娇鐢級
  - `tests/unit/test_reranker_fallback.py`
- **楠屾敹鏍囧噯**锛氭ā鎷熷悗绔紓甯告椂涓嶅奖鍝嶆渶缁堣繑鍥烇紝涓旀爣璁?fallback=true銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_reranker_fallback.py`銆?

### D7锛氳剼鏈叆鍙?query.py锛堟煡璇㈠彲鐢級
- **鐩爣**锛氬疄鐜?`scripts/query.py`锛屼綔涓哄湪绾挎煡璇㈢殑鍛戒护琛屽叆鍙ｏ紝璋冪敤瀹屾暣鐨?HybridSearch + Reranker 娴佺▼骞惰緭鍑烘绱㈢粨鏋溿€?
- **鍓嶇疆渚濊禆**锛欴5锛圚ybridSearch锛夈€丏6锛圧eranker锛?
- **淇敼鏂囦欢**锛?
  - `scripts/query.py`
- **瀹炵幇鍔熻兘**锛?
  - **鍙傛暟鏀寔**锛?
    - `--query "闂"`锛氬繀濉紝鏌ヨ鏂囨湰
    - `--top-k 10`锛氬彲閫夛紝杩斿洖缁撴灉鏁伴噺锛堥粯璁?10锛?
    - `--collection xxx`锛氬彲閫夛紝闄愬畾妫€绱㈤泦鍚?
    - `--verbose`锛氬彲閫夛紝鏄剧ず鍚勯樁娈典腑闂寸粨鏋?
    - `--no-rerank`锛氬彲閫夛紝璺宠繃 Reranker 闃舵
  - **杈撳嚭鍐呭**锛?
    - 榛樿妯″紡锛歍op-K 缁撴灉锛堝簭鍙枫€乻core銆佹枃鏈憳瑕併€佹潵婧愭枃浠躲€侀〉鐮侊級
    - Verbose 妯″紡锛氶澶栨樉绀?Dense 鍙洖缁撴灉銆丼parse 鍙洖缁撴灉銆丗usion 缁撴灉銆丷erank 缁撴灉
  - **鍐呴儴娴佺▼**锛?
    1. 鍔犺浇閰嶇疆 `Settings`
    2. 鍒濆鍖栫粍浠讹紙EmbeddingClient銆乂ectorStore銆丅M25Indexer銆丷eranker锛?
    3. 鍒涘缓 `QueryProcessor`銆乣DenseRetriever`銆乣SparseRetriever`銆乣HybridSearch` 瀹炰緥
    4. 璋冪敤 `HybridSearch.search()` 鑾峰彇鍊欓€夌粨鏋?
    5. 璋冪敤 `Reranker.rerank()` 杩涜绮炬帓锛堥櫎闈?`--no-rerank`锛?
    6. 鏍煎紡鍖栬緭鍑虹粨鏋?
- **楠屾敹鏍囧噯**锛?
  - 鍛戒护琛屽彲杩愯锛歚python scripts/query.py --query "濡備綍閰嶇疆 Azure锛?`
  - 杩斿洖鏍煎紡鍖栫殑 Top-K 妫€绱㈢粨鏋?
  - `--verbose` 妯″紡鏄剧ず鍚勯樁娈典腑闂寸粨鏋滐紙渚夸簬璋冭瘯锛?
  - 鏃犳暟鎹椂杩斿洖鍙嬪ソ鎻愮ず锛堝"鏈壘鍒扮浉鍏虫枃妗ｏ紝璇峰厛杩愯 ingest.py 鎽勫彇鏁版嵁"锛?
- **娴嬭瘯鏂规硶**锛氭墜鍔ㄨ繍琛?`python scripts/query.py --query "娴嬭瘯鏌ヨ" --verbose`锛堜緷璧栧凡鎽勫彇鐨勬暟鎹級銆?
- **涓?MCP Tool 鐨勫叧绯?*锛?
  - `scripts/query.py` 鏄紑鍙戣皟璇曠敤鐨勫懡浠よ宸ュ叿
  - `E3 query_knowledge_hub` 鏄敓浜х幆澧冪殑 MCP Tool
  - 涓よ€呭叡浜?Core 灞傞€昏緫锛圚ybridSearch + Reranker锛夛紝浣嗗叆鍙ｅ拰杈撳嚭鏍煎紡涓嶅悓

---

## 闃舵 E锛歁CP Server 灞備笌 Tools锛堢洰鏍囷細瀵瑰鍙敤鐨?MCP tools锛?

### E1锛歁CP Server 鍏ュ彛涓?Stdio 绾︽潫
- **鐩爣**锛氬疄鐜?`mcp_server/server.py`锛氶伒寰?stdout 鍙緭鍑?MCP 娑堟伅锛屾棩蹇楀埌 stderr"銆?
- **淇敼鏂囦欢**锛?
  - `src/mcp_server/server.py`
  - `tests/integration/test_mcp_server.py`
- **楠屾敹鏍囧噯**锛氬惎鍔?server 鑳藉畬鎴?initialize锛泂tderr 鏈夋棩蹇椾絾 stdout 涓嶆薄鏌撱€?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/integration/test_mcp_server.py`锛堝瓙杩涚▼鏂瑰紡锛夈€?

### E2锛歅rotocol Handler 鍗忚瑙ｆ瀽涓庤兘鍔涘崗鍟?
- **鐩爣**锛氬疄鐜?`mcp_server/protocol_handler.py`锛氬皝瑁?JSON-RPC 2.0 鍗忚瑙ｆ瀽锛屽鐞?`initialize`銆乣tools/list`銆乣tools/call` 涓夌被鏍稿績鏂规硶锛屽苟瀹炵幇瑙勮寖鐨勯敊璇鐞嗐€?
- **淇敼鏂囦欢**锛?
  - `src/mcp_server/protocol_handler.py`
  - `tests/unit/test_protocol_handler.py`
- **瀹炵幇瑕佺偣**锛?
  - **ProtocolHandler 绫?*锛?
    - `handle_initialize(params)` 鈫?杩斿洖 server capabilities锛堟敮鎸佺殑 tools 鍒楄〃銆佺増鏈俊鎭級
    - `handle_tools_list()` 鈫?杩斿洖宸叉敞鍐岀殑 tool schema锛坣ame, description, inputSchema锛?
    - `handle_tools_call(name, arguments)` 鈫?璺敱鍒板叿浣?tool 鎵ц锛屾崟鑾峰紓甯稿苟杞崲涓?JSON-RPC error
  - **閿欒鐮佽鑼?*锛氶伒寰?JSON-RPC 2.0锛?32600 Invalid Request, -32601 Method not found, -32602 Invalid params, -32603 Internal error锛?
  - **鑳藉姏鍗忓晢**锛氬湪 `initialize` 鍝嶅簲涓０鏄?`capabilities.tools`
- **楠屾敹鏍囧噯**锛?
  - 鍙戦€?`initialize` 璇锋眰鑳借繑鍥炴纭殑 `serverInfo` 鍜?`capabilities`
  - 鍙戦€?`tools/list` 鑳借繑鍥炲凡娉ㄥ唽 tools 鐨?schema
  - 鍙戦€?`tools/call` 鑳芥纭矾鐢卞苟杩斿洖缁撴灉鎴栬鑼冮敊璇?
  - **閿欒澶勭悊**锛氭棤鏁堟柟娉曡繑鍥?-32601锛屽弬鏁伴敊璇繑鍥?-32602锛屽唴閮ㄥ紓甯歌繑鍥?-32603 涓斾笉娉勯湶鍫嗘爤
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_protocol_handler.py`銆?

### E3锛氬疄鐜?tool锛歲uery_knowledge_hub
- **鐩爣**锛氬疄鐜?`tools/query_knowledge_hub.py`锛氳皟鐢?HybridSearch + Reranker锛屾瀯寤哄甫寮曠敤鐨勫搷搴旓紝杩斿洖 Markdown + structured citations銆?
- **鍓嶇疆渚濊禆**锛欴5锛圚ybridSearch锛夈€丏6锛圧eranker锛夈€丒1锛圫erver锛夈€丒2锛圥rotocol Handler锛?
- **淇敼鏂囦欢**锛?
  - `src/mcp_server/tools/query_knowledge_hub.py`
  - `src/core/response/response_builder.py`锛堟柊澧烇細鏋勫缓 MCP 鍝嶅簲鏍煎紡锛?
  - `src/core/response/citation_generator.py`锛堟柊澧烇細鐢熸垚寮曠敤淇℃伅锛?
  - `tests/unit/test_response_builder.py`锛堟柊澧烇級
  - `tests/integration/test_mcp_server.py`锛堣ˉ鐢ㄤ緥锛?
- **瀹炵幇绫?鍑芥暟**锛?
  - `ResponseBuilder.build(retrieval_results, query) -> MCPResponse`锛氭瀯寤?MCP 鏍煎紡鍝嶅簲
  - `CitationGenerator.generate(retrieval_results) -> List[Citation]`锛氱敓鎴愬紩鐢ㄥ垪琛?
  - `query_knowledge_hub(query, top_k?, collection?) -> MCPToolResult`锛歍ool 鍏ュ彛鍑芥暟
- **楠屾敹鏍囧噯**锛?
  - tool 杩斿洖 `content[0]` 涓哄彲璇?Markdown锛堝惈 `[1]`銆乣[2]` 绛夊紩鐢ㄦ爣娉級
  - `structuredContent.citations` 鍖呭惈 `source`/`page`/`chunk_id`/`score` 瀛楁
  - 鏃犵粨鏋滄椂杩斿洖鍙嬪ソ鎻愮ず鑰岄潪绌烘暟缁?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/integration/test_mcp_server.py -k query_knowledge_hub`銆?

### E4锛氬疄鐜?tool锛歭ist_collections
- **鐩爣**锛氬疄鐜?`tools/list_collections.py`锛氬垪鍑?`data/documents/` 涓嬮泦鍚堝苟闄勫甫缁熻锛堝彲寤跺悗鍒颁笅涓€姝ワ級銆?
- **淇敼鏂囦欢**锛?
  - `src/mcp_server/tools/list_collections.py`
  - `tests/unit/test_list_collections.py`
- **楠屾敹鏍囧噯**锛氬 fixtures 涓殑鐩綍缁撴瀯鑳借繑鍥為泦鍚堝悕鍒楄〃銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_list_collections.py`銆?

### E5锛氬疄鐜?tool锛歡et_document_summary
- **鐩爣**锛氬疄鐜?`tools/get_document_summary.py`锛氭寜 doc_id 杩斿洖 title/summary/tags锛堝彲鍏堜粠 metadata/缂撳瓨鍙栵級銆?
- **淇敼鏂囦欢**锛?
  - `src/mcp_server/tools/get_document_summary.py`
  - `tests/unit/test_get_document_summary.py`
- **楠屾敹鏍囧噯**锛氬涓嶅瓨鍦?doc_id 杩斿洖瑙勮寖閿欒锛涘瓨鍦ㄦ椂杩斿洖缁撴瀯鍖栦俊鎭€?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_get_document_summary.py`銆?

### E6锛氬妯℃€佽繑鍥炵粍瑁咃紙Text + Image锛?
- **鐩爣**锛氬疄鐜?`multimodal_assembler.py`锛氬懡涓?chunk 鍚?image_refs 鏃惰鍙栧浘鐗囧苟 base64 杩斿洖 ImageContent銆?
- **淇敼鏂囦欢**锛?
  - `src/core/response/multimodal_assembler.py`
  - `tests/integration/test_mcp_server.py`锛堣ˉ鍥惧儚杩斿洖鐢ㄤ緥锛?
- **楠屾敹鏍囧噯**锛氳繑鍥?content 涓寘鍚?image type锛宮imeType 姝ｇ‘锛宒ata 涓?base64 瀛楃涓层€?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/integration/test_mcp_server.py -k image`銆?

---

## 闃舵 F锛歍race 鍩虹璁炬柦涓庢墦鐐癸紙鐩爣锛欼ngestion + Query 鍙岄摼璺彲杩借釜锛?

### F1锛歍raceContext 澧炲己锛坒inish + 鑰楁椂缁熻 + trace_type锛?
- **鐩爣**锛氬寮哄凡鏈夌殑 `TraceContext`锛圕5 宸插疄鐜板熀纭€鐗堬級锛屾坊鍔?`finish()` 鏂规硶銆佽€楁椂缁熻銆乣trace_type` 瀛楁锛堝尯鍒?query/ingestion锛夈€乣to_dict()` 搴忓垪鍖栧姛鑳姐€?
- **淇敼鏂囦欢**锛?
  - `src/core/trace/trace_context.py`锛堝寮猴細娣诲姞 trace_type/finish/elapsed_ms/to_dict锛?
  - `src/core/trace/trace_collector.py`锛堟柊澧烇細鏀堕泦骞舵寔涔呭寲 trace锛?
  - `tests/unit/test_trace_context.py`锛堣ˉ鍏?finish/to_dict 鐩稿叧娴嬭瘯锛?
- **瀹炵幇绫?鍑芥暟**锛?
  - `TraceContext.__init__(trace_type: str = "query")`锛氭敮鎸?`"query"` 鎴?`"ingestion"` 绫诲瀷
  - `TraceContext.finish() -> None`锛氭爣璁?trace 缁撴潫锛岃绠楁€昏€楁椂
  - `TraceContext.elapsed_ms(stage_name?) -> float`锛氳幏鍙栨寚瀹氶樁娈垫垨鎬昏€楁椂
  - `TraceContext.to_dict() -> dict`锛氬簭鍒楀寲涓哄彲 JSON 杈撳嚭鐨勫瓧鍏革紙鍚?trace_type锛?
  - `TraceCollector.collect(trace: TraceContext) -> None`锛氭敹闆?trace 骞惰Е鍙戞寔涔呭寲
- **楠屾敹鏍囧噯**锛?
  - `record_stage` 杩藉姞闃舵鏁版嵁锛堝凡鏈夛級
  - `finish()` 鍚?`to_dict()` 杈撳嚭鍖呭惈 `trace_id`銆乣trace_type`銆乣started_at`銆乣finished_at`銆乣total_elapsed_ms`銆乣stages`
  - 杈撳嚭 dict 鍙洿鎺?`json.dumps()` 搴忓垪鍖?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_trace_context.py`銆?


### F2锛氱粨鏋勫寲鏃ュ織 logger锛圝SON Lines锛?
- **鐩爣**锛氬寮?`observability/logger.py`锛屾敮鎸?JSON Lines 鏍煎紡杈撳嚭锛屽苟瀹炵幇 trace 鎸佷箙鍖栧埌 `logs/traces.jsonl`銆?
- **淇敼鏂囦欢**锛?
  - `src/observability/logger.py`锛堝寮猴細娣诲姞 JSONFormatter + FileHandler锛?
  - `tests/unit/test_jsonl_logger.py`
- **瀹炵幇绫?鍑芥暟**锛?
  - `JSONFormatter`锛氳嚜瀹氫箟 logging Formatter锛岃緭鍑?JSON 鏍煎紡
  - `get_trace_logger() -> logging.Logger`锛氳幏鍙栭厤缃簡 JSON Lines 杈撳嚭鐨?logger
  - `write_trace(trace_dict: dict) -> None`锛氬皢 trace 瀛楀吀鍐欏叆 `logs/traces.jsonl`
- **涓?F1 鐨勫垎宸?*锛?
  - F1 璐熻矗 TraceContext 鐨勬暟鎹粨鏋勶紙鍚?`trace_type`锛夊拰 `finish()` 鏂规硶
  - F2 璐熻矗灏?`trace.to_dict()` 鐨勭粨鏋滄寔涔呭寲鍒版枃浠?
- **楠屾敹鏍囧噯**锛氬啓鍏ヤ竴鏉?trace 鍚庢枃浠舵柊澧炰竴琛屽悎娉?JSON锛屽寘鍚?`trace_type` 瀛楁銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_jsonl_logger.py`銆?

### F3锛氬湪 Query 閾捐矾鎵撶偣
- **鐩爣**锛氬湪 HybridSearch/Rerank 涓敞鍏?TraceContext锛坄trace_type="query"`锛夛紝鍒╃敤 B 闃舵鎶借薄鎺ュ彛涓鐣欑殑 `trace` 鍙傛暟锛屾樉寮忚皟鐢?`trace.record_stage()` 璁板綍鍚勯樁娈垫暟鎹€?
- **鍓嶇疆渚濊禆**锛欴5锛圚ybridSearch锛夈€丏6锛圧eranker锛夈€丗1锛圱raceContext 澧炲己锛夈€丗2锛堢粨鏋勫寲鏃ュ織锛?
- **淇敼鏂囦欢**锛?
  - `src/core/query_engine/hybrid_search.py`锛堝鍔?trace 璁板綍锛歞ense/sparse/fusion 闃舵锛?
  - `src/core/query_engine/reranker.py`锛堝鍔?trace 璁板綍锛歳erank 闃舵锛?
  - `tests/integration/test_hybrid_search.py`锛堟柇瑷€ trace 涓瓨鍦ㄥ悇闃舵锛?
- **璇存槑**锛欱 闃舵鐨勬帴鍙ｅ凡棰勭暀 `trace: TraceContext | None = None` 鍙傛暟锛屾湰浠诲姟璐熻矗鍦ㄨ皟鐢ㄦ椂浼犲叆瀹為檯鐨?TraceContext 瀹炰緥锛屽苟鍦ㄥ悇闃舵璁板綍 `method`/`provider`/`details` 瀛楁銆?
- **楠屾敹鏍囧噯**锛?
  - 涓€娆℃煡璇㈢敓鎴?trace锛屽寘鍚?`query_processing`/`dense_retrieval`/`sparse_retrieval`/`fusion`/`rerank` 闃舵
  - 姣忎釜闃舵璁板綍 `elapsed_ms` 鑰楁椂瀛楁鍜?`method` 瀛楁
  - `trace.to_dict()` 涓?`trace_type == "query"`
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/integration/test_hybrid_search.py`銆?

### F4锛氬湪 Ingestion 閾捐矾鎵撶偣
- **鐩爣**锛氬湪 IngestionPipeline 涓敞鍏?TraceContext锛坄trace_type="ingestion"`锛夛紝璁板綍鍚勬憚鍙栭樁娈电殑澶勭悊鏁版嵁銆?
- **鍓嶇疆渚濊禆**锛欳5锛圥ipeline锛夈€丗1锛圱raceContext 澧炲己锛夈€丗2锛堢粨鏋勫寲鏃ュ織锛?
- **淇敼鏂囦欢**锛?
  - `src/ingestion/pipeline.py`锛堝鍔?trace 浼犻€掞細load/split/transform/embed/upsert 闃舵锛?
  - `tests/integration/test_ingestion_pipeline.py`锛堟柇瑷€ trace 涓瓨鍦ㄥ悇闃舵锛?
- **楠屾敹鏍囧噯**锛?
  - 涓€娆℃憚鍙栫敓鎴?trace锛屽寘鍚?`load`/`split`/`transform`/`embed`/`upsert` 闃舵
  - 姣忎釜闃舵璁板綍 `elapsed_ms`銆乣method`锛堝 markitdown/recursive/chroma锛夊拰澶勭悊璇︽儏
  - `trace.to_dict()` 涓?`trace_type == "ingestion"`
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/integration/test_ingestion_pipeline.py`銆?

### F5锛歅ipeline 杩涘害鍥炶皟 (on_progress)
- **鐩爣**锛氬湪 `IngestionPipeline.run()` 鏂规硶涓柊澧炲彲閫?`on_progress` 鍥炶皟鍙傛暟锛屾敮鎸佸閮ㄥ疄鏃惰幏鍙栧鐞嗚繘搴︺€?
- **鍓嶇疆渚濊禆**锛欶4锛圛ngestion 鎵撶偣锛?
- **淇敼鏂囦欢**锛?
  - `src/ingestion/pipeline.py`锛堝湪鍚勯樁娈佃皟鐢?`on_progress(stage_name, current, total)`锛?
  - `tests/unit/test_pipeline_progress.py`锛堟柊澧烇細楠岃瘉鍥炶皟琚纭皟鐢級
- **瀹炵幇瑕佺偣**锛?
  - 鍥炶皟绛惧悕锛歚on_progress(stage_name: str, current: int, total: int)`
  - `on_progress` 涓?`None` 鏃跺畬鍏ㄤ笉褰卞搷鐜版湁琛屼负
  - 鍚勯樁娈靛湪澶勭悊姣忎釜 batch 鎴栧畬鎴愭椂瑙﹀彂鍥炶皟
- **楠屾敹鏍囧噯**锛歅ipeline 杩愯鏃朵紶鍏?mock 鍥炶皟锛屾柇瑷€鍚勯樁娈靛潎琚皟鐢ㄤ笖鍙傛暟姝ｇ‘銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_pipeline_progress.py`銆?

---

## 闃舵 G锛氬彲瑙嗗寲绠＄悊骞冲彴 Dashboard锛堢洰鏍囷細鍏〉闈㈠畬鏁村彲瑙嗗寲绠＄悊锛?

### G1锛欴ashboard 鍩虹鏋舵瀯涓庣郴缁熸€昏椤?
- **鐩爣**锛氭惌寤?Streamlit 澶氶〉闈㈠簲鐢ㄦ鏋讹紝瀹炵幇绯荤粺鎬昏椤甸潰锛堝睍绀虹粍浠堕厤缃笌鏁版嵁缁熻锛夈€?
- **鍓嶇疆渚濊禆**锛欶1-F2锛圱race 鍩虹璁炬柦锛?
- **淇敼鏂囦欢**锛?
  - `src/observability/dashboard/app.py`锛堥噸鍐欙細澶氶〉闈㈠鑸灦鏋勶級
  - `src/observability/dashboard/pages/overview.py`锛堟柊澧烇細绯荤粺鎬昏椤甸潰锛?
  - `src/observability/dashboard/services/config_service.py`锛堟柊澧烇細閰嶇疆璇诲彇鏈嶅姟锛?
  - `scripts/start_dashboard.py`锛堟柊澧烇細Dashboard 鍚姩鑴氭湰锛?
- **瀹炵幇瑕佺偣**锛?
  - `app.py` 浣跨敤 `st.navigation()` 娉ㄥ唽鍏釜椤甸潰锛堟湭瀹屾垚鐨勯〉闈㈡樉绀哄崰浣嶆彁绀猴級
  - Overview 椤甸潰锛氳鍙?`Settings` 灞曠ず缁勪欢鍗＄墖锛岃皟鐢?`ChromaStore.get_collection_stats()` 灞曠ず鏁版嵁缁熻
  - `ConfigService`锛氬皝瑁?Settings 璇诲彇锛屾牸寮忓寲缁勪欢閰嶇疆淇℃伅
- **楠屾敹鏍囧噯**锛歚streamlit run src/observability/dashboard/app.py` 鍙惎鍔紝鎬昏椤靛睍绀哄綋鍓嶉厤缃俊鎭€?
- **娴嬭瘯鏂规硶**锛氭墜鍔ㄨ繍琛?`python scripts/start_dashboard.py` 骞堕獙璇侀〉闈㈡覆鏌撱€?

### G2锛欴ocumentManager 瀹炵幇
- **鐩爣**锛氬疄鐜?`src/ingestion/document_manager.py`锛氳法瀛樺偍鐨勬枃妗ｇ敓鍛藉懆鏈熺鐞嗭紙list/delete/stats锛夈€?
- **鍓嶇疆渚濊禆**锛欳5锛圥ipeline + 鍚勫瓨鍌ㄦā鍧楀凡灏辩华锛?
- **淇敼鏂囦欢**锛?
  - `src/ingestion/document_manager.py`锛堟柊澧烇級
  - `src/libs/vector_store/chroma_store.py`锛堝寮猴細娣诲姞 `delete_by_metadata`锛?
  - `src/ingestion/storage/bm25_indexer.py`锛堝寮猴細娣诲姞 `remove_document`锛?
  - `src/libs/loader/file_integrity.py`锛堝寮猴細娣诲姞 `remove_record` + `list_processed`锛?
  - `tests/unit/test_document_manager.py`锛堟柊澧烇級
- **瀹炵幇绫?鍑芥暟**锛?
  - `DocumentManager.__init__(chroma_store, bm25_indexer, image_storage, file_integrity)`
  - `DocumentManager.list_documents(collection?) -> List[DocumentInfo]`
  - `DocumentManager.get_document_detail(doc_id) -> DocumentDetail`
  - `DocumentManager.delete_document(source_path, collection) -> DeleteResult`
  - `DocumentManager.get_collection_stats(collection?) -> CollectionStats`
- **楠屾敹鏍囧噯**锛?
  - `list_documents` 杩斿洖宸叉憚鍏ユ枃妗ｅ垪琛紙source銆乧hunk 鏁般€佸浘鐗囨暟锛?
  - `delete_document` 鍗忚皟鍒犻櫎 Chroma + BM25 + ImageStorage + FileIntegrity 鍥涗釜瀛樺偍
  - 鍒犻櫎鍚庡啀娆?list 涓嶅寘鍚凡鍒犻櫎鏂囨。
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_document_manager.py`銆?

### G3锛氭暟鎹祻瑙堝櫒椤甸潰
- **鐩爣**锛氬疄鐜?Dashboard 鏁版嵁娴忚鍣ㄩ〉闈紙鏌ョ湅鏂囨。鍒楄〃銆丆hunk 璇︽儏銆佸浘鐗囬瑙堬級銆?
- **鍓嶇疆渚濊禆**锛欸1锛圖ashboard 鏋舵瀯锛夈€丟2锛圖ocumentManager锛?
- **淇敼鏂囦欢**锛?
  - `src/observability/dashboard/pages/data_browser.py`锛堟柊澧烇級
  - `src/observability/dashboard/services/data_service.py`锛堟柊澧烇細灏佽 ChromaStore/ImageStorage 璇诲彇锛?
- **瀹炵幇瑕佺偣**锛?
  - 鏂囨。鍒楄〃瑙嗗浘锛氬睍绀?source_path銆侀泦鍚堛€乧hunk 鏁般€佹憚鍏ユ椂闂达紱鏀寔闆嗗悎绛涢€?
  - Chunk 璇︽儏瑙嗗浘锛氱偣鍑绘枃妗ｅ睍寮€鎵€鏈?chunk锛屾樉绀哄唴瀹癸紙鍙姌鍙狅級銆乵etadata 瀛楁銆佸叧鑱斿浘鐗?
  - `DataService`锛氬皝瑁?`ChromaStore.get_by_metadata()` 鍜?`ImageStorage.list_images()` 璋冪敤
- **楠屾敹鏍囧噯**锛氬彲鍦?Dashboard 涓祻瑙堝凡鎽勫叆鐨勬枃妗ｅ拰 chunk 璇︽儏銆?
- **娴嬭瘯鏂规硶**锛氭墜鍔ㄩ獙璇侊紙鍏?ingest 鏍蜂緥鏁版嵁锛屽啀鍦?Dashboard 娴忚锛夈€?

### G4锛欼ngestion 绠＄悊椤甸潰
- **鐩爣**锛氬疄鐜?Dashboard Ingestion 绠＄悊椤甸潰锛堟枃浠朵笂浼犺Е鍙戞憚鍙栥€佽繘搴﹀睍绀恒€佹枃妗ｅ垹闄わ級銆?
- **鍓嶇疆渚濊禆**锛欸2锛圖ocumentManager锛夈€丟3锛圖ataService锛夈€丗5锛坥n_progress 鍥炶皟锛?
- **淇敼鏂囦欢**锛?
  - `src/observability/dashboard/pages/ingestion_manager.py`锛堟柊澧烇級
- **瀹炵幇瑕佺偣**锛?
  - 鏂囦欢涓婁紶锛歚st.file_uploader` 閫夋嫨鏂囦欢 + 闆嗗悎閫夋嫨
  - 鎽勫彇瑙﹀彂锛氳皟鐢?`IngestionPipeline.run(on_progress=...)` + `st.progress()` 瀹炴椂杩涘害
  - 鏂囨。鍒犻櫎锛氬湪鏂囨。鍒楄〃涓彁渚涘垹闄ゆ寜閽紝璋冪敤 `DocumentManager.delete_document()`
- **楠屾敹鏍囧噯**锛氬彲鍦?Dashboard 涓笂浼犳枃浠惰Е鍙戞憚鍙栥€佺湅鍒板疄鏃惰繘搴︽潯銆佸垹闄ゅ凡鏈夋枃妗ｃ€?
- **娴嬭瘯鏂规硶**锛氭墜鍔ㄩ獙璇侊紙涓婁紶 PDF 鈫?瑙傚療杩涘害 鈫?鍒犻櫎 鈫?纭宸茬Щ闄わ級銆?

### G5锛欼ngestion 杩借釜椤甸潰
- **鐩爣**锛氬疄鐜?Dashboard Ingestion 杩借釜椤甸潰锛堟憚鍙栧巻鍙插垪琛ㄣ€侀樁娈佃€楁椂鐎戝竷鍥撅級銆?
- **鍓嶇疆渚濊禆**锛欶4锛圛ngestion 鎵撶偣锛夈€丟1锛圖ashboard 鏋舵瀯锛?
- **淇敼鏂囦欢**锛?
  - `src/observability/dashboard/pages/ingestion_traces.py`锛堟柊澧烇級
  - `src/observability/dashboard/services/trace_service.py`锛堟柊澧烇細瑙ｆ瀽 traces.jsonl锛?
- **瀹炵幇瑕佺偣**锛?
  - 鍘嗗彶鍒楄〃锛氭寜鏃堕棿鍊掑簭灞曠ず `trace_type == "ingestion"` 璁板綍
  - 璇︽儏椤碉細妯悜鏉″舰鍥惧睍绀?load/split/transform/embed/upsert 鑰楁椂鍒嗗竷
  - `TraceService`锛氳鍙?`logs/traces.jsonl`锛岃В鏋愪负 Trace 瀵硅薄鍒楄〃
- **楠屾敹鏍囧噯**锛氭墽琛?ingest 鍚庯紝Dashboard 鏄剧ず瀵瑰簲鐨勮拷韪褰曚笌鑰楁椂鐎戝竷鍥俱€?
- **娴嬭瘯鏂规硶**锛氭墜鍔ㄩ獙璇侊紙鍏?ingest 鈫?鎵撳紑 Dashboard 鈫?鏌ョ湅杩借釜锛夈€?

### G6锛歈uery 杩借釜椤甸潰
- **鐩爣**锛氬疄鐜?Dashboard Query 杩借釜椤甸潰锛堟煡璇㈠巻鍙层€丏ense/Sparse 瀵规瘮銆丷erank 鍙樺寲锛夈€?
- **鍓嶇疆渚濊禆**锛欶3锛圦uery 鎵撶偣锛夈€丟1锛圖ashboard 鏋舵瀯锛夈€丟5锛圱raceService 宸插疄鐜帮級
- **淇敼鏂囦欢**锛?
  - `src/observability/dashboard/pages/query_traces.py`锛堟柊澧烇級
- **瀹炵幇瑕佺偣**锛?
  - 鍘嗗彶鍒楄〃锛氭寜鏃堕棿鍊掑簭灞曠ず `trace_type == "query"` 璁板綍锛屾敮鎸佹寜 Query 鍏抽敭璇嶆悳绱?
  - 璇︽儏椤碉細鑰楁椂鐎戝竷鍥?+ Dense vs Sparse 骞跺垪瀵规瘮 + Rerank 鍓嶅悗鎺掑悕鍙樺寲
- **楠屾敹鏍囧噯**锛氭墽琛?query 鍚庯紝Dashboard 鏄剧ず鏌ヨ杩借釜璇︽儏涓庡悇闃舵瀵规瘮銆?
- **娴嬭瘯鏂规硶**锛氭墜鍔ㄩ獙璇侊紙鍏?query 鈫?鎵撳紑 Dashboard 鈫?鏌ョ湅杩借釜锛夈€?

---

## 闃舵 H锛氳瘎浼颁綋绯伙紙鐩爣锛氬彲鎻掓嫈璇勪及 + 鍙噺鍖栧洖褰掞級

### H1锛歊agasEvaluator 瀹炵幇
- **鐩爣**锛氬疄鐜?`ragas_evaluator.py`锛氬皝瑁?Ragas 妗嗘灦锛屽疄鐜?`BaseEvaluator` 鎺ュ彛銆?
- **淇敼鏂囦欢**锛?
  - `src/observability/evaluation/ragas_evaluator.py`锛堟柊澧烇級
  - `src/libs/evaluator/evaluator_factory.py`锛堟敞鍐?ragas provider锛?
  - `tests/unit/test_ragas_evaluator.py`锛堟柊澧烇級
- **瀹炵幇绫?鍑芥暟**锛?
  - `RagasEvaluator(BaseEvaluator)`锛氬疄鐜?`evaluate()` 鏂规硶
  - 鏀寔鎸囨爣锛欶aithfulness, Answer Relevancy, Context Precision
  - 浼橀泤闄嶇骇锛歊agas 鏈畨瑁呮椂鎶涘嚭鏄庣‘鐨?`ImportError` 鎻愮ず
- **楠屾敹鏍囧噯**锛歮ock LLM 鐜涓嬶紝`evaluate()` 杩斿洖鍖呭惈 faithfulness/answer_relevancy 鐨?metrics 瀛楀吀銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_ragas_evaluator.py`銆?

### H2锛欳ompositeEvaluator 瀹炵幇
- **鐩爣**锛氬疄鐜?`composite_evaluator.py`锛氱粍鍚堝涓?Evaluator 骞惰鎵ц锛屾眹鎬荤粨鏋溿€?
- **淇敼鏂囦欢**锛?
  - `src/observability/evaluation/composite_evaluator.py`锛堟柊澧烇級
  - `tests/unit/test_composite_evaluator.py`锛堟柊澧烇級
- **瀹炵幇绫?鍑芥暟**锛?
  - `CompositeEvaluator.__init__(evaluators: List[BaseEvaluator])`
  - `CompositeEvaluator.evaluate() -> dict`锛氬苟琛屾墽琛屾墍鏈?evaluator锛屽悎骞?metrics
  - 閰嶇疆椹卞姩锛歚evaluation.backends: [ragas, custom]` 鈫?宸ュ巶鑷姩缁勫悎
- **楠屾敹鏍囧噯**锛氶厤缃袱涓?evaluator 鏃讹紝杩斿洖鐨?metrics 鍖呭惈涓よ€呯殑鎸囨爣銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/unit/test_composite_evaluator.py`銆?

### H3锛欵valRunner + Golden Test Set
- **鐩爣**锛氬疄鐜?`eval_runner.py`锛氳鍙?`tests/fixtures/golden_test_set.json`锛岃窇 retrieval 骞朵骇鍑?metrics銆?
- **鍓嶇疆渚濊禆**锛欴5锛圚ybridSearch锛夈€丠1-H2锛堣瘎浼板櫒锛?
- **淇敼鏂囦欢**锛?
  - `src/observability/evaluation/eval_runner.py`锛堟柊澧烇級
  - `tests/fixtures/golden_test_set.json`锛堟柊澧烇細榛勯噾娴嬭瘯闆嗭級
  - `scripts/evaluate.py`锛堟柊澧烇細璇勪及杩愯鑴氭湰锛?
- **瀹炵幇绫?鍑芥暟**锛?
  - `EvalRunner.__init__(settings, hybrid_search, evaluator)`
  - `EvalRunner.run(test_set_path) -> EvalReport`锛氳繍琛岃瘎浼板苟杩斿洖鎶ュ憡
  - `EvalReport`锛氬寘鍚?hit_rate, mrr, 鍚?query 缁撴灉璇︽儏
- **golden_test_set.json 鏍煎紡**锛?
  ```json
  {
    "test_cases": [
      {
        "query": "濡備綍閰嶇疆 Azure OpenAI锛?,
        "expected_chunk_ids": ["chunk_abc_001", "chunk_abc_002"],
        "expected_sources": ["config_guide.pdf"]
      }
    ]
  }
  ```
- **楠屾敹鏍囧噯**锛歚python scripts/evaluate.py` 鍙繍琛岋紝杈撳嚭 metrics銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/integration/test_hybrid_search.py` 鎴?`python scripts/evaluate.py`銆?

### H4锛氳瘎浼伴潰鏉块〉闈?
- **鐩爣**锛氬疄鐜?Dashboard 璇勪及闈㈡澘椤甸潰锛堣繍琛岃瘎浼般€佹煡鐪嬫寚鏍囥€佸巻鍙插姣旓級銆?
- **鍓嶇疆渚濊禆**锛欻3锛圗valRunner锛夈€丟1锛圖ashboard 鏋舵瀯锛?
- **淇敼鏂囦欢**锛?
  - `src/observability/dashboard/pages/evaluation_panel.py`锛堝疄鐜帮細鏇挎崲鍗犱綅鎻愮ず锛?
- **瀹炵幇瑕佺偣**锛?
  - 閫夋嫨璇勪及鍚庣涓?golden test set
  - 鐐瑰嚮杩愯锛屽睍绀鸿瘎浼扮粨鏋滐紙hit_rate銆乵rr銆佸悇 query 鏄庣粏锛?
  - 鍙€夛細鍘嗗彶璇勪及缁撴灉瀵规瘮鍥?
- **楠屾敹鏍囧噯**锛氬彲鍦?Dashboard 涓繍琛岃瘎浼板苟鏌ョ湅鎸囨爣銆?
- **娴嬭瘯鏂规硶**锛氭墜鍔ㄩ獙璇併€?

### H5锛歊ecall 鍥炲綊娴嬭瘯锛圗2E锛?
- **鐩爣**锛氬疄鐜?`tests/e2e/test_recall.py`锛氬熀浜?golden set 鍋氭渶灏忓彫鍥為槇鍊硷紙渚嬪 hit@k锛夈€?
- **鍓嶇疆渚濊禆**锛欻3锛圗valRunner + golden_test_set锛?
- **淇敼鏂囦欢**锛?
  - `tests/e2e/test_recall.py`锛堟柊澧烇級
  - `tests/fixtures/golden_test_set.json`锛堣ˉ榻愯嫢骞叉潯锛?
- **楠屾敹鏍囧噯**锛歨it@k 杈惧埌闃堝€硷紙闃堝€煎啓姝诲湪娴嬭瘯閲岋紝渚夸簬鍥炲綊锛夈€?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/e2e/test_recall.py`銆?

---

## 闃舵 I锛氱鍒扮楠屾敹涓庢枃妗ｆ敹鍙ｏ紙鐩爣锛氬紑绠卞嵆鐢ㄧ殑"鍙鐜?宸ョ▼锛?

### I1锛欵2E锛歁CP Client 渚ц皟鐢ㄦā鎷?
- **鐩爣**锛氬疄鐜?`tests/e2e/test_mcp_client.py`锛氫互瀛愯繘绋嬪惎鍔?server锛屾ā鎷?tools/list + tools/call銆?
- **淇敼鏂囦欢**锛?
  - `tests/e2e/test_mcp_client.py`
- **楠屾敹鏍囧噯**锛氬畬鏁磋蛋閫?query_knowledge_hub 骞惰繑鍥?citations銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/e2e/test_mcp_client.py`銆?

### I2锛欵2E锛欴ashboard 鍐掔儫娴嬭瘯
- **鐩爣**锛氶獙璇?Dashboard 鍚勯〉闈㈠湪鏈夋暟鎹椂鍙甯告覆鏌撱€佹棤 Python 寮傚父銆?
- **淇敼鏂囦欢**锛?
  - `tests/e2e/test_dashboard_smoke.py`锛堟柊澧烇級
- **瀹炵幇瑕佺偣**锛?
  - 浣跨敤 Streamlit 鐨?`AppTest` 妗嗘灦杩涜鑷姩鍖栧啋鐑熸祴璇?
  - 楠岃瘉 6 涓〉闈㈠潎鍙姞杞姐€佷笉鎶涘紓甯?
- **楠屾敹鏍囧噯**锛氭墍鏈夐〉闈㈠啋鐑熸祴璇曢€氳繃銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q tests/e2e/test_dashboard_smoke.py`銆?

### I3锛氬畬鍠?README锛堣繍琛岃鏄?+ 娴嬭瘯璇存槑 + MCP 閰嶇疆 + Dashboard 浣跨敤锛?
- **鐩爣**锛氳鏂扮敤鎴疯兘鍦?10 鍒嗛挓鍐呰窇閫?ingest + query + dashboard + tests锛屽苟鑳藉湪 Copilot/Claude 涓娇鐢ㄣ€?
- **淇敼鏂囦欢**锛?
  - `README.md`
- **楠屾敹鏍囧噯**锛歊EADME 鍖呭惈浠ヤ笅绔犺妭锛?
  - **蹇€熷紑濮?*锛氬畨瑁呬緷璧栥€侀厤缃?API Key銆佽繍琛岄娆℃憚鍙?
  - **閰嶇疆璇存槑**锛歚settings.yaml` 鍚勫瓧娈靛惈涔?
  - **MCP 閰嶇疆绀轰緥**锛欸itHub Copilot `mcp.json` 涓?Claude Desktop `claude_desktop_config.json`
  - **Dashboard 浣跨敤鎸囧崡**锛氬惎鍔ㄥ懡浠ゃ€佸悇椤甸潰鍔熻兘璇存槑銆佹埅鍥剧ず渚?
  - **杩愯娴嬭瘯**锛氬崟鍏冩祴璇曘€侀泦鎴愭祴璇曘€丒2E 娴嬭瘯鍛戒护
  - **甯歌闂**锛欰PI Key 閰嶇疆銆佷緷璧栧畨瑁呫€佽繛鎺ラ棶棰樻帓鏌?
- **娴嬭瘯鏂规硶**锛氭寜 README 鎵嬪姩璧颁竴閬嶃€?

### I4锛氭竻鐞嗘帴鍙ｄ竴鑷存€э紙濂戠害娴嬭瘯琛ラ綈锛?
- **鐩爣**锛氫负鍏抽敭鎶借薄锛圴ectorStore / Reranker / Evaluator / DocumentManager锛夎ˉ榻愬绾︽祴璇曘€?
- **淇敼鏂囦欢**锛?
  - `tests/unit/test_vector_store_contract.py`锛堣ˉ榻?delete_by_metadata 杈圭晫锛?
  - `tests/unit/test_reranker_factory.py`锛堣ˉ榻愯竟鐣岋級
  - `tests/unit/test_custom_evaluator.py`锛堣ˉ榻愯竟鐣岋級
- **楠屾敹鏍囧噯**锛歚pytest -q` 鍏ㄧ豢锛屼笖 contract tests 瑕嗙洊涓昏杈撳叆杈撳嚭褰㈢姸銆?
- **娴嬭瘯鏂规硶**锛歚pytest -q`銆?

### I5锛氬叏閾捐矾 E2E 楠屾敹
- **鐩爣**锛氭墽琛屽畬鏁寸殑绔埌绔獙鏀舵祦绋嬶細ingest 鈫?query via MCP 鈫?Dashboard 鍙鍖?鈫?evaluate銆?
- **淇敼鏂囦欢**锛氭棤鏂版枃浠讹紝楠屾敹宸叉湁鍔熻兘
- **楠屾敹鏍囧噯**锛?
  - `python scripts/ingest.py --path tests/fixtures/sample_documents/ --collection test` 鎴愬姛
  - `python scripts/query.py --query "娴嬭瘯鏌ヨ" --verbose` 杩斿洖缁撴灉
  - Dashboard 鍙睍绀烘憚鍙栦笌鏌ヨ杩借釜
  - `python scripts/evaluate.py` 杈撳嚭璇勪及鎸囨爣
- **娴嬭瘯鏂规硶**锛氭墜鍔ㄥ叏閾捐矾璧伴€?+ `pytest -q` 鍏ㄩ噺娴嬭瘯銆?

---

### 浜や粯閲岀▼纰戯紙寤鸿锛?

- **M1锛堝畬鎴愰樁娈?A+B锛?*锛氬伐绋嬪彲娴?+ 鍙彃鎷旀娊璞″眰灏辩华锛屽悗缁疄鐜板彲骞惰鎺ㄨ繘銆?
- **M2锛堝畬鎴愰樁娈?C锛?*锛氱绾挎憚鍙栭摼璺彲鐢紝鑳芥瀯寤烘湰鍦扮储寮曘€?
- **M3锛堝畬鎴愰樁娈?D+E锛?*锛氬湪绾挎煡璇?+ MCP tools 鍙敤锛屽彲鍦?Copilot/Claude 涓皟鐢ㄣ€?
- **M4锛堝畬鎴愰樁娈?F锛?*锛欼ngestion + Query 鍙岄摼璺彲杩借釜锛孞SON Lines 鎸佷箙鍖栥€?
- **M5锛堝畬鎴愰樁娈?G锛?*锛氬叚椤甸潰鍙鍖栫鐞嗗钩鍙板氨缁紙璇勪及闈㈡澘涓哄崰浣嶏級锛屾暟鎹彲娴忚銆佸彲绠＄悊銆侀摼璺彲杩借釜銆?
- **M6锛堝畬鎴愰樁娈?H+I锛?*锛氳瘎浼颁綋绯诲畬鏁?+ E2E 楠屾敹閫氳繃 + 鏂囨。瀹屽杽锛屽舰鎴?闈㈣瘯/鏁欏/婕旂ず"鍙鐜伴」鐩€?



## 7. 鍙墿灞曟€т笌鏈潵灞曟湜

### 7.1 浜戠閮ㄧ讲涓庡悗绔灦鏋勫涔?
铏界劧褰撳墠闃舵鎴戜滑涓昏閲囩敤鈥滄湰鍦拌繍琛屸€濇ā寮忥紝浣嗘湰椤圭洰鐨勬灦鏋勮璁″畬鍏ㄦ敮鎸佸悜浜戠杩佺Щ銆傝繖涔熸槸涓€涓瀬浣崇殑瀛︿範鍚庣宸ョ▼鍖栫殑鍒囧叆鐐广€?
- **Server 瀹瑰櫒鍖?*锛氳鍒掔紪鍐?Dockerfile锛屽皢 MCP Server 鎵撳寘涓哄鍣ㄣ€傝繖璁╂垜浠湁鏈轰細娣卞叆鐞嗚В Python 鐜闅旂銆佷緷璧栫鐞嗕互鍙?Docker 鐨勬渶浣冲疄璺点€?
- **浜戠鎺ュ叆**锛氭湭鏉ュ彲浠ュ皢 Server 閮ㄧ讲鑷?Azure Container Apps 鎴?AWS Lambda銆?
    - **鎸戞垬涓庡涔犵偣**锛氬鐞嗙綉缁滃欢鏃躲€侀厤缃?API Gateway銆佸鍔?AuthN/AuthZ 閴存潈鏈哄埗锛堜繚鎶ょ鏈夋暟鎹笉琚叕寮€璁块棶锛夈€?
- **澶氱鎴蜂笌骞跺彂**锛氫粠鍗曠敤鎴锋湰鍦版湇鍔¤浆鍙樹负鏀寔鍥㈤槦鍏变韩鐨勬湇鍔°€?
    - **瀛︿範鐐?*锛氬湪 Chroma 涓疄鐜?Namespace 闅旂銆佸鐞嗗苟鍙戣姹傞攣銆佷紭鍖?embedding 缂撳瓨绛栫暐銆?

### 7.2 涓氬姟娣辫€曪細浠?閫氱敤"鍒?鍨傜洿" (Vertical Domain Adaptation)
RAG 绯荤粺鐨勪笂闄愬彇鍐充簬鍏跺鐗瑰畾涓氬姟鏁版嵁鐨勭悊瑙ｆ繁搴︺€傛湭鏉ョ殑鏍稿績鎵╁睍鏂瑰悜鏄皢閫氱敤鐨勬妧鏈鏋朵笌鍏蜂綋鐨勪笟鍔″満鏅繁搴︾粨鍚堛€傚湪灏嗘湰椤圭洰搴旂敤鍒板疄闄呯敓浜х幆澧冩椂锛岃瘑鍒苟瑙ｅ喅浠ヤ笅鈥滄渶鍚庝竴鍏噷鈥濈殑闅鹃锛屽皢鏄彁鍗囩郴缁熶环鍊肩殑鍏抽敭锛?

- **澶氭簮寮傛瀯鏁版嵁鐨勫鏉傞€傞厤**锛?
    - 鐜板疄涓氬姟涓笉浠呮湁 PDF锛岃繕澶ч噺瀛樺湪 PPTX, DOCX, XLSX 鐢氳嚦 HTML 鏁版嵁銆?
    - **鎸戞垬**锛氬浣曞鐞嗕笉鍚屾牸寮忕殑鐗规湁璇箟锛熶緥濡?PPT 涓殑婕旇鑰呭娉ㄥ線寰€姣旀鏂囨洿鍏抽敭锛孍xcel 涓殑鍏紡閫昏緫涓庤法琛屽叧鑱斿浣曚繚鐣欙紵鐩墠鐨勯€氱敤澶勭悊鏂瑰紡瀹规槗涓㈠け杩欎簺鈥滈殣鎬х煡璇嗏€濓紝鏈潵闇€瑕侀拡瀵规瘡绉嶆牸寮忔帰绱㈡洿娣卞害鐨勮В鏋愯兘鍔涖€?

- **澶嶆潅缁撴瀯鍖栨暟鎹殑绮剧‘鐞嗚В**锛?
    - 绠€鍗曠殑鏂囨湰鍒囧垎锛圕hunking锛夊湪澶勭悊琛ㄦ牸銆佸眰绾у垪琛ㄦ椂寰€寰€浼氱牬鍧忚涔夈€?
    - **鎸戞垬**锛?
        - **琛ㄦ牸鐞嗚В**锛氬浣曞鐞嗚法椤甸暱琛ㄦ牸銆佸悎骞跺崟鍏冩牸浠ュ強鍚湁澶嶆潅琛ㄥご鐨勮储鍔℃姤琛紵濡傛灉鍒囧垎涓嶅綋锛屾绱㈡椂鍙兘鎵惧埌鏁板瓧鍗翠笉鐭ラ亾瀵瑰簲鐨勫垪鍚嶏紙鎸囨爣鍚箟锛夈€?
        - **涓婁笅鏂囨柇瑁?*锛氬綋涓€涓畬鏁寸殑閫昏緫娈佃惤锛堝鍚堝悓鏉℃锛夎鍒囧垎鍒颁袱涓?chunk 鏃讹紝濡備綍淇濊瘉妫€绱㈠叾涓竴娈垫椂鑳芥劅鐭ュ埌鏁翠綋鐨勪笂涓嬫枃绾︽潫锛?

- **涓氬姟閫昏緫椹卞姩鐨勭敓鎴愭帶鍒?*锛?
    - 浠呬粎鏍规嵁鈥滅浉浼煎害鈥濆彫鍥炴枃妗ｅ湪浼佷笟绾у満鏅腑寰€寰€涓嶅銆?
    - **鎸戞垬**锛?
        - **鏃舵晥鎬т笌鐗堟湰绠＄悊**锛氬綋鐭ヨ瘑搴撲腑鍚屾椂瀛樺湪鈥?023鐗堚€濆拰鈥?024鐗堚€濊绔犳椂锛屽浣曠‘淇濈郴缁熶笉浼氭贩娣嗗巻鍙叉暟鎹笌鏈€鏂版爣鍑嗭紵
        - **鏉冮檺涓庡彈浼楅€傞厤**锛氶潰瀵瑰唴閮ㄥ憳宸ヤ笌澶栭儴瀹㈡埛锛屽浣曟帶鍒剁敓鎴愮瓟妗堢殑璇︾暐绋嬪害涓庢晱鎰熶俊鎭姭闇诧紵
        - **鎷掔瓟鏈哄埗**锛氬綋鍙洖鍐呭鐨勭疆淇″害涓嶈冻鏃讹紝濡備綍璁╃郴缁熻瘹瀹炲湴鍥炵瓟鈥滀笉鐭ラ亾鈥濊€屼笉鏄熀浜庣浉鍏虫€ц緝浣庣殑鐗囨寮鸿鎷煎噾绛旀锛堝够瑙夐棶棰橈級锛?

### 7.3 杩堝悜鑷富鏅鸿兘锛欰gentic RAG 鐨勬紨杩涜矾寰?
褰撳墠鐨?RAG 鏋舵瀯涓昏閬靛惊鈥滀竴娆℃绱?涓€娆＄敓鎴愨€濈殑鍥烘湁鑼冨紡锛屼絾鍦ㄩ潰瀵规瀬鍏跺鏉傜殑闂锛堝璺ㄦ枃妗ｅ姣斻€佸姝ユ帹鐞嗭級鏃讹紝鍗曚竴鐨勭嚎鎬ф祦绋嬪線寰€鍔涗笉浠庡績銆傛湰椤圭洰浣滀负鏍囧噯鐨?MCP Server锛屽ぉ鐒跺叿澶囧悜 **Agentic RAG锛堜唬鐞嗗紡 RAG锛?* 婕旇繘鐨勬綔鍔涖€傝繖涓嶉渶瑕侀噸鍐欑幇鏈変唬鐮侊紝鑰屾槸閫氳繃鍦?Server 绔彁渚涙洿缁嗙矑搴︾殑宸ュ叿锛岃祴鑳?Client 绔殑 Agent 鍏峰鏇村己鐨勮嚜涓绘€э細

- **浠庘€滃崟姝ユ绱⑩€濆埌鈥滃姝ュ喅绛栤€?*锛?
    - 鐩墠 Agent 鍙兘鍙皟鐢ㄤ竴涓€氱敤鐨?`search` 宸ュ叿銆?
    - **鏈潵婕旇繘**锛歋erver 鍙互鏆撮湶濡?`list_directory`锛堟煡鐪嬬洰褰曠粨鏋勶級銆乣preview_document`锛堥瑙堟憳瑕侊級銆乣verify_fact`锛堜簨瀹炴牳鏌ワ級绛夋洿鍘熷瓙鍖栫殑宸ュ叿銆侫gent 鍙互鍍忎汉绫荤爺绌跺憳涓€鏍凤紝鍏堢湅鐩綍鍦堝畾鑼冨洿锛屽啀閽堝鎬ч槄璇伙紝鏈€鍚庝氦鍙夐獙璇佷俊鎭紝浠庤€岃В鍐冲鏉傞棶棰樸€?
- **璁?Agent 鍏峰鈥滃弽鎬濃€濊兘鍔?*锛?
    - **鏈潵婕旇繘**锛氬埄鐢ㄧ幇鏈夌殑璇勪及妯″潡锛孲erver 鍙互鎻愪緵涓€涓?`self_check` 鎺ュ彛銆侫gent 鍦ㄧ敓鎴愮瓟妗堝悗锛屽彲浠ヨ嚜涓昏皟鐢ㄨ鎺ュ彛妫€娴嬫槸鍚﹀瓨鍦ㄥ够瑙夛紝鎴栬€呮绱㈢粨鏋滄槸鍚︾湡姝ｆ敮鎾戜簡璁虹偣銆傚鏋滃彂鐜颁笉瓒筹紝Agent 鍙互鑷富鍐冲畾杩涜绗簩杞洿娣卞害鐨勬悳绱€?
- **鍔ㄦ€佺瓥鐣ラ€夋嫨**锛?
    - **鏈潵婕旇繘**锛氫笉鍐嶇‖缂栫爜浣跨敤娣峰悎妫€绱€係erver 鍙互灏?`keyword_search` 鍜?`semantic_search` 浣滀负鐙珛宸ュ叿鏆撮湶銆侫gent 鍙互鏍规嵁鐢ㄦ埛鎰忓浘鑷富鍒ゆ柇锛氬鏋滄槸鎼滀汉鍚嶏紝鍙敤鍏抽敭璇嶆悳锛涘鏋滄槸鎼滄蹇碉紝閫氳繃璇箟鎼溿€傝繖绉嶅伐鍏蜂娇鐢ㄧ殑鐏垫椿鎬ф鏄?Agentic RAG 鐨勬牳蹇冮瓍鍔涖€?

杩欑婕旇繘鏂瑰悜灏嗘妸鏈」鐩粠涓€涓€滄櫤鑳芥悳绱㈠紩鎿庘€濆崌绾т负涓€涓€滄櫤鑳界爺绌跺姪鐞嗏€濈殑鍩虹璁炬柦搴曞骇銆?


