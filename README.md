# Szafka_Glosowa_STM32_ESP32

Rzeczywisty, edytowalny schemat KiCad **9.0.2**, przygotowany na podstawie
`docs/input/BOM_i_polaczenia.xlsx` i załączonego polecenia. Jest to **projekt
roboczy do przeglądu**, a nie projekt dopuszczony do zamówienia PCB/PCBA.

## Otwarcie

Rozpakuj cały ZIP do jednego katalogu. W KiCad 9 otwórz
`Szafka_Glosowa_STM32_ESP32.kicad_pro`, a następnie edytor schematów.
Na stronie głównej wejdź do arkusza przez jego prostokąt. Zachowaj pliki
potomne, `Szafka.kicad_sym` i `sym-lib-table` razem z projektem.
Standardowe biblioteki footprintów KiCad 9 są potrzebne do ich przeglądania.

Projekt ma stronę główną i pięć arkuszy:

1. `Power_12V_5V_3V3`: wejście 12 V DC, ochrona, dwa bucki, diodowe OR USB/5 V.
2. `STM32_Control_SWD`: MCU, zasilanie/odsprzęganie, STDC14, reset, LED.
3. `ESP32_USB_Audio`: moduł N8, USB-C, ESD, BOOT/RESET, złącze mikrofonu I2S.
4. `Motor_Drivers`: dwa DRV8876 RGT z mapy XLSX, IPROPI, VREF, charge pump.
5. `Safety_Sensors_Connectors`: szereg NC, bramka AND, krańcówki i ToF.

Połączenia między stronami wykorzystują etykiety globalne o jednakowych nazwach.
Wszystkie referencje BOM-u mają pola `MPN` i `LCSC`. Symbole zasilania/flag nie
są fizycznymi pozycjami BOM-u. Nie wygenerowano PCB, Gerberów ani CPL.

## Co sprawdzono

KiCad wczytał projekt i wyeksportował sześciostronicowy PDF, BOM oraz netlistę.
ERC przeprowadzono z wszystkimi poziomami kontroli i kodem błędu przy naruszeniu:
**0 błędów, 0 ostrzeżeń; bez wyłączeń ERC i bez markerów `no_erc`.**

Kontrola eksportowanej netlisty sprawdziła 83 fizyczne elementy, 274 połączone
piny i 59 zamierzonych niepodłączonych pinów. Dodatkowo sprawdzono UART cross,
SWD, PWM/ADC, USB, I2S, ToF, szereg NC, bramkę AND i oddzielne sieci USB/napędów.
To są kontrole schematu; nie wykonano pomiarów sprzętu ani symulacji siłowników.

## Co pozostaje otwarte

**Nie potwierdzono niezależnie żadnego wpisu JLCPCB.** Kody i MPN przeniesiono
z XLSX; deklaracje „Zweryfikowano” w arkuszu nie są naszym potwierdzeniem.
Dostęp HTTPS do kart producentów i katalogów został zablokowany przez politykę
sieci środowiska. Lista potrzebnych domen jest zapisana w szkicu ustawień.

Najważniejsze ograniczenia: pinout i footprint RGT/EP, dokładne footprinty
J2–J5, L1 i kondensatorów elektrolitycznych; montaż mieszany USB-C; prąd i model
siłowników; VREF/IPROPI; zasilacz/bezpiecznik; termika; EMC/ESD; testy prototypowego
łańcucha NC. Szczegóły i warunki zamknięcia: `VERIFY_BEFORE_ORDER.md`.

## Pliki wynikowe

- `Szafka_Glosowa_STM32_ESP32.kicad_pro`, plik główny `.kicad_sch` i pięć potomnych `.kicad_sch`.
- `Szafka.kicad_sym`, `sym-lib-table`: przenośna biblioteka symboli projektu.
- `Szafka_Glosowa_STM32_ESP32.pdf`: rzeczywisty eksport schematu z KiCad.
- `ERC_report.txt`: wynik bieżącej kontroli ERC.
- `JLCPCB_BOM_preview.csv`: eksport BOM-u z KiCad; **podgląd, nie do zamówienia**.
- `reports/PIN_NET_MAP.csv`, `reports/netlist.xml`: piny i sieci.
- `reports/PART_VERIFICATION.csv`: status każdej części i brakujące footprinty.
- `reports/UNUSED_PINS.csv`: uzasadnienia markerów NC.
- `reports/CONNECTIVITY_VALIDATION.txt`: wynik dodatkowej walidacji.
- `CHANGELOG.md`, `VERIFY_BEFORE_ORDER.md`, `docs/SOURCES.md`: zmiany i otwarte kwestie.

## Powtórzenie kontroli

W zwykłym lokalnym KiCad nie potrzeba zmiany katalogów XDG. W środowisku chmurowym
z katalogiem użytkownika tylko do odczytu użyj:

```bash
mkdir -p /workspace/kicad-runtime/config /workspace/kicad-runtime/cache /workspace/kicad-runtime/data
export XDG_CONFIG_HOME=/workspace/kicad-runtime/config
export XDG_CACHE_HOME=/workspace/kicad-runtime/cache
export XDG_DATA_HOME=/workspace/kicad-runtime/data
cd /workspace/inznierka
kicad-cli sch erc Szafka_Glosowa_STM32_ESP32.kicad_sch --severity-all --exit-code-violations -o ERC_report.txt
kicad-cli sch export netlist Szafka_Glosowa_STM32_ESP32.kicad_sch --format kicadxml -o reports/netlist.xml
kicad-cli sch export bom Szafka_Glosowa_STM32_ESP32.kicad_sch --fields 'Reference,${QUANTITY},Value,Footprint,LCSC' --labels 'Reference,Quantity,Value,Footprint,LCSC' --group-by 'Value,Footprint,LCSC,MPN' --exclude-dnp -o JLCPCB_BOM_preview.csv
kicad-cli sch export pdf Szafka_Glosowa_STM32_ESP32.kicad_sch -o Szafka_Glosowa_STM32_ESP32.pdf
python tools/validate_netlist.py
```

Polecenia KiCad uruchamiaj kolejno, aby nie współdzieliły blokady projektu.
Generator w `tools/generate_project.py` wymaga `openpyxl` i `sexpdata==1.0.2`.
W tej instancji: `PYTHONPATH=/workspace/kicad-runtime/python_deps python tools/generate_project.py`.
Generator odtwarza i nadpisuje pliki wynikowe: **nie uruchamiaj go na ręcznie
zmodyfikowanym projekcie bez zachowania swoich zmian**. Dalsze poprawki można
wprowadzać normalnie w edytorze KiCad. Zadania chmurowe są już izolowane;
używaj istniejącego checkoutu bez tworzenia dodatkowego worktree.
