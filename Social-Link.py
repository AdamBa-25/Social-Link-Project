import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from typing import List, Tuple, Set, Dict
from matplotlib.animation import FuncAnimation

ACTIVITIES = [
    "Fan de Re:Zero",
    "Fan de Mushoku Tensei",
    "Fan de Feldup",
    "Fan de Five Nights at Freddy's",
    "Fan de Photographie",
    "Fan de Cuisine",
    "Fan de Jardinage",
    "Fan de livre de romance",
    "Fan de Jeux vidéo",
    "Fan d'Échecs",
    "Fan de Peinture",
    "Fan de The Binding Of Isaac",
    "Fan de Minecraft",
    "Fan de Bloons TD 6",
    "Fan de Dispatch",
    "Fan de Pâté en Croûte",
    "Fan de Natation",
    "Fan de livre d'horreur",
    "Fan de livre de Dark romance",
    "Fan de Programmation",
    "Fan de Mathématiques",
    "Fan de Sciences",
    "Fan de Cinéma",
    "Fan de Séries TV",
    "Fan d'Anime",
    "Fan de Manga",
    "Fan de Musique Rock",
    "Fan de Musique Classique",
    "Fan de Cyclisme",
    "Fan de Fitness",
    "Fan de Astronomie",
    "Fan de Technologies",
    "Fan de Guyeux"
]


class SocialNetwork:
    def __init__(self, G: nx.Graph, groups: List[List[int]], group_activities: Dict[int, str]):
        self.G = G
        self.groups = groups
        self.group_activities = group_activities
        self.rumor_state = {}

    def get_friend_recommendations(self, user_id: int, max_recommendations: int = 5) -> List[Tuple[int, int]]:
        if user_id not in self.G:
            return []

        friends = set(self.G.neighbors(user_id))
        recommendations = {}

        for friend in friends:
            for friend_of_friend in self.G.neighbors(friend):
                if friend_of_friend != user_id and friend_of_friend not in friends:
                    recommendations[friend_of_friend] = recommendations.get(friend_of_friend, 0) + 1

        sorted_recommendations = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return sorted_recommendations[:max_recommendations]

    def get_farthest_person(self, user_id: int) -> Tuple[int, int]:
        if user_id not in self.G:
            return None, None

        try:
            distances = nx.single_source_shortest_path_length(self.G, user_id)

            if len(distances) <= 1:
                return None, None

            farthest_user = max(distances.items(), key=lambda x: x[1])
            return farthest_user[0], farthest_user[1]
        except:
            return None, None

    def find_cliques(self, max_size: int = 10) -> List[Set[int]]:
        cliques = list(nx.find_cliques(self.G))
        return [set(clique) for clique in cliques if len(clique) <= max_size]

    def propagate_rumor(self, origin_user: int, probability: float = 0.7, max_steps: int = 10) -> Dict[int, int]:
        if origin_user not in self.G:
            return {}

        infected = {origin_user: 0}
        current_wave = [origin_user]

        for step in range(1, max_steps + 1):
            next_wave = []

            for user in current_wave:
                for neighbor in self.G.neighbors(user):
                    if neighbor not in infected and random.random() < probability:
                        infected[neighbor] = step
                        next_wave.append(neighbor)

            if not next_wave:
                break

            current_wave = next_wave

        self.rumor_state = infected
        return infected


def ask_positive_int(prompt: str, min_value: int) -> int:
    while True:
        text = input(prompt)
        if text.isdigit():
            value = int(text)
            if value >= min_value:
                return value
            print(f"Erreur : Entrez un entier >= {min_value}")
        else:
            print("Erreur : Entrez un entier valide")


def ask_float(prompt: str, min_value: float = 0.0, max_value: float = 1.0) -> float:
    while True:
        try:
            value = float(input(prompt))
            if min_value <= value <= max_value:
                return value
            print(f"Erreur : Entrez un nombre entre {min_value} et {max_value}")
        except ValueError:
            print("Erreur : Entrez un nombre valide")


def generate_social_graph(nb_groups: int, max_people_per_group: int, p_in: float = 0.6) -> Tuple[
    nx.Graph, List[List[int]], Dict[int, str]]:
    G = nx.Graph()
    groups = []
    group_activities = {}
    current_id = 0

    available_activities = ACTIVITIES.copy()
    random.shuffle(available_activities)

    for group_idx in range(nb_groups):
        size = random.randint(5, max_people_per_group)
        group_nodes = list(range(current_id, current_id + size))

        G.add_nodes_from(group_nodes)
        groups.append(group_nodes)

        if group_idx < len(available_activities):
            group_activities[group_idx] = available_activities[group_idx]
        else:
            group_activities[group_idx] = f"Activité {group_idx + 1}"

        current_id += size

        for i, node_i in enumerate(group_nodes):
            for node_j in group_nodes[i + 1:]:
                if random.random() < p_in:
                    G.add_edge(node_i, node_j)

        if G.subgraph(group_nodes).number_of_edges() == 0:
            for i in range(len(group_nodes) - 1):
                G.add_edge(group_nodes[i], group_nodes[i + 1])

    for i in range(nb_groups):
        for j in range(i + 1, nb_groups):
            num_connections = random.randint(2, 5)
            connections_made = 0
            attempts = 0
            max_attempts = num_connections * 10

            while connections_made < num_connections and attempts < max_attempts:
                node_a = random.choice(groups[i])
                node_b = random.choice(groups[j])

                if not G.has_edge(node_a, node_b):
                    G.add_edge(node_a, node_b)
                    connections_made += 1

                attempts += 1

    return G, groups, group_activities


def get_group_color(group_index: int, total_groups: int):
    cmap = plt.cm.tab10 if total_groups <= 10 else plt.cm.tab20
    return cmap(group_index % (10 if total_groups <= 10 else 20))


def visualize_network(network: SocialNetwork, highlight_nodes: Set[int] = None,
                      highlight_colors: Dict[int, str] = None, title: str = "Réseau Social",
                      use_circular: bool = True, show_legend: bool = False):
    G = network.G
    groups = network.groups

    node_colors = []
    for node in G.nodes():
        if highlight_colors and node in highlight_colors:
            node_colors.append(highlight_colors[node])
        else:
            for i, group in enumerate(groups):
                if node in group:
                    node_colors.append(get_group_color(i, len(groups)))
                    break

    plt.figure(figsize=(14, 10))

    if use_circular:
        pos = nx.circular_layout(G)
    else:
        pos = nx.spring_layout(G, seed=42, k=0.5, iterations=50)

    node_sizes = [800 if highlight_nodes and node in highlight_nodes else 500 for node in G.nodes()]

    if highlight_colors:
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9)
    else:
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes, alpha=0.9)

    nx.draw_networkx_edges(G, pos, alpha=0.3, width=1.5)
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')

    if show_legend and not highlight_colors:
        legend_elements = []
        for i, group in enumerate(groups):
            color = get_group_color(i, len(groups))
            activity = network.group_activities.get(i, f"Groupe {i + 1}")
            label = f'{activity} ({len(group)} pers.)'
            legend_elements.append(Patch(facecolor=color, label=label, alpha=0.9))

        plt.legend(handles=legend_elements, loc='upper left',
                   framealpha=0.95, fontsize=10, title="Groupes d'activités")

    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def visualize_rumor_propagation_realtime(network: SocialNetwork, origin: int, probability: float = 0.7,
                                         max_steps: int = 10):
    G = network.G

    if origin not in G:
        print(f"L'utilisateur {origin} n'existe pas dans le réseau.")
        return

    infected = {origin: 0}
    current_wave = [origin]
    propagation_steps = [{origin: 0}]
    new_infected_per_step = [[origin]]

    for step in range(1, max_steps + 1):
        next_wave = []

        for user in current_wave:
            for neighbor in G.neighbors(user):
                if neighbor not in infected and random.random() < probability:
                    infected[neighbor] = step
                    next_wave.append(neighbor)

        if not next_wave:
            break

        current_wave = next_wave
        propagation_steps.append(dict(infected))
        new_infected_per_step.append(next_wave.copy())

    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 2, height_ratios=[4, 0.3, 0.3], width_ratios=[3, 1])

    ax_graph = fig.add_subplot(gs[0, :])
    ax_progress = fig.add_subplot(gs[1, :])
    ax_stats = fig.add_subplot(gs[2, :])

    pos = nx.circular_layout(G)
    cmap = plt.cm.Reds

    def update(frame):
        ax_graph.clear()
        ax_progress.clear()
        ax_stats.clear()

        current_infected = propagation_steps[frame]
        max_step = max(current_infected.values()) if current_infected else 1

        node_colors = []
        for node in G.nodes():
            if node in current_infected:
                intensity = current_infected[node] / max(max_step, 1)
                node_colors.append(cmap(0.3 + 0.7 * intensity))
            else:
                node_colors.append('lightgray')

        node_sizes = []
        for node in G.nodes():
            if node == origin:
                node_sizes.append(1200)
            elif frame > 0 and node in new_infected_per_step[frame]:
                node_sizes.append(900)
            elif node in current_infected:
                node_sizes.append(600)
            else:
                node_sizes.append(400)

        normal_edges = []
        infected_edges = []

        for edge in G.edges():
            if edge[0] in current_infected and edge[1] in current_infected:
                infected_edges.append(edge)
            else:
                normal_edges.append(edge)

        nx.draw_networkx_edges(G, pos, edgelist=normal_edges, alpha=0.3, width=1.5, ax=ax_graph)

        nx.draw_networkx_edges(G, pos, edgelist=infected_edges, edge_color='red',
                               alpha=0.6, width=2.5, ax=ax_graph)

        nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                               node_size=node_sizes, alpha=0.9, ax=ax_graph)
        nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold', ax=ax_graph)

        if frame > 0 and new_infected_per_step[frame]:
            new_positions = {node: pos[node] for node in new_infected_per_step[frame]}
            nx.draw_networkx_nodes(G, new_positions,
                                   nodelist=new_infected_per_step[frame],
                                   node_color='none',
                                   edgecolors='yellow', linewidths=4,
                                   node_size=1000, ax=ax_graph)

        infected_count = len(current_infected)
        total_count = G.number_of_nodes()
        coverage = (infected_count / total_count) * 100

        ax_graph.set_title(f"Propagation de la rumeur - Étape {frame}/{len(propagation_steps) - 1}\n"
                           f"Infectés: {infected_count}/{total_count} ({coverage:.1f}%) | "
                           f"Origine: Utilisateur {origin} | Probabilité: {probability:.0%}",
                           fontsize=14, fontweight='bold', pad=20)
        ax_graph.axis('off')

        progress = frame / (len(propagation_steps) - 1) if len(propagation_steps) > 1 else 1
        ax_progress.barh([0], [progress], color='green', alpha=0.7, height=0.5)
        ax_progress.barh([0], [1 - progress], left=[progress], color='lightgray', alpha=0.3, height=0.5)
        ax_progress.set_xlim(0, 1)
        ax_progress.set_ylim(-0.5, 0.5)
        ax_progress.set_yticks([])
        ax_progress.set_xticks([0, 0.25, 0.5, 0.75, 1])
        ax_progress.set_xticklabels(['0%', '25%', '50%', '75%', '100%'])
        ax_progress.set_title('Progression de l\'animation', fontsize=10, pad=5)

        ax_stats.axis('off')

        if frame > 0:
            new_count = len(new_infected_per_step[frame])
            stats_text = f"[Étape {frame}] {new_count} nouvelle(s) personne(s) infectée(s)\n"
            stats_text += f"Nouveaux: {sorted(new_infected_per_step[frame])}"
        else:
            stats_text = f"[Étape 0] Rumeur lancée par l'utilisateur {origin}"

        ax_stats.text(0.5, 0.5, stats_text,
                      fontsize=11, ha='center', va='center',
                      bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    frames_count = len(propagation_steps)

    print(f"\n[Animation] Propagation sur {frames_count} étapes...")
    print("   Fermez la fenêtre pour continuer.")

    anim = FuncAnimation(fig, update, frames=frames_count,
                         interval=1500, repeat=True)

    plt.tight_layout()
    plt.show()

    final_infected = propagation_steps[-1]
    total_users = G.number_of_nodes()
    infected_count = len(final_infected)
    non_infected_count = total_users - infected_count
    coverage = (infected_count / total_users) * 100
    non_coverage = (non_infected_count / total_users) * 100

    print(f"\n" + "=" * 60)
    print("[RÉSUMÉ :]")
    print("=" * 60)

    print(f"\n[Statistiques globales]")
    print(f"   - Total utilisateurs dans le réseau : {total_users}")
    print(f"   - Utilisateurs infectés : {infected_count} ({coverage:.2f}%)")
    print(f"   - Utilisateurs non-infectés : {non_infected_count} ({non_coverage:.2f}%)")
    print(f"   - Nombre d'étapes de propagation : {len(propagation_steps) - 1}")
    print(f"   - Probabilité de transmission : {probability:.0%}")

    infected_edges_count = 0
    total_edges = G.number_of_edges()
    for edge in G.edges():
        if edge[0] in final_infected and edge[1] in final_infected:
            infected_edges_count += 1

    print(f"\n[Analyse du réseau infecté]")
    print(f"   - Connexions totales dans le réseau : {total_edges}")
    print(f"   - Connexions entre personnes infectées : {infected_edges_count}")
    if infected_count > 0:
        avg_connections = (infected_edges_count * 2) / infected_count
        print(f"   - Connexions moyennes par infecté : {avg_connections:.2f}")

    print(f"\n[Vitesse de propagation]")
    if len(propagation_steps) > 1:
        avg_new_per_step = infected_count / (len(propagation_steps) - 1)
        print(f"   - Moyenne de nouvelles infections par étape : {avg_new_per_step:.2f}")

        max_new_infections = max(len(step) for step in new_infected_per_step[1:]) if len(
            new_infected_per_step) > 1 else 0
        print(f"   - Maximum d'infections en une seule étape : {max_new_infections}")

    print(f"\n[Propagation détaillée par étape]")
    for step in range(len(new_infected_per_step)):
        new_users = new_infected_per_step[step]
        if step == 0:
            print(f"   Étape {step} : Origine → Utilisateur {origin}")
        else:
            cumulative = sum(len(new_infected_per_step[i]) for i in range(step + 1))
            cumulative_pct = (cumulative / total_users) * 100
            print(
                f"   Étape {step} : {len(new_users)} nouveau(x) → {sorted(new_users)} (Total cumulé: {cumulative}/{total_users} = {cumulative_pct:.1f}%)")


def menu_friend_recommendations(network: SocialNetwork):
    print("\n" + "=" * 60)
    print("[RECOMMANDATION D'AMIS]")
    print("=" * 60)

    user_id = ask_positive_int("\n> Entrez l'ID de l'utilisateur : ", 0)

    if user_id not in network.G:
        print(f"L'utilisateur {user_id} n'existe pas dans le réseau.")
        return

    friends = list(network.G.neighbors(user_id))
    print(f"\n[Amis actuels de l'utilisateur {user_id}]")
    if friends:
        print(f"   {sorted(friends)}")
        print(f"   Nombre total d'amis : {len(friends)}")
    else:
        print("   Aucun ami pour le moment.")

    recommendations = network.reco_friend(user_id)

    farthest_user, distance = network.get_farthest_person(user_id)

    if recommendations:
        print(f"\n[RECOMMANDATIONS D'AMIS POTENTIELS]")
        print(f"   (Personnes que vous ne connaissez pas encore, avec des amis en commun)")
        print()
        for i, (recommended_user, common_friends) in enumerate(recommendations, 1):
            print(f"   {i}. Utilisateur {recommended_user} -> {common_friends} ami(s) commun(s)")

        if farthest_user is not None:
            print(f"\n[PERSONNE LA PLUS ÉLOIGNÉE SOCIALEMENT]")
            print(f"   Utilisateur {farthest_user} - Distance : {distance} connexion(s)")
            print(f"   (Cette personne sera affichée en ROUGE sur le graphe)")

        highlight = {user_id} | {rec[0] for rec in recommendations}
        if farthest_user is not None:
            highlight.add(farthest_user)

        colors = {}
        for node in network.G.nodes():
            if node == user_id:
                colors[node] = 'blue'
            elif farthest_user is not None and node == farthest_user:
                colors[node] = 'red'
            elif node in friends:
                colors[node] = 'green'
            elif node in [rec[0] for rec in recommendations]:
                colors[node] = 'orange'
            else:
                colors[node] = 'lightgray'

        visualize_network(network, highlight_nodes=highlight, highlight_colors=colors,
                          title=f"Recommandations pour l'utilisateur {user_id}\n"
                                f"Bleu=Vous | Vert=Vos amis | Orange=Recommandations | Rouge=Plus éloigné")
    else:
        print("\nAucune recommandation disponible.")


def menu_find_cliques(network: SocialNetwork):
    print("\n" + "=" * 60)
    print("[DÉTECTION DE CERCLES D'AMIS COMPLETS]")
    print("=" * 60)

    max_size = ask_positive_int("\n> Taille MAXIMALE des cercles à détecter : ", 3)

    print("\n[Recherche en cours...]")
    cliques = network.find_cliques(max_size)

    if cliques:
        print(f"\n[RÉSULTATS] {len(cliques)} cercle(s) complet(s) trouvé(s) de taille <= {max_size}")

        cliques_sorted = sorted(cliques, key=len, reverse=True)

        print(f"\n[TOP 10 DES CERCLES LES PLUS GRANDS (taille <= {max_size})]")
        for i, clique in enumerate(cliques_sorted[:10], 1):
            clique_list = sorted(clique)
            print(f"\n   Cercle #{i} - Taille : {len(clique)} personnes")
            print(f"   Membres : {clique_list}")

            if len(clique) <= 5:
                print(f"   Connexions :", end=" ")
                connections = []
                clique_list_sorted = sorted(clique)
                for j in range(len(clique_list_sorted)):
                    for k in range(j + 1, len(clique_list_sorted)):
                        connections.append(f"{clique_list_sorted[j]}-{clique_list_sorted[k]}")
                print(", ".join(connections[:10]))
                if len(connections) > 10:
                    print(f" (+ {len(connections) - 10} autres connexions)")

        if len(cliques) > 10:
            print(f"\n   ... et {len(cliques) - 10} autre(s) cercle(s)")

        largest_clique = cliques_sorted[0]
        print(f"\n[VISUALISATION DU PLUS GRAND CERCLE (taille <= {max_size})]")
        print(f"   Taille : {len(largest_clique)} personnes")
        print(f"   Membres : {sorted(largest_clique)}")

        colors = {}
        for node in network.G.nodes():
            if node in largest_clique:
                colors[node] = 'red'
            else:
                colors[node] = 'lightgray'

        visualize_network(network, highlight_nodes=largest_clique,
                          highlight_colors=colors,
                          title=f"Plus grand cercle d'amis complet détecté (taille <= {max_size})\n({len(largest_clique)} membres qui se connaissent tous)")

        print(f"\n[INTERPRÉTATION]")
        print(f"   Dans ce cercle de {len(largest_clique)} personnes :")
        total_connections = len(largest_clique) * (len(largest_clique) - 1) // 2
        print(f"   - Il y a {total_connections} connexions au total")
        print(f"   - Chaque personne connaît les {len(largest_clique) - 1} autres membres")

    else:
        print(f"\nAucun cercle complet de taille <= {max_size} trouvé.")


def menu_rumor_propagation(network: SocialNetwork):
    print("\n" + "=" * 60)
    print("[SIMULATION DE PROPAGATION DE RUMEUR (TEMPS RÉEL)]")
    print("=" * 60)

    origin = ask_positive_int("\n> ID de l'utilisateur à l'origine de la rumeur : ", 0)

    if origin not in network.G:
        print(f"L'utilisateur {origin} n'existe pas dans le réseau.")
        return

    probability = ask_float("> Probabilité de partage (0.0 - 1.0) : ", 0.0, 1.0)
    max_steps = ask_positive_int("> Nombre maximum d'étapes : ", 1)

    visualize_rumor_propagation_realtime(network, origin, probability, max_steps)


def analyze_graph(G: nx.Graph, groups: List[List[int]], group_activities: Dict[int, str]):
    print("\n" + "=" * 60)
    print("[ANALYSE DU RÉSEAU SOCIAL]")
    print("=" * 60)

    print(f"\n[Statistiques globales]")
    print(f"   - Nombre de personnes : {G.number_of_nodes()}")
    print(f"   - Nombre de connexions : {G.number_of_edges()}")
    print(f"   - Réseau connexe : {'Oui' if nx.is_connected(G) else 'Non'}")
    print(f"   - Densité du réseau : {nx.density(G):.2%}")

    degrees = dict(G.degree())
    avg_degree = sum(degrees.values()) / G.number_of_nodes()
    print(f"   - Degré moyen : {avg_degree:.2f} amis par personne")

    max_degree_user = max(degrees.items(), key=lambda x: x[1])
    min_degree_user = min(degrees.items(), key=lambda x: x[1])

    print(f"   - Personne avec le plus d'amis : Utilisateur {max_degree_user[0]} ({max_degree_user[1]} amis)")
    print(f"   - Personne avec le moins d'amis : Utilisateur {min_degree_user[0]} ({min_degree_user[1]} amis)")

    top_connected = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:5]
    print(f"\n[Les 5 personnes avec le plus de connexions]")
    for i, (user, degree) in enumerate(top_connected, 1):
        print(f"   {i}. Utilisateur {user} : {degree} amis")

    print(f"\n[Connexions inter-groupes]")
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            inter_edges = 0
            for node_i in groups[i]:
                for node_j in groups[j]:
                    if G.has_edge(node_i, node_j):
                        inter_edges += 1
            activity_i = group_activities.get(i, f"Groupe {i + 1}")
            activity_j = group_activities.get(j, f"Groupe {j + 1}")
            print(f"   {activity_i} <-> {activity_j} : {inter_edges} connexion(s)")

    print(f"\n[Composition des groupes ({len(groups)} groupes)]")
    print("=" * 60)

    color_codes = [
        '\033[91m',  # rouge
        '\033[92m',  # vert
        '\033[93m',  # jaune
        '\033[94m',  # bleu
        '\033[95m',  # magenta
        '\033[96m',  # cyan
        '\033[97m',  # blanc
    ]
    reset_code = '\033[0m'

    for i, group in enumerate(groups):
        subgraph = G.subgraph(group)
        internal_edges = subgraph.number_of_edges()

        color = color_codes[i % len(color_codes)]
        activity = group_activities.get(i, f"Groupe {i + 1}")

        print(f"{color}   [{activity}]{reset_code}")
        print(f"      - Membres : {sorted(group)}")
        print(f"      - Taille : {len(group)} personnes")
        print(f"      - Connexions internes : {internal_edges}")
        print()


def interactive_menu():
    network = None

    while True:
        print("\n" + "=" * 60)
        print("[Bienvenue sur Social-Link]")
        print("=" * 60)
        print("\n[MENU]")
        print(" - 1. Générer un nouveau réseau social")
        print(" - 2. Visualiser le réseau actuel (layout circulaire)")
        print(" - 3. Analyser le réseau (statistiques détaillées)")
        print(" - 4. Recommandation d'amis potentiels")
        print(" - 5. Détecter les cercles d'amis complets")
        print(" - 6. Simuler la propagation d'une rumeur (TEMPS RÉEL)")
        print(" - 0. Quitter")

        choice = input("\n> Votre choix : ").strip()

        if choice == "1":
            print("\n" + "=" * 60)
            print("[GÉNÉRATION D'UN NOUVEAU RÉSEAU]")
            print("=" * 60)
            nb_groups = ask_positive_int("\n> Nombre de sous-groupes : ", 2)
            max_people = ask_positive_int("> Nombre MAX de personnes par sous-groupe (min: 4) : ", 4)

            print("\n[Génération du réseau en cours...]")
            G, groups, group_activities = generate_social_graph(nb_groups, max_people)
            network = SocialNetwork(G, groups, group_activities)

            print("\n[Réseau généré avec succès]")
            print("\n[Activités assignées aux groupes :]")
            for i, activity in group_activities.items():
                print(f"   Groupe {i + 1} : {activity}")

        elif choice == "2":
            if network is None:
                print("\nAucun réseau n'a été généré. Veuillez d'abord générer un réseau (option 1).")
            else:
                visualize_network(network, use_circular=True, show_legend=True)

        elif choice == "3":
            if network is None:
                print("\nAucun réseau n'a été généré. Veuillez d'abord générer un réseau (option 1).")
            else:
                analyze_graph(network.G, network.groups, network.group_activities)

        elif choice == "4":
            if network is None:
                print("\nAucun réseau n'a été généré. Veuillez d'abord générer un réseau (option 1).")
            else:
                menu_friend_recommendations(network)

        elif choice == "5":
            if network is None:
                print("\nAucun réseau n'a été généré. Veuillez d'abord générer un réseau (option 1).")
            else:
                menu_find_cliques(network)

        elif choice == "6":
            if network is None:
                print("\nAucun réseau n'a été généré. Veuillez d'abord générer un réseau (option 1).")
            else:
                menu_rumor_propagation(network)

        elif choice == "0":
            print("\nMerci d'avoir utilisé Social-Link.")
            break

        else:
            print("\nChoix invalide. Veuillez réessayer.")


if __name__ == "__main__":
    interactive_menu()