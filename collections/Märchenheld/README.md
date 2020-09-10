# Märchenbuch-Sammlung *"Märchenheld"*

Die Märchenbuch-Sammlung "[*Märchenheld*](https://maerchenheld-sammlung.de/)" umfasst 30 Märchen:

Name des Märchens | ID | Datei-Name | Datei-Grösse | Ausgabe | Erscheinungsdatum | Buchrücken-Nummer
----------------- | -- | ---------- | ------------ | ------- | ----------------- | -----------------
Rotkäppchen | 0001 | TMB01/T0001.smp | 14341199 | 1 | 19.08.2020 | 2
Die drei kleinen Schweinchen | 0002 | TMB01/T0002.smp | 13359938 | 2 | 09.09.2020 | 3
Pinocchio | 0003 | TMB01/T0003.smp | 14680898 | 3 | 16.09.2020 | 19
Der gestiefelte Kater | 0004 | TMB01/T0004.smp | 13266817 | 4 | 23.09.2020 | 10
Hänsel und Gretel | 0005 | TMB01/T0005.smp | 14689538 | 6 | 07.10.2020 | 6
Dornröschen | 0007 | TMB01/T0007.smp | 13048897 | 7 | 14.10.2020 | 1
Das hässliche Entlein | 0008 | TMB01/T0008.smp | 13953362 | ? | ? | ?
Die kleine Meerjungfrau | 0009 | TMB01/T0009.smp | 13638482 | ? | ? | ?
Das Dschungelbuch | 0010 | TMB01/T0010.smp | 12810001 | 8 | 21.10.2020 | 9
Schneewittchen und die sieben Zwerge | 0011 | TMB01/T0011.smp | 15498818 | 5 | 30.09.2020 | 4
Eine Weihnachtsgeschichte | 0012 | TMB01/T0012.smp | 14404562 | ? | ? | ?
Das tapfere Schneiderlein | 0013 | TMB01/T0013.smp | 13800722 | ? | ? | ?
Nussknacker und Mausekönig | 0014 | TMB01/T0014.smp | 14887298 | ? | ? | ?
Goldlöckchen und die drei Bären | 0015 | TMB01/T0015.smp | 11840401 | ? | ? | ?
Der Rattenfänger von Hameln | 0016 | TMB01/T0016.smp | 13463762 | ? | ? | ?
Aschenputtel | 0017 | TMB01/T0017.smp | 15716882 | ? | ? | ?
Des Kaisers neue Kleider | 0018 | TMB01/T0018.smp | 13571282 | ? | ? | ?
Alice im Wunderland | 0019 | TMB01/T0019.smp | 15007442 | ? | ? | ?
Der Zauberer von Oz | 0020 | TMB01/T0020.smp | 15441362 | ? | ? | ?
Die Bremer Stadtmusikanten | 0023 | TMB01/T0023.smp | 12473041 | ? | ? | ?
Die Prinzessin auf der Erbse | 0024 | TMB01/T0024.smp | 12120577 | ? | ? | ?
Robin Hood | 0025 | TMB01/T0025.smp | 13641218 | ? | ? | ?
Rapunzel | 0028 | TMB01/T0028.smp | 15946178 | ? | ? | ?
Gullivers Reisen | 0029 | TMB01/T0029.smp | 13191121 | ? | ? | ?
Der kleine Däumling | 0032 | TMB01/T0032.smp | 14790483 | ? | ? | ?
Die Schöne und das Biest | 0034 | TMB01/T0034.smp | 13926482 | ? | ? | ?
Aladdin und die Wunderlampe | 0038 | TMB01/T0038.smp | 14707778 | ? | ? | ?
Der Wolf und die sieben Geisslein | 0040 | TMB01/T0040.smp | 14278802 | ? | ? | ?
Die Schneekönigin | 0042 | TMB01/T0042.smp | 14848082 | ? | ? | ?
Der Schuster und die Wichtelmänner | 0044 | TMB01/T0044.smp | 13148881 | ? | ? | ?

## NFC-Tags

Zu jedem Märchen gibt es eine zugehörige Figur - wird diese auf den Audiocube gestellt, so wird das entsprechende Märchen abgespielt. Technisch funktioniert dies, indem jede Figur im Sockel unter der Fuss der Figur ein "*Mifare Classic 1k*"-NFC-Tag enthält, auf dem die ID des zugehörigen Märchens gespeichert ist.

Diese NFC-Tags können auch selbst hergestellt werden, z.B. wenn eine Figur einmal kaputt oder verloren gehen sollte. Im Order [nfc](nfc/) finden Sie für jedes Märchen eine `.mct`-Datei, die Sie mittels der kostenlosen Android-App "[MIFARE Classic Tool - MCT](https://play.google.com/store/apps/details?id=de.syss.MifareClassicTool)" auf ein geeignetes *"Mifare Classic 1k"*-NFC-Tag kopieren können, falls Sie ein NFC-fähiges Android-Smartphone besitzen. 

Gehen Sie dazu folgendermassen vor:

1. Kopieren Sie die `.mct`-Dateien aus dem [nfc](nfc/)-Order in das Verzeichnis `/sdcard/MifareClassicTool/dump-files/` ihres Android-Smartphones
2. Öffnen Sie die *MIFARE Classic Tool*-App
3. Wählen Sie "*Write Tag*"
4. Wählen Sie "*Write Dump (Clone)*"
5. Klicken Sie auf "*Select Dump*"
6. Wählen Sie die `.mct`-Datei des gewünschten Märchens
7. Klicken Sie auf "*Select Dump*"
8. Halten Sie das `*Mifare Classic 1k*`-NFC-Tag, das Sie beschreiben wollen, an die Stelle ihres Smartphones, an der sich der NFC-Reader befindet. Ein Ton sollte erklingen und "*New Tag found (UID:xxxxxxxx)*" eingeblendet werden
9. Belassen Sie das zu beschreibende NFC-Tag in dieser Position, und klicken Sie auf "*OK*"
10. Klicken Sie auf "*Select all*", dann auf "*Start mapping and write dump*"

## Speicherkarte

Die zugehörige Speicherkarte hat eine Kapazität von 512MB, die Audio-Dateien sind mit 48kHz Stereo @ 320kbit kodiert.