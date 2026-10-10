#!/usr/bin/env python3
"""Check KiCad's exported connectivity, actual BOM, and design requirements.

This validates the editable schematic, not the unverified physical pinouts or
part availability. It deliberately does not certify an assembly-ready board.
"""
import csv
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
xml = ET.parse(ROOT / 'reports/netlist.xml').getroot()
actual = {(p.get('ref'), p.get('pin')): net.get('name')
          for net in xml.findall('nets/net') for p in net.findall('node')}
components = {c.get('ref'): c for c in xml.findall('components/comp')}
expected = json.loads((ROOT / 'reports/expected_connectivity.json').read_text())
connected = 0
unused = 0
for r in expected:
    if r['Reference'].startswith('#'):
        continue  # Power symbols and flags are nonphysical and omitted by KiCad.
    pin = (r['Reference'], r['Pin'])
    net = actual.get(pin)
    if r['Net'] == 'NC':
        assert net is None or net.startswith('unconnected-'), (pin, net)
        unused += 1
    else:
        assert net == r['Net'], (pin, r['Net'], net)
        connected += 1

# Independent, explicit checks for critical requested connections.
critical = {
    ('U1','33'): 'STM_TX_ESP_RX', ('U2','11'): 'STM_TX_ESP_RX',
    ('U1','34'): 'ESP_TX_STM_RX', ('U2','10'): 'ESP_TX_STM_RX',
    ('U1','35'): 'SWDIO', ('J2','4'): 'SWDIO',
    ('U1','36'): 'SWCLK', ('J2','6'): 'SWCLK',
    ('U1','10'): 'STM_NRST', ('J2','12'): 'STM_NRST',
    ('U1','4'): '+3V3', ('U1','5'): '+3V3', ('U1','6'): '+3V3', ('U1','7'): 'GND',
    ('U1','17'): 'M1_IN1', ('U1','18'): 'M1_IN2',
    ('U1','19'): 'M2_IN1', ('U1','20'): 'M2_IN2',
    ('U1','11'): 'M1_CURRENT_ADC', ('U1','12'): 'M2_CURRENT_ADC',
    ('U1','28'): 'MOTOR_MCU_ENABLE', ('U8','1'): 'MOTOR_MCU_ENABLE',
    ('U1','26'): 'SAFETY_LOOP_OK', ('U8','2'): 'SAFETY_LOOP_OK',
    ('U8','4'): 'MOTOR_DRV_ENABLE', ('U3','1'): 'MOTOR_DRV_ENABLE', ('U4','1'): 'MOTOR_DRV_ENABLE',
    ('U2','13'): 'USB_D_MINUS_MCU', ('U2','14'): 'USB_D_PLUS_MCU',
    ('U2','4'): 'I2S_BCLK', ('U2','5'): 'I2S_WS', ('U2','6'): 'I2S_DATA',
    ('J8','6'): 'GND', ('J6','5'): 'TOF1_XSHUT', ('J7','5'): 'TOF2_XSHUT',
    ('J13','1'): '+3V3', ('J13','2'): 'SAFETY_LINK_1', ('J14','1'): 'SAFETY_LINK_1',
    ('J14','2'): 'SAFETY_LINK_2', ('J15','1'): 'SAFETY_LINK_2', ('J15','2'): 'SAFETY_LOOP_OK',
    ('R7','1'): 'MOTOR_MCU_ENABLE', ('R7','2'): 'GND',
    ('R8','1'): 'SAFETY_LOOP_OK', ('R8','2'): 'GND',
    ('R18','1'): 'MOTOR_DRV_ENABLE', ('R18','2'): 'GND',
    ('D1','2'): 'VIN_12V_EXTERNAL', ('D1','1'): 'VM_MOTORS',
    ('D2','2'): '5V_BUCK', ('D2','1'): '5V_OR',
    ('D3','2'): 'USB_VBUS', ('D3','1'): '5V_OR',
    ('U5','3'): 'VM_MOTORS', ('U6','3'): '5V_OR',
    ('U5','1'): '5V_BUCK', ('U6','1'): '+3V3',
}
for pin, net in critical.items():
    assert actual.get(pin) == net, (pin, net, actual.get(pin))
for m, ref in [(1,'U3'),(2,'U4')]:
    for pin,net in {'9':'VM_MOTORS','14':'+3V3','15':f'M{m}_IN1','16':f'M{m}_IN2',
                    '3':f'M{m}_VREF','4':f'M{m}_CURRENT_ADC','6':f'MOTOR_{m}_A',
                    '8':f'MOTOR_{m}_B','7':'GND','13':'GND','EP':'GND'}.items():
        assert actual[(ref,pin)] == net, (ref,pin,net)
    assert actual.get((ref,'5'),'unconnected-').startswith('unconnected-')
    assert not components[ref].findtext('footprint'), 'RGT footprint may not be guessed'
for rail in ['USB_VBUS','5V_OR','+3V3','GND']:
    assert actual[('U3','9')] != rail and actual[('U4','9')] != rail
assert actual[('U5','5')] != actual[('U6','5')], 'Buck switch nodes shorted'
for ref in ['R19','R20','R14','R15','R16','R17','C21','C22','C23','C24']:
    assert actual[(ref,'1')] != actual[(ref,'2')], (ref,'shorted passive')
for ref in ['LED1','LED2']:
    assert actual[(ref,'1')] == 'GND', 'LED cathode polarity'

with (ROOT/'JLCPCB_BOM_preview.csv').open(encoding='utf-8-sig',newline='') as f:
    bom=list(csv.DictReader(f))
assert sum(int(row['Quantity']) for row in bom) == len(components) == 83
assert all(re.fullmatch(r'C\d+',row['LCSC']) for row in bom)
assert all(c.findtext("fields/field[@name='MPN']") for c in components.values())
erc = (ROOT/'ERC_report.txt').read_text()
assert 'ERC messages: 0  Errors 0  Warnings 0' in erc
json.loads((ROOT/'Szafka_Glosowa_STM32_ESP32.kicad_pro').read_text())

report = '\n'.join([
    'PASS: KiCad 9 exported all 83 physical components.',
    f'PASS: {connected} connected physical pins match documented net assignments.',
    f'PASS: {unused} intentionally unused physical pins have no assigned circuit net.',
    'PASS: UART cross, SWD, PWM, ADC, native USB, I2S and ToF connector pin maps.',
    'PASS: NC chain -> AND -> both nSLEEP; explicit three pulldowns.',
    'PASS: motor VM distinct from USB, logic and ground nets; correctly oriented OR diodes.',
    'PASS: independent buck switch nodes; VCP/CP and VREF passives not shorted.',
    'PASS: exported BOM Quantity total=83; all assembly references carry MPN and workbook LCSC.',
    'PASS: ERC errors=0, warnings=0, exclusions=0.',
    'LIMIT: checks are of digital schematic connectivity; no hardware test or manufacturer/catalog verification.',
    'HOLD: provisional RGT numbered pins from workbook; EP placeholder; missing/conditional footprints.',
    'HOLD: actuator current, supply/fuse, thermal/RF/USB/layout and prototype safety tests pending.',
]) + '\n'
(ROOT/'reports/CONNECTIVITY_VALIDATION.txt').write_text(report)
print(report)
