# Social-Link

Social-Link est un programme Python permettant d’explorer et de comprendre les dynamiques sociales au sein d’un groupe à l’aide de la théorie des graphes.

---

## Technologies utilisées

* Python

  * NetworkX
  * Matplotlib
  * SciPy

---

## Explication du projet

Social-Link repose sur la modélisation mathématique d’un réseau social à l’aide d’un graphe non orienté.

* Chaque personne est représentée par un sommet.
* Chaque relation d’amitié est représentée par une arête.

Le programme permet de :

* Générer un réseau social aléatoire composé de plusieurs sous-groupes, avec un nombre maximal de personnes par groupe
* Visualiser graphiquement le réseau
* Analyser le graphe (nombre d’amis, degré moyen, utilisateur le plus connecté, densité, connexité)
* Proposer un système de recommandation d’amis basé sur les amis en commun
* Détecter des cliques (groupes totalement interconnectés)
* Simuler la propagation d’une rumeur en temps réel selon une probabilité donnée

---

## Connaissances des graphes mobilisées

### Modélisation par un graphe

Le graphe est non orienté, car les relations sociales sont supposées réciproques.

---

### Sous-graphes

Les sous-graphes représentent des communautés internes (ici représenté).

Chaque sous-groupe est densément connecté en interne, puis relié aux autres groupes par plusieurs connexions aléatoires (entre 2 et 5), garantissant l’existence d’un réseau global cohérent.

---

### Connexité

La connexité assure que l’ensemble des sous-groupes forme un unique grand réseau social.

Le programme vérifie cette propriété à l’aide des outils d’analyse de graphes.

---

### Degré des sommets

Le degré d’un sommet correspond au nombre d’amis d’un utilisateur.

Cela permet :

* De calculer le degré moyen
* D’identifier l’utilisateur le plus connecté
* De comparer les niveaux d’intégration sociale

---

### Densité du graphe

La densité mesure la proportion de connexions existantes par rapport au nombre maximal possible.

Elle permet d’évaluer si un réseau est fortement soudé ou relativement fragmenté.

---

### Cliques

Une clique est un sous-ensemble de sommets où chaque sommet est relié à tous les autres.

Le programme détecte automatiquement les cliques de taille minimale donnée, représentant des groupes sociaux très fermés.

---

### Chemins dans les graphes

Les chemins sont essentiels pour modéliser :

* La distance sociale entre deux personnes
* La propagation d’une rumeur

Deux types de parcours sont utilisés dans le projet :

1. **Parcours en largeur**
   Utilisé pour déterminer les plus courtes distances sociales à partir d’un individu donné. Il permet notamment d’identifier la personne la plus éloignée dans le réseau.

2. **Propagation itérative de proche en proche**
   Lors de la simulation de rumeur, le programme parcourt progressivement les voisins d’un sommet infecté, étape par étape. Ce mécanisme s’apparente à un parcours en largeur probabiliste, où chaque arête peut transmettre la rumeur selon une probabilité donnée.

---

## Répartition du travail :
| Fonction / Méthode | Responsable |
| ------------------ | ----------- |
|   __init__         |      Adam       |
| get_friend_recommendations|     Adam   |
| get_farthest_person|     Adam    |
|  find_cliques      |     Adam    | 
|  propagate_rumor   |      Adam   |
| ask_positive_int   |       Lukas |
|  ask_float         |       Lukas |
|generate_social_graph|     Adam   | 
|get_group_color     |    Lukas    |
|visualize_network   |    Lukas    |
|visualize_rumor_propagation_realtime |     Adam / Lukas |
| menu_friend_recommendations |   Lukas   | 
| menu_find_cliques  |  Lukas    |
| menu_rumor_propagation|     Lukas        |
| analyze_graph      |       Adam / Lukas     |
| interactive_menu       |         Lukas    | 


---

## Conclusion et perspectives

Ce projet a été refait à deux reprises. Initialement, il devait prendre la forme d’un système proche d’une base de données où chaque utilisateur pouvait entrer son propre réseau d’amis afin de l’analyser.

En raison de la complexité liée à la saisie des données de test et à l’intégration conjointe de SQL et Python, le projet a évolué vers une version centrée exclusivement sur la modélisation par graphes, offrant une approche plus claire et mathématiquement cohérente.


