# Digitálna zbierka slovenskej prózy (prípadová štúdia) {#sec:dispro labe="Digitálna zbierka slovenskej prózy"}

V tejto kapitole opisujeme vývoj digitálneho korpusu slovenskej prózy vydanej
pred rokom 1950, pričom osobitnú pozornosť v nej venujeme prieniku literárnej
vedy a prostriedkov výpočtových technológií. Cieľom projektu, bolo zostaviť
reprezentatívnu a na výskum pripravenú zbierku beletristickej prózy, ktorá by
odrážala formálny, tematický a jazykový vývoj slovenskej literatúry od
polovice 19. storočia do začiatku povojnového obdobia. Korpus, ktorý čerpal z
rôznych archívnych zdrojov - vrátane Slovenskej národnej knižnice, univerzitných
repozitárov, jazykovedného inštitútu SAV a historických vydavateľských
záznamov - pozostáva z desiatok XML súborov zodpovedajúcich schéme TEI [^1]
podporujúcej prístupy blízkeho aj vzdialeného čítania. Tento štruktúrovaný súbor
údajov umožňuje celý rad vedeckých výskumov, od štylistickej analýzy a
klasfikácie žánrov až po sieťové modelovanie autorských a publikačných kotextov.
Namiesto vytvárania uzavretého kánonu projekt poskytuje otvorenú platformu na
skúmanie literárnej histórie prostredníctvom počítačových nástrojov, pričom
zostáva zakotvený v interpretačných tradíciách humanitných vied.

[^1]: Text Encoding Initiative

## Opis výskumného projektu

## Použité technológie

### Linux

Dôležitou, ale často opomínanou zložkou pracovného postupu tvorby korpusu, bolo
použitie operačného systému Linux ako technologického základu projektu.
Linux poskytoval stabilné prostredie s otvoreným zdrojovým kódom, ktoré sa ideálne hodilo na požiadavky
rozsiahleho spracovania textu, kontroly verzií a automatizácie. Jeho
kompatibilita so základnými nástrojmi - ako sú knižnice na spracovanie TEI, XML
a skriptovacími jazykmi, ako sú Python a Bash - nám umožnil výskumnému tímu
vytvoriť vlastné postupy na čistenie údajov, kódovanie a správu korpusu.
Okrem toho modulárna konštrukcia systému Linux umožnila jemnú kontrolu nad systémom
správania, od oprávnení súborov až po plánovanie úloh, čo sa ukázalo ako nevyhnutné, keď
pri práci so súbormi údajov archívneho rozsahu. V tejto časti sa uvádza, ako systém Linux podporoval
technickú infraštruktúru projektu, pričom sa zdôrazňuje jeho úloha pri zabezpečovaní
transparentnosti, reprodukovateľnosti a dlhodobej udržiavateľnosti - hodnôt, ktoré zdieľa
digitálnych humanitných vied a komunitách open-source.

### Programovacie jazyky

Medzi základné technológie použité v projekte budovania korpusu patria
programovacie jazyky Python a Lua, ktoré zohrávali odlišné, ale vzájomne sa
dopĺňajúce úlohy. Python slúžil ako primárny jazyk na manipuláciu s údajmi,
spracovanie textu, a integráciu s knižnicami na spracovanie TEI-XML, parsovanie
regulárnych výrazov, a transformáciu metadát. Jeho čitateľnosť, všestrannosť a
rozsiahly ekosystém sa hodil na vytváranie robustných skriptov na automatizáciu
úloh, ako sú čistenie OCR, overovanie štrukturálnych značiek a štatistické
analýzy. Jazyk Lua sme používali predovšetkým na vývoj vlastných filtrov a
zapisovačov pre Pandoc, čo umožnilo jemnú kontrolu nad konverziou dokumentov
najmä na generovanie konzistentných výstupov z textov zakódovaných v TEI do
formátov ako HTML, Markdown alebo LaTeX. Táto skriptovacia vrstva umožnila tímu
prispôsobiť transformáciu zložitých štruktúr XML do použiteľných formátov na
vedeckú prezentáciu aj výpočtovú analýzu. Táto časť skúma, ako Python a Lua
prispeli k modulárnemu, reprodukovateľnému projektu. pracovných postupov, čím sa
posilňuje hodnota ľahkého, účelovo vytvoreného skriptovania v digitálnej
humanitnej infraštruktúry.

Among the core technologies employed in the corpus-building project, the
programming languages Python and Lua played distinct yet complementary roles.
Python served as the primary language for data manipulation, text processing,
and integration with libraries for TEI-XML handling, regular expression parsing,
and metadata transformation. Its readability, versatility, and extensive
ecosystem made it well-suited for building robust scripts to automate tasks such
as OCR cleanup, structural markup verification, and corpus-wide statistical
analysis. Lua, on the other hand, was primarily used to develop custom filters
and writers for Pandoc, enabling fine-grained control over document conversion
pipelines—particularly for generating consistent outputs from TEI-encoded texts
to formats such as HTML, Markdown, or LaTeX. This scripting layer allowed the
team to tailor the transformation of complex XML structures into usable formats
for both scholarly presentation and computational analysis. This section
explores how Python and Lua contributed to the project’s modular, reproducible
workflow, reinforcing the value of lightweight, purpose-built scripting in
digital humanities infrastructure.

In digital humanities projects, programming is less about building complex
software and more about designing flexible tools to help explore, transform, and
interpret data. Two languages especially useful in this context are Python and
Lua—each with its own strengths and roles within a DH workflow.

Python is one of the most widely used languages in the digital humanities due to
its readability, extensive libraries, and active community. It’s especially
well-suited for tasks such as cleaning text data, analyzing word frequencies,
converting file formats, or querying metadata. For example, using libraries like
lxml or BeautifulSoup, students can extract information from XML or HTML
documents, while tools like pandas allow for powerful data manipulation and
statistical summaries with just a few lines of code. Python is ideal for
building repeatable, modular scripts that can be shared and reused across
projects.

Lua, by contrast, is a lightweight scripting language often embedded within
other tools. In DH contexts, it shines when used for customizing workflows
inside software like Pandoc—a universal document converter that plays a key role
in many text transformation pipelines. With Lua, students can write compact
filters that modify how documents are converted, such as reformatting chapter
titles, removing footnotes, or extracting specific TEI elements before exporting
to HTML or PDF. Lua’s simplicity makes it easy to learn for specific, focused
tasks, especially when working within structured publishing systems.

Together, Python and Lua offer a powerful toolkit: Python for data processing
and analysis, Lua for document transformation and customization. Mastery of even
basic scripts in these languages can significantly extend what’s possible in
digital humanities research, bridging the gap between traditional scholarship
and computational methods.

### XML

V digitálnych humanitných vedách nie je výber formátu na reprezentáciu
textových údajov neutrálnym rozhodnutím - určuje, čo môžeme s textom robiť, ako
ho interpretujeme a ako ho zdieľame s ostatnými. Medzi voľby, ktorá sú zrejme
najbližšie bežnému užívateľovi, patria formáty textových procesorov, ako
napríklad .docx programu Microsoft Word alebo .odt súbory používané v
OpenOffice. Takéto programy ponúkajú vizuálne orientované prostredie, v ktorom môžu
používatelia rýchlo písať, upravovať a formátovať texty bez potreby technických
znalostí. Funkcie ako tučné písmo, kurzíva, poznámky pod čiarou a nadpisy sú
vďaka intuitívnemu užívateľskému rozhraniu ľahko použiteľné a spoluprácu s
ďalšími ľuďmi zjednodušujú zabudované komentovanie a systémy sledovania zmien.
Pri bežnom narábaní s textom v digitálnom prostredí sú vďaka takejto
jednoduchosti používania procesory jasnou voľbou.

Táto voľba však so sebou nesie určité obmedzenia, pre ktoré nie sú textové
procesory, resp. súborové formáty, ktorými tieto programy reprezentujú texty,
vhodné pre ciele, ktoré sledujeme v digitálnych humanitných vedách. Tieto
obmedzenia nie sú len technickými prekážkami, ale ovplyvňujú samotný spôsob
interpretácie, zdieľania a uchovávania textov vo vedeckej práci, ktorá čoraz
viac závisí od štruktúrovaných, pre stroje čitateľných údajov.

Jedným z najzásadnejších problémov je, že textové procesory sú navrhnuté s
ohľadom na vizuálnu prezentáciu textov, nie na ich sémantickú zrozumiteľnosť.
Funkcie formátovania textu, ktoré tieto programy poskytujú, sú zamerané na to,
ako text vyzerá pre čitateľa: tučné písmo pre zvýraznenie, kurzíva pre nadpisy,
zalomenie riadkov pre odseky. Toto vizuálne štylizovanie však v sebe nenesie
žiadne informácie o význame alebo funkcii danej časti textu. Tučným písmom
zvýraznený výraz v programe Word môže označovať rečníka v divadelnej hre,
postavu v románe alebo nadpis v odbornom článku, čo stroj, bez ďalšej
informácie, nemôže vedieť. Táto absencia sémantického značenia veľmi sťažuje
extrakciu, analýzu alebo opätovné spracovanie textu pomocou výpočtovej techniky.
Aj keď je vizuálne formátovanie konzistentné, základná štruktúra súboru je
zvyčajne neprehľadná - uložená ako zazipovaná zbierka binárnych súborov, ktoré je ťažké
analyzovať bez špecializovaných nástrojov.

Okrem toho sú súbory textových procesorov často nekonzistentné a
idiosynkratické. Používatelia používajú rôzne formátovanie v závislosti od
osobných zvykov, inštitucionálnych šablón alebo predvolených nastavení softvéru.
Jedna vedkyňa môže používať kurzívu pre názvy kníh, iný môže používať úvodzovky.
Niektorí môžu ručne vkladať zalomenia riadkov, aby vytvorili dojem medzier, iní
sa spoliehajú na štýly. Tieto nezrovnalosti sa v spoločných alebo rozsiahlych
projektoch rýchlo hromadia, takže automatizované spracovanie alebo analýza sú
bez rozsiahleho čistenia a štandardizácie nespoľahlivé.

Ďalšou nevýhodou je netransparentnosť verziovania súborov textového procesora.
Word síce ponúka funkcie ako „sledovanie zmien“, tie však nie sú štandardizované
ani prenosné medzi rôznymi platformami a nedajú sa ľahko extrahovať alebo
analyzovať v priebehu času.

Z hľadiska uchovávania sú formáty textových procesorov tiež príliš krehké. Keďže sa
spoliehajú na proprietárne alebo poloproprietárne formáty, sú náchylné na
zastarávanie softvéru alebo zmeny v predvolenom správaní v jeho rôznych verziách.
Súbor .docx vytvorený v programe Word 2007 sa nemusí správať rovnako v novších
verziách alebo v open-source editoroch, čo môže viesť k strate údajov, posunu
formátovania alebo k neželaným zmenám v rozložení textu.

Napokon, pre projekty digitálnych humanitných vied, ktorých cieľom je publikovať
alebo prezentovať texty na webe, prepojiť ich s metadátami alebo zabezpečiť ich
plnotextovú vyhľadateľnosť a analýzu, sú súbory textového procesora jednoducho nevyhovujúce.
Konverzia súborov .docx do štruktúrovaných formátov
si zvyčajne vyžaduje buď množstvo manuálnej práce alebo použitie nástrojov,
akým je program Pandoc, prípadne vlastné skripty - ani tie nám však nepomôžu, ak
nemá pôvodný súbor konzistentnú štruktúru.

Hoci teda formáty textových procesorov dominujú pri bežnom písaní a akademickom
publikovaní, ich obmedzenia sa prejavia vo vzťahu k požiadavkám digitálnej
humanitnej práce - konkrétne s potrebou modelovať, analyzovať a uchovávať texty
bohatým a štruktúrovaným spôsobom. Práve tu ponúka XML (eXtensible Markup
Language) presvedčivú a robustnú alternatívu. Je to jazyk navrhnutý na
reprezentáciu informácií v štruktúrovanom, pre človeka a stroj čitateľnom
formáte. Pri jeho návrhu sa kládol dôraz najmä na jednoduchosť, všeobecnosť a
použiteľnosť v prostredí internetu[@extensible2025] a vyznačuje sa silnou
podporou takmer všektých ľudských jazykov vďaka kompatibilite s Unicode
štandardom.^[Ide o univerzálne kódovanie znakov určené na podporu celosvetovej
výmeny, spracovania a zobrazovania písaných textov rôznych jazykov a technických
disciplín moderného sveta.[@unicode2025]] Hoci mal jazyk XML pôvodne slúžiť
najmä na reprezentáciu dokumentov, v súčasnosti sa extenzívne používa na
reprezentáciu ľubovoľných dátových štruktúr,[@fennell_extremes_2013] napríklad
tých, ktoré sa vyskytujú vo webových službách.[@whatisxml2025]

## Sémantická jasnosť a explicitná štruktúra

Jednou z najvýznamnejších výhod jazyka XML je schopnosť sémantického
značkovania. Na rozdiel od súborov textových procesorov, ktoré používajú
formátovanie predovšetkým na označenie vizuálnych prvkov, XML vyžaduje
explicitné definovanie, čo jednotlivé časti textu vlastne predstavujú. Ak
chceme, napríklda, v nejakom texte zaznamenať, že určitý reťazec znakov
predstavuje meno autora, prostriedkami XML to dosiahneme tak, že danú pasáž
uzavrieme v značke <autor>, ktorá má vopred definovaný význam.^[V tomto kontexte
by mohlo ísť o význam "tvorca textu, ktorého je označený reťazec časťou"] Týmto sa
stane rola daného reťazca v dokumente explicitná a jednoznačná.

Táto jasnosť sa zreteľnejšie ukáže pri komplexnejších príkladoch. Historický
dokument môže obsahovať vrstvené úrovne citácií, redakčných poznámok, odkazov,
marginálií a autorských poznámok - každý z týchto prvkov možno presne reprezentovať
označením pomocou prostriedkov XML. Vďaka tomu tak výskumníci môžu systematicky
vyhľadávať prípady konkrétneho hovorcu, sledovať pomenované entity, identifikovať
tematické vzory alebo rozlišovať medzi pôvodným textom a redakčnými zásahmi.

XML tak slúži ako nástroj pre formalizované vyjadrenie vedeckej interpretácie.
Zviditeľňuje štrukturálne a interpretačné rozhodnutia, ktoré humanisti často
nechávajú v tradičnom písaní implicitné. To sa obzvlášť dobre zhoduje s cieľmi
tvorby kritických edícií, vied o texte a archívnej práce, kde je prvoradá
vernosť materiálnemu a intelektuálnemu kontextu.

## Interoperabilita a opakovaná použiteľnosť

Ďalšou kľúčovou výhodou XML je jeho interoperabilita. Keďže je nezávislý od
výpočtovej platformy a riadi sa otvorenými štandardmi, súbory tohto formátu
možno používať v širokom spektre softvérových prostredí, od databáz a webových
aplikácií až po transformačné systémy a nástroje na vizualizáciu údajov.

Súbor vo formáte XML možno napríklad transformovať do HTML formátu určeného na
publikovanie na webe, PDF formátu vhodného pre tlač, formátu ePub používaného v
elektronických čítačkách alebo
dokonca do formátu JSON na integráciu do webových rozhraní. Tieto transformácie sa zvyčajne
realizujú pomocou XSLT ^[XSLT (Extensible Stylesheet Language Transformations)
je jazyk pôvodne navrhnutý na transformáciu dokumentov XML do iných XML
dokumentov alebo iných formátov, ako je HTML, obyčajný text alebo formátovacie
objekty XSL. Tieto formáty možno následne konvertovať do formátov, ako sú PDF,
PostScript a PNG. Podpora transformácie JSON a obyčajného textu bola pridaná v
neskorších aktualizáciách špecifikácie XSLT 1.0.[@xslt2025]] alebo iných transformačných
"potrubí", čo umožňuje, aby jeden zdrojový súbor slúžil na viacero účelov bez
vynakladania duplicitnej práce. Toto je obzvlášť cenné pre dlhodobé vedecké
projekty, ktoré sa môžu časom vyvíjať alebo meniť platformy.

Okrem toho, keďže sa XML sa riadi konzistentnými pravidlami a súbory v tomto
formáte môžeme validovať voči vopred definovaným schémam, je ľahké udržiavať
texty dobre sformované a vnútorne konzistentné. Toto zabezpečuje opakovateľnú
použiteľnosť a zdieľateľnosť korpusov pozostávajúcich z XML súborov - nielen
pôvodnými autormi, ale aj inými výskumníkmi a inštitúciami.

## Strojová čitateľnosť a výpočtová analýza

Vďaka hierarchickej a na pravidlách založenej štruktúre XML, súbory v tomto
formáte posyktujú ideálny substrát pre dištančné čítanie, stylometriu, sieťovú
analýzu, modelovanie tém a ďalšie formy metód používané v digitálnych
humanitných vedách. Vhodne anotované texty nám napríklad umožňujú ľahko
zodpovedať otázky ako koľko ženských postáv hovorí v slovenských románoch z 19.
storočia, ako často sa objavujú odkazy na určité miesta alebo ako sa mení
štruktúra dialógov v čase. Na tieto typy otázok je takmer nemožné spoľahlivo
odpovedať pri použití formátov textového procesora, ktoré nemajú vnútornú
štruktúru potrebnú na to, aby boli vhodnými vstupmi pre automatizované
spracovanie.

Okrem toho možno dokumenty XML spracúvať pomocou širokej škály programovacích
jazykov a knižníc určených na dolovanie textu a vizualizáciu údajov. Kombinácia
s metadátami a externými súbormi údajov umožňuje textom zakódovaným v XML
formáte stať sa predmetmi interdisciplinárneho výskumu, spájajúceho literatúru s
históriou, geografiou a ďalšími oblasťami.

## Transparentnosť a uchovávanie

Keďže XML je čisto textový formát ^[Máme tu na mysli to, čo sa v anglickom jazyku
    označuje ako "plain text", teda dáta, ktoré obsahujú len reprezentácie
    znakov čitateľného materiálu bez ich grafickej reprezentácie alebo ďalších
objektov (čísiel, s pohyblivovu desatinnou čiarkou, obrázkov, atď.) Niekedy sa
    síce XML považuje za tzv. bohatý text ("rich text"), keďže okrem
    reprezentácií znakov čitateľného materiálu obsahuje aj informácie o
    štruktúre dokumentu, prípadne o 
    čitateľného materiálu obsahuje obsahuje aj   ],
vyznačuje sa transparentnosťou a trvácnosťou. Na rozdiel od proprietárnych
formátov textových procesorov možno súbory v tomto formáte otvoriť a čítať v
akomkoľvek textovom editore, v akomkoľvek operačnom systéme, bez špeciálneho
softvéru. 

Vďaka Zmeny v súboroch XML sa dajú presne sledovať pomocou systémov na kontrolu
verzií, ako je napríklad Git, čo je obzvlášť užitočné v kolaboratívnom vedeckom
prostredí. Každá úprava, doplnenie alebo oprava sa stáva súčasťou
kontrolovateľnej histórie, čo umožňuje budúcim výskumníkom pochopiť vývoj
digitálneho objektu.

Okrem toho, keďže XML oddeľuje obsah od prezentácie, podporuje čistejšie
pracovné postupy a znižuje riziko poškodenia údajov v dôsledku problémov s
formátovaním. Prezentácia - či už pre web, tlač alebo mobilné zariadenia - sa dá
spracovať nezávisle prostredníctvom súborov štýlov a šablón, pričom základné
údaje zostanú nedotknuté.

## Komunita a štandardy

XML v digitálnych humanitných vedách ťaží zo silných komunít, najmä okolo TEI
(Text Encoding Initiative), ktorá poskytuje dobre vyvinutý a vyvíjajúci sa
štandard pre textovú vedu. TEI ponúka nielen rozsiahly slovník značiek pre
širokú škálu textových funkcií - poskytuje aj dokumentáciu, príklady, nástroje a
komunitu vedcov, editorov a vývojárov, ktorí aktívne podporujú jeho prijatie.

Prijatím XML a TEI sa výskumníci zapájajú do ekosystému, ktorý si cení
transparentnosť, udržateľnosť a vedeckú prísnosť. Toto zosúladenie so spoločnými
štandardmi zvyšuje hodnotu a viditeľnosť vlastnej práce, čo uľahčuje jej
zdieľanie, uchovávanie a budovanie.

### Webové technológie

Transforming a structured digital corpus into an accessible, user-friendly web
resource requires more than just solid encoding—it demands thoughtful design and
the right technical stack. In this project, a combination of standard web
technologies—HTML, JavaScript, and CSS—was used to build a responsive, readable
interface for interacting with the corpus. HTML served as the backbone for
content display, CSS ensured typographic and structural clarity, and JavaScript
enabled interactive features such as search, filtering, and basic
visualizations. To bridge the gap between TEI-encoded data and the web
presentation layer, the project made extensive use of TEI Publisher, an
open-source framework designed specifically for publishing TEI documents online.
TEI Publisher provided out-of-the-box support for rendering TEI-XML, managing
search indexes, and offering faceted browsing, while also allowing for deep
customization through XSLT, CSS, and optional integration with JavaScript
frameworks like Vue.js. This section explores how TEI Publisher, combined with
modern web technologies, enabled the creation of a platform that is both
technically robust and accessible to a broad range of users, from researchers to
general readers.

## Digitization: From Printed Page to Machine-Readable Text

The foundation of the corpus-building process began with the digitization of
physical novels, many of which existed only in aging print editions or archival
microfilm. This phase involved careful selection of source materials based on
availability, historical significance, and condition, followed by
high-resolution scanning and optical character recognition (OCR). While OCR
technologies offer substantial time savings, the process also revealed the
limitations of automated text capture when applied to older Slovak
orthographies, non-standard typography, or damaged pages. As a result, post-OCR
correction—both automated and manual—became a key component of the digitization
workflow. This section outlines the practical and methodological considerations
that shaped the transition from analog texts to machine-readable data, including
the tools, standards, and quality control measures employed to ensure that the
digital texts would be suitable for subsequent encoding and analysis.

## Encoding: Structuring the Text with TEI

Once the novels were digitized and cleaned, the next step involved enriching the
plain text with semantic and structural markup using the Text Encoding
Initiative (TEI) guidelines. This phase was central to transforming the corpus
into a scholarly resource that could support both humanistic inquiry and
computational analysis. TEI encoding allowed for detailed representation of
textual features such as chapter divisions, narrative perspective shifts, named
entities, quotations, and paratextual elements (e.g., prefaces, footnotes). It
also facilitated the inclusion of bibliographic metadata, authorial information,
and historical publication context. Balancing descriptive accuracy with encoding
efficiency required the development of project-specific schemas and tagging
conventions, as well as the use of both automated tagging scripts and manual
interventions. This section delves into the rationale behind the encoding
strategy, the challenges of modeling 19th- and early 20th-century Slovak prose,
and the tools and workflows adopted to ensure consistency and interpretive
flexibility.

## Presentation: Publishing with TEI Publisher

With the corpus fully encoded, the final phase focused on making the material
available through a web-based interface that preserved the richness of the TEI
markup while offering a smooth, intuitive user experience. For this, TEI
Publisher served as the central platform, chosen for its native support of
TEI-XML and its flexibility in presenting complex textual structures. The
platform enabled not only the display of texts but also faceted browsing,
full-text search, and customizable views tailored to different user
groups—whether scholars, educators, or general readers. TEI Publisher’s reliance
on standards-based technologies like XSLT and REST APIs also allowed for future
integration with visualization tools or external datasets. This section
discusses the implementation of TEI Publisher in the context of the corpus,
detailing how its configuration and extensions were used to bridge the gap
between encoded data and accessible digital editions.
