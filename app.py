import tkinter as tk
from tkinter import messagebox
import random

PIECES = {
    "I": ("IMG", "#00f0f0", "4 en ligne"),
    "O": ("IMG", "#f0f000", "2x2"),
    "T": ("IMG", "#a000f0", "3 + 1 au milieu"),
    "S": ("IMG", "#00f000", "Zigzag droit"),
    "Z": ("IMG", "#f00000", "Zigzag gauche"),
    "J": ("IMG", "#0000f0", "L inversé"),
    "L": ("IMG", "#f0a000", "L normal")
}

# ^^^ Liste des pieces (possible d'en ajouter ou enlever.

class Tetris3D:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tetris 3D - Controleur")
        self.root.geometry("500x400")
        self.root.configure(bg="#2c3e50")
        
        self.joueurs = []
        self.tour = 0
        self.manche = 1
        self.piece_actuelle = None
        
        self.creer_ecran_accueil()
        
# Base de l'app
    
    def creer_ecran_accueil(self):
        self.effacer_ecran()
        
        tk.Label(self.root, text="Tetris 3D", font=("Arial", 30, "bold"),
                bg="#2c3e50", fg="white").pack(pady=20)
        
        tk.Label(self.root, text="Nombre de joueurs:", 
                bg="#2c3e50", fg="white", font=("Arial", 12)).pack()
        
        self.entree_joueurs = tk.Spinbox(self.root, from_=2, to=10, width=10,
                                        font=("Arial", 14))
        self.entree_joueurs.pack(pady=10)
        
        tk.Button(self.root, text="Configurer", command=self.configurer_joueurs,
                 font=("Arial", 12), width=15, bg="#3498db", fg="white").pack(pady=10)
    
    

    def configurer_joueurs(self):
        nb = int(self.entree_joueurs.get())
        self.joueurs = [{"nom": f"Joueur {i+1}", "score": 0} for i in range(nb)]
        
        self.effacer_ecran()
        
        tk.Label(self.root, text="Noms des joueurs", 
                font=("Arial", 18, "bold"), bg="#2c3e50", fg="white").pack(pady=10)
        
        self.entrees_noms = []
        for i in range(nb):
            frame = tk.Frame(self.root, bg="#2c3e50")
            frame.pack(pady=2)
            tk.Label(frame, text=f"J{i+1}:", bg="#2c3e50", fg="white").pack(side="left")
            entree = tk.Entry(frame, font=("Arial", 12), width=20)
            entree.insert(0, f"Joueur {i+1}")
            entree.pack(side="left", padx=5)
            self.entrees_noms.append(entree)
        
        tk.Button(self.root, text="Démarrer", command=self.demarrer_jeu,
                 font=("Arial", 14), bg="#2ecc71", fg="white").pack(pady=20)
    
    def demarrer_jeu(self):
        for i, entree in enumerate(self.entrees_noms):
            self.joueurs[i]["nom"] = entree.get() or f"Joueur {i+1}"
        
        self.effacer_ecran()
        self.creer_interface_jeu()
        self.maj_affichage()
    
    def creer_interface_jeu(self):
        # Info en haut
        self.frame_info = tk.Frame(self.root, bg="#34495e")
        self.frame_info.pack(fill="x", padx=10, pady=5)
        
        self.label_tour = tk.Label(self.frame_info, text="", font=("Arial", 16),
                                  bg="#34495e", fg="#3498db")
        self.label_tour.pack(side="left", padx=10)
        
        self.label_manche = tk.Label(self.frame_info, text="Manche: 1",
                                    font=("Arial", 14), bg="#34495e", fg="white")
        self.label_manche.pack(side="right", padx=10)
        
        # Liste joueurs
        self.frame_liste = tk.Frame(self.root, bg="#2c3e50")
        self.frame_liste.pack(fill="x", padx=10, pady=5)
        
        self.liste_joueurs = tk.Listbox(self.frame_liste, height=6, font=("Arial", 11))
        self.liste_joueurs.pack(fill="x")
        
        # Affichage pièce
        self.frame_piece = tk.Frame(self.root, bg="#2c3e50")
        self.frame_piece.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.label_piece_lettre = tk.Label(self.frame_piece, text="?",
                                          font=("Arial", 100, "bold"), bg="#2c3e50")
        self.label_piece_lettre.pack(expand=True)
        
        self.label_piece_nom = tk.Label(self.frame_piece, text="Appuyez sur le bouton",
                                       font=("Arial", 14), bg="#2c3e50", fg="white")
        self.label_piece_nom.pack()
        
        self.label_piece_desc = tk.Label(self.frame_piece, text="",
                                        font=("Arial", 11), bg="#2c3e50", fg="#bdc3c7")
        self.label_piece_desc.pack()
        
        # Boutons
        self.frame_boutons = tk.Frame(self.root, bg="#2c3e50")
        self.frame_boutons.pack(pady=10)
        
        self.bouton_tirer = tk.Button(self.frame_boutons, text="Tirer Pièce",
                                     command=self.tirer_piece,
                                     font=("Arial", 14), bg="#e74c3c", fg="white",
                                     width=12)
        self.bouton_tirer.pack(side="left", padx=5)
        
        self.bouton_placer = tk.Button(self.frame_boutons, text="Placée",
                                      command=self.piece_placee, state="disabled",
                                      font=("Arial", 14), bg="#2ecc71", fg="white",
                                      width=10)
        self.bouton_placer.pack(side="left", padx=5)
        
        tk.Button(self.frame_boutons, text="Passer", command=self.passer_tour,
                 font=("Arial", 12)).pack(side="left", padx=5)
    
    def maj_affichage(self):
        joueur = self.joueurs[self.tour]
        self.label_tour.config(text=f"Tour: {joueur['nom']}")
        self.label_manche.config(text=f"Manche: {self.manche}")
        
        self.liste_joueurs.delete(0, "end")
        for i, j in enumerate(self.joueurs):
            prefix = "→ " if i == self.tour else "  "
            self.liste_joueurs.insert("end", f"{prefix}{j['nom']}: {j['score']} pts")
            if i == self.tour:
                self.liste_joueurs.itemconfig("end", {"bg": "#3498db", "fg": "white"})
    
    def tirer_piece(self):
        lettre, (nom, couleur, desc) = random.choice(list(PIECES.items()))
        self.piece_actuelle = lettre
        
        self.label_piece_lettre.config(text=lettre, fg=couleur)
        self.label_piece_nom.config(text=nom, fg=couleur)
        self.label_piece_desc.config(text=desc)
        
        self.bouton_tirer.config(state="disabled")
        self.bouton_placer.config(state="normal")
    
    def piece_placee(self):
        if self.piece_actuelle:
            self.joueurs[self.tour]["score"] += 4
        
        self.piece_actuelle = None
        self.label_piece_lettre.config(text="?", fg="black")
        self.label_piece_nom.config(text="Pièce placée.", fg="white")
        self.label_piece_desc.config(text="")
        
        self.bouton_tirer.config(state="normal")
        self.bouton_placer.config(state="disabled")
        
        self.tour_suivant()
    
    def passer_tour(self):
        self.piece_actuelle = None
        self.label_piece_lettre.config(text="?", fg="black")
        self.label_piece_nom.config(text="Tour passé.", fg="white")
        self.label_piece_desc.config(text="")
        
        self.bouton_tirer.config(state="normal")
        self.bouton_placer.config(state="disabled")
        
        self.tour_suivant()
    
    def tour_suivant(self):
        self.tour = (self.tour + 1) % len(self.joueurs)
        if self.tour == 0:
            self.manche += 1
        self.maj_affichage()
    
    def effacer_ecran(self):
        for widget in self.root.winfo_children():
            widget.destroy()

Tetris3D().root.mainloop()