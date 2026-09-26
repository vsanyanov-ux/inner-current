const fs = require('fs');

let itContent = fs.readFileSync('book_outline_it.md', 'utf8');

// Task 1: AVVERTIMENTO AL LETTORE
const task1Text = `### AVVERTIMENTO AL LETTORE: QUESTO LIBRO NON È UN TAPPETO MAGICO
#### Perché costruiamo il razzo di Ciolkovskij e non vendiamo illusioni

> *«La Terra è la culla della ragione, ma non si può vivere per sempre in una culla.»*  
> — **Konstantin Ciolkovskij** (1911)

Se avete aperto questo libro sperando di trovare l'ennesimo "tappeto magico" del pensiero positivo, dolci meditazioni o la promessa di un'illuminazione istantanea — **chiudetelo immediatamente**.

Per 10.000 anni l'umanità ha inventato fiabe sui tappeti magici. Gli uomini hanno indossato le ali di cera di Icaro, hanno ideato le fantasie di Cyrano de Bergerac sulle fiale di rugiada mattutina, credendo di potersi salvare dalla sofferenza con il moralismo, la fede cieca o l'acquisto del prossimo attributo esterno di status. Ma il risultato è stato invariabile: *ogni volta il "tappeto magico" è precipitato, schiantandosi contro la spietata gravità della paura biologica, del senso di colpa e del surriscaldamento ohmico dell'ego*.

Nel 1903, nella remota provincia di Kaluga, il modesto insegnante di fisica semissordo Konstantin Ciolkovskij si sedette a un tavolo di legno e fece ciò che tutti i narratori del mondo non erano riusciti a fare. Non inventò fiabe — egli derivò **l'equazione del moto a reazione**:
$$\\Delta v = v_e \\ln \\frac{m_0}{m_f}$$
Egli calcolò la formula esatta per superare l'attrazione terrestre: ossigeno liquido, camera di combustione e un treno missilistico a più stadi che espelle i serbatoi vuoti. Mezzo secolo dopo, Gagarin volò sopra il pianeta.

**Questo libro è il progetto di Kaluga di Ciolkovskij per il vostro mondo interiore.**  
Non promettiamo miracoli. Noi affermiamo: la sofferenza, la colpa, l'ansia e la dipendenza non sono una maledizione mistica, ma **il pozzo gravitazionale dell'ego primordiale ($R_{\\text{ego}} > 0$)**. Per sfuggirvi, non vi servono mantra. Vi serve un reattore Tanden funzionante, lo scarico della zavorra morta secondo il canone Kanso e il calcolo della **Seconda velocità cosmica dello spirito**, che porta la coscienza nell'assenza di gravità della pura superconduttività ($R \\to 0$, Mushin).

Non avete davanti a voi letteratura di evasione. Avete davanti a voi il progetto ingegneristico del vostro volo orbitale.

`;
itContent = itContent.replace(
  "### A CHI È RIVOLTO QUESTO LIBRO (E A CHI NO)",
  task1Text + "### A CHI È RIVOLTO QUESTO LIBRO (E A CHI NO)"
);

// Task 2: TABELLA DI MARCIA DEL PENSIERO
const task2Text = `### TABELLA DI MARCIA DEL PENSIERO: 6 GRADINI DELL'ASCESA
#### Dalla cassetta di pronto soccorso ingegneristica al fusibile civilizzazionale della singolarità

Questo libro non è strutturato come una raccolta di consigli lineari, ma come un **veicolo di lancio del pensiero a più stadi**. Man mano che leggete, salirete a livelli di astrazione sempre più alti:

1. **Gradino I (Self-help applicato):** Cassetta di pronto soccorso ingegneristica. Il principio *Pain-First*, rimozione del burnout acuto, bilanciamento delle 6 lampade dello scudo vitale.
2. **Gradino II (Elettrodinamica):** Transizione alle scienze esatte. Le leggi di Ohm, Joule-Lenz ($Q = I^2 R t$) e Kirchhoff. Sostituzione del senso di colpa con un multimetro oggettivo.
3. **Gradino III (Motore Zen):** "L'Automobile della Coscienza" (140 anni da Karl Benz a Vladimir Anyanov). Biiezione matematica dei 23 canoni Zen e la somatica del Tanden nelle rumorose strade della metropoli.
4. **Gradino IV (Consilienza dei Sistemi):** Teoria universale del flusso diretto. Perché lo Zen, il Bitcoin di Satoshi Nakamoto, il Georgismo di Henry George e la Termodinamica di Carnot obbediscono a un unico invariante: l'eliminazione del parassita-intermediario ($R \\to 0$).
5. **Gradino V (La Grande Sintesi):** Ontologia "Bottom-Up". La felicità come *Summum Bonum* e la dissoluzione dei 7 eterni enigmi maledetti della filosofia (morte, amore, libero arbitrio, male, karma, solipsismo, senso della vita).
6. **Gradino VI (Lo Zenit della Singolarità):** Cosmonautica della Coscienza di Ciolkovskij, Seconda velocità cosmica dello spirito, eliminazione del divario antropologico di Wilson di 10.000 anni e risposta alla principale sfida civilizzazionale dell'era AGI (*Human Alignment* invece di *AI Alignment*).

`;
itContent = itContent.replace(
  "Se il tuo voltmetro è attivo e la tua mente anela a una fisica pura e a un'incrollabile chiarezza — benvenuto nell'Architettura della Felicità.\n\n---",
  "Se il tuo voltmetro è attivo e la tua mente anela a una fisica pura e a un'incrollabile chiarezza — benvenuto nell'Architettura della Felicità.\n\n" + task2Text + "\n---"
);

// Task 3: IL NUOVO ORGANO
const task3Text = `### Il Nuovo Organo della Psicologia: Da 130 anni di scolastica al criterio dei frutti pratici
#### Francis Bacon (1620) e la distruzione dei quattro idoli della meccanica dell'anima

> *«La vera misura della validità di una teoria è la sua capacità di generare frutti pratici... Ciò che nella teoria è la causa, nell'azione è la regola... La scienza e il potere umano coincidono, poiché l'ignoranza della causa ci priva dell'effetto.»*  
> — **Francis Bacon**, *«Novum Organum Scientiarum»*, 1620

Nel 1620, il grande pensatore inglese Francis Bacon pubblicò un trattato che capovolse il corso della civiltà europea: *«Novum Organum»*. Il titolo del libro era una sfida aperta all'«Organon» di Aristotele: Bacon proclamò che la scolastica medievale, che per secoli aveva dibattuto su sillogismi logici, categorie e definizioni teologiche, era sterile. Generava infinite biblioteche di trattati, ma non alleviava la fatica fisica del contadino, non costruiva navi sicure e non curava le malattie.

Bacon formulò una legge inderogabile: **la verità di una teoria è dimostrata esclusivamente dalla sua capacità di produrre frutti pratici (*experimenta fructifera*)**. Se una concezione speculativa è bella e logica, ma è impotente nel modificare la realtà fisica, allora è falsa. Questo criterio ha generato la fisica sperimentale moderna di Galilei e Newton, la chimica, la medicina basata sull'evidenza e la trazione a vapore della rivoluzione industriale.

Ma guardate alla psicologia e alle dottrine sullo spirito umano degli ultimi 130 anni, dall'avvento della psicoanalisi di Sigmund Freud.
La psicologia ha replicato fedelmente il tragico destino della scolastica medievale:
- Sono stati scritti milioni di tesi, articoli accademici e bestseller di self-help.
- Sono state create centinaia di scuole e modalità psicoterapeutiche in competizione tra loro.
- L'industria dell'assistenza psicologica è valutata in centinaia di miliardi di dollari l'anno.

**Ma dove sono i frutti pratici?**
Al 2026, il tasso di depressione clinica, disturbi d'ansia, attacchi di panico, burnout e solitudine esistenziale nel mondo ha battuto tutti i record storici. La civiltà ha dominato i calcoli quantistici e si è avvicinata all'AGI, ma l'uomo di fronte al disordine dell'anima è impotente quanto un pastore antico di fronte al temporale.

La causa di questa tragedia civilizzazionale è esattamente la stessa di 400 anni fa: **la psicologia è rimasta una scolastica priva di uno strumento di misurazione (senza un Organon)**. Si è smarrita nelle interpretazioni soggettive, adorando ciò che Bacon definì **i Quattro Idoli della Mente (Idola Mentis)**.

#### Decostruzione dei quattro idoli della meccanica dell'anima

L'Architettura della Felicità è **il Nuovo Organo della meccanica dell'anima**. Applica il criterio dei frutti di Bacon all'architettura della coscienza umana, demolendo sistematicamente tutti e quattro i fantasmi mentali secolari:

\`\`\`mermaid
flowchart TD
    subgraph Idols["I Quattro Idoli della scolastica (Bacon, 1620)"]
        I1["1. Idola Tribus<br>Proiezione delle proprietà della mente sulle cose"]
        I2["2. Idola Specus<br>Illusione del trauma unico"]
        I3["3. Idola Fori<br>Nebbia verbale ed etichette"]
        I4["4. Idola Theatri<br>Culto delle autorità e delle scuole"]
    end
    
    subgraph Circuit["Nuovo Organo: Elettrodinamica del circuito (2026)"]
        C1["⚡ Errore di attribuzione rimosso:<br>Le cose sono lampade fredde R_L, la luce nasce dal generatore"]
        C2["⚡ Invarianza della neurofisica:<br>Le leggi di Ohm e Kirchhoff sono identiche per 8 miliardi di persone"]
        C3["⚡ Metrica strumentale:<br>Sostituzione delle etichette con la fisica: U (volt), R (ohm), I (ampere), Q (joule)"]
        C4["⚡ Operatore sovrano Self-Hosted:<br>Eliminazione dei mediatori, protocollo di 30 secondi nel corpo"]
    end
    
    I1 ==>|Decostruzione| C1
    I2 ==>|Decostruzione| C2
    I3 ==>|Decostruzione| C3
    I4 ==>|Decostruzione| C4
\`\`\`

1. **Idoli della Tribù (Idola Tribus) — Errore di attribuzione e cecità da batteria:**  
   La mente umana tende a proiettare proprietà interne sugli oggetti esterni. Le persone hanno ingenuamente creduto che una nuova auto, una posizione di prestigio o un matrimonio contenessero in sé la sostanza della felicità. Pregavano la lampadina, non comprendendo che la lampadina è morta senza un circuito chiuso. La "Corrente Interiore" svela la fisica: la felicità non è un oggetto, ma un regime di superconduttività della corrente di attenzione ($I > 0, R_{\\text{ego}} \\to 0$).
2. **Idoli della Caverna (Idola Specus) — L'illusione del "trauma unico":**  
   Ogni persona è rinchiusa nella caverna della propria biografia. La terapia tradizionale indaga per anni la configurazione individuale di questa caverna: *«A che età tua madre non ti ha amato abbastanza?»*. Ma a livello delle leggi di conservazione questo non ha importanza. Se fate cadere un martello sul vostro piede, la legge di gravitazione universale di Newton non si interessa della vostra infanzia. Allo stesso modo, le leggi di Ohm ($I = U/R$) e di Joule-Lenz ($Q = I^2 R t$) sono universali: il filo dell'attenzione bloccato brucia la rete neurale in modo identico per tutti gli 8 miliardi di abitanti della Terra.
3. **Idoli della Piazza (Idola Fori) — La nebbia verbale e il mercato delle etichette:**  
   Le parole, nate per comodità quotidiana, hanno schiavizzato il pensiero. La psicologia si è ricoperta di migliaia di etichette astratte: "gestalt incompiuta", "procrastinazione", "burnout", "tossicità", "sindrome dell'impostore". L'individuo passa anni da specialisti, collezionando diagnosi anziché guarigione. La "Corrente Interiore" sostituisce il vocabolario scolastico con tre variabili fondamentali: **tensione della vita ($U$), conduttività dell'attenzione ($1/R$) e potenza utile del carico ($P = I^2 R_L$)**.
4. **Idoli del Teatro (Idola Theatri) — L'adorazione cieca di sacerdoti e scuole:**  
   Le scuole psicologiche ed esoteriche si sono costituite per secoli come sette chiuse e teatri dogmatici: psicoanalisi, junghismo, comportamentismo, gestalt. L'individuo viene collocato nella posizione dipendente di paziente, acquistando per anni indulgenze di pace mentale dai sacerdoti. La "Corrente Interiore" realizza la Grande Disintermediazione: all'uomo viene restituito il **quadro di comando sovrano e autonomo del proprio circuito**. Voi non siete pazienti. Voi siete ingegneri di bordo sovrani.

#### Il criterio dei frutti in 30 secondi

Secondo Bacon, la verità deve dare frutti non "dopo 5 anni di psicoterapia", ma qui e ora:
> *Se una teoria afferma di aver compreso la struttura della pace mentale, è obbligata a dimostrare un frutto ingegneristico nel vostro corpo fisico in 30 secondi.*

Proprio ora, leggendo queste righe, potete applicare questo Nuovo Organo nella pratica:
- **Passo 1:** Spostate l'attenzione dal rumore mentale errante al nucleo fisico del basso addome (*Tanden*).
- **Passo 2:** Rimuovete la resistenza parassita dell'Ego — abbandonate la disputa con la realtà, accettate il fatto che il momento presente sia esattamente così com'è ($R_{\\text{ego}} \\to 0$).
- **Passo 3:** Indirizzate la corrente di attenzione liberata nell'azione più vicina — leggere queste righe o la respirazione del corpo ($I > 0$).

Cosa è successo in questo secondo?  
Il bruciore ohmico alle tempie è scomparso. Lo spasmo muscolare nel petto si è sciolto. Nel corpo si è diffuso un calore tranquillo, costante, ad alta tensione.

Questo è il criterio dei frutti di Francis Bacon. Questa non è fede, né training autogeno, né ipnosi. Questa è la **rigorosa meccanica del circuito elettrico chiuso**.

`;
itContent = itContent.replace(
  "### Il relativismo umanistico: «La felicità è diversa per ciascuno»",
  task3Text + "### Il relativismo umanistico: «La felicità è diversa per ciascuno»"
);

// Task 4: ANATOMIA DELLA SEMPLICITÀ
const task4Text = `### ANATOMIA DELLA SEMPLICITÀ: PERCHÉ NESSUNO CI HA PENSATO PRIMA?
#### Il modello della torcia tascabile, la legge della valigia con le ruote e 4 ragioni della millenaria cecità dell'umanità

> *«Quanto bisognava essere idioti per non averci pensato prima?!»*  
> — **Thomas Huxley**, dopo aver letto «L'Origine delle Specie» di Charles Darwin (1859)

Se priviamo l'Architettura della felicità di tutta la sua patina accademica fatta di formule, preprint e grafici, si svela una verità che può essere spiegata in cinque minuti in cucina davanti a una tazza di tè.

L'essere umano non è strutturato in modo più complesso di una **comune torcia tascabile**. È composto da soli quattro elementi:
1. **La Batteria (Il tuo generatore):** la forza vitale nel basso addome (*Tanden*), il respiro, la fisiologia del corpo. Appartiene a ogni essere vivente ogni mattina per diritto di nascita ($\\mathcal{E} > 0$).
2. **Il Cavo:** la tua **attenzione**. Dove scorre l'attenzione, lì si dirige l'intera energia.
3. **La Lampadina (Il Carico):** l'attività che stai svolgendo proprio in questo istante a $t = \\text{now}$. Lavare i piatti, scrivere codice, bere il tè, passeggiare con tuo figlio. Quando il circuito si chiude sull'azione, la lampadina si accende e tu provi una felicità quieta e limpida.
4. **Il Fusibile (Zanshin):** la consapevolezza che la lampadina può bruciarsi o rompersi, ma **il tuo generatore rimarrà intatto**.

\`\`\`mermaid
flowchart LR
    Battery["1. BATTERIA (TANDEN)<br>Basso addome · Respiro · Forza vitale"] 
    -->|Cavo dell'attenzione| Bulb["3. LAMPADINA (AZIONE)<br>Carico proprio ora (Tè, codice, figlio)"]
    Bulb -->|Filo di ritorno della realtà| Battery
    
    Ego["💥 PARASSITA (EGO-DOGANIERE)<br>«E cosa penseranno di me?!»<br>Resistenza R > 0"]
    
    Battery -.->|Cavo bloccato| Ego
    Ego -.->|Inferno ohmico Q = I²Rt| Bulb
\`\`\`

#### Allora dov'è il guasto di cui soffre l'umanità?
In questo circuito elementare l'uomo ha inserito **un parassita: il proprio EGO** (*«E cosa penseranno di me?», «E se fallissi?», «Devono rispettarmi!»*).  
L'ego si posiziona sul cavo dell'attenzione come un avido doganiere, lo comprime con il piede e pretende: *«Prima devi nutrire me! Dimostra la mia importanza!»*.

La corrente proveniente dall'addome fluisce, ma incontra resistenza. E secondo la legge di Joule-Lenz ($Q = I^2 R t$), **quando la corrente incontra una resistenza, il filo diventa incandescente**.  
Questo filo arroventato è ciò che l'umanità da millenni chiama "stress", "burnout", "attacchi di panico" e "depressione". Vengono bruciati vivi dalla loro stessa energia bloccata!

#### Perché nessuno ci ha pensato prima?
1. **La scissione tra fisici e umanisti:** I maestri Zen conoscevano il Tanden 2500 anni fa, ma non avevano circuiti elettrici né voltmetri (parlavano per poesie d'acqua e di luna). I fisici del XIX secolo conoscevano la legge di Ohm, ma studiavano motori e cavi, ritenendo l'anima affare da preti. E gli psicologi erano letterati senza alcuna conoscenza delle leggi di conservazione. Nessuno ha mai unito questi mondi nello stesso fuoco.
2. **La trappola dell'Ego stesso ("L'occhio non può vedere se stesso"):** La mente che risolve il problema del dolore è essa stessa la fonte del dolore. L'ego non dirà mai: *«Spegni me per 30 secondi e il dolore svanirà»*. Ha tutto l'interesse a inventare terapie decennali, diagnosi complesse e sofferenze, pur di rimanere il protagonista del dramma.
3. **L'industria dei mediatori:** La semplicità e un interruttore gratuito di 30 secondi sono economicamente letali per le industrie trilionarie della farmaceutica, della psicoterapia a pagamento, dei culti e dell'iperconsumismo.
4. **La legge della "valigia con le ruote" (Canone Kanso):** La ruota ha 5000 anni, le valigie centinaia di anni, ma l'idea di applicare le ruote alla valigia è arrivata solo nel 1970. Steve Jobs ha eliminato 50 pulsanti e il pennino, lasciando un solo tasto sull'iPhone. L'Architettura della felicità ha rimosso 10.000 anni di rituali sacerdotali e moralismi, mettendo a nudo un semplice circuito a flusso diretto composto da 4 elementi.

`;
itContent = itContent.replace(
  "Iniziamo il nostro lavoro ingegneristico laddove la scheda è integra.\n\n---",
  "Iniziamo il nostro lavoro ingegneristico laddove la scheda è integra.\n\n" + task4Text + "\n---"
);

// MOC updates
itContent = itContent.replace(
  "| ✅ | **Parte III: Cap. 3.3** | Circuitistica delle relazioni: Sincronizzazione di due circuiti senza cortocircuito ed eliminazione di $R_{\\text{future}}$ | 100% | [[02_Wiki/Inner Current (Case Study - Engineer Romance Approach)\\|Case Study - Romance Approach]], [[02_Wiki/Inner Current (Happiness Relativity vs Circuit Invariance)\\|Happiness Relativity]] |",
  "| ✅ | **Parte III: Cap. 3.3** | L'Automobile della Coscienza | 100% | |\n| ✅ | **Parte III: Cap. 3.4** | Elettrodinamica dell'Amore | 100% | |\n| ✅ | **Parte III: Cap. 3.5** | Circuitistica delle relazioni: Sincronizzazione di due circuiti senza cortocircuito ed eliminazione di $R_{\\text{future}}$ | 100% | [[02_Wiki/Inner Current (Case Study - Engineer Romance Approach)\\|Case Study - Romance Approach]], [[02_Wiki/Inner Current (Happiness Relativity vs Circuit Invariance)\\|Happiness Relativity]] |"
);
itContent = itContent.replace(
  "| ✅ | **Parte III: Cap. 3.4** | Il protocollo «Black Start» (Avvio da zero)",
  "| ✅ | **Parte III: Cap. 3.6** | Il protocollo «Black Start» (Avvio da zero)"
);
itContent = itContent.replace(
  "| ✅ | **Parte III: Cap. 3.5** | Circuitistica dei collettivi",
  "| ✅ | **Parte III: Cap. 3.7** | Circuitistica dei collettivi"
);
itContent = itContent.replace(
  "| ✅ | **Parte III: Cap. 3.6** | Elettrodinamica del capitale",
  "| ✅ | **Parte III: Cap. 3.8** | Elettrodinamica del capitale"
);
itContent = itContent.replace(
  "| ✅ | **Parte IV: Cap. 4.1**",
  "| ✅ | **Parte III: Cap. 3.9** | Summerhill e la Pedagogia della Superconduttività | 100% | |\n| ✅ | **Parte IV: Cap. 4.1**"
);
itContent = itContent.replace(
  "| ✅ | **Conclusione** | Il ponte verso il mondo esterno",
  "| ✅ | **Conclusione** | Il ponte verso il mondo esterno: Adattamento di impedenza e Magnetismo Esterno | 100% | [[02_Wiki/Inner Current (Impression Architecture and Impedance Matching)\\|Impression Architecture]] |\n| ✅ | **Epilogo** | La Verticale dell'Ascesa | 100% | |"
);

// Rename chapters 3.3-3.6 in text
itContent = itContent.replace("### Capitolo 3.3 — Circuitistica delle relazioni", "### Capitolo 3.5 — Circuitistica delle relazioni");
itContent = itContent.replace("### Capitolo 3.4 — Il protocollo «Black Start»", "### Capitolo 3.6 — Il protocollo «Black Start»");
itContent = itContent.replace("### Capitolo 3.5 — Circuitistica dei collettivi", "### Capitolo 3.7 — Circuitistica dei collettivi");
itContent = itContent.replace("### Capitolo 3.6 — Elettrodinamica del capitale", "### Capitolo 3.8 — Elettrodinamica del capitale");

fs.writeFileSync('book_outline_it.md', itContent);
