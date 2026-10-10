# Źródła i status weryfikacji

## Dostępne źródła

- `input/BOM_i_polaczenia.xlsx`: oryginalny załącznik użytkownika. Arkusze:
  BOM PCBA, Mapa sygnałów, Poza PCB, Przeczytaj. To dane projektowe do sprawdzenia.
- `input/02_PROMPT_DLA_CODEX.md`: wymagania projektu; pozostałe wymienione MD/CSV
  nie zostały załączone. XLSX wykorzystano jako źródło BOM-u i połączeń.
- Lokalne biblioteki symboli i footprintów KiCad 9.0.2. Symbole skopiowano do
  biblioteki projektu; kopie i tablica pinów są dostępne bez łączenia z Internetem.
  Nie traktowano biblioteki KiCad jako niezależnej weryfikacji datasheet producenta.
- Pinout DRV8876 RGT: tylko XLSX. Symbol zawiera tymczasowy pad **EP**, nie przypisano
  numeru padu i footprintu bez dokumentacji. Wymagane porównanie TI.

## Źródła producentów do pobrania i sprawdzenia

Poniższe żądania zwróciły blokadę CONNECT 403 z proxy środowiska. Nie pobrano
ich zawartości, nie odczytano rewizji/stron i **nie uznano ich za zweryfikowane**:

- [TI DRV8876](https://www.ti.com/lit/ds/symlink/drv8876.pdf)
- [ST STM32G030C8](https://www.st.com/resource/en/datasheet/stm32g030c8.pdf)
- [Espressif ESP32-S3-WROOM-1/1U](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf)
- [Diodes AP63200/01/03/05](https://www.diodes.com/assets/Datasheets/AP63200-AP63201-AP63203-AP63205.pdf)
- [ST STLINK-V3MINIE / UM2910](https://www.st.com/resource/en/user_manual/um2910-stlinkv3minie-debuggerprogrammer-tiny-probe-for-stm32-microcontrollers-stmicroelectronics.pdf)
- [ST USBLC6-2](https://www.st.com/resource/en/datasheet/usblc6-2.pdf)
- [TI SN74LVC1G08](https://www.ti.com/lit/ds/symlink/sn74lvc1g08.pdf)
- [JLCPCB C1852100](https://jlcpcb.com/partdetail/C1852100)

Pozostałe adresy katalogowe JLCPCB przeniesiono z XLSX do kolumny `url`
w `reports/PART_VERIFICATION.csv`. Nie uzyskano potwierdzenia aktualnego stanu.
Rysunki mechaniczne JST PH, Samtec FTSH, USB-C i pozostałych elementów również
wymagają odczytu u producenta i porównania z faktycznie sprzedawanym MPN.

## Zapisane dodatki do domen

W szkicu ustawień środowiska zapisano: `www.ti.com`, `www.st.com`,
`www.espressif.com`, `docs.espressif.com`, `www.diodes.com`, `jlcpcb.com`,
`www.lcsc.com`, `datasheet.lcsc.com`, `www.jst-mfg.com`, `www.samtec.com`.
Zachowano istniejące presety pakietów/Git. Zapis szkicu nie zmienia automatycznie
polityki bieżącej maszyny i nie publikuje środowiska. Wymagane zapisanie zmian
w ustawieniach; ponowne próby dopiero po zastosowaniu zmian.

Nie wyłączano weryfikacji TLS, podpisów ani sum kontrolnych.
