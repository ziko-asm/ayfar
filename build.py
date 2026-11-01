"""Builds index.html and p/<slug>.html from the project data below.

Run:  python build.py
"""
import html
import os

from ru import RU

MISSING = []


def R(en):
    """Russian text for an English string (ru.py). Missing ones are collected and fail the build."""
    if en in RU:
        return RU[en]
    MISSING.append(en)
    return en

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://ayfar.vercel.app"
CANON = SITE  # switch to "https://ayfar.az" once the domain points here
V = "29"  # cache-busting for assets

# Contact
PHONE = "+994772172358"
PHONE_SHOW = "+994\u00a077\u00a0217\u00a023\u00a058"
WA = "https://wa.me/994772172358"
WA_ORDER = WA + "?text=" + "Salam%20Ziya!%20Sayt%20sifari%C5%9Fi%20il%C9%99%20ba%C4%9Fl%C4%B1%20yaz%C4%B1ram."
EMAIL = "ziyaazizov9@gmail.com"
SCAN_SITE = "https://saytyoxla.vercel.app"
SCAN_API = SCAN_SITE + "/api/scan"
INSTAGRAM = "https://www.instagram.com/ayfar.web/"
X_URL = "https://x.com/ayfar_web"

# Services. price: None shows "price on request"; set e.g. ("150 ₼-dan", "from 150 ₼") to show a number.
SERVICES = [
    dict(icon="⚡", price=None,
         name=("Landing page", "Landing page"),
         desc=("Bir səhifəlik, sürətli sayt: biznesinizi, xidmətlərinizi və əlaqə məlumatlarınızı bir yerdə göstərir.",
               "A fast one-page site that shows your business, services and contacts in one place."),
         feats=(["Mobilə tam uyğun", "WhatsApp və zəng düyməsi", "Google-da görünmək üçün SEO", "Domen və hostinqin qurulması"],
                ["Fully mobile-friendly", "WhatsApp and call buttons", "SEO so Google can find you", "Domain and hosting set up"])),
    dict(icon="🏢", price=None,
         name=("Biznes saytı", "Business website"),
         desc=("Çoxsəhifəli korporativ sayt: xidmətlər, işlərinizdən şəkillər, haqqınızda və əlaqə səhifələri.",
               "A multi-page company site: services, photos of your work, about and contact pages."),
         feats=(["AZ · EN · RU dil dəstəyi", "Real iş şəkilləri, qalereya", "Google Xəritə və əlaqə forması", "Sürət və təhlükəsizlik yoxlaması"],
                ["AZ · EN · RU languages", "Real photos and a gallery", "Google Maps and contact options", "Speed and security check"])),
    dict(icon="🛒", price=None,
         name=("Onlayn mağaza", "Online shop"),
         desc=("Məhsul kataloqu, səbət və sifariş sistemi olan mağaza. Sifarişlər birbaşa WhatsApp-a gəlir.",
               "A shop with a product catalog, cart and ordering. Orders come straight to your WhatsApp."),
         feats=(["Kateqoriyalar və axtarış", "Səbət və sifariş", "WhatsApp ilə sifariş qəbulu", "Məhsulları özünüz yeniləyə bilərsiniz"],
                ["Categories and search", "Cart and checkout", "Orders over WhatsApp", "Update products yourself"])),
]

STEPS = [
    (("Yazırsınız", "You message me"), ("WhatsApp-da biznesinizi və nə istədiyinizi qısaca yazırsınız.", "Tell me on WhatsApp about your business and what you need.")),
    (("Plan və qiymət", "Plan and price"), ("Sizə uyğun həlli, müddəti və qiyməti pulsuz təklif edirəm.", "I send a free proposal with the plan, timeline and price.")),
    (("Dizayn və hazırlanma", "Design and build"), ("Saytı hazırlayıram, siz hər mərhələdə baxıb fikir bildirirsiniz.", "I build the site and you review it at every stage.")),
    (("Canlıya çıxır", "Go live"), ("Domen və hostinqi qururam, sayt Google-da görünməyə başlayır.", "I set up the domain and hosting, and the site goes live on Google.")),
]

# Client reviews: (quote_az, quote_en, name, business). The section stays hidden while this is empty.
# Add only real quotes from real clients.
REVIEWS = [
    ("Ziya MANSIA üçün çox gözəl və sürətli onlayn mağaza hazırladı. Brendimizin ruhunu tam başa düşdü, sifarişlər birbaşa WhatsApp-a gəlir. Hər mərhələdə bizimlə məsləhətləşdi. Tövsiyə edirəm!",
     "Ziya built a beautiful, fast online shop for MANSIA. He fully understood the spirit of our brand, and orders come straight to WhatsApp. He consulted us at every stage. I recommend him!",
     "Kamal", "MANSIA"),  # approved by the client on WhatsApp, 31.10.2026
]

CATS = {
    "game": ("Oyunlar", "Games"),
    "research": ("Tədqiqat", "Research"),
    "service": ("Xidmət və alətlər", "Services &amp; tools"),
    "web": ("Biznes saytları", "Business websites"),
}

P = [
    dict(
        slug="metro-tycoon", cat="game", status="on", c1="#ff4fd8", c2="#ffc94d",
        name=("Metro Tycoon", "Metro Tycoon"),
        url="https://siloveu.itch.io/metro-tycoon", show="siloveu.itch.io/metro-tycoon",
        tag=("Oyun · Brauzerdə", "Game · In the browser"),
        go=("İndi oyna", "Play now"), media=("scene", "metro"),
        metric=("₼ 2 mlrd", "manata qədər pul yığa bilərsən, sonra deponu 8 milyarda qaldırırsan.",
                "You can stack up to 2 billion manat, then upgrade your vault to 8 billion."),
        summary=("Bakı metrosunda qatar sürmə və biznes qurma oyunu: metronu qur, qatarı sür, milyonçu ol. İçərişəhərdən Həzi Aslanova qədər stansiya aç, coin yığ, maneələri keç, gizli kodları tap.",
                 "A train-driving tycoon game on the Baku metro: build the metro, drive the train, become a millionaire. Open stations from İçərişəhər to Həzi Aslanov, collect coins, beat obstacles and find hidden codes."),
        body=(["Metro Tycoon Bakı metrosunda keçən qatar sürmə və biznes qurma oyunudur. Qatarı İçərişəhərdən Həzi Aslanova qədər sürürsən. Yol boyu yeni stansiyalar açırsan: qatar orada dayanır, sərnişin götürür və sənə bonus verir.",
               "Yol boyu düzülmüş coinləri toplayıb pul qazanırsan. Qazancla vaqon, bilet, avtopilot, qatar və yol dizaynları, sürücün üçün paltar və kostyumlar alırsan, xarakterini dəyişirsən (Kamran, Leyla və başqaları).",
               "Oyunda iki valyuta var: manat və dollar (2 ₼ = 1 $). Əvvəlcə 2 milyard manat və 1 milyard dollara qədər yığa bilərsən, sonra deponu artırıb limiti 8 milyarda qaldırırsan."],
              ["Metro Tycoon is a train-driving and tycoon game set on the Baku metro. You drive from İçərişəhər all the way to Həzi Aslanov, opening new stations where the train stops, picks up passengers and pays you a bonus.",
               "Collect the coins lined up along the track and spend your earnings on wagons, tickets, autopilot, train and track designs, and outfits for your driver, or switch characters (Kamran, Leyla and more).",
               "There are two currencies, manat and dollars (2 ₼ = 1 $). At first you can hold up to 2 billion manat and 1 billion dollars, then upgrade your vault to raise the limit to 8 billion."]),
        bullets=(["<b>Maneələr:</b> yanğını şlanqla söndür, daş divarı silahla və ya Boşluq düyməsi ilə qır, elektrik telini ekrana toxunub kəs, qırıq relsi təmir et.",
                  "<b>Buz:</b> 28 May-dan sonra yol buz bağlayır, qatar sabit sürətlə sürüşür. Təkər yüksəlişi buzdan keçmə müddətini 8 saniyədən 3-ə endirir.",
                  "<b>Sirlər:</b> stansiyalarda tapmaca kimi gizlədilmiş kodlar gizli \"İnterfeys 2\"-ni açır. 100 milyon manatı almaza çevirsən, sirli \"Sevgi xətti\" açılır.",
                  "<b>Onlayn:</b> 2 oyunçu yarışı, hesab sistemi (istənilən cihazdan giriş), hədiyyə kodları, gündəlik bonus.",
                  "<b>Ədalətli oyun:</b> autoclicker aşkarlanır, söyüş işlədən hesab bloklanır.",
                  "<b>İdarəetmə:</b> telefonda ekrana basıb saxla, kompüterdə W / S və ya ↑ / ↓. Dillər: Azərbaycan, ingilis, rus."],
                 ["<b>Obstacles:</b> put out fires with a hose, smash stone walls with a gun or the Space key, cut live wires by tapping, repair broken rails.",
                  "<b>Ice:</b> after 28 May the track ices over and the train slides at a fixed speed. A wheel upgrade cuts the ice crossing from 8 seconds to 3.",
                  "<b>Secrets:</b> codes hidden as puzzles at stations unlock a secret \"Interface 2\". Turn 100 million manat into a diamond to open the mysterious \"Love Line\".",
                  "<b>Online:</b> 2-player races, accounts you can use on any device, gift codes and a daily bonus.",
                  "<b>Fair play:</b> auto-clickers are detected and accounts that swear get blocked.",
                  "<b>Controls:</b> press and hold the screen on a phone, or W / S and ↑ / ↓ on a computer. Languages: Azerbaijani, English, Russian."]),
        chips=["HTML5", "Canvas", "AZ · EN · RU", "itch.io"],
        github=None, note=None,
    ),
    dict(
        slug="provguard", cat="research", status="on", c1="#34f5b0", c2="#5b8cff",
        name=("ProvGuard", "ProvGuard"),
        url="https://provguard.vercel.app", show="provguard.vercel.app",
        tag=("Tədqiqat · Alət", "Research · Tool"), go=("Sayta keç", "Open site"), media=("reel", 4),
        metric=("33%→0%", "Canlı Qwen3 8B agentində hücum uğuru ProvGuard ilə belə düşdü. AgentDojo bank hücumlarının 144/144-ü dayandırıldı.",
                "Attack success on a live Qwen3 8B agent with ProvGuard. All 144 of 144 AgentDojo banking attacks were stopped."),
        summary=("AI agentlərini prompt injection hücumlarından qoruyan açıq mənbəli Python kitabxanası. Mətnin zərərli olub-olmadığını təxmin etmir, hər həssas arqumentin hansı mənbədən gəldiyini yoxlayır.",
                 "An open-source Python library that protects AI agents from prompt injection. It doesn't guess whether text is malicious; it checks which source supplied each sensitive argument."),
        body=(["AI agentləri yad adamların yazdığı e-poçtları, veb səhifələri və sənədləri oxuyur, sonra pul köçürmə, məktub göndərmə kimi real əməliyyatlar edir. Hücumçu mətnin içinə gizli əmr yazıb agenti idarə edə bilər.",
               "ProvGuard bu problemi fərqli yolla həll edir. Agentin gördüyü hər mətni etiketləyir (etibarlı və ya etibarsız), alət çağırılmazdan əvvəl isə hər arqumentin (alıcı, IBAN, məbləğ) haradan gəldiyini yoxlayır. Yalnız e-poçtda görünən IBAN, e-poçt necə yazılmasından asılı olmayaraq, pul köçürə bilməz.",
               "Saytda brauzerdə işləyən playground var: agenti \"hijack\" edib ProvGuard-ın necə qərar verdiyini canlı görmək olar. Nəticələr AgentDojo (ETH Zürich) benchmark-ında ölçülüb."],
              ["AI agents read e-mails, web pages and documents written by strangers, then take real actions like sending money or e-mail. An attacker can hide an instruction in that text and steer the agent.",
               "ProvGuard takes a different approach. It labels everything the agent sees as trusted or untrusted, and before a tool runs it checks where each argument (recipient, IBAN, amount) came from. An IBAN that only appears in an e-mail cannot move money, however the e-mail is worded.",
               "The site has an in-browser playground where you can hijack an agent and watch ProvGuard decide. Results are measured on the AgentDojo benchmark from ETH Zürich."]),
        bullets=(["<b>AgentDojo, modelsiz:</b> bank 144/144 (100%), Slack 97/105 (92%), workspace 200/240 (83%), travel 79/120 (66%).",
                  "<b>Canlı agent:</b> Qwen3 8B-də hücum uğuru 16/48-dən 0/48-ə düşdü, faydalılıq ölçülə biləcək qədər azalmadı.",
                  "<b>Açıq məhdudiyyətlər:</b> nəyi tuta bilmədiyi README-də açıq yazılıb."],
                 ["<b>AgentDojo, model-free:</b> banking 144/144 (100%), Slack 97/105 (92%), workspace 200/240 (83%), travel 79/120 (66%).",
                  "<b>Live agent:</b> on Qwen3 8B, attack success fell from 16/48 to 0/48 with no measurable utility drop.",
                  "<b>Honest limits:</b> what it can't catch is written up front in the README."]),
        chips=["Python", "LLM agents", "AgentDojo", "Ollama"],
        github="https://github.com/ziko-asm/provguard", note=None,
    ),
    dict(
        slug="prompt-injection-detector", cat="research", status="on", c1="#5b8cff", c2="#34f5b0",
        name=("Prompt Injection Detector Benchmark", "Prompt Injection Detector Benchmark"),
        url="https://prompt-injection-detector-snowy.vercel.app/", show="prompt-injection-detector-snowy.vercel.app",
        tag=("Tədqiqat · Benchmark", "Research · Benchmark"), go=("Sayta keç", "Open site"), media=("reel", 3),
        metric=("0.97→0.54", "Transformerin F1-i öz datasetində 0.97-dir, başqa datasetdə 0.54-ə düşür.",
                "Transformer F1 on its own dataset vs. on the other one."),
        summary=("Prompt injection detektorlarının həqiqətən nə qədər etibarlı olduğunu ölçən tədqiqat. Beş növ detektor iki açıq datasetdə öyrədilib və bir-birinin datasetində yoxlanılıb.",
                 "A study of how reliable prompt injection detectors really are. Five kinds of detector were trained on two public datasets and tested on each other's data."),
        body=(["Bir çox şirkət AI chatbotunu qorumaq üçün \"zərərli mətni tanıyan\" detektorlardan istifadə edir. Bu tədqiqat həmin detektorların data dəyişəndə nə qədər etibarlı qaldığını yoxlayır.",
               "Beş növ detektor sınanıb: açar söz qaydası, TF-IDF + logistik reqressiya, fine-tune olunmuş çoxdilli DistilBERT transformer, kaskad sistem və lokal Llama 3.2 3B və Llama 3.1 8B modelləri (LLM hakim). Hamısı iki açıq datasetdə (deepset və jackhhao) öyrədilib və bir-birinin datasetində test olunub.",
               "Nəticə: eyni datasetdə 0.96–0.98 F1 göstərən detektor digər datasetdə ya hücumların çoxunu buraxır, ya da zərərsiz mətnlərin 97%-ni bloklayır. Sayt bütün nəticələri interaktiv qrafiklər, sürət-dəqiqlik müqayisəsi və tam cədvəllə göstərir."],
              ["Many companies protect their AI chatbots with detectors that try to recognise malicious text. This study checks how reliable those detectors stay when the data changes.",
               "Five kinds of detector were tested: a keyword rule, TF-IDF + logistic regression, a fine-tuned multilingual DistilBERT transformer, a cascade, and local Llama 3.2 3B and Llama 3.1 8B models as LLM judges. All were trained on two public datasets (deepset and jackhhao) and tested on each other's data.",
               "The result: a detector that scores 0.96–0.98 F1 on its own dataset either misses most attacks on the other one or blocks up to 97% of harmless text. The site shows every result with interactive charts, a speed-vs-accuracy plot and the full table."]),
        bullets=(["<b>İki datasetdə birgə öyrətmək</b> boşluğun çoxunu bağlayır.",
                  "<b>Llama 3.1 8B</b> heç öyrədilmədən jackhhao-da 0.947 F1 alır, amma transformerdən 2100 dəfə yavaşdır.",
                  "<b>Kaskad</b> özündən əmin, amma səhv olan modeli xilas edə bilmir."],
                 ["<b>Training on both datasets</b> closes most of the gap.",
                  "<b>Llama 3.1 8B</b> reaches 0.947 F1 on jackhhao with no training, but is 2,100× slower than the transformer.",
                  "<b>A cascade</b> cannot rescue a model that is confidently wrong."]),
        chips=["PyTorch", "DistilBERT", "scikit-learn", "Llama 3"],
        github="https://github.com/ziko-asm/prompt-injection-detector", note=None,
    ),
    dict(
        slug="graphguard-iot", cat="research", status="on", c1="#34f5b0", c2="#ff7a45",
        name=("GraphGuard IoT", "GraphGuard IoT"),
        url="https://graphguard-iot.vercel.app/", show="graphguard-iot.vercel.app",
        tag=("Tədqiqat · IoT", "Research · IoT"), go=("Sayta keç", "Open site"), media=("reel", 3),
        metric=("0.70→0.01", "Botlar koordinasiyalı hərəkət edəndə GCN-in F1-i belə düşür.",
                "GCN F1 when the bots coordinate."),
        summary=("IoT şəbəkəsində ələ keçirilmiş cihazları (botnet) tapan qraf neyron şəbəkələrinin hücuma davamlılığını ölçən interaktiv benchmark.",
                 "An interactive benchmark of how well graph neural networks that find compromised IoT devices (botnets) hold up under attack."),
        body=(["Ağıllı evlərdə, zavodlarda minlərlə IoT cihazı bir-biri ilə danışır. Onlardan biri ələ keçiriləndə onu tapmaq üçün qraf neyron şəbəkələrindən (GNN) istifadə olunur. Bu layihə həmin detektorların hücum altında nə qədər davam gətirdiyini ölçür.",
               "GCN, GAT və GraphSAGE modelləri 1500 cihazlı IoT şəbəkəsində öyrədilib. Sonra iki yolla hücuma məruz qalıblar: şəbəkə əlaqələrini dəyişməklə (gradient və DICE hücumları) və botların öz trafikini dəyişməklə (PGD). DropEdge, kosinus budama və adversarial təlim müdafiələri müqayisə olunur.",
               "Sayt interaktivdir: hücum gücünü sürüşdürüb hər modelin necə çökdüyünü izləmək olar. 5 seed, hər rəqəm bir əmrlə təkrarlanır."],
              ["Thousands of IoT devices talk to each other in smart homes and factories. When one is compromised, graph neural networks (GNNs) are used to find it. This project measures how well those detectors hold up under attack.",
               "GCN, GAT and GraphSAGE were trained on a 1,500-device IoT network, then attacked in two ways: by rewiring links (gradient and DICE attacks) and by bots shifting their own traffic (PGD). DropEdge, cosine pruning and adversarial training are compared as defences.",
               "The site is interactive: drag the attack budget and watch each model degrade. 5 seeds, every number reproducible with one command."]),
        bullets=(["<b>Yalnız GraphSAGE</b> qrafdan real fayda görür (F1 0.81, AUC 0.97).",
                  "<b>Struktur hücumları</b> 3–8 F1 bal azaldır.",
                  "<b>Heç bir müdafiə pulsuz deyil</b> və heç biri koordinasiyalı yayınmanı tam həll etmir."],
                 ["<b>Only GraphSAGE</b> gets real value from the graph (F1 0.81, AUC 0.97).",
                  "<b>Structural attacks</b> cost 3–8 F1 points.",
                  "<b>No defence is free</b>, and none fixes coordinated evasion."]),
        chips=["PyTorch Geometric", "GNN", "FastAPI", "GNNExplainer"],
        github="https://github.com/ziko-asm/gnn-nids-robustt", note=None,
    ),
    dict(
        slug="ai-nids-lab", cat="research", status="on", c1="#ff7a45", c2="#34f5b0",
        name=("AI-NIDS Robustness Lab", "AI-NIDS Robustness Lab"),
        url="https://ai-nids-robustness.streamlit.app", show="ai-nids-robustness.streamlit.app",
        tag=("Tədqiqat · Şəbəkə", "Research · Network"), go=("Sayta keç", "Open site"), media=("scene", "nids"),
        metric=("3.7×", "UNSW-NB15-də hücumlar normal trafikə 3.7 dəfə yaxındır, ona görə detektorlar orada çökür.",
                "UNSW-NB15 attacks sit 3.7× closer to benign traffic, so detectors break there."),
        summary=("Şəbəkə hücumlarını aşkarlayan neyron şəbəkələrinin, hücumçu trafikini bir az dəyişəndə nə qədər asan aldandığını ölçən tədqiqat. Streamlit-də interaktiv dashboard.",
                 "A study of how easily neural network intrusion detectors are fooled when an attacker slightly shapes its own traffic, with an interactive Streamlit dashboard."),
        body=(["Neyron şəbəkə şəbəkə hücumlarını 99.9% dəqiqliklə tanıya bilər. Bəs hücumçu öz trafikini bir az dəyişsə, nə olur? Bu tədqiqat məhz bunu ölçür.",
               "MLP və 1D-CNN modelləri iki datasetdə öyrədilib: köhnə KDD Cup 1999 və daha müasir UNSW-NB15. Sonra FGSM və PGD hücumları ilə iki təhlükə modeli altında yoxlanılıb. Adversarial təlim müdafiə kimi sınanıb, hücumların gradient boosted ağaclara keçib-keçmədiyi ölçülüb, qərarlar Integrated Gradients ilə izah olunub.",
               "Əsas nəticə: KDD-də davamlı görünən detektorlar UNSW-NB15-də çökür, standart müdafiə isə orada iflasa uğrayır."],
              ["A neural network can detect network intrusions with 99.9% accuracy. But what happens when the attacker slightly reshapes its own traffic? That is what this study measures.",
               "MLP and 1D-CNN models were trained on two datasets, the old KDD Cup 1999 and the newer UNSW-NB15, then attacked with FGSM and PGD under two threat models. Adversarial training is tested as a defence, transfer to gradient-boosted trees is measured, and decisions are explained with Integrated Gradients.",
               "The headline: detectors that look robust on KDD break on UNSW-NB15, and the standard defence collapses there."]),
        bullets=(["<b>Standart adversarial təlim</b> UNSW-NB15-də CNN-in təmiz aşkarlama dərəcəsini 0.025-ə endirir.",
                  "<b>Qarışıq təlim</b> çöküşün qarşısını alır, amma davamlılığı şişirdilmiş görünür.",
                  "<b>Ağaclar</b> transfer hücumlarına qarşı daha yaxşı dayanır."],
                 ["<b>Standard adversarial training</b> drops the CNN's clean detection rate to 0.025 on UNSW-NB15.",
                  "<b>Mixed training</b> avoids the collapse, but its robustness is overstated.",
                  "<b>Trees</b> hold up better against transferred attacks."]),
        chips=["PyTorch", "1D-CNN", "PGD / FGSM", "Streamlit"],
        github="https://github.com/ziko-asm/ai-nids-adversarial-benchmark",
        note=("Streamlit tətbiqi boş qalanda yatır, ilk açılış bir neçə saniyə çəkə bilər.",
              "The Streamlit app sleeps when idle, so the first load can take a few seconds."),
    ),
    dict(
        slug="agent-audit", cat="service", status="on", c1="#5b8cff", c2="#ff4fd8",
        name=("Agent Audit", "Agent Audit"),
        url="https://agent-audit-ten.vercel.app/", show="agent-audit-ten.vercel.app",
        tag=("Xidmət", "Service"), go=("Sayta keç", "Open site"), media=("reel", 3),
        metric=("$0", "mini-skan həmişə pulsuzdur. Tam audit $400–800, aylıq monitorinq $150–300.",
                "the mini-scan is always free. Full audit $400–800, monthly monitoring $150–300."),
        summary=("Şirkətlərin AI chatbot və agentləri üçün təhlükəsizlik auditi xidməti: hücumları sınayır, sübutlar və konkret düzəlişlərlə hesabat verir.",
                 "A security audit service for companies' AI chatbots and agents: it runs real attacks and delivers a report with evidence and concrete fixes."),
        body=(["Əksər şirkətlər AI chatbotunu prompt injection-a qarşı heç yoxlamadan istifadəyə verir. Chatbot e-poçt, sənəd və ya veb səhifə oxuyub alətlərdən istifadə edirsə, ona yazan hər kəs onu idarə etməyə cəhd edə bilər.",
               "Agent Audit sistemi prompt injection, jailbreak, məlumat sızması, alət sui-istifadəsi və sistem promptunun oğurlanması hücumlarına qarşı test edir. Hər cavab hücumun işlədiyinə dair sübut üçün qiymətləndirilir. Sonda icmal, ciddilik cədvəli, sübutlar və düzəlişlərlə PDF hesabat verilir.",
               "Test yalnız sistem sahibinin yazılı icazəsi ilə aparılır."],
              ["Most teams ship an AI chatbot without ever testing it against prompt injection. If the assistant reads e-mails, documents or web pages and can call tools, anyone who writes to it can try to steer it.",
               "Agent Audit tests the system for prompt injection, jailbreaks, data exfiltration, tool misuse and system-prompt leakage. Each response is scored for evidence that an attack worked, and the result is a PDF report with an executive summary, a severity table, evidence and fixes.",
               "Testing only starts once the system owner has given written permission."]),
        bullets=(["<b>Pulsuz mini-skan:</b> 10–15 hücum yoxlaması, 1 səhifəlik xülasə.",
                  "<b>Tam audit ($400–800):</b> bütün hücum kitabxanası, çoxaddımlı ssenarilər, PDF hesabat, 30 dəqiqəlik zəng.",
                  "<b>Aylıq monitorinq ($150–300):</b> model və ya prompt dəyişəndə geriləmələri tutur."],
                 ["<b>Free mini-scan:</b> 10–15 attack probes and a one-page summary.",
                  "<b>Full audit ($400–800):</b> the full attack library, multi-turn scenarios, a PDF report and a 30-minute call.",
                  "<b>Monthly monitoring ($150–300):</b> catches regressions when prompts or models change."]),
        chips=["LLM security", "Red teaming", "PDF report"],
        github=None, note=None,
    ),
    dict(
        slug="saytyoxla", cat="service", status="on", c1="#34f5b0", c2="#5b8cff",
        name=("SaytYoxla", "SaytYoxla"),
        url="https://saytyoxla.vercel.app", show="saytyoxla.vercel.app",
        tag=("Pulsuz alət", "Free tool"), go=("Sayta keç", "Open site"), media=("scene", "yox"),
        metric=("30 san", "ərzində saytın təhlükəsizliyi, sürəti, mobil uyğunluğu və Google görünüşü yoxlanır.",
                "to check a site's security, speed, mobile readiness and Google visibility."),
        summary=("Azərbaycandakı kiçik bizneslər üçün pulsuz sayt yoxlama aləti. Nəticəni sadə Azərbaycan dilində izah edir, 0–100 bal və A–F qiymət verir.",
                 "A free website check for small businesses in Azerbaijan. It explains the result in plain Azerbaijani with a 0–100 score and an A–F grade."),
        body=(["Kiçik biznes sahibləri çox vaxt saytlarının təhlükəsiz olub-olmadığını, Google-da necə göründüyünü bilmir. SaytYoxla bunu 30 saniyədə, texniki biliyə ehtiyac olmadan göstərir.",
               "Saytın ünvanını yazırsınız: alət səhifəni bir dəfə yükləyir, TLS sertifikatına və iki açıq DNS qeydinə (SPF, DMARC) baxır. Hər tapıntı üçün status, sadə izah və düzəliş yolu verilir. Hesabatı PDF kimi çap etmək və WhatsApp ilə əlaqə saxlamaq olar.",
               "Alət yalnız adi ziyarətçinin brauzerinin gördüyünə baxır: gizli yolları yoxlamır, saytı sındırmağa cəhd etmir."],
              ["Small business owners often don't know whether their site is secure or how it looks to Google. SaytYoxla shows them in 30 seconds, with no technical knowledge needed.",
               "Enter an address: the tool loads the page once and checks the TLS certificate and two public DNS records (SPF, DMARC). Every finding comes with a status, a plain explanation and a fix. The report can be printed as a PDF, and there is a WhatsApp contact button.",
               "It only looks at what any visitor's browser sees: it never probes hidden paths or tries to break in."]),
        bullets=(["<b>Təhlükəsizlik:</b> HTTPS, sertifikat müddəti, HSTS, CSP, clickjacking qoruması, versiya sızması.",
                  "<b>E-poçt:</b> SPF və DMARC qeydləri.",
                  "<b>Sürət, mobil və Google:</b> cavab müddəti, HTML ölçüsü, viewport, başlıq, təsvir."],
                 ["<b>Security:</b> HTTPS, certificate expiry, HSTS, CSP, clickjacking protection, version disclosure.",
                  "<b>E-mail:</b> SPF and DMARC records.",
                  "<b>Speed, mobile &amp; Google:</b> response time, HTML size, viewport, title, description."]),
        chips=["Python", "FastAPI", "Vercel"],
        github="https://github.com/ziko-asm/saytyoxla",
        note=None,
    ),
    dict(
        slug="bathshop", cat="web", status="on", c1="#ffc94d", c2="#5b8cff",
        name=("bathshop.az", "bathshop.az"),
        url="https://bathshop-az-selling-site.vercel.app/", show="bathshop-az-selling-site.vercel.app",
        tag=("Onlayn mağaza", "Online shop"), go=("Sayta keç", "Open site"), media=("reel", 3),
        metric=("3 dil", "Azərbaycan, ingilis və rus dillərində işləyir.", "Works in Azerbaijani, English and Russian."),
        summary=("Bakıda hamam və isitmə avadanlıqları satan onlayn mağaza: su qızdırıcıları, qaz kombiləri, su nasosları. Səbət və sifariş sistemi ilə.",
                 "An online store for bathroom and heating equipment in Baku: water heaters, gas boilers and water pumps, with a cart and ordering."),
        body=(["bathshop.az Bakıda hamam və isitmə avadanlıqları satan onlayn mağazadır. Məhsullar kateqoriyalara bölünüb: su qızdırıcıları, qaz kombiləri və su nasosları.",
               "Müştəri məhsulları filtrləyir, ətraflı məlumata baxır, səbətə atır və sifarişi təsdiq edir. Sifarişlər ayrıca backend xidmətində işlənir. Saytda WhatsApp düyməsi, Bakı daxili sürətli çatdırılma və rəsmi zəmanət haqqında məlumat var."],
              ["bathshop.az is an online store for bathroom and heating equipment in Baku. Products are sorted into categories: water heaters, gas boilers and water pumps.",
               "Customers filter products, view details, add them to a cart and confirm an order, which is handled by a separate backend service. The site has a WhatsApp button and information on fast delivery within Baku and official warranty."]),
        bullets=(["<b>Kataloq:</b> kateqoriya filtrləri, qiymətlər, məhsul səhifələri.",
                  "<b>Səbət və sifariş:</b> səbətə at, sifarişi təsdiq et.",
                  "<b>Dillər:</b> Azərbaycan, ingilis, rus."],
                 ["<b>Catalogue:</b> category filters, prices, product pages.",
                  "<b>Cart &amp; checkout:</b> add to cart and confirm the order.",
                  "<b>Languages:</b> Azerbaijani, English, Russian."]),
        chips=["JavaScript", "Backend API", "AZ · EN · RU", "Vercel"],
        github=None, note=None,
    ),
    dict(
        slug="mexaniki-emal", cat="web", status="on", c1="#ffc94d", c2="#ff7a45",
        name=("Karusel torna emalı", "Vertical lathe machining"),
        url="https://mexaniki-emal.vercel.app/", show="mexaniki-emal.vercel.app",
        tag=("Biznes saytı", "Business site"), go=("Sayta keç", "Open site"), media=("reel", 3),
        metric=("Ø1750", "mm-ə qədər detallar. Adi tornada bu ölçü təxminən Ø400 mm olur.",
                "mm maximum part diameter, vs. about Ø400 mm on a standard lathe."),
        summary=("Mühəndis Telman Əzizovun Bakıdakı karusel torna emalı sexi üçün sayt: fırladıla bilən 3D flans modeli, real istehsalat şəkilləri və birbaşa WhatsApp sifarişi.",
                 "A website for engineer Telman Azizov's vertical lathe workshop in Baku, with a rotatable 3D flange, real workshop photos and direct WhatsApp ordering."),
        body=(["Bu sayt mühəndis Telman Əzizovun Bakıdakı karusel torna emalı sexi üçün hazırlanıb. Sex diametri 1750 mm-ə qədər olan iri sənaye detallarını emal edir: flanslar, halqalar, reduktor və nasos gövdələri, barabanlar, çarx gövdələri, plitələr və çertyoj üzrə işlər.",
               "Saytda texniki çertyoj üslubunda dizayn, fırladıla bilən 3D flans modeli, real istehsalat şəkilləri qalereyası, hər xidmət üçün ayrıca səhifə, ünvan, xəritə və birbaşa WhatsApp sifarişi var. Google axtarışı üçün optimallaşdırılıb."],
              ["This site was built for engineer Telman Azizov's vertical lathe (carousel) workshop in Baku. The workshop machines large industrial parts up to 1,750 mm in diameter: flanges, rings, gearbox and pump housings, drums, wheel bodies, plates and parts made from drawings.",
               "It has a technical-drawing look, a rotatable 3D flange model, a gallery of real workshop photos, a page for each service, address and map, and direct WhatsApp ordering. It is optimised for Google search."]),
        bullets=(["<b>3D model:</b> sürüşdürəndə fırlanan flans, \"altdan bax\" rejimi.",
                  "<b>Görülən işlər:</b> 10 real istehsalat şəkli, böyüdülə bilən.",
                  "<b>Dillər:</b> Azərbaycan, rus, ingilis."],
                 ["<b>3D model:</b> a flange you spin by dragging, with a \"view from below\" mode.",
                  "<b>Past work:</b> 10 real workshop photos you can zoom.",
                  "<b>Languages:</b> Azerbaijani, Russian, English."]),
        chips=["3D model", "SEO", "WhatsApp", "AZ · RU · EN"],
        github=None, note=None,
    ),
    dict(
        slug="mansia", cat="web", status="on", c1="#c084fc", c2="#ffc94d",
        name=("MANSIA", "MANSIA"),
        url="https://mansia.az/", show="mansia.az",
        tag=("Onlayn mağaza · Brend", "Online shop · Brand"), go=("Sayta keç", "Open site"), media=("reel", 4),
        metric=("11 növ", "təbii sabun, hər biri 95 qram, 5 kateqoriyada: üz, bədən, saç, xanımlar, xüsusi qulluq.",
                "of natural soap, 95 g each, in 5 categories: face, body, hair, women and special care."),
        summary=("Zəfərandan ilhamlanan təbii, əl işi sabun brendi MANSIA üçün onlayn mağaza: kolleksiya, hədiyyə qutuları, brendin hekayəsi və WhatsApp ilə sifariş.",
                 "An online shop for MANSIA, a brand of natural handmade soaps inspired by saffron: the collection, gift boxes, the brand story and ordering through WhatsApp."),
        body=(["MANSIA zəfərandan ilhamlanan təbii, əl işi sabunlar istehsal edən brenddir: zəfəran, yağlı zəfəran, sidr, düyü, çobanyastığı, qızılgül, dəfnə, rozmarin, kükürd və başqaları. Bu sayt brendin onlayn mağazası və vizit kartıdır.",
               "Müştəri kolleksiyaya baxır, sabunu kateqoriyaya görə süzür, karta toxunanda ətraflı məlumat, şəkillər və istifadə qaydası açılır. Səbət seçimləri və cəmi məbləği göstərir, bir düymə ilə sifariş hazır mesaj kimi WhatsApp-a göndərilir. Ödəniş sifariş təsdiqləndikdən sonra kartla edilir.",
               "Saytda hədiyyə qutuları, brendin 2022-ci ildə zəfəran soğanaqları ilə başlayan hekayəsi, \"Necə sifariş edim?\" bələdçisi və müştəri rəyləri bölməsi də var. Dizayn brendin bənövşəyi və qızılı rənglərində, zərif serif şriftlərlə hazırlanıb."],
              ["MANSIA is a brand of natural handmade soaps inspired by saffron: saffron, saffron oil, cedar, rice, chamomile, rose, bay leaf, rosemary, sulphur and more. This site is the brand's online shop and calling card.",
               "Customers browse the collection, filter soaps by category, and tap a card to open details, photos and how to use it. The cart shows the selection and total, and one button sends the order to WhatsApp as a ready-made message. Payment is by card once the order is confirmed.",
               "The site also has gift boxes, the brand story that began with saffron bulbs in 2022, a \"How do I order?\" guide and a reviews section. The design uses the brand's purple and gold with elegant serif type."]),
        bullets=(["<b>Kolleksiya:</b> 11 növ sabun, kateqoriya filtrləri, hər sabun üçün ətraflı pəncərə.",
                  "<b>Sifariş:</b> səbət, cəmi məbləğ, bir düymə ilə WhatsApp sifarişi, kartla ödəniş.",
                  "<b>Hədiyyəlik:</b> 6 sabunluq kraft hədiyyə qutusu və fotoqalereya.",
                  "<b>Brend hekayəsi:</b> zəfəran tarlasından sabuna qədər yol, zaman xətti ilə."],
                 ["<b>Collection:</b> 11 kinds of soap, category filters and a detail window for each.",
                  "<b>Ordering:</b> cart, running total, one-tap WhatsApp order, card payment.",
                  "<b>Gifts:</b> a 6-soap kraft gift box and a photo gallery.",
                  "<b>Brand story:</b> from the saffron field to the soap, told as a timeline."]),
        chips=["HTML · CSS · JS", "WhatsApp sifariş", "Mobil uyğun", ".az domen"],
        github=None, note=None,
    )
]

E = html.escape

# Metric values and chips written in Azerbaijani get their own English text; Russian comes from ru.py.
LOCAL_EN = {"₼ 2 mlrd": "₼ 2 bn", "30 san": "30 sec", "3 dil": "3 languages", "11 növ": "11 kinds",
            "WhatsApp sifariş": "WhatsApp orders", "Mobil uyğun": "Mobile-friendly", ".az domen": ".az domain"}


def L(text, tag="span", cls=""):
    """A short label in all three languages, or as-is when it reads the same everywhere."""
    if text in LOCAL_EN:
        return T(E(text), E(LOCAL_EN[text]), tag, cls)
    return f'<{tag} class="{cls}">{E(text)}</{tag}>' if cls else E(text)


def T(az, en, tag="span", cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c} lang="az">{az}</{tag}><{tag}{c} lang="en">{en}</{tag}><{tag}{c} lang="ru">{R(en)}</{tag}>'


def head(title_az, title_en, desc, url, og, depth=""):
    return f"""<!doctype html>
<html lang="az" data-lang="az">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title_az)}</title>
<meta name="title-az" content="{E(title_az)}">
<meta name="title-en" content="{E(title_en)}">
<meta name="title-ru" content="{E(R(title_en))}">
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{E(title_az)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{SITE}/{og}">
<meta name="theme-color" content="#05070b">
<meta name="google-site-verification" content="9FHzK0T2MlxLEmw8k1gnPzawKyXvbkJhKm1MKYsDFh4" />
<meta name="msvalidate.01" content="071B769B591B43B1773023FFFF98515D" />
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%2305070b'/%3E%3Ccircle cx='32' cy='32' r='17' fill='none' stroke='%2334f5b0' stroke-width='5'/%3E%3Ccircle cx='32' cy='32' r='5' fill='%23ff4fd8'/%3E%3C/svg%3E">
<link rel="apple-touch-icon" href="{depth}img/icon-180.png">
<link rel="manifest" href="{depth}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700;900&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<script>
document.documentElement.classList.add('js');
setTimeout(function(){{var b=document.body;if(!b)return;b.classList.remove('loading');b.classList.add('ready');var l=document.getElementById('loader');if(l)l.classList.add('done','gone');document.querySelectorAll('.reveal').forEach(function(e){{e.classList.add('in')}});}},5000);
</script>
<link rel="stylesheet" href="{depth}assets/site.css?v={V}">
"""


def chrome_bits(home_href):
    return f"""<a class="skip" href="#main">{T("Məzmuna keç", "Skip to content")}</a>
<div id="curtain" aria-hidden="true"><b>ayfar</b></div>
<canvas id="net" aria-hidden="true"></canvas>
<div class="aurora" aria-hidden="true"><i></i><i></i><i></i></div>
<div class="grain" aria-hidden="true"></div>
<div class="cur-dot" aria-hidden="true"></div>
<div class="cur-ring" aria-hidden="true"><span class="lbl">AÇ</span></div>
<div id="progress"></div>
<header class="top" id="hdr">
  <div class="bar">
    <a class="logo" href="{home_href}" data-nav><span class="dot"></span>ayfar</a>
    <nav class="links">
      <a href="{home_href}#projects" data-nav>{T("Layihələr", "Projects")}</a>
      <a href="{home_href}#services" data-nav>{T("Xidmətlər", "Services")}</a>
      <a href="{home_href}#about" data-nav>{T("Haqqımda", "About")}</a>
      <a href="{home_href}#contact" data-nav>{T("Əlaqə", "Contact")}</a>
    </nav>
    <button type="button" class="menu-btn" aria-expanded="false" aria-controls="mnav"><span class="sr">{T("Menyu", "Menu")}</span><i></i><i></i></button>
    <div class="lang" role="group" aria-label="Language">
      <span class="pill"></span>
      <button type="button" data-set-lang="az" aria-pressed="true">AZ</button>
      <button type="button" data-set-lang="en" aria-pressed="false">EN</button>
      <button type="button" data-set-lang="ru" aria-pressed="false">RU</button>
    </div>
  </div>
  <nav class="mnav" id="mnav" aria-label="Mobile">
    <a href="{home_href}#projects" data-nav>{T("Layihələr", "Projects")}</a>
    <a href="{home_href}#services" data-nav>{T("Xidmətlər", "Services")}</a>
    <a href="{home_href}#about" data-nav>{T("Haqqımda", "About")}</a>
    <a href="{home_href}#contact" data-nav>{T("Əlaqə", "Contact")}</a>
    <a class="mnav-wa" href="{WA_ORDER}" target="_blank" rel="noopener">{WA_SVG}<span>WhatsApp · {PHONE_SHOW}</span></a>
  </nav>
</header>
<aside class="wa-wrap" aria-label="WhatsApp"><a class="wa-float" href="{WA_ORDER}" target="_blank" rel="noopener" aria-label="WhatsApp">{WA_SVG}<span>{T("Yazın", "Message")}</span></a></aside>
"""


WA_SVG = '<svg viewBox="0 0 32 32" width="22" height="22" aria-hidden="true"><path fill="currentColor" d="M16 3C8.8 3 3 8.7 3 15.8c0 2.5.7 4.9 2 6.9L3 29l6.5-2c1.9 1 4.1 1.6 6.5 1.6 7.2 0 13-5.7 13-12.8S23.2 3 16 3zm0 23.3c-2.1 0-4.1-.6-5.8-1.7l-.4-.3-3.9 1.2 1.2-3.7-.3-.4c-1.2-1.8-1.9-3.9-1.9-6.1C4.9 9.8 9.9 5 16 5s11.1 4.8 11.1 10.8S22.1 26.3 16 26.3zm6.1-8c-.3-.2-2-1-2.3-1.1-.3-.1-.5-.2-.8.2-.2.3-.9 1.1-1.1 1.3-.2.2-.4.2-.7.1-.3-.2-1.4-.5-2.7-1.7-1-.9-1.7-2-1.9-2.3-.2-.3 0-.5.1-.7l.5-.6c.2-.2.2-.4.3-.6.1-.2 0-.4 0-.6l-1-2.5c-.3-.7-.6-.6-.8-.6h-.7c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.3 1.4 3.5c.2.2 2.4 3.6 5.8 5 .8.3 1.4.5 1.9.7.8.3 1.5.2 2.1.1.6-.1 2-.8 2.2-1.6.3-.8.3-1.4.2-1.6-.1-.1-.3-.2-.6-.4z"/></svg>'


def footer():
    return f"""<footer><div class="wrap">© 2026 ayfar · {T("Ziya Əzizov", "Ziya Azizov")} · <a href="tel:{PHONE}">{PHONE_SHOW}</a> · {T("Bakıda hazırlanıb", "Made in Baku")}</div></footer>"""


def scene(kind):
    if kind == "metro":
        return """<div class="scene metro" aria-hidden="true">
  <svg viewBox="0 0 600 420" preserveAspectRatio="xMidYMid slice">
    <defs><radialGradient id="tg"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#ff4fd8" stop-opacity="0"/></radialGradient></defs>
    <path class="track2" d="M40 330 L160 330 L230 260 L360 260 L430 190 L560 190"/>
    <path id="mpath" class="track" d="M40 300 L150 300 L220 230 L350 230 L420 160 L560 160"/>
    <g><circle class="coin" cx="95" cy="300" r="5"/><circle class="coin" cx="185" cy="265" r="5" style="animation-delay:.3s"/><circle class="coin" cx="285" cy="230" r="5" style="animation-delay:.6s"/><circle class="coin" cx="385" cy="195" r="5" style="animation-delay:.9s"/><circle class="coin" cx="490" cy="160" r="5" style="animation-delay:1.2s"/></g>
    <circle class="st" cx="40" cy="300" r="9"/><circle class="st" cx="150" cy="300" r="9"/><circle class="st" cx="220" cy="230" r="9"/><circle class="st" cx="350" cy="230" r="9"/><circle class="st" cx="420" cy="160" r="9"/><circle class="st" cx="560" cy="160" r="9"/>
    <text class="stl" x="48" y="330" text-anchor="middle">İçərişəhər</text><text class="stl" x="150" y="330" text-anchor="middle">28 May</text><text class="stl" x="220" y="212" text-anchor="middle">Nərimanov</text><text class="stl" x="350" y="258" text-anchor="middle">Koroğlu</text><text class="stl" x="420" y="142" text-anchor="middle">Əhmədli</text><text class="stl" x="540" y="142" text-anchor="middle">Həzi Aslanov</text>
    <g><circle r="26" fill="url(#tg)" opacity=".55"/><rect x="-24" y="-9" width="48" height="18" rx="7" fill="#fff"/><rect x="-24" y="-2" width="48" height="5" fill="#e5394a"/><rect x="12" y="-6" width="9" height="5" rx="1.5" fill="#1b2230"/>
      <animateMotion dur="7s" repeatCount="indefinite" rotate="auto" keyPoints="0;1;1" keyTimes="0;.85;1" calcMode="linear"><mpath href="#mpath"/></animateMotion></g>
  </svg>
  <div class="hud"><div class="cash">₼ <span>0</span></div><div class="spd"><span>0</span> KM/S</div></div>
  <div class="title"><small>★ BAKI · METRO ★</small>METRO<br>TYCOON</div>
</div>"""
    if kind == "nids":
        return """<div class="chrome"><i></i><i></i><i></i><b>ai-nids-robustness.streamlit.app</b></div>
<div class="scene nids" aria-hidden="true">
  <div class="cap"><span>DETECTION RATE</span><b>PGD ε = 0.5</b></div>
  <div class="bars"><div class="grp"><div class="bar"></div><div class="bar atk"></div></div><div class="grp"><div class="bar"></div><div class="bar atk"></div></div><div class="grp"><div class="bar"></div><div class="bar atk"></div></div><div class="grp"><div class="bar"></div><div class="bar atk"></div></div></div>
  <div class="lbls"><span>MLP</span><span>CNN</span><span>MLP·U</span><span>CNN·U</span></div>
  <div class="legend"><span><i></i>clean</span><span><i class="o"></i>attacked</span></div>
</div>"""
    return """<div class="chrome"><i></i><i></i><i></i><b>saytyoxla.vercel.app</b></div>
<div class="scene yox" aria-hidden="true">
  <div class="gauge"><svg viewBox="0 0 140 140"><defs><linearGradient id="gg" x1="0" x2="1"><stop offset="0" stop-color="#34f5b0"/><stop offset="1" stop-color="#5b8cff"/></linearGradient></defs><circle class="trk" cx="70" cy="70" r="60"/><circle class="val" cx="70" cy="70" r="60"/></svg>
    <div class="g"><div><b>A</b><small>87 / 100</small></div></div></div>
  <div class="checks"><div><i>✓</i>HTTPS</div><div><i>✓</i>SSL · 84 gün</div><div><i>✓</i>HSTS</div><div><i class="w">!</i>DMARC</div><div><i>✓</i>Mobile</div></div>
</div>"""


IMG_SLUG = {"provguard": "provguard", "prompt-injection-detector": "detector", "graphguard-iot": "graphguard",
            "agent-audit": "agentaudit", "bathshop": "bathshop", "mexaniki-emal": "mexaniki", "mansia": "mansia"}


def media_fixed(p, depth, badges=True, sizes="(min-width: 900px) 560px, 100vw"):
    kind, val = p["media"]
    if kind == "reel":
        base = IMG_SLUG[p["slug"]]
        alt = E(p["name"][1])
        imgs = "".join(
            f'<img src="{depth}img/{base}-{i}-s.webp" srcset="{depth}img/{base}-{i}-s.webp 960w, {depth}img/{base}-{i}.webp 1920w" '
            f'sizes="{sizes}" width="1920" height="1200" alt="{alt} — screenshot {i}" loading="lazy" decoding="async">'
            for i in range(1, val + 1))
        inner = f'<div class="chrome"><i></i><i></i><i></i><b>{E(p["show"])}</b></div><div class="reel n{val}"><div class="strip">{imgs}</div></div><span class="rec">LIVE</span>'
    else:
        inner = scene(val)
    b = ""
    if badges:
        st = T("canlı", "live") if p["status"] == "on" else T("müvəqqəti dayanıb", "offline for now")
        b = f'<div class="badge"><span class="tag {p["cat"]}">{T(*p["tag"])}</span><span class="tag {p["status"]}">{st}</span></div>'
    return f'<div class="media" style="--c1:{p["c1"]};--c2:{p["c2"]}">{inner}{b}</div>'


FAQ = [('Ayfar kimdir?', 'Who is ayfar?', 'Ayfar — Ziya Əzizovun internetdəki ləqəbidir. Ziya Bakıdan olan proqramlaşdırma, kibertəhlükəsizlik və süni intellekt mühəndisidir; saytlar, oyunlar və tədqiqat layihələri hazırlayır.', 'Ayfar is the online name of Ziya Azizov, a programming, cybersecurity and AI engineer from Baku who builds websites, games and research projects.'), ('Ziya Əzizov nə ilə məşğuldur?', 'What does Ziya Azizov do?', 'Kibertəhlükəsizlik və süni intellekt üzrə tədqiqatlar aparır (ProvGuard, Prompt Injection Detector Benchmark, GraphGuard IoT), bizneslər üçün saytlar (bathshop.az, karusel torna emalı) və oyunlar (Metro Tycoon) hazırlayır.', 'He does cybersecurity and AI research (ProvGuard, Prompt Injection Detector Benchmark, GraphGuard IoT) and builds business websites (bathshop.az, a lathe workshop site) and games (Metro Tycoon).'), ('Ziya Əzizov harada təhsil alıb?', 'Where did Ziya Azizov study?', 'Bakalavr təhsilini ADNSU-da Mexatronika və Robototexnika üzrə alıb. Hazırda Bakı Ali Neft Məktəbində (BHOS) texniki sistemlərdə idarəetmə üzrə magistraturada oxuyur.', "He holds a bachelor's in Mechatronics and Robotics from ASOIU and is now a master's student in control of technical systems at Baku Higher Oil School (BHOS)."), ('Ziya Əzizovla necə əlaqə saxlamaq olar?', 'How can I contact Ziya Azizov?', 'WhatsApp və ya zəng (+994 77 217 23 58), e-poçt (ziyaazizov9@gmail.com), Instagram (@ayfar.web), LinkedIn və ya GitHub vasitəsilə əlaqə saxlaya bilərsiniz.', 'By WhatsApp or phone (+994 77 217 23 58), e-mail (ziyaazizov9@gmail.com), Instagram (@ayfar.web), LinkedIn or GitHub.'),
       ('ayfar Ayfar Otomotiv ilə eyni şirkətdir?', 'Is ayfar the same as Ayfar Otomotiv?', 'Xeyr. ayfar — bakılı mühəndis Ziya Əzizovun şəxsi brendidir: saytlar, oyunlar və kibertəhlükəsizlik layihələri. Türkiyədəki avtomobil hissələri istehsalçısı Ayfar Otomotiv ilə heç bir əlaqəsi yoxdur.', 'No. ayfar is the personal brand of Ziya Azizov, an engineer from Baku who builds websites, games and cybersecurity projects. It has no connection to Ayfar Otomotiv, the Turkish auto parts manufacturer.'),
       ('Ziya Əzizovdan sayt sifariş etmək olar?', 'Can I order a website from Ziya Azizov?', 'Bəli. Landing page, biznes saytı və onlayn mağaza hazırlayır. WhatsApp-a (+994 77 217 23 58) yazın, pulsuz qiymət təklifi göndərsin.', 'Yes. He builds landing pages, business websites and online shops. Message him on WhatsApp (+994 77 217 23 58) for a free quote.')]


def faq_html():
    return "".join(f"""
        <details class="qa reveal">
          <summary>{T(qa, qe)}<i></i></summary>
          {T(aa, ae, "p")}
        </details>""" for qa, qe, aa, ae in FAQ)


def schema():
    import json
    person = {
        "@context": "https://schema.org", "@type": "Person", "@id": CANON + "/#ziya",
        "name": "Ziya Əzizov", "alternateName": ["ayfar", "Ziya Azizov", "Ziya Ezizov"],
        "url": CANON + "/",
        "image": {"@type": "ImageObject", "url": SITE + "/img/ziya-azizov-ayfar.jpg", "width": 720, "height": 720,
                  "caption": "Ziya Əzizov (ayfar), veb developer və kibertəhlükəsizlik mühəndisi, Bakı",
                  "creditText": "Ziya Əzizov", "creator": {"@id": CANON + "/#ziya"}, "copyrightNotice": "© Ziya Əzizov"},
        "telephone": PHONE, "email": EMAIL,
        "jobTitle": "Proqramlaşdırma, kibertəhlükəsizlik və süni intellekt mühəndisi",
        "address": {"@type": "PostalAddress", "addressLocality": "Bakı", "addressCountry": "AZ"},
        "alumniOf": {"@type": "CollegeOrUniversity", "name": "Azərbaycan Dövlət Neft və Sənaye Universiteti"},
        "affiliation": {"@type": "CollegeOrUniversity", "name": "Bakı Ali Neft Məktəbi"},
        "knowsAbout": ["Proqramlaşdırma", "Kibertəhlükəsizlik", "Süni intellekt", "Veb saytlar", "Oyun hazırlama"],
        "sameAs": ["https://www.linkedin.com/in/ziya-azizov-91bba638a", INSTAGRAM, X_URL, "https://github.com/ziko-asm", "https://siloveu.itch.io"],
    }
    site = {"@context": "https://schema.org", "@type": "WebSite", "name": "ayfar", "url": CANON + "/",
            "inLanguage": ["az", "en", "ru"], "publisher": {"@id": CANON + "/#ziya"}}
    service = {
        "@context": "https://schema.org", "@type": "ProfessionalService", "@id": CANON + "/#ayfar",
        "name": "ayfar", "alternateName": "ayfar — veb sayt hazırlanması",
        "description": "Bakıda bizneslər üçün landing page, korporativ sayt və onlayn mağaza hazırlanması. Ziya Əzizov.",
        "url": CANON + "/#services", "logo": SITE + "/img/og/home.png", "image": SITE + "/img/og/home.png",
        "telephone": PHONE, "email": EMAIL, "founder": {"@id": CANON + "/#ziya"},
        "areaServed": {"@type": "City", "name": "Bakı"},
        "address": {"@type": "PostalAddress", "addressLocality": "Bakı", "addressCountry": "AZ"},
        "knowsLanguage": ["az", "en", "ru"],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Xidmətlər", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"][0], "description": s["desc"][0]}}
            for s in SERVICES]},
        "sameAs": [INSTAGRAM, X_URL, "https://www.linkedin.com/in/ziya-azizov-91bba638a", "https://github.com/ziko-asm"],
    }
    faqp = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, _, a, _ in FAQ]}
    return "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in (person, site, service, faqp))


LASTMOD = "2026-10-31"  # bump when content changes


def llms_txt():
    lines = [
        "# ayfar",
        "",
        "> ayfar is the online name and personal brand of Ziya Azizov (Ziya Əzizov), an engineer from Baku, Azerbaijan "
        "(born 2005) working in programming, cybersecurity and AI. He builds websites for businesses, games and security "
        "research tools. Not related to Ayfar Otomotiv (Turkey).",
        "",
        "ayfar — Bakıdan olan mühəndis Ziya Əzizovun brendidir. Bizneslər üçün saytlar (landing page, korporativ sayt, "
        "onlayn mağaza), oyunlar və kibertəhlükəsizlik layihələri hazırlayır.",
        "",
        f"Contact / Əlaqə: WhatsApp and phone {PHONE}, e-mail {EMAIL}",
        "",
        "## Services / Xidmətlər",
        "",
    ]
    lines += [f"- {s['name'][1]} ({s['name'][0]}): {s['desc'][1]}" for s in SERVICES]
    lines += ["", "## Projects / Layihələr", ""]
    lines += [f"- [{p['name'][1]}]({CANON}/p/{p['slug']}.html): {p['summary'][1]} Live: {p['url']}" for p in P]
    lines += ["", "## Links", "",
              f"- [Home]({CANON}/)", f"- [Services]({CANON}/#services)", f"- [About]({CANON}/#about)",
              "- [GitHub](https://github.com/ziko-asm)", "- [LinkedIn](https://www.linkedin.com/in/ziya-azizov-91bba638a)", ""]
    return "\n".join(lines)


def build_seo_files():
    urls = [CANON + "/"] + [f"{CANON}/p/{p['slug']}.html" for p in P]
    photo = (f"<image:image><image:loc>{SITE}/img/ziya-azizov-ayfar.jpg</image:loc></image:image>")
    xml = "\n".join(f"  <url><loc>{u}</loc><lastmod>{LASTMOD}</lastmod>{photo if u == CANON + '/' else ''}</url>" for u in urls)
    with open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(llms_txt())
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n{xml}\n</urlset>\n')
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {CANON}/sitemap.xml\n")


def sec_no(base):
    """Sections after services move down by one when the reviews section is shown."""
    return f"{(base + 1 if REVIEWS else base):02d}"


def services_html():
    cards = []
    for s in SERVICES:
        price = T(*s["price"]) if s["price"] else T("Qiymət layihəyə görə", "Price on request")
        fa = "".join(f"<li>{x}</li>" for x in s["feats"][0])
        fe = "".join(f"<li>{x}</li>" for x in s["feats"][1])
        fr = "".join(f"<li>{R(x)}</li>" for x in s["feats"][1])
        cards.append(f"""
        <article class="svc reveal">
          <div class="svc-ic" aria-hidden="true">{s['icon']}</div>
          <h3>{T(*s['name'])}</h3>
          {T(s['desc'][0], s['desc'][1], 'p')}
          <ul lang="az">{fa}</ul><ul lang="en">{fe}</ul><ul lang="ru">{fr}</ul>
          <div class="svc-price">{price}</div>
          <a class="btn small magnet" href="{WA_ORDER}" target="_blank" rel="noopener">{T("Təklif al", "Get a quote")} <span class="arr">→</span></a>
        </article>""")
    steps = "".join(f"""
        <li class="step reveal"><b>{n:02d}</b><h4>{T(*t)}</h4>{T(d[0], d[1], 'p')}</li>""" for n, (t, d) in enumerate(STEPS, 1))
    return f"""
  <section id="services">
    <div class="wrap">
      <div class="sec-head reveal"><div><div class="sec-num">02 — {T("XİDMƏTLƏR", "SERVICES")}</div><h2>{T("Sizə sayt", "A site for you")}</h2></div></div>
      {T("Bizneslər üçün sürətli, müasir və mobilə uyğun saytlar hazırlayıram. Yuxarıdakı bathshop.az, MANSIA və torna sexi saytları bu işlərdəndir.", "I build fast, modern, mobile-friendly websites for businesses. bathshop.az, MANSIA and the lathe workshop site above are examples.", "p", "svc-lead reveal")}
      {scan_html()}
      <div class="svc-grid">{''.join(cards)}
      </div>
      <div class="sec-num steps-h reveal">{T("NECƏ İŞLƏYİRİK", "HOW IT WORKS")}</div>
      <ol class="steps">{steps}
      </ol>
      <div class="svc-cta reveal">
        <a class="btn primary magnet" href="{WA_ORDER}" target="_blank" rel="noopener">{WA_SVG}<span>{T("WhatsApp-a yaz", "Message on WhatsApp")}</span></a>
        <a class="btn magnet" href="tel:{PHONE}">📞 <span>{PHONE_SHOW}</span></a>
      </div>
    </div>
  </section>"""


def scan_html():
    """Live site check powered by SaytYoxla (results come from its API; see assets/home.js)."""
    return f"""<div class="scan reveal" id="scan">
        <div class="scan-intro">
          <div class="sec-num">{T("PULSUZ YOXLAMA", "FREE CHECK")}</div>
          {T("Saytınız neçə bal alır?", "How does your site score?", "h3")}
          {T('Ünvanı yazın: təhlükəsizlik, sürət, mobil uyğunluq və Google görünüşü bir neçə saniyəyə yoxlanılır. Yoxlamanı mənim hazırladığım <a href="' + SCAN_SITE + '" target="_blank" rel="noopener">SaytYoxla</a> aparır.',
             'Enter an address: security, speed, mobile readiness and Google visibility are checked in seconds. The check runs on <a href="' + SCAN_SITE + '" target="_blank" rel="noopener">SaytYoxla</a>, a tool I built.', "p")}
        </div>
        <form class="scan-form" id="scanForm" data-api="{SCAN_API}" data-site="{SCAN_SITE}" data-wa="{WA}" novalidate>
          <label class="sr" for="scanUrl">{T("Saytın ünvanı", "Website address")}</label>
          <input id="scanUrl" name="url" type="text" inputmode="url" autocomplete="url" autocapitalize="off" spellcheck="false" maxlength="300" placeholder="example.az" required>
          <button class="btn primary" type="submit"><span class="scan-go">{T("Yoxla", "Check")}</span><span class="scan-wait">{T("Yoxlanılır…", "Checking…")}</span></button>
        </form>
        <div class="scan-out" id="scanOut" aria-live="polite"></div>
      </div>"""


def reviews_html():
    if not REVIEWS:
        return ""
    cards = "".join(f"""
        <figure class="rev reveal"><blockquote>{T(qa, qe, 'p')}</blockquote><figcaption><b>{E(n)}</b><span>{E(b)}</span></figcaption></figure>"""
                    for qa, qe, n, b in REVIEWS)
    return f"""
  <section id="reviews">
    <div class="wrap">
      <div class="sec-head reveal"><div><div class="sec-num">03 — {T("RƏYLƏR", "REVIEWS")}</div><h2>{T("Müştərilər deyir", "What clients say")}</h2></div></div>
      <div class="rev-grid">{cards}
      </div>
    </div>
  </section>"""


def build_index():
    n = len(P)
    counts = {k: sum(1 for p in P if p["cat"] == k) for k in CATS}
    slides = []
    for i, p in enumerate(P):
        gh = f'<a class="btn small" href="{p["github"]}" target="_blank" rel="noopener">GitHub</a>' if p["github"] else ""
        slides.append(f"""
      <article class="slide" data-cat="{p['cat']}" style="--c1:{p['c1']};--c2:{p['c2']}">
        <a class="slide-media tiltable" data-tilt="5" href="p/{p['slug']}.html" data-nav aria-label="{E(p['name'][0])}">{media_fixed(p, '', sizes="(min-width: 900px) 620px, 92vw")}</a>
        <div class="slide-body">
          <div class="slide-idx"><b>{i + 1:02d}</b> / {n:02d} · {T(*CATS[p['cat']])}</div>
          <h3>{T(*p['name'])}</h3>
          <div class="url">{E(p['show'])}</div>
          {T(p['summary'][0], p['summary'][1], 'p', 'sum')}
          <div class="metric"><div class="v">{L(p['metric'][0])}</div>{T(p['metric'][1], p['metric'][2], 'div', 'd')}</div>
          <div class="slide-go">
            <a class="btn primary small magnet" href="p/{p['slug']}.html" data-nav>{T('Ətraflı', 'Details')}<span class="arr">→</span></a>
            <a class="btn small magnet" href="{p['url']}" target="_blank" rel="noopener">{T(*p['go'])} <span>↗</span></a>
            {gh}
          </div>
        </div>
      </article>""")
    chips = "".join(f'<button type="button" data-jump="{k}">{T(*v)}<sup>{counts[k]}</sup></button>' for k, v in CATS.items())

    page = head("ayfar — Ziya Əzizov | Saytlar, oyunlar və layihələr", "ayfar — Ziya Azizov | Websites, games & projects",
                "Ayfar — Ziya Əzizov, Bakıdan proqramlaşdırma, kibertəhlükəsizlik və süni intellekt mühəndisi. Saytları, oyunları (Metro Tycoon) və tədqiqat layihələri bir yerdə.",
                CANON + "/", "img/og/home.png")
    page += f'<link rel="stylesheet" href="assets/home.css?v={V}">\n' + schema() + '</head>\n<body>\n'
    page += """<div id="loader" aria-hidden="true">
  <div class="panel t"></div><div class="panel b"></div>
  <div class="inner">
    <svg viewBox="0 0 600 150" width="min(86vw,520px)"><text x="50%" y="115" text-anchor="middle">ayfar</text><text class="fill" x="50%" y="115" text-anchor="middle">ayfar</text></svg>
    <div class="bar"><i id="lbar"></i></div>
    <div class="count"><span id="lnum">000</span> / 100</div>
  </div>
</div>
"""
    page += chrome_bits("./")
    page += f"""
<main id="main">
  <div class="wrap hero">
    <div class="eyebrow reveal-hero"><span class="live"></span>{T(f"Ziya Əzizov · Bakı · {n} canlı layihə", f"Ziya Azizov · Baku · {n} live projects")}</div>
    <h1 class="word" aria-label="ayfar"><span aria-hidden="true">a</span><span aria-hidden="true">y</span><span aria-hidden="true">f</span><span aria-hidden="true">a</span><span aria-hidden="true">r</span></h1>
    <p class="tagline reveal-hero d1">{T('Mən <span class="rot" data-words="saytlar|oyunlar|alətlər|layihələr">saytlar</span> yaradıram.', 'I build <span class="rot" data-words="websites|games|tools|projects">websites</span>.')}</p>
    {T("Hazırladığım bütün saytlar, alətlər, oyunlar və layihələr bu səhifədədir. Aşağıdakı metroda qatarı özünüz sürün, sonra layihələrə keçin.", "Every site, tool, game and project I've built is on this page. Drive the metro below yourself, then scroll on to the projects.", "p", "lead reveal-hero d2")}

    <div class="mgame reveal-hero d3" id="gameWrap">
      <canvas id="game" role="img" aria-label="Mini metro game"></canvas>
      <div class="g-hud">
        <div class="cash">₼ <b id="gCash">0</b></div>
        <div><b id="gSpd">0</b> KM/S</div>
        <div class="next">{T("Növbəti", "Next")}: <b id="gNext">—</b></div>
        <div class="best">{T("Rekord", "Best")}: <b id="gBest">0</b> ₼</div>
      </div>
      <button type="button" class="g-start" id="gStart">
        <span class="g-play">▶</span>
        <span>{T("OYNA", "PLAY")}</span>
        <small>{T("Basılı saxla: qaz · burax: tormoz · stansiyada dayan · qırmızı işıqdan keçmə", "Hold: go · release: brake · stop at stations · never run a red")}</small>
      </button>
      <div class="g-over" id="gOver">
        <b>{T("Qəza!", "Crash!")}</b>
        <div class="g-score"><span>{T("Qazanc", "Earned")}</span><strong data-score>0 ₼</strong><span>{T("Rekord", "Best")}: <em data-best>0 ₼</em></span></div>
        <div class="g-row">
          <button type="button" class="btn primary small" data-again>{T("Yenidən", "Again")} ↻</button>
          <a class="btn small" href="https://siloveu.itch.io/metro-tycoon" target="_blank" rel="noopener">{T("Tam oyunu oyna", "Play the full game")} ↗</a>
        </div>
      </div>
      <div class="g-toast" id="gToast"></div>
    </div>

    <div class="cta reveal-hero d4">
      <a class="btn primary magnet" href="#projects">{T("Layihələrə bax", "See the projects")}<span class="arr">→</span></a>
      <a class="btn magnet" href="#services">{T("Sayt sifariş et", "Order a website")}<span class="arr">→</span></a>
      <a class="btn magnet" href="https://siloveu.itch.io/metro-tycoon" target="_blank" rel="noopener"><span>🎮</span>{T("Metro Tycoon tam versiya", "Metro Tycoon full game")}</a>
    </div>
  </div>

  <div class="wrap">
    <div class="stats reveal">
      <div class="stat"><div class="n" data-count="{n}">0</div><div class="l">{T("canlı layihə", "live projects")}</div></div>
      <div class="stat"><div class="n" data-count="{counts['game']}">0</div><div class="l">{T("oyun", "game")}</div></div>
      <div class="stat"><div class="n" data-count="{counts['research']}">0</div><div class="l">{T("tədqiqat layihəsi", "research projects")}</div></div>
      <div class="stat"><div class="n" data-count="{counts['service'] + counts['web']}">0</div><div class="l">{T("sayt, xidmət və alət", "sites, services &amp; tools")}</div></div>
    </div>
  </div>

  <div class="marquee" aria-hidden="true"><div class="tilt">
    <div class="mq"><span class="f">METRO TYCOON</span><span class="x">✦</span><span>PROVGUARD</span><span class="x">✦</span><span class="s">BATHSHOP.AZ</span><span class="x">✦</span><span>GRAPHGUARD</span><span class="x">✦</span><span class="f">MANSIA</span><span class="x">✦</span><span>AGENT AUDIT</span><span class="x">✦</span><span class="f">METRO TYCOON</span><span class="x">✦</span><span>PROVGUARD</span><span class="x">✦</span><span class="s">BATHSHOP.AZ</span><span class="x">✦</span><span>GRAPHGUARD</span><span class="x">✦</span><span class="f">SAYTYOXLA</span><span class="x">✦</span><span>AGENT AUDIT</span><span class="x">✦</span></div>
    <div class="mq rev"><span>KARUSEL TORNA</span><span class="x">●</span><span class="s">AI-NIDS LAB</span><span class="x">●</span><span>PROMPT INJECTION</span><span class="x">●</span><span class="f">AYFAR</span><span class="x">●</span><span>KARUSEL TORNA</span><span class="x">●</span><span class="s">AI-NIDS LAB</span><span class="x">●</span><span>PROMPT INJECTION</span><span class="x">●</span><span class="f">AYFAR</span><span class="x">●</span></div>
  </div></div>

  <section id="projects" class="hs" >
    <div class="hs-sticky" id="hs">
      <div class="hs-head wrap">
        <div>
          <div class="sec-num">01 — {T("İŞLƏR", "WORK")}</div>
          <h2>{T("Layihələr", "Projects")}</h2>
        </div>
        <div class="hs-meta">
          <div class="hs-count"><b data-cur>01</b><span>/ {n:02d}</span></div>
          <div class="hs-chips">{chips}</div>
        </div>
      </div>
      <div class="hs-track">{''.join(slides)}
      </div>
      <div class="hs-foot wrap"><div class="hs-bar"><i></i></div><span class="hs-hint">{T("Aşağı sürüşdür →", "Scroll down →")}</span></div>
    </div>
  </section>

{services_html()}
{reviews_html()}
  <section id="about">
    <div class="wrap">
      <div class="sec-head reveal"><div><div class="sec-num">{sec_no(3)} — {T("MƏN", "ME")}</div><h2>{T("Haqqımda", "About me")}</h2></div></div>
      <div class="about">
        <div class="reveal">
          <p class="big" lang="az">Salam, mən <em>Ziya Əzizovam</em>. İnternetdə <em>ayfar</em> kimi tanınıram.</p>
          <p class="big" lang="en">Hi, I'm <em>Ziya Azizov</em>, known online as <em>ayfar</em>.</p>
          <p class="big" lang="ru">Привет, я <em>Зия Азизов</em>, в сети известен как <em>ayfar</em>.</p>
          {T("2005-ci ildə Bakı şəhərində anadan olmuşam və Bakıda yaşayıram. Proqramlaşdırma, kibertəhlükəsizlik və süni intellekt ilə məşğul olan mühəndisəm.", "I was born in Baku in 2005 and still live there. I'm an engineer working in programming, cybersecurity and artificial intelligence.", "p")}
          {T("Bakalavr təhsilimi Azərbaycan Dövlət Neft və Sənaye Universitetində (ADNSU) Mexatronika və Robototexnika ixtisası üzrə almışam. Hazırda Bakı Ali Neft Məktəbində (BHOS) texniki sistemlərdə idarəetmə üzrə magistr təhsili alıram.", "I earned my bachelor's degree in Mechatronics and Robotics at Azerbaijan State Oil and Industry University (ASOIU). I'm now studying for a master's degree in control of technical systems at Baku Higher Oil School (BHOS).", "p")}
          {T("Bu dünyanı mənə bakalavrın 1-ci kursunda keçdiyimiz <b>Fundamentals of Programming</b> fənni tanıtdı. 2023-cü ildə, hələ 2-ci kursda ikən proqramlaşdırma və kibertəhlükəsizliyə ciddi maraq saldım və işə öz kompüterimə <b>Kali Linux</b> əməliyyat sistemini quraşdırmaqla, özüm başladım.", "This world was opened to me by the <b>Fundamentals of Programming</b> course in my first year. In 2023, in my second year, I got seriously into programming and cybersecurity and started on my own by installing <b>Kali Linux</b> on my computer.", "p")}
          {T("Düşünürəm ki, kibertəhlükəsizlik və süni intellekt uzun illər boyu ən güclü sahələr olaraq qalacaq və bu sahələrdə bacarıqlı mühəndislərə həmişə ehtiyac olacaq. Bu sahələrdəki işimdən əlavə, şirkətlərin, professorların və insanların işini əhəmiyyətli dərəcədə yüngülləşdirə biləcək maraqlı layihələr də yaradıram. Onların hamısı bu saytdadır.", "I believe cybersecurity and AI will stay among the strongest fields for many years, and skilled engineers will always be needed there. Alongside that work, I build projects that can make life noticeably easier for companies, professors and everyday people. All of them are on this site.", "p")}
          <div class="skills" aria-hidden="true"><div class="mq"><span>Python</span><span>JavaScript</span><span>HTML5 · CSS</span><span>Canvas</span><span>PyTorch</span><span>FastAPI</span><span>Game dev</span><span>C++</span><span>Assembly</span><span>Linux</span><span>Docker</span><span>Vercel</span><span>Python</span><span>JavaScript</span><span>HTML5 · CSS</span><span>Canvas</span><span>PyTorch</span><span>FastAPI</span><span>Game dev</span><span>C++</span><span>Assembly</span><span>Linux</span><span>Docker</span><span>Vercel</span></div></div>
        </div>
        <div class="idcard reveal tiltable">
          <div class="photo"><img src="img/ziya-azizov-ayfar-s.webp" srcset="img/ziya-azizov-ayfar-s.webp 360w, img/ziya-azizov-ayfar.webp 720w" sizes="(min-width: 900px) 440px, 92vw" width="720" height="720" alt="Ziya Əzizov (ayfar), Bakıdan veb developer və kibertəhlükəsizlik mühəndisi" loading="lazy" decoding="async"><span class="photo-badge"><i></i>Bakı · 2005</span></div>
          <h3>{T("Ziya Əzizov", "Ziya Azizov")}</h3>
          <div class="handle">@ayfar</div>
          <dl>
            <div><dt>{T("Nə edirəm", "What I make")}</dt>{T("Saytlar · Oyunlar · Alətlər · Tədqiqat", "Websites · Games · Tools · Research", "dd")}</div>
            <div><dt>{T("Təhsil", "Education")}</dt>{T("BHOS: Texniki sistemlərdə idarəetmə, magistratura (2026–)", "BHOS: M.S. Control of Technical Systems (2026–)", "dd")}{T("ADNSU: Mexatronika və Robototexnika, bakalavr (2022–2026)", "ASOIU: B.S. Mechatronics &amp; Robotics (2022–2026)", "dd")}</div>
            <div><dt>{T("Dillər", "Languages")}</dt>{T("Azərbaycan · İngilis (C1) · Türk", "Azerbaijani · English (C1) · Turkish", "dd")}</div>
            <div><dt>{T("Yer", "Location")}</dt>{T("Bakı, Azərbaycan · 2005", "Baku, Azerbaijan · born 2005", "dd")}</div>
            <div><dt>{T("Sahələr", "Fields")}</dt>{T("Proqramlaşdırma · Kibertəhlükəsizlik · Süni intellekt", "Programming · Cybersecurity · AI", "dd")}</div>
          </dl>
        </div>
      </div>
    </div>
  </section>

  <section id="faq">
    <div class="wrap">
      <div class="sec-head reveal"><div><div class="sec-num">{sec_no(4)} — {T("SUAL-CAVAB", "FAQ")}</div><h2>{T("Tez-tez soruşulanlar", "Questions")}</h2></div></div>
      <div class="faq">{faq_html()}
      </div>
    </div>
  </section>

  <section id="contact">
    <div class="wrap">
      <div class="contact reveal">
        <div class="sec-num">{sec_no(5)} — {T("ƏLAQƏ", "CONTACT")}</div>
        {T("Gəl, danışaq.", "Let's talk.", "h2")}
        {T("Özünüzə sayt sifariş etmək istəyirsinizsə, ya da sayt, oyun və ya layihə haqqında sualınız varsa, WhatsApp-a yazın və ya zəng edin.", "Want a website of your own, or have a question about a site, game or project? Message me on WhatsApp or call.", "p")}
        <div class="row">
          <a class="btn primary magnet" href="{WA_ORDER}" target="_blank" rel="noopener">{WA_SVG}<span>WhatsApp</span></a>
          <a class="btn magnet" href="tel:{PHONE}">📞 <span>{PHONE_SHOW}</span></a>
          <a class="btn magnet" href="mailto:{EMAIL}">✉ E-mail</a>
          <a class="btn magnet" href="https://www.linkedin.com/in/ziya-azizov-91bba638a" target="_blank" rel="noopener">LinkedIn <span class="arr">→</span></a>
          <a class="btn magnet" href="{INSTAGRAM}" target="_blank" rel="noopener">Instagram <span class="arr">→</span></a>
          <a class="btn magnet" href="{X_URL}" target="_blank" rel="noopener">X <span class="arr">→</span></a>
          <a class="btn magnet" href="https://github.com/ziko-asm" target="_blank" rel="noopener">GitHub <span class="arr">→</span></a>
        </div>
      </div>
    </div>
  </section>
</main>
"""
    page += footer()
    page += f'\n<script src="assets/site.js?v={V}"></script>\n<script src="assets/home.js?v={V}"></script>\n</body>\n</html>\n'
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(page)


def build_project(i, p):
    nxt = P[(i + 1) % len(P)]
    prv = P[(i - 1) % len(P)]
    name_az, name_en = p["name"]
    desc = p["summary"][0]
    page = head(f"{name_az} — ayfar", f"{name_en} — ayfar", desc, f"{CANON}/p/{p['slug']}.html", f"img/og/{p['slug']}.png", "../")
    page += f'<link rel="stylesheet" href="../assets/project.css?v={V}">\n</head>\n<body class="proj" style="--c1:{p["c1"]};--c2:{p["c2"]}">\n'
    page += chrome_bits("../")
    body_az = "".join(f"<p>{x}</p>" for x in p["body"][0])
    body_en = "".join(f"<p>{x}</p>" for x in p["body"][1])
    body_ru = "".join(f"<p>{R(x)}</p>" for x in p["body"][1])
    bul_az = "".join(f"<li>{x}</li>" for x in p["bullets"][0])
    bul_en = "".join(f"<li>{x}</li>" for x in p["bullets"][1])
    bul_ru = "".join(f"<li>{R(x)}</li>" for x in p["bullets"][1])
    note = f'{T(p["note"][0], p["note"][1], "div", "note")}' if p["note"] else ""
    gh = f'<a class="btn magnet" href="{p["github"]}" target="_blank" rel="noopener">GitHub <span class="arr">→</span></a>' if p["github"] else ""
    chips = "".join(L(c, "span", "chip") for c in p["chips"])
    st = T("canlı", "live") if p["status"] == "on" else T("müvəqqəti dayanıb", "offline for now")
    page += f"""
<main id="main">
  <section class="p-hero wrap">
    <a class="back" href="../#projects" data-nav>← {T("Bütün layihələr", "All projects")}</a>
    <div class="p-tags reveal-hero"><span class="tag {p['cat']}">{T(*p['tag'])}</span><span class="tag {p['status']}">{st}</span><span class="p-num">{i + 1:02d} / {len(P):02d}</span></div>
    <h1 class="reveal-hero d1">{T(name_az, name_en)}</h1>
    {T(p['summary'][0], p['summary'][1], 'p', 'p-lead reveal-hero d2')}
    <div class="p-cta reveal-hero d3">
      <a class="btn primary magnet" href="{p['url']}" target="_blank" rel="noopener">{T(*p['go'])} <span class="arr">↗</span></a>
      {gh}
    </div>
    <a class="p-media reveal-hero d4 tiltable" data-tilt="4" href="{p['url']}" target="_blank" rel="noopener" aria-label="{E(p['name'][0])}: {E(p['show'])}">{media_fixed(p, '../', badges=False, sizes="min(1170px, 100vw)")}</a>
  </section>

  <section class="wrap p-grid">
    <div class="p-text reveal">
      <div class="sec-num">{T("NƏ EDİR", "WHAT IT DOES")}</div>
      <div lang="az">{body_az}</div><div lang="en">{body_en}</div><div lang="ru">{body_ru}</div>
      {note}
    </div>
    <div class="p-side reveal">
      <div class="metric big"><div class="v">{L(p['metric'][0])}</div>{T(p['metric'][1], p['metric'][2], 'div', 'd')}</div>
      <div class="p-box">
        <div class="sec-num">{T("ƏSAS XÜSUSİYYƏTLƏR", "HIGHLIGHTS")}</div>
        <ul lang="az">{bul_az}</ul><ul lang="en">{bul_en}</ul><ul lang="ru">{bul_ru}</ul>
      </div>
      <div class="p-box">
        <div class="sec-num">{T("TEXNOLOGİYALAR", "BUILT WITH")}</div>
        <div class="chips">{chips}</div>
        <div class="p-url"><span>URL</span><a href="{p['url']}" target="_blank" rel="noopener">{E(p['show'])} ↗</a></div>
      </div>
    </div>
  </section>

  <section class="wrap p-next">
    <a class="prev" href="{prv['slug']}.html" data-nav><small>← {T("Əvvəlki", "Previous")}</small><b>{T(*prv['name'])}</b></a>
    <a class="next" href="{nxt['slug']}.html" data-nav style="--c1:{nxt['c1']};--c2:{nxt['c2']}"><small>{T("Növbəti layihə", "Next project")} →</small><b>{T(*nxt['name'])}</b></a>
  </section>
</main>
"""
    page += footer()
    page += f'\n<script src="../assets/site.js?v={V}"></script>\n</body>\n</html>\n'
    os.makedirs(os.path.join(ROOT, "p"), exist_ok=True)
    with open(os.path.join(ROOT, "p", f"{p['slug']}.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(page)


def build_404():
    page = head("Səhifə tapılmadı — ayfar", "Page not found — ayfar", "Bu səhifə mövcud deyil.", CANON + "/", "img/og/home.png", "/")
    page = page.replace('<link rel="canonical"', '<meta name="robots" content="noindex">\n<link rel="canonical"')
    page += '</head>\n<body>\n' + chrome_bits("/")
    page += f"""
<main id="main">
  <section class="nf wrap">
    <div class="nf-code" aria-hidden="true">404</div>
    {T("Bu stansiya hələ açılmayıb", "This station isn't open yet", "h1")}
    {T("Axtardığınız səhifə yoxdur və ya yeri dəyişib. Ana səhifəyə qayıdın və ya birbaşa yazın.", "The page you're looking for doesn't exist or has moved. Go back home or message me directly.", "p")}
    <div class="nf-go">
      <a class="btn primary magnet" href="/">{T("Ana səhifə", "Home")} <span class="arr">→</span></a>
      <a class="btn magnet" href="/#projects">{T("Layihələr", "Projects")} <span class="arr">→</span></a>
      <a class="btn magnet" href="{WA_ORDER}" target="_blank" rel="noopener">{WA_SVG}<span>WhatsApp</span></a>
    </div>
  </section>
</main>
"""
    page += footer()
    page += f'\n<script src="/assets/site.js?v={V}"></script>\n</body>\n</html>\n'
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(page)


def build_vercel_json():
    """Security headers for Vercel. The CSP allows the inline <script> in head() by its hash,
    so it is recomputed on every build and stays in sync if that script changes."""
    import base64
    import glob
    import hashlib
    import json
    import re
    hashes = set()
    for f in [os.path.join(ROOT, "index.html")] + glob.glob(os.path.join(ROOT, "p", "*.html")):
        with open(f, encoding="utf-8") as fh:
            for m in re.finditer(r"<script>(.*?)</script>", fh.read(), re.S):
                hashes.add("'sha256-" + base64.b64encode(hashlib.sha256(m.group(1).encode()).digest()).decode() + "'")
    csp = ("default-src 'self'; "
           f"script-src 'self' {' '.join(sorted(hashes))}; "
           "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
           "font-src 'self' https://fonts.gstatic.com; "
           "img-src 'self' data:; connect-src 'self' " + SCAN_SITE + "; "
           "frame-ancestors 'self'; base-uri 'self'; form-action 'self'; object-src 'none'; upgrade-insecure-requests")
    headers = [
        ("X-Frame-Options", "SAMEORIGIN"),
        ("X-Content-Type-Options", "nosniff"),
        ("Referrer-Policy", "strict-origin-when-cross-origin"),
        ("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=()"),
        ("Strict-Transport-Security", "max-age=63072000; includeSubDomains"),
        ("Content-Security-Policy", csp),
    ]
    cfg = {"headers": [{"source": "/(.*)", "headers": [{"key": k, "value": v} for k, v in headers]}]}
    with open(os.path.join(ROOT, "vercel.json"), "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(cfg, indent=2) + "\n")


if __name__ == "__main__":
    build_index()
    build_seo_files()
    for i, p in enumerate(P):
        build_project(i, p)
    build_404()
    build_vercel_json()
    if MISSING:
        import sys
        miss = sorted(set(MISSING))
        with open(os.path.join(ROOT, "ru_missing.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(miss))
        sys.exit(f"{len(miss)} strings have no Russian translation in ru.py (listed in ru_missing.txt)")
    print("built index.html and", len(P), "project pages")
