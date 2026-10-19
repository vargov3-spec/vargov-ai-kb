# Der generative 3D-Konfigurator von Vargov®Design

Rubrik: Fertigung · Datum: 31. August 2026 · Slug: konfigurator

Der generative 3D-Konfigurator baut eine Hängekomposition aus den Elementen der Marke, zeigt sie räumlich und liefert die Spezifikation, nach der sie gefertigt wird.

Normalerweise läuft die Auswahl von Autorenlicht so: Der Architekt findet im Katalog eine passende Komposition, schreibt eine E-Mail, beschreibt Größe und Dichte in Worten — und wartet. Einen Tag später kommt eine Visualisierung. Irgendetwas stimmt nicht: zu viele Elemente, die Silhouette passt nicht. Noch eine E-Mail, noch ein Tag.

Der Konfigurator erspart diesen Schriftwechsel. Die Komposition entsteht direkt im Browser, in wenigen Minuten, und ist sofort räumlich zu sehen.

Was er kann

Sie geben eine Katalogposition und die Maße der Wolke in Millimetern vor — die Engine zieht die realen Baugrößen des Elements, seine Leistung und seine 3D-Form heran. Dann folgt die Form der Komposition selbst: Würfel, Kugel, Halbkugel, Kegel, Zylinder, Pyramide, Kaskade, Ring, Welle, Spirale, Tropfen, Linse, Trichter, Rahmen, Bogen, Schlangenlinie, Helix, Etagen, Schale, Keil oder Bioform — einundzwanzig Varianten.

Dichte: luftig, mittel, dicht — oder eine exakte Anzahl von Elementen. Anordnung vertikal, horizontal, gemischt; Drehung zufällig, aus der Mitte oder im regelmäßigen Raster; Neigung um jede Achse von −90° bis +90°. In einer Komposition lassen sich zwei Artikel in gewähltem Verhältnis mischen.

Die Farbe der Elemente kommt aus dem RAL-Katalog — 210 Farben mit Suche nach Code und Namen; in einer Komposition lassen sich bis zu acht Farben des Katalogs mischen, jede mit eigener Transparenz (Bänder haben eine einzige Glasfarbe). Daneben stehen die hauseigenen Farben, die Galvanik (transparente Töne und Spiegelbeschichtungen) und „Klar und farblos“; Transparenz wird nur dort angeboten, wo das Element auch in Wirklichkeit transparent sein kann. Bei Kompositionen mit Metallbeschlägen wird das Metall über einen Code aus dem JN-Oberflächenkatalog festgelegt — 24 Muster, acht Farben in drei Ausführungen. Eine Pipette gibt es im Konfigurator bewusst nicht: In der Spezifikation steht ein RAL-Code, die Bezeichnung der galvanischen Oberfläche oder ein JN-Code — etwas, das die Fertigung tatsächlich reproduzieren kann.

Eine Verteilung, die nicht lügt

Entscheidend bei der generativen Anordnung ist nicht das schöne Bild, sondern physikalische Ehrlichkeit. Weder Elemente noch Seile überschneiden sich. Das Kabel jedes Elements wird gegen den echten Befestigungspunkt geprüft — bei einigen Formen die Fassung, bei anderen die Bohrung im Glas — und gegen die reale Silhouette der Nachbarn, vom Modell selbst abgenommen. Die Regel wird vor jedem Release automatisch geprüft.

Eine Konfiguration ergibt immer dieselbe Verteilung: Wer Ihren Link öffnet, sieht genau dasselbe. Die Schaltfläche zum Neuberechnen bietet eine andere Variante gleicher Dichte.

Für Bänder gibt es eine eigene Engine: Zehn Artikel entstehen nicht als Wolke aus Elementen, sondern als durchgehendes Band mit Glasröhren auf einem Gerüst — eigene Plastizität, eigene Länge und ein Farbverlauf über die Strecke.

Die Zahlen, die der Monteur braucht

Der Konfigurator zeigt die Anzahl der Elemente, die tatsächlichen Maße der Wolke, den tiefsten Punkt unter der Decke, die Aufteilung nach Baugrößen, die Gesamtleistung — und das Gewicht der Komposition, automatisch aus ihrem Aufbau berechnet.

Das Gewicht ist keine Nebenangabe. Von ihm hängt ab, welcher Anker die Aufhängung trägt und ob die Decke verstärkt werden muss. Früher wurde diese Zahl per E-Mail ermittelt, wenn der Aufbau bereits feststand; jetzt steht sie von Anfang an neben der Silhouette.

Was Sie mitnehmen können

IFC4 für BIM: Längen in Millimetern, jeder Befestigungspunkt ein eigenes Objekt mit der Anzahl der daran hängenden Elemente und, wenn die Masse bekannt ist, der rechnerischen Last. Das Modell wird unter eine Decke in der Höhe gesetzt, die im Feld „Deckenhöhe, mm“ neben der IFC-Schaltfläche eingetragen ist (standardmäßig 2700 mm): Befestigungspunkte an der Decke, Koordinatenursprung auf dem Boden. Eine PDF-Spezifikation mit Aufbau, Masse, Leistung, Montage, Fertigungszeit und Garantie sowie QR-Code zur Konfiguration selbst. Ein Ausschreibungsblatt für Einkauf und Zoll. Die DXF-Zeichnung für AutoCAD ist nur für den internen Gebrauch bestimmt: Fertigung und Händler der Marke. Fertige 3D-Modelle des Artikels (max, fbx) auf 3ddd.ru und 3dsky.org; ein Modell der zusammengesetzten Komposition auf Anfrage. Gespeicherte Projekte liegen im Browser selbst, ohne Konto, und der Link trägt den vollständigen Zustand der Konfiguration.

Die Komposition lässt sich mit dem Smartphone im eigenen Raum ausprobieren: USDZ auf iOS, GLB auf Android. Die Oberfläche läuft in acht Sprachen, Arabisch von rechts nach links inbegriffen.

Worin er sich von einem üblichen Konfigurator unterscheidet

In der Szene stehen echte Erzeugnisse. Die Formen sind von Produktionsmodellen abgenommen — mit der echten Stärke der Teile, den Fassungen und den Punkten, an denen in der Fertigung das Seil befestigt wird. Keine Icons, keine Platzhalterkugeln.

Die Komposition wird erzeugt, nicht ausgewählt. Die Engine verteilt die Elemente im Volumen der gewählten Form und achtet auf Silhouette und Abstände; über die Nummer der Variante entsteht dieselbe Komposition Bit für Bit.

Die Regeln der Marke sind fest eingebaut und werden automatisch geprüft. Das Seil kreuzt kein Glas — Strahlprüfung gegen die Dreiecke des Meshes; Körper berühren einander nicht; die Kegelschräge läuft gerade von der oberen Ebene zur Spitze. Vor jedem Release laufen diese Wächter.

Die Masse wird aus der Geometrie berechnet: Hüllen nach Wandstärke, Flachteile nach eigener Geometrie, Gussteile nach Volumen — und mit den Werkslieferungen abgeglichen.

Wie viel es ist

Im Konfigurator liegen Hunderte von Licht- und dekorativen Kompositionen. Diejenigen, die sich mit vollständiger Berechnung öffnen, exportieren sofort ein IFC4-Modell, eine PDF-Spezifikation und ein Ausschreibungsblatt. Die Verteilungsdichte ist an realen Aufträgen kalibriert. Jeder Artikel im Konfigurator hat eine eigene Seite auf Russisch und Englisch; die genauen aktuellen Zahlen stehen auf der Konfigurator-Seite der Website, wo sie aus seinen Daten berechnet werden.

Ein Urteil von außen

Der 3D-Konfigurator wurde bei Awwwards angenommen und bewertet — auf der internationalen Plattform, die die besten Websites der Welt nach Design, Usability, Inhalt und Kreativität auswählt. Status: Nominee 2026. Für ein Werkzeug, das eine Nischenaufgabe für ein Nischenpublikum erfüllt, bestätigt das: Auch ein Außenstehender kommt damit zurecht.

Wo Sie ihn öffnen

Außerhalb Russlands — vargov.design. In Russland — configurator.vargov.ru.

Die fertige Komposition lässt sich direkt aus dem Konfigurator an den Konstrukteur der Marke schicken. Klicken Sie auf „Angebot anfordern“ und wählen Sie Telegram, WhatsApp oder E-Mail: Der Anfragetext wird automatisch eingefügt — Sie müssen nur noch auf „Senden“ klicken. Die Antwort kommt auf demselben Weg zurück.

Vargov®Design — für alle, die den Unterschied sehen.

Made in Vargov.
