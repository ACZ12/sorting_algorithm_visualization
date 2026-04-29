\# Sorting Visualizer – Algoritmus Vizualizációs és Oktató Program



Ez a projekt egy Python alapú asztali alkalmazás, amely interaktív módon mutatja be a legismertebb rendezési algoritmusok működését. A szoftver célja, hogy segítse az algoritmuselmélet megértését látványos vizualizációval és beépített videós magyarázatokkal.



\## 1. Rendszerarchitektúra és technológiai struktúra

Az alkalmazás \*\*Python 3.x\*\* nyelven íródott, moduláris felépítésű, különválasztva a grafikus megjelenítést a logikai számításoktól.



\* \*\*GUI Keretrendszer:\*\* `tkinter` – a natív ablakkezelésért és az adatok megjelenítéséért (Canvas).

\* \*\*Multithreading:\*\* `threading` könyvtár – biztosítja, hogy a rendezési algoritmus futása ne fagyassza le a felhasználói felületet, így a vizualizáció folyamatos marad.

\* \*\*Multimédia:\*\* `OpenCV` és `PIL` – a magyarázó videók valós idejű, képkockánkénti rendereléséhez az oktató ablakban.



\## 2. Szoftverlogika és folyamatok

A program eseményvezérelt. A felhasználói bemenet után a szoftver egy külön szálon indítja el a kiválasztott algoritmust, hogy a felület reszponzív maradjon.



\*\*A főbb folyamatok:\*\*

1\. \*\*Adatbevitel:\*\* Listagenerálás (elemszám megadásával) vagy manuális számsor rögzítése.

2\. \*\*Paraméterezés:\*\* A lépések közötti késleltetés beállítása milliszekundumban (ms).

3\. \*\*Módválasztás:\*\* A felhasználó választhat a vizualizáció indítása vagy az elméleti magyarázat megtekintése között.

4\. \*\*Mérés:\*\* A rendezés végén a `time.perf\_counter\_ns()` segítségével számított tiszta futási idő kijelzése.



\## 3. Implementált algoritmusok (11 típus)

A szoftver az alábbi algoritmusok működését és hatékonyságát képes demonstrálni:

\* Bubble Sort (Buborékrendezés)

\* Cocktail Sort (Koktélrendezés)

\* Counting Sort (Számláló rendezés)

\* Gnome Sort (Manórendezés)

\* Insertion Sort (Beszúró rendezés)

\* Merge Sort (Összefésülő rendezés)

\* Quick Sort (Gyorsrendezés)

\* Radix Sort (Számjegyes rendezés)

\* Randomized Quick Sort (Véletlenszerű gyorsrendezés)

\* Selection Sort (Kiválasztásos rendezés)

\* Shell Sort (Shell-rendezés)



\## 4. Felhasználói felület (GUI) felépítése



\### Vezérlés ablak 

\* \*\*Bemeneti szakasz:\*\* Itt adható meg a lista hossza vagy az egyéni számsor, illetve a lépésköz (ms). Itt lehet kiválasztani a használni kívánt algoritmust. Innen indítható a vizualizáció vagy a választott algoritmus magyarázata.



\### Vizualizáció ablak

\* \*\*Felső kijelző:\*\* Az eredeti, rendezetlen lista állandó megjelenítése, az elemek alatt a sorszámaikkal a könnyebb követhetőség érdekében.

\* \*\*Alsó vizualizációs terület:\*\* Itt fut maga a rendezés, szintén sorszámozott elemekkel.



\### Magyarázat ablak

\* \*\*Jobb oldal:\*\* Az adott algoritmus működését bemutató videós demonstráció.

\* \*\*Bal oldal:\*\* Az algoritmus elméleti hátterének, működési elvének és komplexitásának szöveges leírása.



\## 5. Mesterséges Intelligencia (AI) használata

A fejlesztés során a \*\*Gemini\*\* modellt a következő munkafolyamatokhoz vettem igénybe:

\* A `threading` és a `tkinter` közötti kommunikáció (szálbiztos GUI frissítés) optimalizálása.

\* Az OpenCV videólejátszási logika integrálása a grafikus felületbe.

\* A technikai dokumentáció szerkezetének kialakítása és a szakmai szövegek stilizálása.



\---

\*\*Készítette:\*\* Czene Ádám

\*\*Verseny:\*\* INFOPROG 2.0

