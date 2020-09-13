from __future__ import unicode_literals, print_function
import spacy
from spacy import displacy
import plac
from pathlib import Path

#output_dir=Path("./ner_models")
output_dir=Path("./ner3")

print("Loading from", output_dir)
nlp = spacy.load(output_dir)

sometext = """
Business Developer som vil være med til at drive den forretningsmæssige udvikling af Office 365
Vi søger en erfaren Business Developer der kan sætte retningen for den forretningsmæssige udvikling og implementering af Microsoft Office 365 platformen og services hos vores kunder i Norden.
Du bliver en central del af et nyoprettet 'Office 365 Kompetencecenter' med dygtige kollegaer, der skal levere modning og implementering af Office 365 platformen til vores kunder. Afdelingen består af Office 365 specialister, arkitekter og projektledere og søger nu en profil, der kan være bindeled mellem kunder og afdeling på leverancesiden, og gå forrest i forhold til at få afdækket kundernes specifikke krav og behov i forhold til platformen.
Du har måske en konsulent-, projektledelses eller anden ledelsesbaggrund, gerne erfaring fra den finansielle sektor, og kan arbejde både selvstændigt og i teams. Du har lyst til og erfaring med at engagere kunder i krav- og løsningsdialoger og er god til at kommunikere skriftligt og mundtligt. Du har personligt drive og stærke planlægnings-, kommunikations-, og samarbejdsevner samt en udadvendt personlighed.
Dine opgaver bliver blandt andet at:
• tage ejerskab for - og drive vores Office 365-roadmap og strategi i tæt dialog med vores kunder, afdelingen og interessenter i SDC
• bistå med at identificere nye værdiskabende forretningsmuligheder for vores kunder
• indsamle og validere kunders krav til implementering af Office 365 standardservices som Teams, SharePoint, Power BI – og på sigt kundespecifikke applikationer
• facilitere og verificere aftalte leverancer sammen med kunderne på workshops
• assistere med udrulning af leverancerne hos vores kunder og være 'ansigtet udadtil' i forhold til opfølgning på det forretningsmæssige pla
• sikre sammenhængen til vores andre leverancer i afdelingen Workplace Services
• drive dialogen med SDC’s andre udviklingsområder, hvor der er behov for samarbejde eller integrationer
• leverancestyring via interne og eksterne teams
• har ”fingeren på pulsen” på nye innovative tiltag inden for domænet
Lidt om dig:
Af professionelle kvalifikationer forstiller vi os at du:
• Har en videregående uddannelse (IT, cand.merc., ingeniør eller lign.)
• Demonstreret evne til at kommunikere effektivt med interessenter hos kunder og internt
• Stor erfaring med at navigere i flere ledelsesniveauer sammen med kunderne
• God til at motivere. Du er I stand til at engagere teamet og at etablere gode samarbejdsrelationer til kunderne
• Behersker dansk – og/eller et andet skandinavisk sprog - og engelsk i skrift og tale
• Flere års erfaring med Office 365 og Microsoft cloud er ønskeligt
• Erfaring med en eller flere af Office 365 services, eks. SharePoint, Teams, OneDrive og Power BI

Nice to have - men ikke et krav:
Erfaring med arkitekturarbejde.
Af personlige kvalifikationer byder du ind med:
• En udadvendt og empatisk adfærd.
• Målbevidst.
• Analytisk og metode-orienteret.
• God problemløser med en konstruktiv tilgang.
• Proaktiv – energisk og nysgerrig.
• Stærk kommunikator.
• Team orienteret.
• Du tør udfordre det bestående og stille spørgsmålstegn på en konstruktiv måde.
• Du formår at bevarer overblikket og kan træffe beslutninger selv når du er under pres.
• Du motiveres af at arbejde i en projektorganisation og i skiftende projekter.
Lidt om os
Du bliver en del af et stærkt team med gode kollegaer og vil have gode muligheder for at kunne forme opgaverne i projekterne.
Du får en, udfordrende og fleksibel arbejdsdag med engagerede og dedikerede kollegaer. Gode medarbejderforhold og mulighed for personlig og faglig udvikling.
Som medarbejder hos os, får du rigtig fine og fleksible arbejdsvilkår, herunder flekstid, pensionsordning og sundheds- og tandlægeforsikring, og det stopper ikke her, ud over den lovbetingede ferie får du en 6 ferieuge, 5 ekstra fridage, forhøjet feriegodtgørelse m.v.
Alt det praktiske
Har du spørgsmål til stillingen, er du velkommen til at kontakte Manager Workplace Services & Output Management Mathias Larsson +45 2935 4882.
Vi opfordrer alle uanset personlig baggrund til at søge stillingen, da vi finder mangfoldigheden som værende en styrke som bidrager til vores fælles succes.
Ansøgningsfrist: 30. september 2020"""




newdoc = nlp(sometext)
displacy.serve(newdoc, style="ent")