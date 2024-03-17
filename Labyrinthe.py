# RYSMAN Karim, DEUTSCHE Sacha
from random import randint, sample


class Maze:
    """
    Classe Labyrinthe
    Représentation sous forme de graphe non-orienté
    dont chaque sommet est une cellule (un tuple (l,c))
    et dont la structure est représentée par un dictionnaire
      - clés : sommets
      - valeurs : ensemble des sommets voisins accessibles
    """

    def __init__(self, height, width):
        """
        Constructeur d'un labyrinthe de height cellules de haut 
        et de width cellules de large 
        Les voisinages sont initialisés à des ensembles vides
        Remarque : dans le labyrinthe créé, chaque cellule est complètement emmurée
        """
        self.height = height
        self.width = width
        self.neighbors = {(i, j): set() for i in range(height) for j in range(width)}

    def info(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Affichage des attributs d'un objet 'Maze' (fonction utile pour deboguer)
        Retour:
            chaîne (string): description textuelle des attributs de l'objet
        """
        txt = "**Informations sur le labyrinthe**\n"
        txt += f"- Dimensions de la grille : {self.height} x {self.width}\n"
        txt += "- Voisinages :\n"
        txt += str(self.neighbors) + "\n"
        valid = True
        for c1 in {(i, j) for i in range(self.height) for j in range(self.width)}:
            for c2 in self.neighbors[c1]:
                if c1 not in self.neighbors[c2]:
                    valid = False
                    break
            else:
                continue
            break
        txt += "- Structure cohérente\n" if valid else f"- Structure incohérente : {c1} X {c2}\n"
        return txt

    def __str__(self):
        """
        **NE PAS MODIFIER CETTE MÉTHODE**
        Représentation textuelle d'un objet Maze (en utilisant des caractères ascii)
        Retour:
             chaîne (str) : chaîne de caractères représentant le labyrinthe
        """
        txt = ""
        # Première ligne
        txt += "┏"
        for j in range(self.width - 1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width - 1):
            txt += "   ┃" if (0, j + 1) not in self.neighbors[(0, j)] else "    "
        txt += "   ┃\n"
        # Lignes normales
        for i in range(self.height - 1):
            txt += "┣"
            for j in range(self.width - 1):
                txt += "━━━╋" if (i + 1, j) not in self.neighbors[(i, j)] else "   ╋"
            txt += "━━━┫\n" if (i + 1, self.width - 1) not in self.neighbors[(i, self.width - 1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += "   ┃" if (i + 1, j + 1) not in self.neighbors[(i + 1, j)] else "    "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width - 1):
            txt += "━━━┻"
        txt += "━━━┛\n"

        return txt

    def get_cells(self):
        L = []
        for i in range(self.height - 1):
            for j in range(self.width - 1):
                L.append((i, j))
        return L

    def add_wall(self, c1, c2):
        # Facultatif : on teste si les sommets sont bien dans le labyrinthe
        assert 0 <= c1[0] < self.height and 0 <= c1[1] < self.width and 0 <= c2[0] < self.height and 0 <= c2[
            1] < self.width, f"Erreur lors de l'ajout d'un mur entre {c1} et {c2} : les coordonnées de sont pas compatibles avec les dimensions du labyrinthe"
        # Ajout du mur
        if c2 in self.neighbors[c1]:  # Si c2 est dans les voisines de c1
            self.neighbors[c1].remove(c2)  # on le retire
        if c1 in self.neighbors[c2]:  # Si c1 est dans les voisines de c2
            self.neighbors[c2].remove(c1)  # on le retire

    def remove_wall(self, c1: tuple, c2: tuple) -> None:
        """
        Fonction supprimant un mur entre deux points

        :param c1: Premier point
        :param c2: Deuxième point
        :return: None
        """
        self.neighbors[c1].add(c2)
        self.neighbors[c2].add(c1)

        return None

    def get_walls(self) -> None:
        """
        Fonction retournant tous les murs sous forme de liste de tuple

        :return: None
        """
        L = []
        for i in range(self.height):
            for j in range(self.width):
                if i + 1 < self.height:
                    if (i + 1, j) not in self.neighbors[(i, j)] and (i, j) not in self.neighbors[(i + 1, j)]:
                        L.append([(i, j), (i + 1, j)])
                if i - 1 > 0:
                    if (i - 1, j) not in self.neighbors[(i, j)] and (i, j) not in self.neighbors[(i - 1, j)]:
                        L.append([(i, j), (i - 1, j)])
                if j + 1 < self.width:
                    if (i, j + 1) not in self.neighbors[(i, j)] and (i, j) not in self.neighbors[(i, j + 1)]:
                        L.append([(i, j), (i, j + 1)])
                if j - 1 > 0:
                    if (i, j - 1) not in self.neighbors[(i, j)] and (i, j) not in self.neighbors[(i, j - 1)]:
                        L.append([(i, j), (i, j - 1)])

        return L

    def fill(self) -> None:
        """
        Fonction ajoutant tous les murs possibles dans le labyrinthe

        :return: None
        """
        for i in range(0, self.height):
            for j in range(0, self.width - 1):
                self.add_wall((i, j), (i, j+1))
        for i in range(0, self.height - 1):
            for j in range(0, self.width):
                self.add_wall((i, j), (i + 1, j))

                """ Tentative initiale
                # Murs verticaux
                if (i, j) in self.neighbors and (i, j + 1) in self.neighbors[(i, j)]:
                    self.neighbors[(i, j)].remove((i, j + 1))
                if (i, j + 1) in self.neighbors and (i, j) in self.neighbors[(i, j + 1)]:
                    self.neighbors[(i, j + 1)].remove((i, j))

                # Murs horizontaux
                if (i, j) in self.neighbors and (i + 1, j) in self.neighbors[(i, j)]:
                    self.neighbors[(i, j)].remove((i + 1, j))
                if (i + 1, j) in self.neighbors and (i, j) in self.neighbors[(i + 1, j)]:
                    self.neighbors[(i + 1, j)].remove((i, j))
                """

        return None

    def empty(self) -> None:
        """
        Fonction retirant tous les murs possibles dans le labyrinthe

        :return: None
        """
        for i in range(self.height):
            for j in range(self.width):
                if i + 1 < self.height:
                    self.remove_wall((i, j), (i + 1, j))
                if i - 1 > 0:
                    self.remove_wall((i, j), (i - 1, j))
                if j + 1 < self.width:
                    self.remove_wall((i, j), (i, j + 1))
                if j - 1 > 0:
                    self.remove_wall((i, j), (i, j - 1))
        return self

    def get_contiguous_cells(self, c) -> list:
        """
        Fonction retournant les cellules contigües d'une cellule

        :param c: Cellule à étudier
        :return: liste des cellules contigües de c
        """
        L_contiguous = []
        if c[0] - 1 >= 0:
            L_contiguous.append((c[0]-1, c[1]))
        if c[0] + 1 < self.height:
            L_contiguous.append((c[0] + 1, c[1]))
        if c[1] - 1 >= 0:
            L_contiguous.append((c[0], c[1] - 1))
        if c[1] + 1 < self.width:
            L_contiguous.append((c[0], c[1] + 1))
        return L_contiguous

    def get_reachable_cells(self, c) -> list:
        """
        Fonction retournant les cellules contigües accessibles d'une cellule

        :param c: Cellule à étudier
        :return: liste des cellules contigües accessibles de c
        """
        L_contiguous = self.get_contiguous_cells(c)
        L_reachable_cells = []
        for cells in L_contiguous:
            if cells in self.neighbors and c in self.neighbors[cells]:
                L_reachable_cells.append(cells)
        return L_reachable_cells

    @classmethod
    def gen_btree(cls, h: int, w: int):
        """
        Génère un labyrinthe utilisant l'algorithme de construction par arbre binaire.

        :param h: le nombre de lignes du labyrinthe
        :param w: le nombre de colonnes du labyrinthe
        :return: un objet Maze représentant le labyrinthe généré
        """
        maze = cls(h, w)
        maze.fill()

        for i in range(0, h):
            for j in range(0, w):
                L_Murs = []
                # On vérifie si (i,j) possède des voisins et si (i, j + 1) fait parti de ses voisins. De plus
                # on vérifie si j+1 est un mur supprimable
                if not((i, j) in maze.neighbors and (i, j + 1) in maze.neighbors[(i, j)]) and j + 1 < w:
                    L_Murs.append((i, j + 1))

                # On vérifie si (i,j) possède des voisins et si (i + 1, j) fait parti de ses voisins. De plus
                # on vérifie si i+1 est un mur supprimable
                if not((i, j) in maze.neighbors and (i + 1, j) in maze.neighbors[(i, j)]) and i + 1 < h:
                    L_Murs.append((i + 1, j))

                if len(L_Murs) != 0:
                    maze.remove_wall((i, j), L_Murs[randint(0, len(L_Murs)-1)])

        return maze

    @classmethod
    def gen_sidewinder(cls, h, w):
        """
        Génère un labyrinthe en utilisant l'algorithme Sidewinder.

        :param cls: La classe elle-même.
        :param h: Le nombre de lignes du labyrinthe.
        :param w: Le nombre de colonnes du labyrinthe.
        :return: Un objet Maze représentant le labyrinthe généré.
        """
        laby = Maze(h, w)
        for i in range(h - 1):
            seq = []
            for j in range(w - 1):

                # ajout de la cellule à une sequence
                seq += [(i, j)]

                # si 0 casser mur EST
                PoF = randint(0, 1)
                if PoF == 0:
                    laby.remove_wall((i, j), (i, j + 1))

                # si 1 casser mur SUD d'une cell au hasard et réinitialiser seq
                else:
                    x = randint(0, len(seq) - 1)
                    laby.remove_wall(seq[x], (seq[x][0] + 1, seq[x][1]))
                    seq = []

                # ajout de la dernière cell et tirage au hasard d'une cell pour retirer son mur SUD
                seq += [(i, w - 1)]
                x = randint(0, len(seq) - 1)
                laby.remove_wall(seq[x], (seq[x][0] + 1, seq[x][1]))

            # casser tous les murs EST de la dernière ligne du laby
            for k in range(w - 1):
                laby.remove_wall((h - 1, k), (h - 1, k + 1))

        return laby

    @classmethod
    def gen_fusion(cls, h, w):
        """
        Génère un labyrinthe en utilisant l'algorithme de fusion.

        :param cls: La classe elle-même.
        :param h: Le nombre de lignes du labyrinthe.
        :param w: Le nombre de colonnes du labyrinthe.
        :return: Un objet Maze représentant le labyrinthe généré.
        """
        laby = Maze(h, w)

        # initialisation d'un dico qui contient la cell et son nom
        nomCell = {(i, j): 1 for i in range(h) for j in range(w)}
        nom = 0

        # attribution des noms pour chaque cell
        for i in range(h):
            for j in range(w):
                nomCell[(i, j)] = nom
                nom += 1

        # tri aleatoire de la liste des murs
        lstWalls = sample(laby.get_walls(), len(laby.get_walls()))

        # parcours de tout les murs
        for j in range(len(lstWalls)):

            # si le nom des cell est différent, casse le mur et affecte le nom de la première cell à toutes les cell
            # ayant le meme nom que la deuxième cell
            if nomCell[lstWalls[j][0]] != nomCell[lstWalls[j][1]]:
                laby.remove_wall(lstWalls[j][0], lstWalls[j][1])
                nomPCell = nomCell[lstWalls[j][1]]
                nomCell[lstWalls[j][1]] = nomCell[lstWalls[j][0]]

                for j in range(h):
                    for k in range(w):
                        if nomCell[(j, k)] == nomPCell:
                            nomCell[(j, k)] = nomCell[lstWalls[j][0]]
        return laby

    @classmethod
    def gen_exploration(cls, h, w):
        """
        Génère un labyrinthe en utilisant l'algorithme d'exploration.

        :param cls: La classe elle-même.
        :param h: Le nombre de lignes du labyrinthe.
        :param w: Le nombre de colonnes du labyrinthe.
        :return: Un objet Maze représentant le labyrinthe généré.
        """
        # Liste de toutes les cellules du labyrinthe
        lstCell = [(i, j) for i in range(h) for j in range(w)]

        # Sélection aléatoire d'une cellule comme point de départ
        randomCell = lstCell[randint(0, len(lstCell) - 1)]

        laby = Maze(h, w)  # Création d'une instance de Maze pour représenter le labyrinthe
        Pile = [randomCell]  # Initialisation de la pile de cellules à visiter
        Visite = [randomCell]  # Initialisation de la liste des cellules visitées

        # Parcours du labyrinthe en profondeur
        while len(Pile) > 0:
            cellAct = Pile[0]  # Sélection de la première cellule de la pile comme cellule actuelle
            del Pile[0]  # Suppression de la première cellule de la pile

            # Récupération des cellules voisines non visitées de la cellule actuelle
            test = laby.get_contiguous_cells(cellAct)

            # Vérification des cellules voisines non visitées
            cellVoisinVisit = True
            lstVoisinNonVisit = []
            for i in range(len(test)):
                # Vérification si les voisins de la cellule actuelle sont visités
                if test[i] not in Visite:
                    cellVoisinVisit = False
                    lstVoisinNonVisit += [test[i]]

            # Ajout des cellules non visitées à la pile pour poursuivre l'exploration
            if cellVoisinVisit == False:
                Pile += [cellAct]
                # Sélection aléatoire d'un voisin non visité
                hasard = lstVoisinNonVisit[randint(0, len(lstVoisinNonVisit) - 1)]
                # Casse le mur entre la cellule actuelle et le voisin sélectionné
                if cellAct != hasard:
                    laby.remove_wall(cellAct, hasard)
                    Visite += [hasard]
                    Pile = [hasard] + Pile

        return laby

    @classmethod
    def gen_wilson(cls, h, w) :
        """
        Génère un labyrinthe en utilisant l'algorithme de Wilson.

        :param cls: La classe elle-même.
        :param h: Le nombre de lignes du labyrinthe.
        :param w: Le nombre de colonnes du labyrinthe.
        :return: Un objet Maze représentant le labyrinthe généré.
        """
        marque = []
        lstCell = []

        #liste des cell
        for i in range(h) :
            for j in range(w) :
                lstCell += [(i, j)]

        laby = Maze(h, w)

        #tirage au hasard et marquage de la première cell
        randCell = lstCell[randint(0, len(lstCell) - 1)]
        marque += [randCell]

        while len(marque) != h*w :  #tant que les cell ne sont pas toutes marquées
            trouver = False

            while trouver == False :
                cellDepart = lstCell[randint(0, len(lstCell) - 1)]
                if cellDepart not in marque :
                    trouver = True

            chemin = []
            chemin += [cellDepart]
            lstVoisins = laby.get_contiguous_cells(cellDepart)
            continuer = True


            while continuer == True :
                 #tirage aléatoire dans la liste des voisins, 3 choses à vérifier
                cell = lstVoisins[randint(0,len(lstVoisins)-1)]

                # 1) si la cellule a deja ete parcourus dans le chemin actuelle -> boucle donc recommencer à zero
                # -> reinitalisation des variables à celle du début
                if cell in chemin:
                    chemin = []
                    chemin = chemin + [cellDepart]
                    lstVoisins = laby.get_contiguous_cells(cellDepart)

                # 2) sinon ajout de cette cellule au chemin et stockage des cell voisines
                else:
                    chemin = chemin + [cell]
                    lstVoisins = laby.get_contiguous_cells(cell)
                # 3) si la cellule est deja marque fin de la boucle while pour casser tous les murs du chemin du parcours
                # et ajouter toutes les cellules du chemin à la liste marque
                    if cell in marque:
                        continuer = False

            #je vais commencer par les marquer
            for i in range(len(chemin)):
                if chemin[i] not in marque:
                    marque = marque + [chemin[i]]


            #et je casse tous les murs
            for j in range(len(chemin)-1):
                laby.remove_wall(chemin[j],chemin[j+1])

        return laby

    def overlay(self, content=None):
        """
        Rendu en mode texte, sur la sortie standard, \
        d'un labyrinthe avec du contenu dans les cellules
        Argument:
            content (dict) : dictionnaire tq content[cell] contient le caractère à afficher au milieu de la cellule
        Retour:
            string
        """
        if content is None:
            content = {(i, j): ' ' for i in range(self.height) for j in range(self.width)}
        else:
            # Python >=3.9
            # content = content | {(i, j): ' ' for i in range(
            #    self.height) for j in range(self.width) if (i,j) not in content}
            # Python <3.9
            new_content = {(i, j): ' ' for i in range(self.height) for j in range(self.width) if (i, j) not in content}
            content = {**content, **new_content}
        txt = r""
        # Première ligne
        txt += "┏"
        for j in range(self.width - 1):
            txt += "━━━┳"
        txt += "━━━┓\n"
        txt += "┃"
        for j in range(self.width - 1):
            txt += " " + content[(0, j)] + " ┃" if (0, j + 1) not in self.neighbors[(0, j)] else " " + content[
                (0, j)] + "  "
        txt += " " + content[(0, self.width - 1)] + " ┃\n"
        # Lignes normales
        for i in range(self.height - 1):
            txt += "┣"
            for j in range(self.width - 1):
                txt += "━━━╋" if (i + 1, j) not in self.neighbors[(i, j)] else "   ╋"
            txt += "━━━┫\n" if (i + 1, self.width - 1) not in self.neighbors[(i, self.width - 1)] else "   ┫\n"
            txt += "┃"
            for j in range(self.width):
                txt += " " + content[(i + 1, j)] + " ┃" if (i + 1, j + 1) not in self.neighbors[(i + 1, j)] else " " + \
                                                                                                                 content[
                                                                                                                     (
                                                                                                                     i + 1,
                                                                                                                     j)] + "  "
            txt += "\n"
        # Bas du tableau
        txt += "┗"
        for i in range(self.width - 1):
            txt += "━━━┻"
        txt += "━━━┛\n"
        return txt

    def solve_dfs(self, start: tuple, stop: tuple) -> list:
        """
        Résout le labyrinthe en utilisant l'algorithme de recherche en profondeur.

        :param self: La classe elle-même.
        :param start: Le tuple représentant les coordonnées de la cellule de départ.
        :param stop: Le tuple représentant les coordonnées de la cellule de destination.
        :return: Une liste représentant le chemin solution du labyrinthe.
        """
        # Initialisation
        pile = [start]
        L_marques = [start]
        pred = {start: start}
        flag = True
        # Tant qu'il y a des cellules non marquées
        while len(L_marques) < self.height*self.width and flag:
            c = pile.pop()

            if c == stop:
                flag = False

            else:
                L_voisines = self.get_reachable_cells(c)
                for voisines in L_voisines:
                    if voisines not in L_marques:
                        L_marques.append(voisines)
                        pile.append(voisines)
                        pred[voisines] = c

        # Reconstruction du chemin
        c = stop
        path = []
        while c != start:
            path.append(c)
            c = pred[c]
        path.append(stop)

        return path

    def solve_bfs(self, start: tuple, stop: tuple) -> list:
        """
        Résout le labyrinthe en utilisant l'algorithme de recherche en largeur.

        :param self: La classe elle-même.
        :param start: Le tuple représentant les coordonnées de la cellule de départ.
        :param stop: Le tuple représentant les coordonnées de la cellule de destination.
        :return: Une liste représentant le chemin solution du labyrinthe.
        """
        # Initialisation
        file = [start]
        L_marques = [start]
        pred = {start: start}
        flag = True
        # Tant qu'il y a des cellules non marquées
        while len(L_marques) < self.height*self.width and flag:
            c = file.pop(0)

            if c == stop:
                flag = False

            else:
                L_voisines = self.get_reachable_cells(c)
                for voisines in L_voisines:
                    if voisines not in L_marques:
                        L_marques.append(voisines)
                        file.append(voisines)
                        pred[voisines] = c

        # Reconstruction du chemin
        c = stop
        path = []
        while c != start:
            path.append(c)
            c = pred[c]
        path.append(stop)

        return path