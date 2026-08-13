#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║          ECHOES OF THE HOLLOW — Terminal Horror RPG          ║
║                   Built by AR-AI / Onyx v67                  ║
╚══════════════════════════════════════════════════════════════╝

Du erwachst in einem verlassenen Sanatorium. Kein Licht. Kein
Ausweg. Nur die Stimme aus den Wänden — und das Ding, das dich
schon lange beobachtet.

Steuerbefehle:
  Richtungen: nord, süd, ost, west, oben, unten
  Aktionen:   nehmen, ablegen, benutzen, untersuchen
  Inventar:   inventar / i
  Status:     status / s
  Karte:      karte / k
  Hilfe:      hilfe / h
  Beenden:    beenden / exit
"""

import os
import sys
import time
import random
import textwrap
import json
from typing import Optional

# ──────────────────────────────────────────────────────────────
# TERMINAL-FARBEN
# ──────────────────────────────────────────────────────────────

class Farbe:
    ROT       = "\033[91m"
    DUNKELROT = "\033[31m"
    GRÜN      = "\033[92m"
    GELB      = "\033[93m"
    BLAU      = "\033[94m"
    LILA      = "\033[95m"
    CYAN      = "\033[96m"
    GRAU      = "\033[90m"
    WEISS     = "\033[97m"
    BOLD      = "\033[1m"
    DIM       = "\033[2m"
    BLINK     = "\033[5m"
    RESET     = "\033[0m"

    @staticmethod
    def rot(text: str) -> str:
        return f"{Farbe.ROT}{text}{Farbe.RESET}"

    @staticmethod
    def dunkelrot(text: str) -> str:
        return f"{Farbe.DUNKELROT}{text}{Farbe.RESET}"

    @staticmethod
    def grün(text: str) -> str:
        return f"{Farbe.GRÜN}{text}{Farbe.RESET}"

    @staticmethod
    def gelb(text: str) -> str:
        return f"{Farbe.GELB}{text}{Farbe.RESET}"

    @staticmethod
    def blau(text: str) -> str:
        return f"{Farbe.BLAU}{text}{Farbe.RESET}"

    @staticmethod
    def lila(text: str) -> str:
        return f"{Farbe.LILA}{text}{Farbe.RESET}"

    @staticmethod
    def cyan(text: str) -> str:
        return f"{Farbe.CYAN}{text}{Farbe.RESET}"

    @staticmethod
    def grau(text: str) -> str:
        return f"{Farbe.GRAU}{text}{Farbe.RESET}"

    @staticmethod
    def bold(text: str) -> str:
        return f"{Farbe.BOLD}{text}{Farbe.RESET}"

    @staticmethod
    def blink(text: str) -> str:
        return f"{Farbe.BLINK}{text}{Farbe.RESET}"

# ──────────────────────────────────────────────────────────────
# HILFSFUNKTIONEN
# ──────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def drucke_langsam(text: str, delay: float = 0.03, newline: bool = True):
    """Zeichen für Zeichen ausgeben — Horror-Atmosphäre."""
    for zeichen in text:
        print(zeichen, end="", flush=True)
        time.sleep(delay)
    if newline:
        print()

def drucke_text(text: str, breite: int = 72):
    """Text mit Zeilenumbruch und Einrückung ausgeben."""
    zeilen = textwrap.wrap(text, breite)
    for zeile in zeilen:
        print(f"  {zeile}")

def drucke_leerzeile():
    print()

def drucke_trennlinie(zeichen: str = "─", länge: int = 72, farbe=None):
    linie = zeichen * länge
    if farbe:
        print(farbe(linie))
    else:
        print(Farbe.grau(linie))

def drucke_horror(text: str, delay: float = 0.05):
    """Roter, langsamer Text für Horror-Momente."""
    print(Farbe.ROT, end="")
    drucke_langsam(text, delay)
    print(Farbe.RESET, end="")

def warte(sekunden: float = 1.5):
    time.sleep(sekunden)

def zufälliger_geräusch() -> str:
    geräusche = [
        "Irgendwo tropft Wasser.",
        "Ein fernes Kratzen an den Wänden.",
        "Du hörst ein leises Stöhnen.",
        "Das Flackern einer unsichtbaren Lichtquelle.",
        "Schritte — aber du bist allein.",
        "Ein langes, ziehendes Atmen.",
        "Das Knacken alten Holzes.",
        "Stille. Zu viel Stille.",
        "Etwas bewegt sich im Schatten.",
        "Eine Fliege summt. Mitten in der Nacht.",
    ]
    return random.choice(geräusche)

def horror_effekt():
    """Zufälliger Horror-Atmosphären-Effekt."""
    if random.random() < 0.25:
        drucke_leerzeile()
        print(Farbe.grau(f"  [{zufälliger_geräusch()}]"))
        drucke_leerzeile()

# ──────────────────────────────────────────────────────────────
# GEGENSTÄNDE
# ──────────────────────────────────────────────────────────────

class Gegenstand:
    def __init__(self, name: str, alias: list[str], beschreibung: str,
                 gewicht: int = 1, verwendbar: bool = False,
                 verwendungs_text: str = "", schlüssel_für: str = ""):
        self.name = name
        self.alias = alias
        self.beschreibung = beschreibung
        self.gewicht = gewicht
        self.verwendbar = verwendbar
        self.verwendungs_text = verwendungs_text
        self.schlüssel_für = schlüssel_für
        self.verbraucht = False

    def __str__(self):
        return self.name

    def passt_zu(self, eingabe: str) -> bool:
        eingabe = eingabe.lower().strip()
        if eingabe == self.name.lower():
            return True
        return any(a in eingabe for a in self.alias)


def erstelle_gegenstände() -> dict[str, Gegenstand]:
    return {
        "taschenlampe": Gegenstand(
            name="Taschenlampe",
            alias=["lampe", "licht", "torch"],
            beschreibung="Eine alte Taschenlampe. Die Batterien flackern, aber sie leuchtet noch.",
            gewicht=1,
            verwendbar=True,
            verwendungs_text="Du schaltest die Taschenlampe an. Der Strahl zittert — "
                             "und fällt auf etwas, das du lieber nicht gesehen hättest.",
        ),
        "tagebuch": Gegenstand(
            name="Tagebuch",
            alias=["buch", "heft", "diary"],
            beschreibung="Ein zerfledderte Tagebuch mit blutbeflecktem Einband. "
                         "Die letzte Eintragung: 'Es hört nie auf zu flüstern.'",
            gewicht=1,
            verwendbar=True,
            verwendungs_text=(
                "Du schlägst das Tagebuch auf:\n\n"
                "  '15. März — Sie haben uns hierher gesperrt. Doktor Voss sagt,\n"
                "  die Behandlung wirkt. Ich glaube ihm nicht mehr.\n\n"
                "  22. März — Zimmer 13 ist jetzt versiegelt. Jemand hat die\n"
                "  Wände vollgeschrieben. Worte, die keinen Sinn ergeben.\n"
                "  Oder doch?\n\n"
                "  30. März — Es kommt nachts. Es flüstert meinen Namen.\n"
                "  Ich habe meinen Namen vergessen.'"
            ),
        ),
        "schlüssel_a": Gegenstand(
            name="Rostiger Schlüssel",
            alias=["schlüssel", "rost", "key", "schluessel"],
            beschreibung="Ein verrosteter Schlüssel. Eingraviert: 'Flügel B — KEIN ZUTRITT'.",
            gewicht=1,
            schlüssel_für="flügel_b",
        ),
        "schlüssel_b": Gegenstand(
            name="Silberner Schlüssel",
            alias=["silber", "silbern", "weißer schlüssel"],
            beschreibung="Ein silberner Schlüssel, eiskalt trotz der Umgebungswärme.",
            gewicht=1,
            schlüssel_für="keller",
        ),
        "messer": Gegenstand(
            name="Skalpell",
            alias=["klinge", "messer", "skalpell", "waffe"],
            beschreibung="Ein chirurgisches Skalpell. Noch scharf. Noch benutzt.",
            gewicht=1,
            verwendbar=True,
            verwendungs_text="Du hältst das Skalpell fest. Es gibt dir eine gewisse Sicherheit — "
                             "aber auch das Gefühl, dass du vielleicht bald weißt, wofür du es brauchst.",
        ),
        "medizin": Gegenstand(
            name="Beruhigungsmittel",
            alias=["pille", "tablette", "medikament", "medizin"],
            beschreibung="Eine Flasche mit weißen Pillen. Beschriftung: 'Dosis: 1. Nie mehr.'",
            gewicht=1,
            verwendbar=True,
            verwendungs_text="Du schluckst eine Pille. Die Panik tritt etwas zurück — "
                             "aber die Schatten tanzen jetzt in Mustern.",
        ),
        "foto": Gegenstand(
            name="Verblasstes Foto",
            alias=["bild", "photo", "foto", "photographie"],
            beschreibung="Ein altes Schwarzweißfoto. Eine Familie vor dem Sanatorium. "
                         "Das Kind in der Mitte hat keine Augen — oder sie wurden herausgebrannt.",
            gewicht=1,
            verwendbar=True,
            verwendungs_text="Du betrachtest das Foto genauer. Auf der Rückseite steht in kindlicher "
                             "Schrift: 'Papa hört es auch schon.' Darunter eine Zahl: 1947.",
        ),
        "notiz": Gegenstand(
            name="Zerknüllte Notiz",
            alias=["zettel", "papier", "note", "nachricht"],
            beschreibung="Eine zerknüllte Notiz. Die Tinte ist verschmiert.",
            gewicht=1,
            verwendbar=True,
            verwendungs_text=(
                "Du glättest die Notiz:\n\n"
                "  'LAUF NICHT — ES HÖRT DAS LAUFEN\n"
                "   SCHREI NICHT — ES LIEBT DAS SCHREIEN\n"
                "   ATME KAUM — ES HASST DAS ATMEN\n\n"
                "   Der Keller. Die Tür. Das Wort an der Wand.\n"
                "   Du weißt schon, welches.'"
            ),
        ),
        "kerze": Gegenstand(
            name="Kerze",
            alias=["licht", "kerze", "wachs"],
            beschreibung="Eine halbverbrannte Kerze mit getrockneten Blutspuren am Docht.",
            gewicht=1,
            verwendbar=True,
            verwendungs_text="Du zündest die Kerze an. Das Flackern wirft riesige Schatten an die Wände — "
                             "Schatten, die sich manchmal gegen das Licht bewegen.",
        ),
        "amulett": Gegenstand(
            name="Schwarzes Amulett",
            alias=["amulett", "kette", "anhänger", "medaillon"],
            beschreibung="Ein schwarzes Amulett in Form eines verzerrten Auges. "
                         "Es ist warm — als würde jemand es halten.",
            gewicht=1,
            verwendbar=True,
            verwendungs_text="Du hältst das Amulett fest. Ein Flüstern durchfährt deine Finger — "
                             "du verstehst kein Wort, aber du weißt, was es meint.",
        ),
        "seite": Gegenstand(
            name="Herausgerissene Seite",
            alias=["seite", "blatt", "text", "ritual"],
            beschreibung="Eine herausgerissene Buchseite, bedeckt mit einem rituellen Diagramm "
                         "und Anweisungen in einer Sprache, die du fast verstehst.",
            gewicht=1,
            verwendbar=True,
            verwendungs_text=(
                "Du liest die Seite:\n\n"
                "  'Das Wesen trägt keinen Namen — aber es kennt deinen.\n"
                "   Um es zu binden, müssen drei Dinge verbrannt werden:\n"
                "   Ein Bild der Vergangenheit.\n"
                "   Ein Werkzeug der Schuld.\n"
                "   Das Blut des Wissenden.\n\n"
                "   Das Zentrum ist der Keller. Die Zeit ist immer jetzt.'"
            ),
        ),
        "kurbel": Gegenstand(
            name="Eisenkurbel",
            alias=["kurbel", "hebel", "eisen", "stab"],
            beschreibung="Eine schwere Eisenkurbel. Wahrscheinlich für einen alten Generator.",
            gewicht=2,
            verwendbar=False,
        ),
        "verbandsmaterial": Gegenstand(
            name="Verbandszeug",
            alias=["verband", "binde", "pflaster", "verbandsmaterial"],
            beschreibung="Altes, aber noch steriles Verbandszeug aus einem Erste-Hilfe-Kasten.",
            gewicht=1,
            verwendbar=True,
            verwendungs_text="Du verbindest deine Wunden. Der Schmerz lässt nach — "
                             "aber etwas sagt dir, du wirst es noch brauchen.",
        ),
    }

# ──────────────────────────────────────────────────────────────
# RÄUME
# ──────────────────────────────────────────────────────────────

class Raum:
    def __init__(self, name: str, beschreibung: str, kurz: str,
                 ausgänge: dict[str, str],
                 gegenstände: list[str] = None,
                 dunkel: bool = False,
                 gesperrt: bool = False,
                 schlüssel: str = "",
                 horror_texte: list[str] = None,
                 ereignis: str = ""):
        self.name = name
        self.beschreibung = beschreibung
        self.kurz = kurz
        self.ausgänge = ausgänge
        self.gegenstände: list[str] = gegenstände or []
        self.dunkel = dunkel
        self.gesperrt = gesperrt
        self.schlüssel = schlüssel
        self.horror_texte = horror_texte or []
        self.ereignis = ereignis
        self.besucht = False
        self.horror_gezeigt = False

    def horror_text(self) -> Optional[str]:
        if self.horror_texte and not self.horror_gezeigt:
            text = random.choice(self.horror_texte)
            self.horror_gezeigt = True
            return text
        return None


def erstelle_räume() -> dict[str, Raum]:
    return {
        "erwachen": Raum(
            name="Verrotteter Korridor",
            beschreibung=(
                "Du erwachst auf einem kalten Steinboden. Die Luft riecht nach Schimmel, "
                "feuchter Erde und etwas Süßlichem, das du nicht benennen willst. "
                "Rissige Fliesen unter deinen Händen. Verblasste Wandfarbe, die sich in "
                "Streifen ablöst wie Haut. An der Wand gegenüber — Kratzer. Hunderte davon. "
                "Als hätte jemand die Tage gezählt und irgendwann aufgehört zu zählen. "
                "Der Korridor erstreckt sich nach Norden und Süden in die Dunkelheit."
            ),
            kurz="Ein verrotteter Korridor. Kratzer an der Wand.",
            ausgänge={"nord": "eingang", "süd": "wartezimmer"},
            gegenstände=["taschenlampe", "notiz"],
            horror_texte=[
                "Die Kratzer an der Wand — sie sind frisch.",
                "Du zählst die Striche. Einer fehlt. Dann zwei. Dann keiner mehr.",
            ],
            ereignis="erstes_erwachen",
        ),
        "eingang": Raum(
            name="Eingangshalle",
            beschreibung=(
                "Eine hohe, einst prächtige Eingangshalle. Der Kronleuchter hängt schief — "
                "die Glühbirnen längst zerborsten, Glassplitter auf dem Marmorboden. "
                "Eine Rezeptionstheke aus dunklem Holz, dahinter ein umgeworfener Stuhl. "
                "Auf dem Tresen liegt ein aufgeschlagenes Buch — die Einträge hören "
                "abrupt auf. Datum des letzten Eintrags: 3. April 1987. "
                "Türen führen nach Osten, Süden und Westen. Eine breite Treppe steigt "
                "nach oben, in die Dunkelheit."
            ),
            kurz="Die große Eingangshalle. Kronleuchter. Stille.",
            ausgänge={"süd": "erwachen", "ost": "büro", "west": "flügel_a_eingang", "oben": "oberer_korridor"},
            gegenstände=["foto"],
            horror_texte=[
                "Das Buch auf dem Tresen — du hast es nicht umgeblättert. Aber die Seite hat sich gedreht.",
                "Im Spiegel hinter der Theke siehst du dich. Aber dein Spiegelbild ist schon gegangen.",
            ],
        ),
        "büro": Raum(
            name="Büro des Direktors",
            beschreibung=(
                "Das Büro eines Mannes, der zu viel wusste. Aktenberge auf dem Boden, "
                "die meisten angesengt. Ein massiver Schreibtisch mit aufgebrochener Schublade. "
                "An der Wand: ein Porträt von Doktor Emil Voss — die Augen herausgeschnitten. "
                "Auf dem Schreibtisch ein Telefon, der Hörer abgenommen, der Kabelstecker lose. "
                "Hinter dem Schreibtisch eine Wand voller Krankenakten — einige blutig beschmiert. "
                "Im Regal: ein leerer Tresor, offen, und ein Glas mit einer eingetrockneten "
                "Flüssigkeit, deren Farbe du nicht einordnen kannst."
            ),
            kurz="Direktors Büro. Zerbrochene Akten. Leerer Tresor.",
            ausgänge={"west": "eingang"},
            gegenstände=["tagebuch", "schlüssel_a"],
            horror_texte=[
                "Das Telefon — du hörst etwas in der Leitung. Atmen.",
                "Die Krankenakte mit deinem Namen liegt offen. Du hast keine Erinnerung daran.",
            ],
        ),
        "wartezimmer": Raum(
            name="Wartezimmer",
            beschreibung=(
                "Stühle in Reihen, manche umgeworfen, manche noch akkurat ausgerichtet — "
                "als würden unsichtbare Patienten noch warten. Vergilbte Magazine, deren "
                "Cover zeigen Gesichter mit herausgetilgten Augen. Eine Uhr an der Wand, "
                "deren Zeiger fehlen. An der Wand gegenüber: ein Kindermalbild an einem "
                "Pinnwand — ein schwarzes Haus, ein schwarzer Baum, eine kleine Figur "
                "ohne Gesicht. Ausgänge: Nord, Ost."
            ),
            kurz="Das Wartezimmer. Leere Stühle. Uhne Zeiger.",
            ausgänge={"nord": "erwachen", "ost": "behandlungszimmer"},
            gegenstände=["kerze"],
            horror_texte=[
                "Der Stuhl in der Ecke — du hörst ihn knarren. Als würde jemand aufstehen.",
                "Das Kindermalbild. Das kleine Gesicht. Es war da.",
            ],
        ),
        "behandlungszimmer": Raum(
            name="Behandlungszimmer 3",
            beschreibung=(
                "Steriles Weiß, das jetzt grau ist. Eine Behandlungsliege mit Lederriemen — "
                "die Schnallen poliert, die Riemen zerrissen. Ein Tablett mit chirurgischen "
                "Instrumenten, akkurat ausgelegt, als würde der Arzt gleich eintreten. "
                "Ein EKG-Gerät, dessen Bildschirm schwach flimmert — und eine gerade Linie zeigt. "
                "An der Decke: Brandspuren in Form einer Hand. "
                "Aus dem Lüftungsschacht: ein ganz leises, rhythmisches Pochen."
            ),
            kurz="Behandlungszimmer. Riemen. Flatlines.",
            ausgänge={"west": "wartezimmer", "nord": "labor"},
            gegenstände=["messer", "verbandsmaterial"],
            horror_texte=[
                "Das EKG piept einmal. Nur einmal.",
                "Die Riemen an der Liege — sie waren von innen zerrissen.",
            ],
        ),
        "labor": Raum(
            name="Forschungslabor",
            beschreibung=(
                "Regale voller zerbrochener Flaschen — etwas Dunkles hat sich in den "
                "Ritzen des Bodens festgesetzt. Zentrifugen, Mikroskope, Bunsenbrennersockel. "
                "In einem Glas: eine Flüssigkeit, die pulsiert. Du bist sicher, dass sie das tut. "
                "An einer Kreidetafel: Formeln, die immer wieder in ein Wort münden — "
                "HOLLOWBORN. Darunter: eine Liste von Namen. Dein Name ist der letzte."
            ),
            kurz="Das Labor. Formeln. Dein Name an der Tafel.",
            ausgänge={"süd": "behandlungszimmer", "west": "flügel_a_eingang"},
            gegenstände=["medizin", "seite"],
            horror_texte=[
                "Die Flüssigkeit im Glas. Sie hat sich bewegt. In Richtung deiner Hand.",
                "HOLLOWBORN. Du buchstabierst es rückwärts. Es ergibt genauso viel Sinn.",
            ],
        ),
        "flügel_a_eingang": Raum(
            name="Flügel A — Korridor",
            beschreibung=(
                "Ein langer, schmaler Korridor. Neonröhren, von denen eine noch zuckt — "
                "in einem Rhythmus, der an Morse-Code erinnert. Türen links und rechts, "
                "alle verriegelt. Außer einer. Zimmer 7 — die Tür steht einen Spalt offen. "
                "Aus dem Spalt: Stille. Aber eine Stille, die atmet. "
                "Am Ende des Korridors: eine schwere Metalltür mit der Aufschrift 'Flügel B — KEIN ZUTRITT'."
            ),
            kurz="Flügel A. Zuckende Neonröhren. Offene Tür bei Zimmer 7.",
            ausgänge={"ost": "eingang", "süd": "labor", "nord": "zimmer_7", "west": "flügel_b"},
            horror_texte=[
                "Das Neonlicht blinkt: ... --- ... — SOS in Morsecode.",
                "Zimmer 7. Irgendwann hast du hier gelegen. Du weißt es nicht. Du weißt es.",
            ],
        ),
        "zimmer_7": Raum(
            name="Patientenzimmer 7",
            beschreibung=(
                "Ein kleines, klaustrophobisches Zimmer. Ein Bett, geschnürte Matratze. "
                "An der Wand — von Fingernägeln eingeritzte Worte, tausend Wiederholungen: "
                "'ICH BIN NICHT WAS ICH WAR'. "
                "Auf dem Nachtisch: ein verblasstes Foto, ein zerbrochener Spiegel, "
                "ein Amulett an einer schwarzen Kette. "
                "Unter dem Bett: ein Schuh. Nur einer. "
                "Das Fenster ist von innen vernagelt."
            ),
            kurz="Zimmer 7. Kratzer überall. Amulett.",
            ausgänge={"süd": "flügel_a_eingang"},
            gegenstände=["amulett"],
            horror_texte=[
                "Die Kratzer in der Wand — sie gehen weiter. Bis hinter den Putz. Bis ins Fleisch.",
                "Du siehst dein Gesicht im zerbrochenen Spiegel. Manche Fragmente zeigen etwas anderes.",
            ],
        ),
        "flügel_b": Raum(
            name="Flügel B — Korridor",
            beschreibung=(
                "Du bist jetzt in Flügel B. Die Luft hier ist anders — dicker, schwerer, "
                "als würde die Dunkelheit hier eine eigene Konsistenz haben. "
                "Die Wände sind mit schwarzem Schimmel bedeckt, der seltsame Muster bildet. "
                "Du erkennst Gesichter darin. Die Gesichter erkennen dich. "
                "Eine Tür am Ende: 'ZIMMER 13 — VERSIEGELT'. "
                "Eine Treppe führt nach unten — in den Keller."
            ),
            kurz="Flügel B. Schimmel mit Gesichtern. Treppe nach unten.",
            ausgänge={"ost": "flügel_a_eingang", "nord": "zimmer_13", "unten": "keller_treppe"},
            gesperrt=True,
            schlüssel="flügel_b",
            horror_texte=[
                "Die Gesichter im Schimmel — sie öffnen die Münder. Lautlos.",
                "Du willst nicht wissen, was in Zimmer 13 ist. Du willst es. Du willst es nicht.",
            ],
        ),
        "zimmer_13": Raum(
            name="Zimmer 13 — Das Zentrum",
            beschreibung=(
                "Der Raum, über den alle geschrieben haben. Die Wände sind bedeckt — "
                "nicht mit Schimmel, sondern mit Schrift. Tausende von Wörtern, übereinander, "
                "in verschiedenen Handschriften, als hätten hier viele Menschen die gleiche "
                "Botschaft hinterlassen. In der Mitte: ein schwarzer Fleck auf dem Boden, "
                "perfekt kreisförmig, versengt. Und in der Mitte des Kreises — nichts. "
                "Aber das Nichts hat ein Gewicht. Du spürst es gegen deine Brust drücken. "
                "Auf dem Boden: eine herausgerissene Buchseite."
            ),
            kurz="Zimmer 13. Schriften an allen Wänden. Der schwarze Kreis.",
            ausgänge={"süd": "flügel_b"},
            gegenstände=["seite"] if False else [],
            gesperrt=False,
            horror_texte=[
                "Du liest die Wände. Alle Texte enden mit demselben Satz: 'Es kennt deinen Namen.'",
                "Der schwarze Kreis ist nicht verbrannt. Es ist Schatten. Schatten ohne Licht.",
            ],
            ereignis="zimmer_13_eintritt",
        ),
        "oberer_korridor": Raum(
            name="Oberer Korridor",
            beschreibung=(
                "Die Treppe endet in einem Korridor mit Schrägdach — das Dach eines alten "
                "Gebäudeflügels. Durch ein zerbrochenes Dachfenster fällt kaum Mondlicht. "
                "Regenwasser tropft in Pfützen auf dem Boden. "
                "Hier riecht es nach Verwesung — nicht von Körpern, sondern von Zeit. "
                "Als würde die Zeit hier verrotten. "
                "Zwei Türen: Archiv, Schwesternzimmer."
            ),
            kurz="Oberer Korridor. Mondlicht. Verrottendes Schweigen.",
            ausgänge={"unten": "eingang", "ost": "archiv", "west": "schwesternzimmer"},
            horror_texte=[
                "Im Mondlicht siehst du deinen Schatten. Er bewegt sich zu früh.",
                "Das Tropfen des Wassers hat ein Muster. Du erkennst es. Du verstehst es nicht.",
            ],
        ),
        "archiv": Raum(
            name="Archivraum",
            beschreibung=(
                "Regale, bodentief, voller Patientenakten. Tausende. Einige Akten "
                "sind auf den Boden gefallen und verstreut — Namen, Diagnosen, Behandlungen. "
                "Eine Diagnose wiederholt sich auf jedem dritten Blatt: 'HOLLOWBORN SYNDROM'. "
                "In der Ecke: ein Aktenschrank mit eingeritzten Symbolen. "
                "Auf dem Boden vor dem Schrank: Blutspuren — jung, vielleicht Stunden alt. "
                "Im Aktenschrank: eine Kurbel, irgendwie fehl am Platz."
            ),
            kurz="Archiv. Tausend Akten. Frische Blutspuren.",
            ausgänge={"west": "oberer_korridor"},
            gegenstände=["kurbel"],
            horror_texte=[
                "Die Blutspuren führen zum Aktenschrank. Und dann — sie hören auf. Mitten im Raum.",
                "Du findest deine eigene Akte. Die Diagnose ist geschwärzt — außer einem Wort: HOLLOW.",
            ],
        ),
        "schwesternzimmer": Raum(
            name="Schwesternzimmer",
            beschreibung=(
                "Ein kleines, aufgeräumtes Zimmer — unheimlich aufgeräumt für einen verlassenen Ort. "
                "Bett gemacht, Kissen zurechtgelegt. Ein Schminktisch mit gebrochenem Spiegel, "
                "auf dem Lippenstift liegt — frisch benutzt. Eine Uniform hängt an der Tür. "
                "Auf dem Nachttisch: ein Foto einer lächelnden Frau vor dem Sanatorium. "
                "Dieselbe Frau, von der Uniform. Unter dem Foto: ein silberner Schlüssel."
            ),
            kurz="Schwesternzimmer. Erschreckend ordentlich. Silberner Schlüssel.",
            ausgänge={"ost": "oberer_korridor"},
            gegenstände=["schlüssel_b"],
            horror_texte=[
                "Der Lippenstift auf dem Tisch — warm. Wie gerade benutzt.",
                "Das Foto. Die Frau lächelt. Auf dem zweiten Blick — sie lächelt nicht.",
            ],
        ),
        "keller_treppe": Raum(
            name="Kellertreppe",
            beschreibung=(
                "Steinerne Stufen, feucht und glitschig, führen nach unten. "
                "Mit jedem Schritt nach unten wird es kälter — nicht Kälte des Winters, "
                "sondern die Kälte von Orten, die keine Wärme mehr kennen. "
                "An der Wand: Rillen, tief und parallel — als hätte etwas mit Klauen "
                "hier hinuntergedrückt. Die Rillen sind zu hoch für einen Menschen. "
                "Am Ende der Treppe: eine massive Stahltür."
            ),
            kurz="Kellertreppe. Kälte. Rillen in den Wänden.",
            ausgänge={"oben": "flügel_b", "unten": "keller"},
            gesperrt=True,
            schlüssel="keller",
            horror_texte=[
                "Die Rillen in der Wand — du legst deine Hand hinein. Sie passt nicht. Nichts Menschliches passt.",
                "Unter dir: Stille. Aber die Stille hat Atemzüge.",
            ],
        ),
        "keller": Raum(
            name="Der Keller — Herz der Finsternis",
            beschreibung=(
                "Du bist unten. Der Keller ist größer, als das Gebäude von oben vermuten lässt — "
                "viel größer. Unmöglich groß. Steinwände, nass, mit Schimmel bedeckt. "
                "In der Mitte: ein Altar aus zusammengetragenem Krankenhausinventar — "
                "Betten, Stühle, Schienen — zu einem Kreis aufgetürmt. "
                "Und in der Mitte des Kreises: ES. "
                "Du kannst es nicht direkt ansehen. Dein Gehirn weigert sich, die Form zu verarbeiten. "
                "Aber du weißt: Es hat dich schon lange erwartet. "
                "Es kennt deinen Namen. Es kennt jeden deiner Atemzüge. Es ist hungrig."
            ),
            kurz="Der Keller. Der Altar. ES.",
            ausgänge={"oben": "keller_treppe"},
            horror_texte=[],
            ereignis="finale",
        ),
    }

# ──────────────────────────────────────────────────────────────
# SPIELER
# ──────────────────────────────────────────────────────────────

class Spieler:
    MAX_HP = 100
    MAX_GEIST = 100
    MAX_GEWICHT = 10

    def __init__(self):
        self.name = "Du"
        self.hp = 100
        self.geist = 100
        self.inventar: list[str] = []
        self.aktueller_raum = "erwachen"
        self.schritte = 0
        self.hat_taschenlampe = False
        self.taschenlampe_an = False
        self.besuchte_räume: set[str] = set()
        self.gelöste_ereignisse: set[str] = set()
        self.tot = False
        self.gewonnen = False

    def gewicht(self, gegenstände: dict[str, Gegenstand]) -> int:
        total = 0
        for g_name in self.inventar:
            if g_name in gegenstände:
                total += gegenstände[g_name].gewicht
        return total

    def hp_verlieren(self, menge: int, grund: str = ""):
        self.hp = max(0, self.hp - menge)
        if grund:
            print(Farbe.rot(f"  ─ [{grund}] Du verlierst {menge} HP. ─"))
        if self.hp <= 0:
            self.tot = True

    def geist_verlieren(self, menge: int, grund: str = ""):
        self.geist = max(0, self.geist - menge)
        if grund:
            print(Farbe.lila(f"  ─ [{grund}] Dein Verstand zerbröckelt. -{menge} Geist. ─"))
        if self.geist <= 0:
            self.tot = True

    def hp_heilen(self, menge: int):
        self.hp = min(self.MAX_HP, self.hp + menge)

    def geist_heilen(self, menge: int):
        self.geist = min(self.MAX_GEIST, self.geist + menge)

    def gegenstand_nehmen(self, g_name: str, gegenstände: dict[str, Gegenstand]) -> bool:
        if g_name not in gegenstände:
            return False
        g = gegenstände[g_name]
        if self.gewicht(gegenstände) + g.gewicht > self.MAX_GEWICHT:
            print(Farbe.gelb("  Du kannst nicht mehr tragen."))
            return False
        self.inventar.append(g_name)
        if g_name == "taschenlampe":
            self.hat_taschenlampe = True
        return True

    def hat_gegenstand(self, alias_oder_name: str, gegenstände: dict[str, Gegenstand]) -> Optional[str]:
        for g_name in self.inventar:
            if g_name in gegenstände:
                if gegenstände[g_name].passt_zu(alias_oder_name):
                    return g_name
        return None

    def status_anzeigen(self, gegenstände: dict[str, Gegenstand]):
        drucke_leerzeile()
        drucke_trennlinie("═")
        print(Farbe.bold(f"  ► STATUS"))
        drucke_trennlinie()

        hp_farbe = Farbe.grün if self.hp > 50 else (Farbe.gelb if self.hp > 25 else Farbe.rot)
        geist_farbe = Farbe.cyan if self.geist > 50 else (Farbe.gelb if self.geist > 25 else Farbe.lila)

        hp_balken    = self._balken(self.hp, self.MAX_HP, 20)
        geist_balken = self._balken(self.geist, self.MAX_GEIST, 20)

        print(f"  {Farbe.bold('Körper :')} {hp_farbe(hp_balken)} {hp_farbe(str(self.hp))}/{self.MAX_HP}")
        print(f"  {Farbe.bold('Verstand:')} {geist_farbe(geist_balken)} {geist_farbe(str(self.geist))}/{self.MAX_GEIST}")
        print(f"  {Farbe.bold('Schritte:')} {self.schritte}")
        drucke_trennlinie()
        print(f"  {Farbe.bold('Inventar')} [{self.gewicht(gegenstände)}/{self.MAX_GEWICHT}]:")
        if not self.inventar:
            print(Farbe.grau("  — Leer —"))
        else:
            for g_name in self.inventar:
                if g_name in gegenstände:
                    g = gegenstände[g_name]
                    verbraucht = Farbe.grau(" [verbraucht]") if g.verbraucht else ""
                    print(f"  • {Farbe.gelb(g.name)}{verbraucht}")
        drucke_trennlinie("═")
        drucke_leerzeile()

    @staticmethod
    def _balken(wert: int, maximum: int, länge: int) -> str:
        voll = int((wert / maximum) * länge)
        leer = länge - voll
        return f"[{'█' * voll}{'░' * leer}]"

# ──────────────────────────────────────────────────────────────
# KARTE
# ──────────────────────────────────────────────────────────────

KARTEN_LAYOUT = """
  ╔═══════════════════════════════════════════╗
  ║         SANATORIUM VOSS — KARTE           ║
  ╠═══════════════════════════════════════════╣
  ║                                           ║
  ║  [ARCHIV]──[OB.KORRIDOR]──[SCHWESTER]    ║
  ║                  │                        ║
  ║  [BÜRO]──[EINGANG]──[FLÜGEL A]──[ZI.7]   ║
  ║                  │        │               ║
  ║          [ERWACHEN]  [LABOR]──[FLÜGEL B]  ║
  ║                  │              │         ║
  ║          [WARTEZIMMER]     [ZI.13][KELLER]║
  ║                  │                        ║
  ║          [BEHANDLUNG]──[LABOR]            ║
  ║                                           ║
  ╚═══════════════════════════════════════════╝
"""

def karte_anzeigen(spieler: Spieler, räume: dict[str, Raum]):
    drucke_leerzeile()
    print(Farbe.grau(KARTEN_LAYOUT))
    print(f"  {Farbe.bold('Aktueller Standort:')} {Farbe.gelb(räume[spieler.aktueller_raum].name)}")
    print(f"  {Farbe.grau('(Besuchte Räume: ' + str(len(spieler.besuchte_räume)) + '/' + str(len(räume)) + ')')}")
    drucke_leerzeile()

# ──────────────────────────────────────────────────────────────
# EREIGNISSE
# ──────────────────────────────────────────────────────────────

def erstes_erwachen(spieler: Spieler):
    if "erstes_erwachen" in spieler.gelöste_ereignisse:
        return
    spieler.gelöste_ereignisse.add("erstes_erwachen")
    drucke_leerzeile()
    drucke_trennlinie("~", farbe=Farbe.dunkelrot)
    drucke_horror("  Du öffnest die Augen.", 0.06)
    warte(0.8)
    drucke_horror("  Die Decke — Schimmel, Risse, etwas Dunkles.", 0.05)
    warte(0.8)
    drucke_horror("  Du weißt nicht, wie du hier hingekommen bist.", 0.05)
    warte(0.8)
    drucke_horror("  Du weißt nicht, wie lange du hier warst.", 0.05)
    warte(0.8)
    drucke_horror("  Aber etwas — etwas weiß es.", 0.05)
    warte(1.5)
    drucke_trennlinie("~", farbe=Farbe.dunkelrot)
    drucke_leerzeile()
    spieler.geist_verlieren(5, "Das Erwachen")

def zimmer_13_ereignis(spieler: Spieler):
    if "zimmer_13_eintritt" in spieler.gelöste_ereignisse:
        return
    spieler.gelöste_ereignisse.add("zimmer_13_eintritt")
    drucke_leerzeile()
    drucke_trennlinie("▓", farbe=Farbe.dunkelrot)
    drucke_langsam("  Die Wörter an den Wänden beginnen, sich zu bewegen.", 0.04)
    warte(1.0)
    drucke_horror("  Sie drehen sich. Sie formen deinen Namen.", 0.06)
    warte(1.2)
    drucke_horror("  Hundertmal. Tausendmal.", 0.06)
    warte(1.0)
    drucke_langsam("  Du deckst die Augen ab. Die Worte sind auch hinter deinen Augenlidern.", 0.04)
    warte(1.5)
    drucke_trennlinie("▓", farbe=Farbe.dunkelrot)
    spieler.geist_verlieren(20, "Zimmer 13")
    spieler.hp_verlieren(10, "Die Worte haben Gewicht")

# ──────────────────────────────────────────────────────────────
# FINALE — BOSS KONFRONTATION
# ──────────────────────────────────────────────────────────────

def finale_sequenz(spieler: Spieler, gegenstände: dict[str, Gegenstand]) -> str:
    """Gibt 'sieg', 'tod' oder 'flucht' zurück."""
    clear()
    drucke_trennlinie("█", farbe=Farbe.dunkelrot)
    drucke_leerzeile()
    drucke_horror("  ES IST DA.", 0.15)
    warte(2.0)
    drucke_leerzeile()
    drucke_langsam("  Du kannst es nicht sehen — aber du spürst es.", 0.04)
    warte(1.0)
    drucke_langsam("  Ein Gewicht, das keine Physik kennt.", 0.04)
    warte(1.0)
    drucke_langsam("  Eine Präsenz, die deinen Verstand als Tür benutzt.", 0.04)
    warte(1.5)
    drucke_leerzeile()
    drucke_horror("  Es flüstert. Nicht in Worten. In Erinnerungen.", 0.06)
    warte(2.0)
    drucke_leerzeile()

    hat_foto   = spieler.hat_gegenstand("foto", gegenstände) is not None
    hat_messer = spieler.hat_gegenstand("messer", gegenstände) is not None
    hat_seite  = spieler.hat_gegenstand("seite", gegenstände) is not None
    hat_amulett= spieler.hat_gegenstand("amulett", gegenstände) is not None

    punkte = sum([hat_foto, hat_messer, hat_seite, hat_amulett])

    if punkte >= 3:
        return _finale_sieg(spieler, gegenstände, hat_foto, hat_messer, hat_seite, hat_amulett)
    elif spieler.geist < 20 or spieler.hp < 15:
        return _finale_tod(spieler)
    else:
        return _finale_flucht(spieler)


def _finale_sieg(spieler, gegenstände, hat_foto, hat_messer, hat_seite, hat_amulett) -> str:
    drucke_langsam("  Du erinnerst dich. Die Seite. Die Anweisungen.", 0.04)
    warte(1.0)
    drucke_langsam("  Drei Dinge. Drei Opfer. Das Wesen binden.", 0.04)
    warte(1.5)
    drucke_leerzeile()

    if hat_foto:
        drucke_horror("  Du wirfst das Foto in den Kreis.", 0.05)
        warte(0.8)
        drucke_langsam("  Es verbrennt ohne Flamme — einfach weg.", 0.04)
        warte(1.0)

    if hat_messer:
        drucke_horror("  Du legst das Skalpell nieder. Das Werkzeug aller Schuld hier.", 0.05)
        warte(0.8)
        drucke_langsam("  Es frisst das Metall. Das Metall lacht.", 0.04)
        warte(1.0)

    drucke_leerzeile()
    drucke_horror("  Das Letzte: dein Blut.", 0.08)
    warte(1.5)
    drucke_langsam("  Du drückst den Daumen auf die scharfe Kante einer Bodenfliese.", 0.04)
    warte(0.8)
    drucke_horror("  Der Schmerz ist real. Der Kreis trinkt.", 0.06)
    warte(2.0)
    drucke_leerzeile()

    drucke_trennlinie("░", farbe=Farbe.lila)
    drucke_horror("  DAS WESEN SCHREIT.", 0.12)
    warte(2.0)
    drucke_langsam("  Nicht in Klang. In Stille. Die Stille schreit.", 0.04)
    warte(1.5)
    drucke_leerzeile()

    drucke_langsam("  Und dann — es ist weg.", 0.04)
    warte(1.0)
    drucke_langsam("  Der Keller wird kleiner. Realer. Nur Stein und Stille.", 0.04)
    warte(1.0)
    drucke_langsam("  Du siehst die Treppe. Du siehst das Licht — fern, aber da.", 0.04)
    warte(1.5)
    drucke_leerzeile()

    drucke_trennlinie("═", farbe=Farbe.grün)
    print(Farbe.grün(Farbe.bold("  ENDE — DU HAST ES GEBUNDEN")))
    drucke_trennlinie("═", farbe=Farbe.grün)
    drucke_leerzeile()
    drucke_langsam("  Das Sanatorium Voss lässt dich gehen.", 0.04)
    warte(0.8)
    drucke_langsam("  Dieses Mal.", 0.04)
    warte(2.0)
    return "sieg"


def _finale_tod(spieler) -> str:
    drucke_leerzeile()
    drucke_horror("  Dein Verstand ist zu gebrochen. Dein Körper zu schwach.", 0.06)
    warte(1.5)
    drucke_horror("  Das Wesen braucht keine Worte. Nur dich.", 0.06)
    warte(1.5)
    drucke_leerzeile()
    drucke_horror("  Du merkst nicht, wie du aufhörst, du zu sein.", 0.05)
    warte(2.0)
    drucke_horror("  Es füllt den Raum, den du hinterlässt.", 0.05)
    warte(2.0)
    drucke_leerzeile()
    drucke_trennlinie("█", farbe=Farbe.dunkelrot)
    print(Farbe.dunkelrot(Farbe.bold("  ENDE — DU WURDEST ZU EINEM ECHO")))
    drucke_trennlinie("█", farbe=Farbe.dunkelrot)
    spieler.tot = True
    return "tod"


def _finale_flucht(spieler) -> str:
    drucke_leerzeile()
    drucke_langsam("  Du läufst.", 0.04)
    warte(0.5)
    drucke_horror("  Du läufst, obwohl die Notiz es verboten hat.", 0.05)
    warte(1.0)
    drucke_horror("  Es hört das Laufen.", 0.06)
    warte(1.5)
    drucke_leerzeile()
    drucke_langsam("  Du erreichst die Treppe. Die Tür. Den Korridor.", 0.04)
    warte(0.8)
    drucke_langsam("  Die Schritte hinter dir werden nicht lauter.", 0.04)
    warte(0.8)
    drucke_horror("  Sie müssen nicht lauter werden.", 0.06)
    warte(2.0)
    drucke_leerzeile()

    drucke_trennlinie("─", farbe=Farbe.gelb)
    print(Farbe.gelb(Farbe.bold("  ENDE — DU BIST GEGANGEN. ABER ES AUCH.")))
    drucke_trennlinie("─", farbe=Farbe.gelb)
    drucke_leerzeile()
    drucke_langsam("  Irgendwo wartet das Sanatorium Voss noch.", 0.04)
    drucke_langsam("  Es ist geduldig. Es hat Zeit.", 0.04)
    warte(2.0)
    return "flucht"

# ──────────────────────────────────────────────────────────────
# ZUFÄLLIGE BEGEGNUNGEN
# ──────────────────────────────────────────────────────────────

BEGEGNUNGEN = [
    {
        "chance": 0.12,
        "text": (
            "Aus dem Dunkel hinter dir — ein Atemzug.\n"
            "Zu nah. Zu warm."
        ),
        "hp": 8,
        "geist": 12,
        "grund": "Etwas hat dich berührt",
    },
    {
        "chance": 0.10,
        "text": (
            "Die Wand vor dir wölbt sich. Nur kurz.\n"
            "Als würde etwas dagegen drücken."
        ),
        "hp": 0,
        "geist": 15,
        "grund": "Die Wand atmet",
    },
    {
        "chance": 0.08,
        "text": (
            "Du siehst eine Silhouette am Ende des Flurs.\n"
            "Sie steht falsch. Der Winkel — falsch.\n"
            "Sie dreht sich um. Kein Gesicht."
        ),
        "hp": 5,
        "geist": 20,
        "grund": "Das Gesichtslose",
    },
    {
        "chance": 0.09,
        "text": "Du hörst deinen Namen. Einmal. Klar und deutlich.",
        "hp": 0,
        "geist": 10,
        "grund": "Dein Name",
    },
    {
        "chance": 0.07,
        "text": (
            "Die Taschenlampe flackert dreimal.\n"
            "Im dritten Flackern — eine Hand auf deiner Schulter.\n"
            "Als das Licht zurückkommt, ist sie weg."
        ),
        "hp": 10,
        "geist": 15,
        "grund": "Die unsichtbare Hand",
    },
    {
        "chance": 0.11,
        "text": "Blut auf deinen Händen. Du weißt nicht woher.",
        "hp": 12,
        "geist": 8,
        "grund": "Das Blut",
    },
    {
        "chance": 0.06,
        "text": (
            "Ein Kind weint. Irgendwo.\n"
            "Es hört auf, als du stehst.\n"
            "Es fängt wieder an, als du weitergehst."
        ),
        "hp": 0,
        "geist": 18,
        "grund": "Das weinende Kind",
    },
    {
        "chance": 0.09,
        "text": "Du siehst dich selbst. Zehn Meter vor dir. Du bewegst dich nicht. Es schon.",
        "hp": 5,
        "geist": 25,
        "grund": "Das Spiegelbild",
    },
]

def prüfe_begegnung(spieler: Spieler):
    for b in BEGEGNUNGEN:
        if random.random() < b["chance"]:
            drucke_leerzeile()
            drucke_trennlinie("·", farbe=Farbe.dunkelrot)
            drucke_horror(f"  {b['text']}", 0.04)
            warte(1.5)
            if b["hp"] > 0:
                spieler.hp_verlieren(b["hp"], b["grund"])
            if b["geist"] > 0:
                spieler.geist_verlieren(b["geist"], b["grund"])
            drucke_trennlinie("·", farbe=Farbe.dunkelrot)
            drucke_leerzeile()
            break

# ──────────────────────────────────────────────────────────────
# BEFEHLSVERARBEITUNG
# ──────────────────────────────────────────────────────────────

RICHTUNGEN = {
    "nord": "nord", "n": "nord", "norden": "nord",
    "süd": "süd", "s": "süd", "süden": "süd", "sued": "süd",
    "ost": "ost", "o": "ost", "osten": "ost",
    "west": "west", "w": "west", "westen": "west",
    "oben": "oben", "hoch": "oben", "rauf": "oben", "aufwärts": "oben",
    "unten": "unten", "runter": "unten", "abwärts": "unten",
}

def verarbeite_befehl(
    eingabe: str,
    spieler: Spieler,
    räume: dict[str, Raum],
    gegenstände: dict[str, Gegenstand],
) -> bool:
    """Gibt False zurück, wenn das Spiel beendet werden soll."""
    teile = eingabe.lower().strip().split()
    if not teile:
        return True

    verb = teile[0]
    rest = " ".join(teile[1:]) if len(teile) > 1 else ""

    aktueller_raum = räume[spieler.aktueller_raum]

    # ── BEENDEN ──────────────────────────────────────────────
    if verb in ("beenden", "exit", "quit", "raus", "aufgeben"):
        drucke_leerzeile()
        drucke_langsam("  Du legst das Spiel nieder. Das Sanatorium bleibt.", 0.04)
        drucke_leerzeile()
        return False

    # ── HILFE ────────────────────────────────────────────────
    if verb in ("hilfe", "h", "help", "?"):
        drucke_hilfe()
        return True

    # ── STATUS ───────────────────────────────────────────────
    if verb in ("status", "s", "stats", "stat"):
        spieler.status_anzeigen(gegenstände)
        return True

    # ── KARTE ────────────────────────────────────────────────
    if verb in ("karte", "k", "map"):
        karte_anzeigen(spieler, räume)
        return True

    # ── INVENTAR ─────────────────────────────────────────────
    if verb in ("inventar", "i", "inv", "tasche"):
        spieler.status_anzeigen(gegenstände)
        return True

    # ── SCHAUEN / BESCHREIBUNG ───────────────────────────────
    if verb in ("schauen", "schau", "look", "l", "umsehen", "beschreibung", "umschauen"):
        beschreibe_raum(spieler, räume, gegenstände, erneut=True)
        return True

    # ── BEWEGUNG ─────────────────────────────────────────────
    if verb in RICHTUNGEN or (verb in ("gehe", "geh", "gehen", "go", "laufe", "lauf") and rest in RICHTUNGEN):
        richtung = RICHTUNGEN.get(verb) or RICHTUNGEN.get(rest)
        return bewege_spieler(richtung, spieler, räume, gegenstände)

    # ── NEHMEN ───────────────────────────────────────────────
    if verb in ("nehmen", "nimm", "nehme", "nehm", "aufheben", "pick", "take"):
        return nimm_gegenstand(rest, spieler, aktueller_raum, gegenstände)

    # ── ABLEGEN ──────────────────────────────────────────────
    if verb in ("ablegen", "legen", "leg", "lege", "drop", "ablegen"):
        return lege_gegenstand(rest, spieler, aktueller_raum, gegenstände)

    # ── UNTERSUCHEN ──────────────────────────────────────────
    if verb in ("untersuchen", "untersuche", "prüfen", "prüfe", "inspizieren",
                "inspect", "examine", "betrachten", "betrachte", "lesen", "lese"):
        return untersuche_gegenstand(rest, spieler, aktueller_raum, gegenstände)

    # ── BENUTZEN ─────────────────────────────────────────────
    if verb in ("benutzen", "benutze", "benutzen", "use", "nutzen", "nutze",
                "verwenden", "verwende", "anwenden"):
        return benutze_gegenstand(rest, spieler, aktueller_raum, gegenstände)

    # ── UNBEKANNTER BEFEHL ───────────────────────────────────
    antworten = [
        "Das ergibt hier keinen Sinn.",
        "Nicht jetzt. Nicht in diesem Dunkel.",
        "Das Sanatorium versteht dich nicht. Oder will es nicht.",
        "Die Stille antwortet nicht auf diesen Befehl.",
    ]
    print(Farbe.grau(f"  {random.choice(antworten)}"))
    return True


def bewege_spieler(
    richtung: str,
    spieler: Spieler,
    räume: dict[str, Raum],
    gegenstände: dict[str, Gegenstand],
) -> bool:
    aktueller_raum = räume[spieler.aktueller_raum]

    if richtung not in aktueller_raum.ausgänge:
        antworten = [
            f"In diese Richtung führt kein Weg.",
            f"Die Dunkelheit dort ist zu dicht. Oder zu absichtlich.",
            f"Kein Ausgang nach {richtung}.",
        ]
        print(Farbe.grau(f"  {random.choice(antworten)}"))
        return True

    ziel_raum_name = aktueller_raum.ausgänge[richtung]
    ziel_raum = räume[ziel_raum_name]

    # Gesperrter Raum
    if ziel_raum.gesperrt:
        benötigter_schlüssel = None
        for g_name in spieler.inventar:
            if g_name in gegenstände:
                g = gegenstände[g_name]
                if g.schlüssel_für == ziel_raum.schlüssel:
                    benötigter_schlüssel = g
                    break

        if benötigter_schlüssel is None:
            print(Farbe.gelb(f"  Die Tür ist gesperrt. Du brauchst etwas, um sie zu öffnen."))
            spieler.geist_verlieren(2)
            return True
        else:
            print(Farbe.grün(f"  Du benutzt den {benötigter_schlüssel.name}, um die Tür zu öffnen."))
            ziel_raum.gesperrt = False

    # Bewegung
    spieler.aktueller_raum = ziel_raum_name
    spieler.schritte += 1
    spieler.besuchte_räume.add(ziel_raum_name)

    # Zufällige Begegnung
    if spieler.schritte % 3 == 0:
        prüfe_begegnung(spieler)

    if spieler.tot:
        return True

    drucke_leerzeile()
    beschreibe_raum(spieler, räume, gegenstände, erneut=False)
    horror_effekt()

    # Ereignisse
    if ziel_raum.ereignis == "finale" and "finale" not in spieler.gelöste_ereignisse:
        spieler.gelöste_ereignisse.add("finale")
        warte(1.0)
        ergebnis = finale_sequenz(spieler, gegenstände)
        if ergebnis in ("sieg", "tod", "flucht"):
            spieler.gewonnen = True
            return False
    elif ziel_raum.ereignis == "zimmer_13_eintritt":
        zimmer_13_ereignis(spieler)

    return True


def nimm_gegenstand(
    name: str,
    spieler: Spieler,
    raum: Raum,
    gegenstände: dict[str, Gegenstand],
) -> bool:
    if not name:
        print(Farbe.grau("  Was möchtest du nehmen?"))
        return True

    for g_name in raum.gegenstände[:]:
        if g_name in gegenstände:
            g = gegenstände[g_name]
            if g.passt_zu(name):
                if spieler.gegenstand_nehmen(g_name, gegenstände):
                    raum.gegenstände.remove(g_name)
                    print(Farbe.grün(f"  Du nimmst: {g.name}"))
                    if g_name == "taschenlampe":
                        spieler.hat_taschenlampe = True
                    return True
                return True

    # Auch im Inventar suchen (falls er was im Inventar meint)
    for g_name in spieler.inventar:
        if g_name in gegenstände and gegenstände[g_name].passt_zu(name):
            print(Farbe.grau(f"  {gegenstände[g_name].name} trägst du bereits."))
            return True

    print(Farbe.grau(f"  '{name}' — hier nicht zu finden."))
    return True


def lege_gegenstand(
    name: str,
    spieler: Spieler,
    raum: Raum,
    gegenstände: dict[str, Gegenstand],
) -> bool:
    if not name:
        print(Farbe.grau("  Was möchtest du ablegen?"))
        return True

    g_name = spieler.hat_gegenstand(name, gegenstände)
    if g_name:
        spieler.inventar.remove(g_name)
        raum.gegenstände.append(g_name)
        print(Farbe.gelb(f"  Du legst {gegenstände[g_name].name} ab."))
        if g_name == "taschenlampe":
            spieler.hat_taschenlampe = False
            spieler.taschenlampe_an = False
    else:
        print(Farbe.grau(f"  Du trägst kein '{name}'."))
    return True


def untersuche_gegenstand(
    name: str,
    spieler: Spieler,
    raum: Raum,
    gegenstände: dict[str, Gegenstand],
) -> bool:
    if not name:
        print(Farbe.grau("  Was möchtest du untersuchen?"))
        return True

    # Im Inventar
    g_name = spieler.hat_gegenstand(name, gegenstände)
    if g_name:
        g = gegenstände[g_name]
        drucke_leerzeile()
        print(f"  {Farbe.bold(g.name)}:")
        drucke_text(g.beschreibung)
        drucke_leerzeile()
        return True

    # Im Raum
    for r_g in raum.gegenstände:
        if r_g in gegenstände and gegenstände[r_g].passt_zu(name):
            g = gegenstände[r_g]
            drucke_leerzeile()
            print(f"  {Farbe.bold(g.name)}:")
            drucke_text(g.beschreibung)
            drucke_leerzeile()
            return True

    # Allgemeine Beschreibung
    antworten = [
        f"'{name}' zeigt dir nichts Neues.",
        f"Dunkelheit verschluckt, was du suchen wolltest.",
        f"Nichts Untersuchbares namens '{name}' hier.",
    ]
    print(Farbe.grau(f"  {random.choice(antworten)}"))
    return True


def benutze_gegenstand(
    name: str,
    spieler: Spieler,
    raum: Raum,
    gegenstände: dict[str, Gegenstand],
) -> bool:
    if not name:
        print(Farbe.grau("  Was möchtest du benutzen?"))
        return True

    g_name = spieler.hat_gegenstand(name, gegenstände)
    if not g_name:
        print(Farbe.grau(f"  Du hast kein '{name}'."))
        return True

    g = gegenstände[g_name]
    if not g.verwendbar:
        print(Farbe.grau(f"  Du weißt nicht, wie du {g.name} benutzen könntest."))
        return True

    if g.verbraucht:
        print(Farbe.grau(f"  {g.name} ist bereits verbraucht."))
        return True

    drucke_leerzeile()
    drucke_text(g.verwendungs_text)
    drucke_leerzeile()

    # Spezielle Effekte
    if g_name == "medizin":
        spieler.hp_heilen(15)
        spieler.geist_heilen(10)
        g.verbraucht = True
        print(Farbe.grün("  +15 HP, +10 Geist"))
    elif g_name == "verbandsmaterial":
        spieler.hp_heilen(20)
        g.verbraucht = True
        print(Farbe.grün("  +20 HP"))
    elif g_name == "taschenlampe":
        spieler.taschenlampe_an = not spieler.taschenlampe_an
        zustand = "an" if spieler.taschenlampe_an else "aus"
        print(Farbe.gelb(f"  Taschenlampe: {zustand}"))
    elif g_name == "kerze":
        spieler.geist_heilen(5)
        print(Farbe.grün("  +5 Geist"))

    return True

# ──────────────────────────────────────────────────────────────
# RAUM BESCHREIBEN
# ──────────────────────────────────────────────────────────────

def beschreibe_raum(
    spieler: Spieler,
    räume: dict[str, Raum],
    gegenstände: dict[str, Gegenstand],
    erneut: bool = False,
):
    raum = räume[spieler.aktueller_raum]

    drucke_trennlinie("─")
    print(f"  {Farbe.bold(Farbe.gelb(raum.name))}")
    drucke_trennlinie("─")
    drucke_leerzeile()

    if erneut or not raum.besucht:
        drucke_text(raum.beschreibung)
        raum.besucht = True
    else:
        drucke_text(raum.kurz)

    drucke_leerzeile()

    # Gegenstände im Raum
    if raum.gegenstände:
        sichtbare = [
            gegenstände[g].name
            for g in raum.gegenstände
            if g in gegenstände
        ]
        if sichtbare:
            print(Farbe.cyan(f"  Hier zu sehen: {', '.join(sichtbare)}"))

    # Ausgänge
    ausgänge_str = ", ".join(
        f"{Farbe.grün(r)} ({räume[z].name if z in räume else '?'})"
        for r, z in raum.ausgänge.items()
    )
    print(f"  {Farbe.grau('Ausgänge:')} {ausgänge_str}")
    drucke_leerzeile()

    # Horror-Text (einmalig)
    horror = raum.horror_text()
    if horror:
        warte(0.8)
        drucke_horror(f"  {horror}", 0.04)
        spieler.geist_verlieren(5, "Atmosphäre")
        drucke_leerzeile()

    # Ereignis: Erstes Erwachen
    if raum.ereignis == "erstes_erwachen":
        erstes_erwachen(spieler)

# ──────────────────────────────────────────────────────────────
# HILFE
# ──────────────────────────────────────────────────────────────

def drucke_hilfe():
    drucke_leerzeile()
    drucke_trennlinie("═")
    print(Farbe.bold("  HILFE — BEFEHLE"))
    drucke_trennlinie()
    print(f"  {Farbe.gelb('Bewegung:')}  nord / süd / ost / west / oben / unten")
    print(f"  {Farbe.gelb('Schauen:')}   schauen / schau / look")
    print(f"  {Farbe.gelb('Nehmen:')}    nehmen [gegenstand]")
    print(f"  {Farbe.gelb('Ablegen:')}   ablegen [gegenstand]")
    print(f"  {Farbe.gelb('Untersuchen:')} untersuchen [gegenstand]")
    print(f"  {Farbe.gelb('Benutzen:')} benutzen [gegenstand]")
    print(f"  {Farbe.gelb('Status:')}    status / s")
    print(f"  {Farbe.gelb('Inventar:')} inventar / i")
    print(f"  {Farbe.gelb('Karte:')}     karte / k")
    print(f"  {Farbe.gelb('Hilfe:')}     hilfe / h")
    print(f"  {Farbe.gelb('Beenden:')}   beenden / exit")
    drucke_trennlinie("═")
    drucke_leerzeile()

# ──────────────────────────────────────────────────────────────
# TOD-BILDSCHIRM
# ──────────────────────────────────────────────────────────────

def zeige_tod(spieler: Spieler):
    clear()
    drucke_leerzeile()
    drucke_trennlinie("█", farbe=Farbe.dunkelrot)
    drucke_leerzeile()

    if spieler.hp <= 0:
        drucke_horror("  DEIN KÖRPER HAT VERSAGT.", 0.08)
        warte(1.5)
        drucke_langsam("  Das Sanatorium hält dich jetzt.", 0.04)
    elif spieler.geist <= 0:
        drucke_horror("  DEIN VERSTAND IST GEBROCHEN.", 0.08)
        warte(1.5)
        drucke_langsam("  Es wohnt jetzt in dem Raum, der mal du warst.", 0.04)

    warte(2.0)
    drucke_leerzeile()
    print(Farbe.dunkelrot(Farbe.bold("  — DU BIST TOT —")))
    drucke_leerzeile()
    print(Farbe.grau(f"  Räume erkundet: {len(spieler.besuchte_räume)}"))
    print(Farbe.grau(f"  Schritte: {spieler.schritte}"))
    drucke_leerzeile()
    drucke_trennlinie("█", farbe=Farbe.dunkelrot)
    drucke_leerzeile()

# ──────────────────────────────────────────────────────────────
# INTRO
# ──────────────────────────────────────────────────────────────

def zeige_intro():
    clear()
    drucke_leerzeile()
    drucke_trennlinie("╔", länge=72, farbe=Farbe.dunkelrot)

    zeilen = [
        "╔══════════════════════════════════════════════════════════════════╗",
        "║                                                                  ║",
        "║          E C H O E S   O F   T H E   H O L L O W               ║",
        "║                                                                  ║",
        "║                   Terminal Horror RPG                            ║",
        "║                                                                  ║",
        "╚══════════════════════════════════════════════════════════════════╝",
    ]
    for z in zeilen:
        print(Farbe.dunkelrot(z))
        time.sleep(0.05)

    drucke_leerzeile()
    drucke_langsam("  Sanatorium Voss. Geschlossen seit 1987.", 0.04)
    warte(0.8)
    drucke_langsam("  Offizielle Begründung: Budgetkürzungen.", 0.04)
    warte(0.8)
    drucke_horror("  Inoffizielle Begründung: HOLLOWBORN.", 0.05)
    warte(1.5)
    drucke_leerzeile()
    drucke_langsam("  Du erinnerst dich an nichts.", 0.04)
    warte(0.6)
    drucke_langsam("  Außer diesem Gebäude.", 0.04)
    warte(0.6)
    drucke_horror("  Und dem Ding, das deinen Namen flüstert.", 0.05)
    warte(2.0)
    drucke_leerzeile()
    drucke_trennlinie()
    drucke_langsam("  Tippe 'hilfe' für Befehle. Tippe 'beenden' um aufzugeben.", 0.03)
    drucke_trennlinie()
    drucke_leerzeile()
    input("  [ENTER um zu beginnen]")
    drucke_leerzeile()

# ──────────────────────────────────────────────────────────────
# SPIELSCHLEIFE
# ──────────────────────────────────────────────────────────────

def hauptschleife():
    spieler  = Spieler()
    räume    = erstelle_räume()
    gegenstände = erstelle_gegenstände()

    # Initialer Raum
    spieler.besuchte_räume.add(spieler.aktueller_raum)
    beschreibe_raum(spieler, räume, gegenstände, erneut=False)

    while True:
        # Tod durch HP oder Geist
        if spieler.tot:
            zeige_tod(spieler)
            break

        # Geist-Warnung
        if spieler.geist < 25 and spieler.geist > 0:
            print(Farbe.lila("  [Dein Verstand zerbröckelt am Rand des Abgrunds...]"))

        # HP-Warnung
        if spieler.hp < 20 and spieler.hp > 0:
            print(Farbe.rot("  [Du spürst, wie dein Körper nachgibt...]"))

        # Prompt
        try:
            drucke_trennlinie("·", länge=40, farbe=Farbe.grau)
            eingabe = input(Farbe.grau("  > ")).strip()
        except (KeyboardInterrupt, EOFError):
            drucke_leerzeile()
            drucke_langsam("  Das Sanatorium entlässt dich. Dieses Mal.", 0.04)
            break

        if not eingabe:
            continue

        soll_weitermachen = verarbeite_befehl(eingabe, spieler, räume, gegenstände)

        if not soll_weitermachen:
            if not spieler.tot and not spieler.gewonnen:
                drucke_leerzeile()
                drucke_langsam("  Das Spiel endet. Aber das Sanatorium bleibt.", 0.04)
                drucke_leerzeile()
            break

        # Nachrichten bei niedrigem Status
        if spieler.hp <= 0 or spieler.geist <= 0:
            spieler.tot = True
            zeige_tod(spieler)
            break

    drucke_leerzeile()
    print(Farbe.grau("  — Ende der Sitzung —"))
    drucke_leerzeile()

# ──────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────

def main():
    zeige_intro()
    hauptschleife()


if __name__ == "__main__":
    main()
