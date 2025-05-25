# Transporta-logistikas-planosanas-metozu-izpete-nemot-vera-nenoteiktibas-un-riska-apstaklu-aspektus
Šis repozitorijs ir izveidots manam bakalaura darbam "Transporta loģistikas plānošanas metožu izpēte nenoteiktības un riska apstākļos" ietvaros.

## Saturs

Repozitorijā iekļautas četru klasisku maršrutēšanas algoritmu realizācijas, kurus izmanto sūtījumu piegādes plānošanai no viena noliktavas punkta uz pakomātiem pilsētā:

1. **Tuvākā kaimiņa algoritms (nearest_neighbor.py)**
2. **Ietaupījumu algoritms (savings.py)**
3. **Ievietošanas metode (insertion.py)**
4. **Slaucīšanas algoritms (sweep.py)**

Katrs algoritms ir ieviests atsevišķā `.py` failā. Skripti aprēķina fiksētus piegādes maršrutus, kas tiek izmantoti loģistikas sistēmas modelēšanā.

Repozitorijā pieejams arī **Excel fails**, kurā atrodas klientu (pakomātu) koordinātes.

## Mērķis

Šī koda mērķis ir parādīt, kā darbojas dažādas maršrutēšanas metodes reālai pilsētas loģistikai pietuvinātos apstākļos, un salīdzināt to efektivitāti, veicot modelēšanu "AnyLogistix" vidē ar riskiem un nenoteiktību (kavēšanās, sastrēgumi, negadījumi u.c.).

## Lietošana

1. Ja nepieciešams, instalējiet visu repozitorijas saturu.
2. Palaidiet jebkuru no `.py` failiem, lai iegūtu attiecīgā algoritma maršrutus.(excel failam jābūt vienā mapē)
3. Maršrutus izmantot analīzei AnyLogistix vidē.
