import tkinter as tk
from tkinter import ttk, messagebox
import random
from collections import defaultdict
import json
import os
import math

class AdvancedKanaTrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Kana Trainer Avanzato")
        self.root.geometry("750x550")  # Aumentata la dimensione per i nuovi controlli
        
        # Percorso del file statistiche
        self.stats_file = "kana_trainer_stats.json"
        
        # Dizionari dei kana divisi per gruppi
        self.kana_groups = {
            'hiragana_base': {
                'a': 'あ', 'i': 'い', 'u': 'う', 'e': 'え', 'o': 'お',
                'ka': 'か', 'ki': 'き', 'ku': 'く', 'ke': 'け', 'ko': 'こ',
                'sa': 'さ', 'shi': 'し', 'su': 'す', 'se': 'せ', 'so': 'そ',
                'ta': 'た', 'chi': 'ち', 'tsu': 'つ', 'te': 'て', 'to': 'と',
                'na': 'な', 'ni': 'に', 'nu': 'ぬ', 'ne': 'ね', 'no': 'の',
                'ha': 'は', 'hi': 'ひ', 'fu': 'ふ', 'he': 'へ', 'ho': 'ほ',
                'ma': 'ま', 'mi': 'み', 'mu': 'む', 'me': 'め', 'mo': 'も',
                'ya': 'や', 'yu': 'ゆ', 'yo': 'よ',
                'ra': 'ら', 'ri': 'り', 'ru': 'る', 're': 'れ', 'ro': 'ろ',
                'wa': 'わ', 'wo': 'を', 'n': 'ん'
            },
            'hiragana_dakuten': {
                'ga': 'が', 'gi': 'ぎ', 'gu': 'ぐ', 'ge': 'げ', 'go': 'ご',
                'za': 'ざ', 'ji': 'じ', 'zu': 'ず', 'ze': 'ぜ', 'zo': 'ぞ',
                'da': 'だ', 'ji': 'ぢ', 'zu': 'づ', 'de': 'で', 'do': 'ど',
                'ba': 'ば', 'bi': 'び', 'bu': 'ぶ', 'be': 'べ', 'bo': 'ぼ',
                'pa': 'ぱ', 'pi': 'ぴ', 'pu': 'ぷ', 'pe': 'ぺ', 'po': 'ぽ'
            },
            'katakana_base': {
                'a': 'ア', 'i': 'イ', 'u': 'ウ', 'e': 'エ', 'o': 'オ',
                'ka': 'カ', 'ki': 'キ', 'ku': 'ク', 'ke': 'ケ', 'ko': 'コ',
                'sa': 'サ', 'shi': 'シ', 'su': 'ス', 'se': 'セ', 'so': 'ソ',
                'ta': 'タ', 'chi': 'チ', 'tsu': 'ツ', 'te': 'テ', 'to': 'ト',
                'na': 'ナ', 'ni': 'ニ', 'nu': 'ヌ', 'ne': 'ネ', 'no': 'ノ',
                'ha': 'ハ', 'hi': 'ヒ', 'fu': 'フ', 'he': 'ヘ', 'ho': 'ホ',
                'ma': 'マ', 'mi': 'ミ', 'mu': 'ム', 'me': 'メ', 'mo': 'モ',
                'ya': 'ヤ', 'yu': 'ユ', 'yo': 'ヨ',
                'ra': 'ラ', 'ri': 'リ', 'ru': 'ル', 're': 'レ', 'ro': 'ロ',
                'wa': 'ワ', 'wo': 'ヲ', 'n': 'ン'
            },
            'katakana_dakuten': {
                'ga': 'ガ', 'gi': 'ギ', 'gu': 'グ', 'ge': 'ゲ', 'go': 'ゴ',
                'za': 'ザ', 'ji': 'ジ', 'zu': 'ズ', 'ze': 'ゼ', 'zo': 'ゾ',
                'da': 'ダ', 'ji': 'ヂ', 'zu': 'ヅ', 'de': 'デ', 'do': 'ド',
                'ba': 'バ', 'bi': 'ビ', 'bu': 'ブ', 'be': 'ベ', 'bo': 'ボ',
                'pa': 'パ', 'pi': 'ピ', 'pu': 'プ', 'pe': 'ペ', 'po': 'ポ'
            }
        }
        
        # Carica le statistiche o inizializza
        self.stats = self.load_stats()
        
        # Variabili di stato
        self.current_kana = ''
        self.current_romaji = ''
        self.score = 0
        self.attempts = 0
        self.active_groups = {'hiragana_base': True, 'hiragana_dakuten': False,
                            'katakana_base': False, 'katakana_dakuten': False}
        
        # Filtri per consonanti
        self.consonant_filters = {
            'vocali': ['a', 'i', 'u', 'e', 'o', 'n'],
            'k-': ['ka', 'ki', 'ku', 'ke', 'ko'],
            's-': ['sa', 'shi', 'su', 'se', 'so'],
            't-': ['ta', 'chi', 'tsu', 'te', 'to'],
            'n-': ['na', 'ni', 'nu', 'ne', 'no'],
            'h-': ['ha', 'hi', 'fu', 'he', 'ho'],
            'm-': ['ma', 'mi', 'mu', 'me', 'mo'],
            'y-': ['ya', 'yu', 'yo'],
            'r-': ['ra', 'ri', 'ru', 're', 'ro'],
            'w-': ['wa', 'wo'],
            'g-': ['ga', 'gi', 'gu', 'ge', 'go'],
            'z-': ['za', 'ji', 'zu', 'ze', 'zo'],
            'd-': ['da', 'ji', 'zu', 'de', 'do'],
            'b-': ['ba', 'bi', 'bu', 'be', 'bo'],
            'p-': ['pa', 'pi', 'pu', 'pe', 'po']
        }
        self.active_consonants = {consonant: False for consonant in self.consonant_filters.keys()}
        self.active_consonants['vocali'] = True  # Di default attivo
        
        # Crea il notebook (schede)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Crea le schede
        self.create_training_tab()
        self.create_settings_tab()
        
        # Inizia con una nuova domanda
        self.new_question()
        
        # Salva le statistiche alla chiusura
        self.update_mode_label()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_training_tab(self):
        """Crea la scheda per l'esercitazione"""
        training_tab = ttk.Frame(self.notebook)
        self.notebook.add(training_tab, text="Esercitazione")
        
        # Frame principale
        main_frame = ttk.Frame(training_tab, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Pannello superiore per i punteggi
        score_frame = ttk.Frame(main_frame)
        score_frame.pack(fill=tk.X, pady=5)
        
        self.score_label = ttk.Label(score_frame, text="Punteggio: 0/0 (0%)", font=('Helvetica', 12))
        self.score_label.pack(side=tk.LEFT)
        
        self.mode_label = ttk.Label(score_frame, text="Modalità: ", font=('Helvetica', 12))
        self.mode_label.pack(side=tk.RIGHT)
        
        # Display del kana
        self.kana_label = ttk.Label(main_frame, text="", font=('Helvetica', 72))
        self.kana_label.pack(pady=20)
        
        # Input dell'utente
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Romaji:").pack(side=tk.LEFT)
        self.answer_entry = ttk.Entry(input_frame, width=20)
        self.answer_entry.pack(side=tk.LEFT, padx=5)
        self.answer_entry.bind('<Return>', lambda e: self.check_answer())
        
        submit_btn = ttk.Button(input_frame, text="Verifica", command=self.check_answer)
        submit_btn.pack(side=tk.LEFT)
        
        # Pulsanti di controllo
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=10)
        
        ttk.Button(control_frame, text="Nuova Domanda", command=self.new_question).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Mostra Risposta", command=self.show_answer).pack(side=tk.LEFT, padx=5)
        
        # Pulsante statistiche
        ttk.Button(main_frame, text="Statistiche", command=self.show_stats).pack(pady=5)
    
    def create_settings_tab(self):
        """Crea la scheda per le impostazioni"""
        settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(settings_tab, text="Impostazioni")
        
        # Frame principale con scrollbar
        main_frame = ttk.Frame(settings_tab)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Pannello selezione gruppi
        group_frame = ttk.LabelFrame(scrollable_frame, text="Seleziona Gruppi Kana", padding=10)
        group_frame.pack(fill=tk.X, pady=10, padx=5)
        
        # Checkbox per i gruppi
        self.group_vars = {}
        for i, group in enumerate(self.kana_groups.keys()):
            self.group_vars[group] = tk.BooleanVar(value=self.active_groups[group])
            cb = ttk.Checkbutton(group_frame, text=group.replace('_', ' ').title(),
                                variable=self.group_vars[group],
                                command=self.update_active_groups)
            cb.grid(row=i//2, column=i%2, sticky=tk.W, padx=5, pady=2)
        
        # Pannello selezione consonanti
        consonant_frame = ttk.LabelFrame(scrollable_frame, text="Filtra per Consonanti", padding=10)
        consonant_frame.pack(fill=tk.X, pady=10, padx=5)
        
        # Checkbox per le consonanti
        self.consonant_vars = {}
        for i, (consonant, kana_list) in enumerate(self.consonant_filters.items()):
            self.consonant_vars[consonant] = tk.BooleanVar(value=self.active_consonants[consonant])
            
            # Crea un frame per ogni riga di checkbox
            row_frame = ttk.Frame(consonant_frame)
            row_frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Checkbox
            cb = ttk.Checkbutton(row_frame, text=consonant,
                                variable=self.consonant_vars[consonant],
                                command=self.update_active_consonants)
            cb.pack(side=tk.LEFT)
            
            # Etichetta con l'elenco dei kana
            kana_chars = " ".join([self.get_kana_char(r) for r in kana_list])
            ttk.Label(row_frame, text=kana_chars).pack(side=tk.LEFT, padx=10)
    
    def get_kana_char(self, romaji):
        """Restituisce il carattere kana corrispondente al romaji"""
        for group in self.kana_groups.values():
            if romaji in group:
                return group[romaji]
        return "?"
    
    def update_active_consonants(self):
        """Aggiorna le consonanti attive in base alle selezioni dell'utente"""
        for consonant, var in self.consonant_vars.items():
            self.active_consonants[consonant] = var.get()
        self.update_mode_label()
        self.score = 0
        self.attempts = 0
        self.update_score()
        self.new_question()

    
    def update_active_groups(self):
        """Aggiorna i gruppi attivi in base alle selezioni dell'utente"""
        for group, var in self.group_vars.items():
            self.active_groups[group] = var.get()
        self.update_mode_label()
        self.score = 0
        self.attempts = 0
        self.update_score()
        self.new_question()

    
    def update_mode_label(self):
        """Aggiorna l'etichetta della modalità corrente"""
        active_modes = []
        if self.active_groups['hiragana_base'] or self.active_groups['hiragana_dakuten']:
            active_modes.append("Hiragana")
        if self.active_groups['katakana_base'] or self.active_groups['katakana_dakuten']:
            active_modes.append("Katakana")
        
        active_consonants = [c for c, active in self.active_consonants.items() if active]
        if active_consonants:
            active_modes.append("Consonanti: " + ", ".join(active_consonants))
        
        if not active_modes:
            active_modes = ["Nessun filtro selezionato"]
        
        self.mode_label.config(text="Modalità: " + " | ".join(active_modes))
    
    def get_active_kana(self):
        """Restituisce il dizionario dei kana attivi in base alle selezioni"""
        active_kana = {}
        
        # Prima filtra per gruppi (hiragana/katakana)
        for group, is_active in self.active_groups.items():
            if is_active:
                active_kana.update(self.kana_groups[group])
        
        # Poi applica il filtro per consonanti
        if any(self.active_consonants.values()):
            filtered_kana = {}
            for romaji, kana in active_kana.items():
                for consonant, kana_list in self.consonant_filters.items():
                    if self.active_consonants[consonant] and romaji in kana_list:
                        filtered_kana[romaji] = kana
                        break
            active_kana = filtered_kana
        
        return active_kana
    
    def load_stats(self):
        """Carica le statistiche dal file o crea un nuovo dizionario"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
                    # Convertiamo le chiavi annidate in defaultdict
                    return defaultdict(lambda: {'correct': 0, 'attempts': 0}, 
                                    {k: defaultdict(lambda: {'correct': 0, 'attempts': 0}, v) 
                                     for k, v in stats.items()})
        except Exception as e:
            messagebox.showwarning("Attenzione", f"Errore nel caricamento delle statistiche: {e}")
        
        return defaultdict(lambda: {'correct': 0, 'attempts': 0})
    
    def save_stats(self):
        """Salva le statistiche su file"""
        try:
            # Creiamo la directory se non esiste
            os.makedirs(os.path.dirname(self.stats_file), exist_ok=True)
            
            # Convertiamo i defaultdict in dict normali per il salvataggio JSON
            stats_to_save = {k: dict(v) for k, v in self.stats.items()}
            
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(stats_to_save, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showwarning("Attenzione", f"Errore nel salvataggio delle statistiche: {e}")
    
    def on_close(self):
        """Salva le statistiche prima di chiudere l'applicazione"""
        self.save_stats()
        self.root.destroy()
    
    def get_weighted_kana_list(self):
        """Restituisce una lista di kana pesata in base alle statistiche"""
        active_kana = self.get_active_kana()
        if not active_kana:
            return []
        
        weighted_list = []
        for romaji, kana in active_kana.items():
            # Calcola un peso inversamente proporzionale alla percentuale di successo
            stats = self.stats[kana]
            attempts = stats['attempts']
            correct = stats['correct']
            
            if attempts == 0:
                # Se non è mai stato provato, alta priorità
                weight = 100
            else:
                accuracy = correct / attempts
                # Pesa di più i caratteri con bassa accuratezza
                MIN_WEIGHT = 5
                weight = int((1 / (accuracy + 0.01)) * 5) + MIN_WEIGHT
            
            weighted_list.extend([(romaji, kana)] * weight)
        
        return weighted_list
    
    def new_question(self):
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
        
        weighted_kana = self.get_weighted_kana_list()
        if not weighted_kana:
            messagebox.showwarning("Attenzione", "Nessun kana selezionato con i filtri attuali!")
            return
        
        self.current_romaji, self.current_kana = random.choice(weighted_kana)
        self.kana_label.config(text=self.current_kana)
    
    def check_answer(self):
        user_answer = self.answer_entry.get().strip().lower()
        if not user_answer:
            return
            
        self.attempts += 1
        
        # Normalizza la risposta (accetta varianti comuni)
        normalized_answer = user_answer
        variants = {
            'si': 'shi',
            'ti': 'chi',
            'tu': 'tsu',
            'hu': 'fu',
            'zi': 'ji',
            'di': 'ji',
            'du': 'zu'
        }
        normalized_answer = variants.get(user_answer, user_answer)
        
        if normalized_answer == self.current_romaji:
            self.score += 1
            self.stats[self.current_kana]['correct'] += 1
        else:
            messagebox.showerror("Sbagliato", f"Errato! {self.current_kana} si legge '{self.current_romaji}', non '{user_answer}'")
        
        self.stats[self.current_kana]['attempts'] += 1
        self.update_score()
        self.new_question()
    
    def show_answer(self):
        messagebox.showinfo("Risposta", f"{self.current_kana} si legge '{self.current_romaji}'")
        self.new_question()
    
    def update_score(self):
        percentage = (self.score / self.attempts * 100) if self.attempts > 0 else 0
        self.score_label.config(text=f"Punteggio: {self.score}/{self.attempts} ({percentage:.1f}%)")
    
    def show_stats(self):
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Statistiche Dettagliate")
        stats_window.geometry("500x500")
        
        # Crea un notebook con schede per ogni gruppo
        notebook = ttk.Notebook(stats_window)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Aggiungi una scheda per ogni gruppo di kana
        for group in self.kana_groups.keys():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=group.replace('_', ' ').title())
            
            # Crea un frame con scrollbar per questa scheda
            canvas = tk.Canvas(frame)
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e, canvas=canvas: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Aggiungi i kana di questo gruppo alle statistiche
            group_kana = self.kana_groups[group]
            sorted_kana = sorted(group_kana.items(), key=lambda x: x[1])

            
            for romaji, kana in sorted_kana:
                stats = self.stats[kana]
                attempts = stats['attempts']
                correct = stats['correct']
                percentage = (correct / attempts * 100) if attempts > 0 else 0
                
                row_frame = ttk.Frame(scrollable_frame)
                row_frame.pack(fill=tk.X, padx=5, pady=2)
                
                ttk.Label(row_frame, text=kana, width=5, font=('Helvetica', 14)).pack(side=tk.LEFT)
                ttk.Label(row_frame, text=romaji, width=10).pack(side=tk.LEFT)
                ttk.Label(row_frame, text=f"{correct}/{attempts}", width=10).pack(side=tk.LEFT)
                ttk.Label(row_frame, text=f"{percentage:.1f}%").pack(side=tk.LEFT)
                
                progress = ttk.Progressbar(row_frame, length=100, maximum=100, value=percentage)
                progress.pack(side=tk.LEFT, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    try:
        app = AdvancedKanaTrainer(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore: {e}")
