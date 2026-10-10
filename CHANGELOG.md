# Zmiany względem załączonego BOM-u i mapy

## Wersja robocza 0.1

- Utworzono pliki KiCad 9, stronę główną i pięć arkuszy. Wszystkie 81 fizycznych
  pozycji źródłowego BOM-u uwzględniono bez duplikowania referencji.
- Dodano **R18 10 kΩ** (`RC0603FR-0710KL`, kod z XLSX `C98220`): jawny pulldown
  wspólnego sygnału `MOTOR_DRV_ENABLE/nSLEEP`. Nie zastępuje R7 i R8.
- Dodano **C28 100 nF** (`CC0603KRX7R9BB104`, kod z XLSX `C14663`): odsprzęganie
  zasilania bramki U8. Łącznie projekt ma 83 fizyczne części.
- Rozróżniono numery GPIO od fizycznych numerów obudowy. Według zainstalowanego
  symbolu STM32G030C8Tx: PA9/PA11 = **33**, PA10/PA12 = **34**, piny **29/32 NC**,
  VBAT/VREF+/VDD/VSS = **4/5/6/7**, NRST = **10**. Nie traktowano nazw PA9/PA10
  jako numerów nóżek. Weryfikacja producenta i remap/AF nadal otwarte.
- Według symbolu ESP32-S3-WROOM-1: GPIO17/18 = fizyczne **10/11**,
  GPIO19/20 (USB) = **13/14**, EN = **3**, GPIO0 = **27**,
  zasilanie 3V3 = **2**, GND = **1/40/41**. Doprowadzono GND również do EP modułu.
- USB D+/D− mają wspólne pary A6/B6 i A7/B7; SBU1/SBU2 są zamierzenie NC.
  U7 chroni stronę złącza, R19/R20 rozdzielają ją od strony modułu ESP.
- USART STM TX/ESP RX i ESP TX/STM RX mają wspólne, skrzyżowane sieci;
  nie użyto rozłącznych nazw `ESP_UART_TX` i `MCU_RX_ESP_TX` dla tego samego przewodu.
- Pin 6 złącza mikrofonu (L/R) połączono z GND zgodnie z dozwolonym w XLSX
  wariantem kanału lewego. Wymaga potwierdzenia pinoutu rzeczywistego modułu/kabla.
- Rozdzielono `VIN_12V_EXTERNAL`, `VM_MOTORS`, `5V_BUCK`, `USB_VBUS`, `5V_OR`
  i `+3V3`. D2/D3: anody do źródeł, katody do 5V_OR. D1: anoda do wejścia 12 V.
- AP63203/AP63205 otrzymały zgodne z biblioteką numery: FB1, EN2, IN3, GND4,
  SW5, BST6. FB podłączono za dławikiem, a kondensator BST między BST i SW.
  Dobór wartości i parametry układów nadal wymagają datasheet.
- Symbole DRV8876 RGT oparto **wyłącznie na tabeli XLSX**; nie przenoszono
  symbolu DRV8876/DRV8870 z innej obudowy. Nie zgadywano numeru padu termicznego:
  otrzymał tymczasowy identyfikator **EP** i GND. Footprint pozostawiono pusty.
  Przed PCB należy potwierdzić wszystkie piny i zastąpić EP numerem właściwego padu.
- Nie przypisano pozornie zgodnych footprintów do J2–J5, U3/U4, L1 i C1/C19/C20
  bez dostępnej dokumentacji. Pozostałe footprinty są kandydatami z bibliotek.
- Footprint `TYPE-C-31-M-12` zawiera styki SMT i kotwy ekranu THT. To otwarta
  niezgodność z wymaganiem pełnego SMD, a nie potwierdzenie montażu jednostronnego.
- Użyto uzasadnionych flag zasilania dla zewnętrznych źródeł i szyn po pasywnych
  diodach/dławikach; nie dodawano ich na ADC ani sygnałach sterowania.
- Markery NC służą wyłącznie nieużywanym GPIO, opcjonalnym sygnałom STDC14,
  SBU, pinom NC STM i celowo pływającemu IMODE. Uzasadnienia zapisano w CSV.
  Brak markerów `no_erc`, wyłączeń ERC i wyłączania klas błędów.

Nie zmieniano oryginalnego XLSX ani polecenia. Nie potwierdzono wpisów JLCPCB,
pinoutów producentów, działania sprzętowego ani gotowości do zamówienia.
