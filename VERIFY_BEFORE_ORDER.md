# Warunki przed layoutem i zamówieniem

**STATUS: DRAFT / HOLD. Nie zamawiać PCB ani PCBA z tego podglądu BOM-u.**

ERC = 0 błędów / 0 ostrzeżeń potwierdza spójność narysowanych połączeń i typów
pinów. Nie potwierdza numeracji obudów, katalogu montażowego ani bezpieczeństwa.
Schemat powstał z XLSX; inne pliki MD/CSV wymienione w poleceniu nie zostały dostarczone.

## Dokumentacja i numery pinów — wymagane

- [ ] Otworzyć aktualne karty producentów i porównać pin po pinie U1–U8, J1 i J2
  z `reports/PIN_NET_MAP.csv`. Zapisać wersję/revizję, stronę i wynik.
- [ ] **U3/U4 DRV8876RGTR, RGT/VQFN16:** potwierdzić WSZYSTKIE piny 1–16,
  nazwę/numery padu termicznego, połączenie EP/PGND/GND oraz land pattern.
  Symbol obecnie korzysta z mapy XLSX, a **EP jest placeholderem**. Oba footprinty
  są puste. Nie używać symbolu ani footprintu HTSSOP/PWP zamiast RGT.
- [ ] Potwierdzić PMODE high = PWM, IMODE Hi-Z = żądany tryb ograniczenia i
  latched OC; warunki resetowania błędu, nSLEEP i zachowanie mostków przy VM=0.
- [ ] **STM32G030C8T6:** pinout LQFP48, PA9/PA10 na 33/34, NC29/32,
  opcje remap, alternatywne funkcje TIM3 i I2C1, dostępność PB10–PB15.
  Zasilanie VDD/VBAT/VREF+, wymagane kondensatory i procedura start/reset.
- [ ] **ESP32-S3-WROOM-1-N8:** dokładna wersja bez PSRAM, piny modułu, EP,
  strapping GPIO0/3/45/46, UART na GPIO17/18, USB GPIO19/20, I2S GPIO4/5/6.
  Sprawdzić wymagania dla pinów strap pozostawionych bez zewnętrznych obwodów.
- [ ] **U5/U6:** potwierdzić IN/EN/SW/BST/FB/GND oraz stałe napięcia,
  dławiki, efektywną pojemność po DC bias, prądy ripple i nasycenia.
  Sprawdzić zapas napięcia wejścia U6 po spadku SS14, także przy USB-only.
- [ ] **STDC14 J2:** potwierdzić fizyczną orientację pin1, reserved1/2/9,
  VTref3, SWDIO4, SWCLK6, GND5/7/11 i NRST12 w dokumentacji ST oraz Samtec.
  Piny8/10/13/14 celowo nieużywane; sprawdzić opcjonalne funkcje.
- [ ] **J1/U7/U8:** pinout USB-C konkretnego producenta, USBLC6-2SC6 i
  SN74LVC1G08DBVR. Przegląd schematu ESD i dobór rezystorów USB 22 Ω.

## JLCPCB i footprinty — wymagane

`reports/PART_VERIFICATION.csv` podaje każdy kod LCSC i MPN z XLSX.
**Liczba części niezależnie potwierdzonych w katalogu JLCPCB: 0.**
Każde oznaczenie w XLSX „Zweryfikowano” jest deklaracją źródła, nie wynikiem
naszego odczytu katalogu. Polityka sieciowa odrzuciła wymagane żądania HTTPS.

- [ ] Sprawdzić zgodność MPN/kodu/obudowy wszystkich 83 elementów oraz rzeczywistą
  możliwość montażu JLCPCB, stock, Basic/Extended, minimum i zamienniki.
- [ ] Uzupełnić **puste footprinty**: C1/C19/C20, J2/J3/J4/J5, L1, U3/U4.
  Przyczyna: brak zweryfikowanego rysunku padów. Nie zastępować na podstawie nazwy obudowy.
- [ ] Potwierdzić pozostałe footprinty kandydatów: rozmiar, pitch, pad numbers,
  polaryzację diod/LED/kondensatorów i tolerancje produkcyjne.
- [ ] **J1 TYPE-C-31-M-12 ma kotwy THT.** Potwierdzić proces montażu mieszany
  JLCPCB albo wybrać i zweryfikować inne gniazdo w osobnej korekcie schematu/BOM.
  Obecny wybór nie spełnia literalnego wymagania samych elementów SMT.
- [ ] **J3–J5 KF2024R-2.54-2P:** potwierdzić rzeczywisty typ złącza, prąd,
  footprint, funkcję blokowania przewodu oraz dostępność pasujących gotowych wiązek.
- [ ] J6–J15 JST PH: potwierdzić kolejność fizycznych pinów przy patrzeniu od
  strony wtyku i zgodność przewodów. Nie zakładać, że wszystkie gotowe moduły
  VL53L0X/INMP441 mają tę samą kolejność pinów.

## Napędy i zasilanie — wymagane pomiary / decyzje

- [ ] Model obu siłowników 12 V, długość po złożeniu < dostępnej przestrzeni
  ok. 300 mm, skok ok. 100 mm, siła, prędkość, duty cycle i krańcówki wewnętrzne.
- [ ] Zmierzyć prąd nominalny, rozruchowy i przy zablokowaniu w najgorszym
  obciążeniu obu szuflad. Z tego wyznaczyć dopuszczalny sterownik, limit i termikę.
- [ ] **VREF tylko wstępne:** 6.8 kΩ górny / 10 kΩ dolny = ok. 1.964 V przy 3.3 V.
  IPROPI ma 2.49 kΩ do GND. Prąd silnika zależy od współczynnika sense i tolerancji
  DRV8876; nie przyjmować automatycznie 0.79 A ani 2.49 V/A z tekstu XLSX.
  Sprawdzić zakres ADC przy największym prądzie i klamrowanie/ochronę wejść ADC.
- [ ] Wybrać certyfikowany zewnętrzny zasilacz 230 VAC -> 12 VDC.
  Na PCB nie ma 230 VAC. Określić moc, prąd impulsowy i reakcję na regenerację silników.
- [ ] Dobrać zewnętrzny bezpiecznik DC i gniazdo. Sprawdzić koordynację
  SS54/SMBJ15A/przewodów, reverse polarity, energię TVS i temperaturę D1.
- [ ] Sprawdzić SS14: spadki, prąd i moc przy pełnych szczytach ESP/Wi-Fi.
  Zmierzyć zasilanie tylko USB, tylko 12 V i obu źródeł jednocześnie.
- [ ] Potwierdzić, że USB programuje logikę/STM/ESP, a nie zasila VM/napędów.
  Netlista rozdziela te szyny; trzeba dodatkowo zbadać back-power przez piny
  sterowników i zachowanie sterownika bez VM.

## Bezpieczeństwo i czujniki — wymagane testy prototypu

Szereg NC E-STOP/kontakt1/kontakt2, bramka AND, ToF i pomiar prądu
**nie są certyfikowanym zabezpieczeniem BHP**.

- [ ] Testy NC: każde rozwarcie i przerwany przewód, reset STM/ESP, brak MCU,
  utrata 12 V/3V3, uruchamianie i błędy programu. Default OFF dzięki R7/R8/R18.
- [ ] Oceniać też zwarcie przewodu do +3V3, sklejenie styku, zwarcie bramki/mostka:
  prosty łańcuch NC nie diagnozuje wszystkich takich uszkodzeń.
- [ ] Zmierzyć drogę/czas zatrzymania i siłę docisku; nSLEEP wyłącza mostek,
  lecz nie gwarantuje natychmiastowego mechanicznego zatrzymania.
- [ ] Zmierzyć czasy filtracji C25 i opóźnienia układu; nie wydłużać bez analizy.
- [ ] Krańcówki J9–J12 są NC do GND, wymagają pull-up w firmware i debouncingu;
  ocenić podatność długich przewodów na EMI, ESD i pływanie przed inicjalizacją.
- [ ] VL53L0X: moduły o logice 3.3 V, XSHUT1/2, sekwencja zmiany identycznego adresu,
  konflikty z pull-upami w modułach, rzeczywista geometria i martwe strefy pomiaru.
- [ ] INMP441: 3.3 V, kabel 6-pin zgodny ze schematem, pin6 L/R=GND/left,
  jakość audio, zakłócenia napędów i zasilania.

## Layout — dopiero po akceptacji schematu

- [ ] Użytkownik zaakceptował schemat po zamknięciu krytycznych pinoutów i wartości.
- [ ] Szerokości miedzi i via zgodne z prądem, grubością miedzi i temperaturą;
  małe pętle prądu VM/OUT/PGND, właściwe termopady i thermal vias obu RGT.
- [ ] Kondensatory VM/bulk/VCP/CPH-CPL i odsprzęganie przy odpowiednich pinach.
- [ ] Buck: małe gorące pętle, krótki SW, właściwa masa/FB/BST, izolacja od RF/audio/ADC.
- [ ] Keepout anteny ESP32 we wszystkich wymaganych warstwach, położenie względem
  obudowy/metalowej szafki i przewodów, brak silników pod anteną.
- [ ] USB: para różnicowa, odniesienie masy, ESD przy gnieździe, krótkie stuby,
  kontrola impedancji i zweryfikowany montaż osłony.
- [ ] Fabryczny montaż wszystkich lutowanych elementów i komplet gotowych przewodów.
- [ ] Zaplanować nieobsadzane miedziane testpady: 12 V, VM, 5V_BUCK, 5V_OR,
  3V3, GND, UART, SWD, ENABLE, SAFETY, ADC. Ilość TP w XLSX = 0, więc brak ich w BOM.
- [ ] Przed produkcją ponowić ERC, DRC, przegląd BOM/CPL i kontrolę polaryzacji.

## Nieobsadzone i warunkowe pozycje

Nie ma fizycznych elementów zaznaczonych DNP. Wszystkie 83 elementy są w BOM,
ale ich katalog/montaż jest niepotwierdzony. Kondensatory elektrolityczne, L1,
złącza J2–J5 i oba sterowniki mają nieprzypisane footprinty; inne są kandydatami.
VREF, RIPROPI, rezystory USB, filtracja i pasywy zasilania są warunkowe po pomiarach.
Symbole `#PWR`/`#FLG` są niefizyczne i wyłączone z BOM. NC opisano w CSV.

Do odblokowania dokumentacji: zapisać zmiany sieci w ustawieniach środowiska
(domeny w `docs/SOURCES.md`), następnie sprawdzić ponownie żądania HTTPS.
Alternatywnie dostarczyć aktualne datasheety i rysunki producentów jako pliki.
Żadna zgoda na layout ani zamówienie nie została udzielona.
