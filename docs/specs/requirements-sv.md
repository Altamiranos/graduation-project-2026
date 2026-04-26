# Kravspecifikation Examensarbete

- **Namn:** Sander Altamirano
- **Klass:** Cloud24
- **Datum:** 26/2 – 1/3 2026

---

## Bakgrund

Eftersom många organisationer använder Kubernetes för att drifta produktionsmiljöer och containerbaserade applikationer är det centralt att förstå hur dessa miljöer designas och konfigureras. Kunskap om klusterarkitektur, nätverk, säkerhet och övervakning utgör en viktig del av yrkesrollen inom Cloud och infrastruktur. Stora molnleverantörer erbjuder färdiga Kubernetes-tjänster där många delar av infrastrukturen är abstrakta, vilket gör att den underliggande arkitekturen ofta blir "osynlig" för både utvecklare och användare. För att uppnå en djupare förståelse för hur en produktionslik miljö är uppbyggd krävs att en sådan miljö designas och implementeras från grunden. Projektet fokuserar därför på att skapa en mindre, open source-baserad Kubernetes-miljö i en lokal labbmiljö, oberoende av hyperscalers och deras ekosystem.

Projektet tar sin utgångspunkt i behovet att förstå infrastrukturen bakom moderna plattformar utan att baseras på abstraherade molntjänster.

---

## Mål och avgränsningar

Syftet med examensarbetet är att designa och implementera en mindre, reproducerbar och produktionslik Kubernetes-miljö som är ubuntu-baserad. Miljön består av en control plane-node och två worker-noder. Minst en applikation ska deployas och exponeras via en ingress-controller. Övervakning implementeras med open source-baserade verktyg för att få en överblick över klustrets hälsa och funktioner. Säker access hanteras genom Kubernetes inbyggda RBAC. Projektet avgränsas till en lokal miljö och inkluderar inte integration med hyperscalers såsom AWS, Azure eller GCP. High availability på en enterprise-level, CI/CD-automation eller multi-region-arkitektur ingår inte i projektets arkitektur. Avgränsningarna säkerställer en realistisk scope inom den givna tidsramen. Projektet kan då uppfylla kraven, målen samt resurs-begränsningen.

---

## Tre frågor som ska kunna besvaras vid projektets slut

1. Hur kan en mindre produktionslik Kubernetes-miljö designas och implementeras med hjälp av open source-verktyg i en lokal infrastruktur?
2. Hur kan en applikation deployas och exponeras via en ingress-controller i klustret?
3. Hur kan övervakning och observability implementeras med open source-baserade verktyg för att säkerställa insyn i klustrets hälsa och funktion?

---

## Tekniker

Projektet genomförs i en lokal Ubuntu-baserad miljö och bygger på en mindre Kubernetes-topologi bestående av en control plane node och två worker nodes. Miljön implementeras med K3s, en lightweight distro av Kubernetes anpassad för resurs begränsade system. Valet motiveras av projektets lokala infrastruktur och behovet av en hanterbar samt reproducerbar lösning. K3s har också stöd för multi-nodes.

Containerisering sker med Docker och minst en testapplikation deployas i klustret för att demonstrera funktionalitet, kommunikation mellan noder samt hur applikationer körs. Exponering av tjänster hanteras via ingress-controller Traefik, som är kompatibel med K3s och möjliggör routing samt extern åtkomst till applikationen. Traefik har en etablerad användning i containerbaserade miljöer. För övervakning och observability används Prometheus för insamling av metrics medan Grafana används för visualisering och analys av klustrets hälsa och funktion. Dessa verktyg är etablerade inom branschen och relevanta för Cloud- och infrastruktur roller.

Behörighetsstyrning implementeras genom Kubernetes inbyggda RBAC-funktionalitet för att hantera åtkomst och rättigheter i klustret. Miljön dokumenteras genom översikt, installationssteg och motivering av konfigurationsval, med målet att skapa en reproducerbar och strukturerad lösning.

---

## Tillagd i efterhand – Terraform, Github Repository

Eftersom projektet handlar om att skapa mindre produktionslik Kubernetes-baserad miljö med open-source verktyg hade jag ursprungligen brainstormat att använda Terraform för automatisering. Terraform har gått över till en business license och är därför inte opensource sen 2023, därför kommer OpenTofu användas för IaC. Eftersom Terraform fortfarande är industry standard är OpenTofu relevant eftersom kompatibiliteten är 95-100 %.

En GitHub repository kommer att skapas sidledes under projektets gång för att kunna bygga upp en portfölj och även förstärka filosofin om att skapa en reproducerbar miljö.

---

## Tillagd i efterhand 2.0

Eftersom min stationära PC hemma är en windows dator vill jag lösa så jag kan ssh eller arbeta från den här datorn. På grund av bekvämligheten. Projektet kommer fortfarande vara detsamma och göras på min Linux laptop där jag använder mig av KVM för projektet.

Enda skillnaden är att arbetet sker från min PC hemma som är stationary.
