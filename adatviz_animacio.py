from tkinter import *
from random import randint
import cv2
from time import *
from threading import Thread
from tkinter import Tk, Canvas, Toplevel, Button,messagebox
from PIL import Image, ImageTk






root = Tk()
fs = True
frame = Frame(root, bg="lightblue")
frame.pack()
arr = []
current_sorting = None
ent_lab = Label(frame, text="Adja meg a lista darabszámát vagy egy vesszővel elválasztott egyéni listát!")
ent_lab.pack()
ent = Entry(frame)
ent.pack()
ent_lab2 = Label(frame, text="Lépések közti várakozási idő (ms):")
ent_lab2.pack()
ent2 = Entry(frame)
ent2.pack()



#lista, ablak inicializalasa, teljeskepernyo
def start_sorting():
    update_array()
start_button = Button(frame, text="Rendezés", command=start_sorting)
start_button.pack()

def update_array():
    global arr, fs
    sorting_window = Toplevel(root)
    fs = False
    sorting_window.attributes("-fullscreen", fs)
    sorting_window.resizable(True, True)
    window_width = min(1600, root.winfo_screenwidth() - 50)
    window_height = min(900, root.winfo_screenheight() - 100)
    sorting_window.geometry(f"{window_width}x{window_height}")
    canvas = Canvas(sorting_window, bg="grey", width=window_width, height=window_height)
    canvas.pack(fill="both", expand=True)
    sorting_window.update_idletasks()
    canvas.delete("szamok")
    canvas.bind('<Configure>', lambda event: alsovonal(arr, canvas))

    def fullscreen(event=None):
        global fs
        fs = not fs
        sorting_window.attributes('-fullscreen', fs)

    sorting_window.bind('<Escape>', fullscreen)

    num_elements = ent.get().strip()
    speed = int(ent2.get().strip()) if ent2.get() else 100

    if not num_elements:
        messagebox.showerror("Hiba", "Érvénytelen bemenet.")
        return
    if "," in num_elements:
        try:
            original_arr = list(map(int, num_elements.split(",")))
            arr = original_arr.copy()
        except ValueError:
            messagebox.showerror("Hiba", "Érvénytelen bemenet.")
            return
    else:
        try:
            num_elements = int(num_elements)
            original_arr = [randint(0, 100) for _ in range(num_elements)]
            arr = original_arr.copy()
        except ValueError:
            messagebox.showerror("Hiba", "Érvénytelen bemenet.")
            return

    canvas.delete("Palcak")
    alsovonal(arr, canvas)

    selected_algorithm = selected_option.get()
    algoritmus = VIZ_Algoritmusok(selected_algorithm, arr, speed, canvas)

    algoritmus.reset_sorting()
    vizsort=Thread(target=algoritmus.sort)
    vizsort.start()



#algoritmus választása
selected_option = StringVar(frame)
selected_option.set("Bubble sort")
options = [
    "Bubble sort", 
    "Insertion sort", 
    "Selection sort", 
    "Merge sort", 
    "Shell sort",
    "Cocktail shaker sort", 
    "Counting sort", 
    "Gnome sort", 
    "Quick sort", 
    "Random quick sort", 
    "Radix sort"
]
option_menu = OptionMenu(frame, selected_option, *options)
option_menu.pack(side="left")




#magyarazat példányosítása funkció, gomb
def start_magy():
    magy=Magyarazat(selected_option.get())
    magy.display_video()

magybut=Button(frame,text="Magyarázat",command=start_magy)
magybut.pack(side="right")


# Ablak méretének beállítása a leggyakoribb felbontásra (1920x1080)
def set_window_size(window):
    width = 1920
    height = 1080
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Ha a monitor kisebb, mint a célfelbontás, akkor a monitor méretét használjuk
    width = min(width, screen_width)
    height = min(height, screen_height)
    
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# A start_sorting hívásakor a fullscreen változót False-ra állítjuk az update_array-ben
fs = False 


def get_canvas_size(canvas, default_width=800, default_height=600):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    if width < 2:
        width = canvas.winfo_reqwidth() or default_width
    if height < 2:
        height = canvas.winfo_reqheight() or default_height
    return width, height


#canvasra torteno kirajzolás
def alsovonal(arr, canvas):
    canvas_width, canvas_height = get_canvas_size(canvas)
    if not arr:
        return
    canvas.delete("Szamok")
    bar_width = max((canvas_width - 50) / len(arr), 1)
    for i in range(len(arr)):
        tavy = (40 if (i % 2 == 0 or i == 0) else 15) if len(arr) > 150 else 15
        canvas.create_text(20 + i * bar_width, (canvas_height / 2) - 80 + tavy, text=str(i), tags="Szamok", fill="lightgreen", angle=90)
        canvas.create_text(20 + i * bar_width, canvas_height - 100 + tavy, text=str(i), tags="Szamok", fill="lightgreen", angle=90)

def rajzold_ki(arr, y, canvas, selected=[]):
    if not arr:
        return
    canvas_width, canvas_height = get_canvas_size(canvas)
    max_height = max(arr)
    bar_width = max((canvas_width - 50) / len(arr), 1)
    canvas.delete("palcak")
    available_height = canvas_height * 0.4

    for i in range(len(arr)):
        bar_height = (arr[i] / max_height) * available_height
        color = "red" if i in selected else "black"

        canvas.create_line(
            20 + i * bar_width, canvas_height - y,
            20 + i * bar_width, canvas_height - y - bar_height,
            fill=color,
            width=max(bar_width - 1, 1),
            tags="palcak" if y == 100 else "Palcak"
        )
        canvas.create_text(
            10 + i * bar_width + 15, canvas_height + 10 - bar_height - y,
            text=str(arr[i]),
            anchor="e",
            font=("Arial", 10),
            tags="palcak" if y == 100 else "Palcak",
            fill="yellow"
        )







#idozito osztaly, docstringek a magyarazo osztalynak
class IDO_Algoritmusok:
    def __init__(self, alg,t1,canvas):
        self.alg=alg
        self.t1=t1
        self.canvas=canvas
        
    def idomero(self,t1,alg):
        telj_label=Label(self.canvas,text=f"A(z) {alg} algoritmus {time()-t1:.6f} mp alatt rendezte a {len(arr)} elemü listát.")
        telj_label.place(x=30,y=20)
    
    def bubblesort(self,arr):
        """Bubble Sort\n\n
Működési elv:\n
            A Bubble Sort algoritmus az elemeket egymás után\n
            összehasonlítja, és ha azokat rossz sorrendben találja,\n
            megcseréli őket. Ezt az egész lista mentén ismétli,\n
            amíg nincs több csere.\n
            Az algoritmus végére a legnagyobb elem "felbuborékol"\n
            a megfelelő helyére.\n
            Bonyolultság: O(n²)\n
Példa:\n
            Kezdeti lista: [5, 3, 8, 4, 2]\n
            Első lépés: [3, 5, 4, 2, 8]\n
            Második lépés: [3, 4, 2, 5, 8]\n
            Harmadik lépés: [3, 2, 4, 5, 8]\n
            Negyedik lépés: [2, 3, 4, 5, 8] (rendezve)."""


        rend=False
        while not rend:
            rend=True
            for i in range(1,len(arr)-1):
                if arr[i-1]>arr[i]:
                    arr[i-1],arr[i]=arr[i],arr[i-1]
                    rend=False
        self.idomero(self.t1,"Bubble sort")

        
    def inssort(self,arr):
        """Insertion Sort\n\n
Működési elv:\n
            Az Insertion Sort algoritmus úgy működik,\n
            hogy egyesével "beilleszti" az elemeket a megfelelő helyükre\n
            a már rendezett részbe.\n
            Kezdetben az első elem rendezettnek tekinthető,\n
            majd minden további elemhez megkeresi a megfelelő helyet\n
            a rendezett részben, és ott beilleszti.\n
            Bonyolultság: O(n²)\n
Példa:\n
            Kezdeti lista: [5, 3, 8, 4, 2]\n
            Első lépés: [3, 5, 8, 4, 2]\n
            Második lépés: [3, 5, 8, 4, 2]\n
            Harmadik lépés: [3, 4, 5, 8, 2]\n
            Negyedik lépés: [2, 3, 4, 5, 8] (rendezve)."""

        for i in range(1,len(arr)):
            while arr[i-1]>arr[i] and i>0:
                arr[i-1],arr[i]=arr[i],arr[i-1]
                i-=1
        self.idomero(self.t1,"Insertion sort")

    def mergesort(self,arr):
        """Merge Sort\n\n
Működési elv:\n
            A Merge Sort egy oszd-meg-és-uralkodj típusú algoritmus,\n
            amely a listát kisebb részekre bontja, amíg egy elemre nem\n
            csökkennek. Ezután a részeket rendezetten összefésüli.\n
            Az algoritmus rekurziót használ az összeillesztés során.\n
            Bonyolultság: O(n log n)\n
Példa:\n
            Kezdeti lista: [5, 3, 8, 4, 2]\n
            Felosztás: [5, 3], [8, 4, 2]\n
            Részrendezés: [3, 5], [2, 4, 8]\n
            Összefésülés: [2, 3, 4, 5, 8] (rendezve)."""

        
        def merge_sort(arr):
            if len(arr) > 1:
                mid = len(arr) // 2
                left_half = arr[:mid]
                right_half = arr[mid:]

                merge_sort(left_half)  
                merge_sort(right_half)  

                i = j = k = 0
                while i < len(left_half) and j < len(right_half):
                    if left_half[i] < right_half[j]:
                        arr[k] = left_half[i]
                        i += 1
                    else:
                        arr[k] = right_half[j]
                        j += 1
                    k += 1

                while i < len(left_half):
                    arr[k] = left_half[i]
                    i += 1
                    k += 1

                while j < len(right_half):
                    arr[k] = right_half[j]
                    j += 1
                    k += 1

        merge_sort(arr)

        self.idomero(self.t1,"Merge sort")



    def selsort(self,arr):
        """Selection Sort\n\n
Működési elv:\n
            A Selection Sort algoritmus úgy működik,\n
            hogy a lista elemeit iteratívan rendezi. Minden lépésben\n
            megkeresi a legkisebb (vagy legnagyobb) elemet az aktuális\n
            rendezetlen részben, és kicseréli azt a rendezetlen rész első\n
            elemével. Ezután a rendezetlen rész egy elemmel kisebb lesz,\n
            és a folyamat ismétlődik, amíg a lista rendezett nem lesz.\n
            Bonyolultság: O(n²)\n
Példa:\n
            Kezdeti lista: [5, 3, 8, 4, 2]\n
            Első lépés: [2, 3, 8, 4, 5]\n
            Második lépés: [2, 3, 8, 4, 5]\n
            Harmadik lépés: [2, 3, 4, 8, 5]\n
            Negyedik lépés: [2, 3, 4, 5, 8] (rendezve)."""

        for i in range(len(arr)):
            cur_min_idx=i
            for j in range(i+1,len(arr)):
                if arr[j]<arr[cur_min_idx]:
                    cur_min_idx=j
                    arr[i],arr[cur_min_idx]=arr[cur_min_idx],arr[i]
        self.idomero(self.t1,"Selection sort")

    def gnome_sort(self,arr):
        """Gnome Sort\n\n
Működési elv:\n
            A Gnome Sort algoritmus hasonló a Bubble Sorthoz,\n
            de az elemeket egy "törpe" lépteti előre vagy hátra.\n
            Ha két egymást követő elem rossz sorrendben van,\n
            azokat megcseréli, majd egyet hátralép. Ha jó sorrendben\n
            vannak, előrelép. Az algoritmus addig folytatja,\n
            amíg végig nem ér a listán.\n
            Bonyolultság: O(n²)\n
Példa:\n
            Kezdeti lista: [5, 3, 8, 4, 2]\n
            Első lépés: [3, 5, 8, 4, 2]\n
            Második lépés: [3, 5, 8, 4, 2]\n
            Harmadik lépés: [3, 5, 4, 8, 2]\n
            Negyedik lépés: [3, 4, 5, 8, 2]\n
            Végső lépés: [2, 3, 4, 5, 8] (rendezve)."""

        index = 0
        while index < len(arr):
            if index == 0 or arr[index] >= arr[index - 1]:
                index += 1
            else:
                arr[index], arr[index - 1] = arr[index - 1], arr[index]
                index -= 1
        self.idomero(self.t1,"Gnome sort")
    
    def quick_sort(self, arr):
        """Quick Sort\n\n
Működési elv:\n
            A Quick Sort egy rekurzív algoritmus,\n
            amely kiválaszt egy úgynevezett pivot elemet,\n
            és a listát a pivot köré rendezi: kisebb elemek balra,\n
            nagyobbak jobbra kerülnek.\n
            Ezután rekurzívan rendezi a bal és jobb részt is.\n
            Bonyolultság: Átlagosan O(n log n)\n
Példa:\n
            Kezdeti lista: [5, 3, 8, 4, 2]\n
            Pivot kiválasztása: 5\n
            Bal oldal: [3, 4, 2], Jobb oldal: [8]\n
            Rendezés után: [2, 3, 4, 5, 8] (rendezve)."""

        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]

        self.idomero(self.t1,"Quick sort")

    def randomized_quick_sort(self,arr):
        """Randomized Quick Sort\n\n
Működési elv:\n
            A Randomized Quick Sort a hagyományos Quick Sorthoz hasonló,\n
            de a pivot elemet véletlenszerűen választja ki, nem pedig\n
            meghatározott hely alapján. Ez csökkenti az esélyét annak,\n
            hogy a legrosszabb eset forduljon elő.\n
            Ezután ugyanúgy rendezi a listát a pivot köré,\n
            és rekurzívan dolgozik a bal és jobb részhalmazokon.\n
            Bonyolultság: Átlagosan O(n log n)\n
Példa:\n
            Kezdeti lista: [5, 3, 8, 4, 2]\n
            Véletlenszerű pivot: 3\n
            Bal oldal: [2], Jobb oldal: [5, 8, 4]\n
            Rendezés után: [2, 3, 4, 5, 8] (rendezve)."""

        if len(arr) <= 1:
            return arr
        pivot = arr[randint(0, len(arr) - 1)]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]

        self.idomero(self.t1,"Random quick sort")

    def radix_sort(self,arr):
        """Radix Sort\n\n
Működési elv:\n
            A Radix Sort az elemeket digitális jelentőség szerint rendezi,\n
            kezdve a legkisebb helyiértékkel (egyestől, tízesig stb.).\n
            Az algoritmus stabil rendezést használ minden helyiértéken.\n
            Bonyolultság: O(nk), ahol k az elemek maximális számjegyeinek száma.\n
Példa:\n
            Kezdeti lista: [170, 45, 75, 90, 802]\n
            Egyes helyiérték: [802, 170, 90, 75, 45]\n
            Tízes helyiérték: [802, 45, 75, 90, 170]\n
            Százas helyiérték: [45, 75, 90, 170, 802] (rendezve)."""
        max_element = max(arr)
        exp = 1
        while max_element // exp > 0:
            self.counting_sort_for_radix(arr, exp)
            exp *= 10
        self.idomero(self.t1,"Radix sort")

    def counting_sort_for_radix(self,arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10
        for i in arr:
            index = (i // exp) % 10
            count[index] += 1
        for i in range(1, 10):
            count[i] += count[i - 1]
        for i in reversed(arr):
            index = (i // exp) % 10
            output[count[index] - 1] = i
            count[index] -= 1
        for i in range(n):
            arr[i] = output[i]

    def counting_sort(self,arr):
        """Counting Sort\n\n
Működési elv:\n
            A Counting Sort algoritmus a számok gyakoriságát számolja meg, majd\n
            azokat a számsorozat megfelelő helyére helyezi. Először is megszámolja\n
            az összes előforduló számot, majd ezt a gyakoriságot felhasználva hozza\n
            létre a rendezett listát. A Counting Sort egy nem összehasonlító algoritmus,\n
            így nagyon gyors lehet, ha a bemenetek kis tartományban helyezkednek el.\n
            Bonyolultság: O(n + k), ahol n a lista hossza, k pedig a számok közötti különbség.\n
Példa:\n
            Kezdeti lista: [5, 3, 8, 4, 2]\n
            Gyakoriság számítás: [0, 0, 1, 1, 1, 1, 0, 0, 1]\n
            Rendezett lista: [2, 3, 4, 5, 8]"""

        max_val = max(arr)
        count = [0] * (max_val + 1)
        for num in arr:
            count[num] += 1
        output = []
        for i, freq in enumerate(count):
            output.extend([i] * freq)

        self.idomero(self.t1,"Counting sort")

    def shell_sort(self,arr):
        """Shell Sort\n\n
Működési elv:\n
            A Shell Sort az Insertion Sort általánosítása,\n
            amely kezdetben távoli elemeket hasonlít össze,\n
            majd fokozatosan csökkenti az összehasonlított elemek közti távolságot.\n
            Az algoritmus hossza csökken, ahogy a lépések mérete csökken,\n
            amíg az utolsó lépés során teljes Insertion Sortot hajt végre.\n
            Bonyolultság: Általában O(n log n), de a pontos érték a lépések\n
            kiválasztásától függ.\n
Példa:\n
            Kezdeti lista: [5, 3, 8, 4, 2]\n
            Első lépés (gap=3): [5, 3, 2, 4, 8]\n
            Második lépés (gap=1): [2, 3, 4, 5, 8] (rendezve)."""

        gap = len(arr) // 2
        while gap > 0:
            for i in range(gap, len(arr)):
                temp = arr[i]
                j = i
                while j >= gap and arr[j - gap] > temp:
                    arr[j] = arr[j - gap]
                    j -= gap
                arr[j] = temp
            gap //= 2

        self.idomero(self.t1,"Shell sort")

    def cocktail_shaker_sort(self,arr):
        """Cocktail Shaker Sort\n\n
Működési elv:\n
            A Cocktail Shaker Sort a Bubble Sort egy variációja,\n
            amely oda-vissza végigmegy a listán. Az első menetben\n
            az elemeket növekvő sorrendbe cseréli, a második menetben\n
            pedig csökkenő sorrendbe. Ezáltal a nagyobb és kisebb elemek\n
            is fokozatosan a megfelelő helyükre kerülnek.\n
            Bonyolultság: O(n²)\n
Példa:\n
            Kezdeti lista: [5, 3, 8, 4, 2]\n
            Első menet: [3, 5, 4, 2, 8]\n
            Második menet: [3, 2, 4, 5, 8]\n
            Harmadik menet: [2, 3, 4, 5, 8] (rendezve)."""
        n = len(arr)
        swapped = True
        start = 0
        end = n - 1
        while swapped:
            swapped = False
            for i in range(start, end):
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    swapped = True
            if not swapped:
                break
            swapped = False
            end -= 1
            for i in range(end - 1, start - 1, -1):
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    swapped = True
            start += 1

        self.idomero(self.t1,"Coctail shaker sort")







#lista VIZUALIS rendezésére szolgáló osztály
class VIZ_Algoritmusok:
    def __init__(self, alg, arr, speed, canvas):
        self.alg = alg
        self.arr = arr
        self.speed = speed
        self.canvas = canvas
        self.sorting_fut = False

    def reset_sorting(self):
        self.sorting_fut = False
        self.canvas.delete("palcak")
        self.canvas.delete("szamok")
        rajzold_ki(self.arr, y=530, canvas=self.canvas)

    def sort(self):
        if self.sorting_fut:
            return
        self.sorting_fut = True
        self.t1=time()

        ido_peldanyositas=IDO_Algoritmusok(self.arr,self.t1,self.canvas)


        if self.alg == "Bubble sort":
            idosort=Thread(target=ido_peldanyositas.bubblesort(self.arr.copy()))
            idosort.start()
            self.bubsort(self.arr, self.speed)
        elif self.alg == "Insertion sort":
            idosort=Thread(target=ido_peldanyositas.inssort(self.arr.copy()))
            idosort.start()
            self.inssort(self.arr, self.speed)
        elif self.alg == "Selection sort":
            idosort=Thread(target=ido_peldanyositas.selsort(self.arr.copy()))
            idosort.start()
            self.selsort(self.arr, self.speed)
        elif self.alg == "Merge sort":
            idosort=Thread(target=ido_peldanyositas.mergesort(self.arr.copy()))
            idosort.start()
            self.mergesort(self.arr, self.speed)
        elif self.alg == "Shell sort":
            idosort=Thread(target=ido_peldanyositas.shell_sort(self.arr.copy()))
            idosort.start()
            self.shellsort(self.arr, self.speed)
        elif self.alg == "Cocktail shaker sort":
            idosort=Thread(target=ido_peldanyositas.cocktail_shaker_sort(self.arr.copy()))
            idosort.start()
            self.coctailsort(self.arr, self.speed)
        elif self.alg == "Counting sort":
            idosort=Thread(target=ido_peldanyositas.counting_sort(self.arr.copy()))
            idosort.start()
            self.countingsort(self.arr, self.speed)
        elif self.alg == "Gnome sort":
            idosort=Thread(target=ido_peldanyositas.gnome_sort(self.arr.copy()))
            idosort.start()
            self.gnomesort(self.arr, self.speed)
        elif self.alg == "Quick sort":
            idosort=Thread(target=ido_peldanyositas.quick_sort(self.arr.copy()))
            idosort.start()
            self.quicksort(self.arr, self.speed)
        elif self.alg == "Radix sort":
            idosort=Thread(target=ido_peldanyositas.radix_sort(self.arr.copy()))
            idosort.start()
            self.radixsort(self.arr, self.speed)
        elif self.alg == "Random quick sort":
            idosort=Thread(target=ido_peldanyositas.randomized_quick_sort(self.arr.copy()))
            idosort.start()
            self.random_quicksort(self.arr, self.speed)
        else:
            raise ValueError("Ilyen algoritmust nem ismerek.")

    def bubsort(self, arr, speed):
        n = len(arr)
        for i in range(n - 1):
            for j in range(n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    rajzold_ki(arr, y=100, canvas=self.canvas, selected=[j, j + 1])
                    root.update()
                    root.after(int(speed))

    def inssort(self, arr, speed):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                rajzold_ki(arr, y=100, canvas=self.canvas, selected=[j, j + 1])
                root.update()
                root.after(int(speed))
                j -= 1
            arr[j + 1] = key

    def selsort(self, arr, speed):
        for i in range(len(arr)):
            min_idx = i
            for j in range(i + 1, len(arr)):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            rajzold_ki(arr, y=100, canvas=self.canvas, selected=[i, min_idx])
            root.update()
            root.after(int(speed))

    def mergesort(self, arr, speed):
        def merge(left, right):
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result

        width = 1
        n = len(arr)
        while width < n:
            for i in range(0, n, 2 * width):
                left = arr[i:i + width]
                right = arr[i + width:i + 2 * width]
                merged = merge(left, right)
                arr[i:i + len(merged)] = merged
                rajzold_ki(arr, y=100, canvas=self.canvas)
                root.update()
                root.after(int(speed))
            width *= 2

    def shellsort(self, arr, speed):
        n = len(arr)
        gap = n // 2
        while gap > 0:
            for i in range(gap, n):
                temp = arr[i]
                j = i
                while j >= gap and arr[j - gap] > temp:
                    arr[j] = arr[j - gap]
                    rajzold_ki(arr, y=100, canvas=self.canvas, selected=[j, j - gap])
                    root.update()
                    root.after(int(speed))
                    j -= gap
                arr[j] = temp
            gap //= 2

    def coctailsort(self, arr, speed):
        start = 0
        end = len(arr) - 1
        while start <= end:
            swapped = False
            for i in range(start, end):
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    swapped = True
                    rajzold_ki(arr, y=100, canvas=self.canvas, selected=[i, i + 1])
                    root.update()
                    root.after(int(speed))
            end -= 1
            for i in range(end, start, -1):
                if arr[i] < arr[i - 1]:
                    arr[i], arr[i - 1] = arr[i - 1], arr[i]
                    swapped = True
                    rajzold_ki(arr, y=100, canvas=self.canvas, selected=[i, i - 1])
                    root.update()
                    root.after(int(speed))
            start += 1
            if not swapped:
                break

    def countingsort(self, arr, speed):
        max_val = max(arr) if arr else 0
        count = [0] * (max_val + 1)
        for num in arr:
            count[num] += 1
        idx = 0
        for num, freq in enumerate(count):
            while freq > 0:
                arr[idx] = num
                idx += 1
                freq -= 1
                rajzold_ki(arr, y=100, canvas=self.canvas)
                root.update()
                root.after(int(speed))

    def gnomesort(self, arr, speed):
        index = 0
        while index < len(arr):
            if index == 0 or arr[index] >= arr[index - 1]:
                index += 1
            else:
                arr[index], arr[index - 1] = arr[index - 1], arr[index]
                rajzold_ki(arr, y=100, canvas=self.canvas, selected=[index, index - 1])
                root.update()
                root.after(int(speed))
                index -= 1

    def quicksort(self, arr, speed):
        stack = [(0, len(arr) - 1)]
        while stack:
            low, high = stack.pop()
            if low < high:
                pivot = arr[high]
                i = low - 1
                for j in range(low, high):
                    if arr[j] < pivot:
                        i += 1
                        arr[i], arr[j] = arr[j], arr[i]
                        rajzold_ki(arr, y=100, canvas=self.canvas, selected=[i, j])
                        root.update()
                        root.after(int(speed))
                arr[i + 1], arr[high] = arr[high], arr[i + 1]
                stack.append((low, i))
                stack.append((i + 2, high))

    def random_quicksort(self, arr, speed):
    
        stack = [(0, len(arr) - 1)]
        while stack:
            low, high = stack.pop()
            if low < high:
                pivot_idx = randint(low, high)
                arr[high], arr[pivot_idx] = arr[pivot_idx], arr[high]  
                pivot = arr[high]
                i = low - 1
                for j in range(low, high):
                    if arr[j] < pivot:
                        i += 1
                        arr[i], arr[j] = arr[j], arr[i]
                        rajzold_ki(arr, y=100, canvas=self.canvas, selected=[i, j])
                        root.update()
                        root.after(int(speed))
                arr[i + 1], arr[high] = arr[high], arr[i + 1]  
                rajzold_ki(arr, y=100, canvas=self.canvas, selected=[i + 1])
                root.update()
                root.after(int(speed))
                stack.append((low, i))
                stack.append((i + 2, high))

    def radixsort(self, arr, speed):
        if not arr:
            return

        max_val = max(arr)
        exp = 1 
        while max_val // exp > 0:
            self.counting_sort_by_digit(arr, exp, speed)
            exp *= 10

    def counting_sort_by_digit(self, arr, exp, speed):
        n = len(arr)
        output = [0] * n
        count = [0] * 10  

        for num in arr:
            index = (num // exp) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        for i in range(n - 1, -1, -1):
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1

        for i in range(n):
            arr[i] = output[i]
            rajzold_ki(arr, y=100, canvas=self.canvas, selected=[i])
            root.update()
            root.after(int(speed))







#magyarazo osztaly cv2-vel


class Magyarazat:
    def __init__(self, alg):
        self.alg = alg
        self.speed = 30  # alap sebesseg
        self.is_playing = True
        self.video_pos = 0
        self.video_ended = False
        self.cap = None
        self.photo = None
        self.path = self.get_video_path(alg)
        self.min_speed = 10  # max idotav a framek kozott
        self.max_speed = 500  # min -||-
        self.video_canvas = None
        self.create_video_window()

    def get_video_path(self, alg):
        paths = {
            "Bubble sort": "videos/bubsort.mp4",
            "Insertion sort": "videos/inssort.mp4",
            "Selection sort": "videos/selsort.mp4",
            "Merge sort": "videos/mergesort.mp4",
            "Shell sort": "videos/shellsort.mp4",
            "Cocktail shaker sort": "videos/coctailsort.mp4",
            "Counting sort": "videos/countingsort.mp4",
            "Gnome sort": "videos/gnomesort.mp4",
            "Quick sort": "videos/quicksort.mp4",
            "Random quick sort": "videos/r-quicksort.mp4",
            "Radix sort": "videos/radixsort.mp4",
        }
        path = paths.get(alg, "")
        return path

    def create_video_window(self):
        self.video_canvas = Toplevel(root)
        target_width, target_height = 500, 500
        self.canvas_controls = Canvas(self.video_canvas, width=target_width, height=50)
        self.canvas_controls.pack(side="bottom")

        self.canvas_video = Canvas(self.video_canvas, width=target_width, height=target_height)
        self.canvas_video.pack(side="left")

        self.canvas_szoveg = Canvas(self.video_canvas, width=target_width, height=target_height)
        self.canvas_szoveg.pack(side="right")

        self.create_buttons()

        self.show_algorithm_description()

        self.display_video()

    def show_algorithm_description(self):
        alg_dict = {
            "Bubble sort": "bubblesort",
            "Insertion sort": "inssort",
            "Selection sort": "selsort",
            "Merge sort": "mergesort",
            "Shell sort": "shell_sort",
            "Cocktail shaker sort": "cocktail_shaker_sort",
            "Gnome sort": "gnome_sort",
            "Quick sort": "quick_sort",
            "Random quick sort": "randomized_quick_sort",
            "Radix sort": "radix_sort",
            "Counting sort": "counting_sort",
        }

        algo_name = alg_dict.get(self.alg)

        if algo_name:
            algo_func = getattr(IDO_Algoritmusok, algo_name, None) #getattr a docstringek lekeresere
            if algo_func and callable(algo_func):
                self.canvas_szoveg.create_text(250, 250, text=algo_func.__doc__) #.__doc__

    def display_video(self):
        self.megnyit_video()
        if not self.cap.isOpened():
            print("Error: Nem lehet megnyitni a videót.")
            return

        self.update_frame()

    def megnyit_video(self):
        if self.cap:
            self.cap.release()
        self.cap = cv2.VideoCapture(self.path)
        self.video_ended = False
        self.video_pos = 0

        if not self.cap.isOpened():
            print(f"Error: Nem talalhato ilyen videó itt: {self.path}")
            return
        print(f"Videó megnyitva: {self.path}")

    def update_frame(self):
        if self.is_playing and not self.video_ended:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.video_pos)
            ret, frame = self.cap.read()
            if not ret:
                self.video_ended = True
                self.is_playing = False
                print("Videó vége.")
            else:
                resized_frame = cv2.resize(frame, (500, 500))
                frame_rgb = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                image_pil = Image.fromarray(frame_rgb)
                self.photo = ImageTk.PhotoImage(image=image_pil)

                self.canvas_video.delete("all")
                self.canvas_video.create_image(0, 0, anchor="nw", image=self.photo)
                self.canvas_video.image = self.photo
                self.video_pos = self.cap.get(cv2.CAP_PROP_POS_FRAMES)

        self.video_canvas.after(max(self.speed, self.min_speed), self.update_frame)

    def create_buttons(self):
        Button(self.canvas_controls, text="Play/Stop", command=self.stop_play).pack(side="left")
        Button(self.canvas_controls, text="Újraindítás", command=self.ujrajatszas_video).pack(side="left")
        Button(self.canvas_controls, text="<< 2 mp", command=self.ugras_hatra_video).pack(side="left")
        Button(self.canvas_controls, text="2 mp >>", command=self.ugras_elore_video).pack(side="left")
        Button(self.canvas_controls, text="Gyorsabb", command=self.gyorsabb_speed).pack(side="left")
        Button(self.canvas_controls, text="Lassabb", command=self.lassabb_speed).pack(side="left")

    def stop_play(self):
        if not self.video_ended:
            self.is_playing = not self.is_playing

    def ujrajatszas_video(self):
        self.megnyit_video()
        self.is_playing = True

    def ugras_hatra_video(self):
        if not self.video_ended:
            current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            new_frame = max(0, current_frame - 2 * self.cap.get(cv2.CAP_PROP_FPS))
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            self.video_pos = new_frame

    def ugras_elore_video(self):
        if not self.video_ended:
            current_frame = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            new_frame = min(self.cap.get(cv2.CAP_PROP_FRAME_COUNT),
                            current_frame + 2 * self.cap.get(cv2.CAP_PROP_FPS))
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, new_frame)
            self.video_pos = new_frame

    def gyorsabb_speed(self):
        if self.speed > self.min_speed:
            self.speed = max(self.min_speed, self.speed - 10)

    def lassabb_speed(self):
        if self.speed < self.max_speed:
            self.speed = min(self.max_speed, self.speed + 10)



root.mainloop()
