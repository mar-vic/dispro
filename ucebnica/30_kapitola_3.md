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
Konverzia súborov .docx do štruktúrovaných formátov, ako je TEI XML alebo HTML,
si zvyčajne vyžaduje buď množstvo manuálnej práce alebo použitie nástrojov,
akým je program Pandoc, prípadne vlastné skripty - ani tie však nie sú
efektívne, ak nemá pôvodný súbor konzistentnú štruktúru.

XML (eXtensible Markup Language) je jazyk navrhnutý na reprezentáciu informácií
v štruktúrovanom, pre človeka a stroj čitateľnom formáte. Pri jeho návrhu sa
kládol dôraz najmä na jednoduchosť, všeobecnosť a použiteľnosť v prostredí
internetu[@extensible2025] a vyznačuje sa silnou podporou takmer všektých
ľudských jazykov vďaka kompatibilite s Unicode štandardom.^[Ide o univerzálne
kódovanie znakov určené na podporu celosvetovej výmeny, spracovania a
zobrazovania písaných textov rôznych jazykov a technických disciplín moderného
sveta.[@unicode2025]] Hoci mal jazyk XML pôvodne slúžiť najmä na reprezentáciu
dokumentov, v súčasnosti sa extenzívne používa na reprezentáciu ľubovoľných
dátových štruktúr,[@fennell_extremes_2013] napríklad tých, ktoré sa vyskytujú vo webových
službách.[@whatisxml2025]

Pre digitálnych humanistov je XML viac ako len technický nástroj - je to metóda na vyjadrenie významu,
štruktúry a vzťahov v texte konzistentným a transparentným spôsobom.

Na rozdiel od textových procesorov, ktoré sa zameriavajú na vzhľad textu, XML sa zameriava na to, ako je text
usporiadaný a interpretovaný. Umožňuje vedcom označiť text pomocou vlastných,
popisných značiek, ktoré odrážajú vnútornú štruktúru textu. Tieto značky sú
uzavreté v hranatých zátvorkách a sú v pároch - napríklad:

Unlike word processors that focus on how text looks, XML focuses on how text is
organized and interpreted. It allows scholars to mark up a text using custom,
descriptive tags that reflect the text’s internal structure. These tags are
enclosed in angle brackets and come in pairs—for example:

    <title>The Cross and the Sword</title>

This line tells both the human reader and the computer that “The Cross and the
Sword” is the title of a work. Tags can represent a wide range of elements, such
as:

    <author>Ľudmila Podjavorinská</author>
    <date when="1910">1910</date>
    <placeName>Martin</placeName>
    <quote>“Freedom must live in the heart before it lives on paper.”</quote>

Each of these elements conveys semantic meaning—not just formatting. You can
also nest elements to reflect more complex relationships, like a paragraph that
contains a name and a date:

    <p>In <date when="1923">1923</date>, 
    <name>Jozef Cíger Hronský</name> 
    published his second novel.</p>

Every well-formed XML document consists of the following basic parts:

- **Elements**: Named sections of content wrapped in opening and closing tags (<title>...</title>).
- **Attributes**: Extra information about an element, written inside the opening tag (<date when="1923">1923</date>).
- **Hierarchy**: XML is structured like a tree, with elements nested inside others to show relationships and structure.

A minimal XML document might look like this:

    <?xml version="1.0" encoding="UTF-8"?>
    <novel>
    <title>Jarné vody</title>
    <author>Božena Slančíková-Timrava</author>
    <date when="1914">1914</date>
    <text>
    <p>Keď sa vrátil z vojny, všetko sa zdalo byť rovnaké, a predsa iné.</p>
    </text>
    </novel>

In digital humanities, XML—especially when guided by frameworks like the Text
Encoding Initiative (TEI)—enables researchers to encode literary texts with a
level of detail and care that reflects the richness of the material itself. This
structured markup makes texts not only easier to preserve, but also searchable,
analyzable, and convertible into other formats such as HTML, PDF, or plain text
for visualization or presentation.

By learning XML, students of the humanities gain the ability to bridge
traditional textual scholarship with digital tools—making their research more
sustainable, collaborative, and computationally powerful. 

#### Introducing TEI: A Shared Language for Encoding Texts

Once students understand the basics of XML, the next step in many digital humanities projects—especially those involving historical or literary texts—is learning how to apply those principles consistently and meaningfully. This is where the Text Encoding Initiative (TEI) comes in.

TEI is an international standard for encoding texts in XML, developed by and for scholars in the humanities. Its guidelines provide a shared vocabulary and structure for representing everything from prose and poetry to letters, plays, critical editions, and historical documents. Rather than inventing their own XML tags for each project, researchers can rely on TEI’s rich and well-documented set of elements, which ensures interoperability, clarity, and long-term preservation.

For example, a simple TEI-encoded excerpt from a novel might look like this:

<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title>Dom v stráni</title>
        <author>Martin Kukučín</author>
      </titleStmt>
      <publicationStmt>
        <publisher>Slovenská akadémia vied</publisher>
        <date when="1904">1904</date>
      </publicationStmt>
      <sourceDesc>
        <bibl>Original print edition from 1904</bibl>
      </sourceDesc>
    </fileDesc>
  </teiHeader>
  <text>
    <body>
      <p>Bol to dom, akých bolo v dedine málo – biely, s oblôčikmi plnými kvetov.</p>
    </body>
  </text>
</TEI>

In this snippet, we see several key features of TEI in action:

    The <teiHeader> provides essential metadata about the document: its title, author, source, publication date, and more.

    The <text> element holds the actual content, typically structured into <body>, <div> (for chapters), and <p> (for paragraphs).

    TEI supports a wide range of additional elements, such as <name>, <placeName>, <persName>, <quote>, and <note>, allowing scholars to capture intricate textual and contextual information.

TEI is designed to be flexible and extensible. Projects can select only the elements they need, or even define custom rules using ODD (One Document Does it all) specifications, which describe how a given TEI customization should behave. This adaptability makes TEI useful for everything from minimalist digital editions to deeply annotated scholarly corpora.

For students and researchers in the digital humanities, TEI is more than just a markup standard—it’s a framework for thinking critically about the structure and meaning of texts. Encoding with TEI encourages close reading, editorial reflection, and a heightened awareness of textual variation, paratexts, and publication history. At the same time, it prepares those texts for computational analysis, digital presentation, and long-term preservation.

##### Getting Started with TEI Encoding: Tools and Tips

Starting a TEI-based project doesn’t require an advanced technical background—just curiosity, patience, and some basic tools. Here are a few ways students can begin:

- Start small. Pick a short text (e.g., a chapter, a short story, or a single letter) and try encoding just the title, author, paragraphs, and chapter divisions.
- Use a TEI-aware XML editor. Tools like oXygen XML Editor (paid, but with academic licenses), Sublime Text with plugins, or the free TEI Publisher’s web-based editor offer validation, autocomplete, and syntax highlighting.
- Follow the Guidelines. The TEI Guidelines are searchable and rich with examples. They’re your best companion for understanding what each element means and how to use it.
- Validate your files. Always check your TEI files for well-formedness and against your project’s schema—either within an editor like oXygen or using online tools like Roma (TEI’s schema builder).
- Join the community. The TEI community is friendly and active. Mailing lists, GitHub repositories, and workshops provide opportunities to ask questions, share schemas, and learn from others.

Whether you’re preparing a digital edition, building a corpus, or experimenting with literary analysis, customizing TEI to your needs is a valuable scholarly exercise. It asks you to consider what matters in a text—not just to you, but to future readers and machines—and how to model that meaning clearly and sustainably.

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
