# RYSMAN Karim, DEUTSCHE Sacha
from random import randint

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
