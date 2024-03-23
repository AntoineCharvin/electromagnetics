import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import Callable, Tuple


def calculChamp(lambda0:float,S:float,l:float,nx:int,cl_gauche:Callable[[float,float],float],
                  cl_droite:Callable[[float,float],float],epsilon:Callable[[float,float,float],float]
                  ) -> Tuple[np.ndarray[float], np.ndarray[np.ndarray[float]]]:
    """Calcul du champ en 1D

    Args:
        lambda0 (float): longueur d'onde [m]
        S (float): facteur de stabilité
        l (float): longueur du domaine [m]
        nx (int): nombre de points spatiaux à calculer
        cl_gauche (Callable[[float,float],float]): condition aux limites à gauche du domaine
        cl_droite (Callable[[float,float],float]): condition aux limites à droite du domaine
        epsilon (Callable[[float,float,float],float]): valeur de epsilon

    Returns:
        Tuple[np.ndarray[float], np.ndarray[np.ndarray[float]]]: vecteurs positions (1D) [m], champ associé (2D)
    """

    # Paramètres et constantes
    c = 299792458
    T = lambda0 / c
    dx = l / nx
    dt = S * dx / c
    nt = int(3 * nx / S) # simulation sur un aller-retour

    # Initialisation des valeurs de return
    X = np.linspace(0, l, nx + 2)
    U = np.zeros((nt + 2, nx + 2))
    
    # Calcul de alpha_j = S^2 / epsilon
    alpha_j = np.array([S**2 / epsilon(dx*(j+1),l,lambda0) for j in range(1,nx+1,1)])

    # Ajout des CL
    for n in range(nt):
        U[n, 0] = cl_gauche(n * dt, T)
        U[n, nx + 1] = cl_droite(n * dt,T)

    # Calcul de U
    for n in range(2, nt + 2, 1):
        U[n, 1:nx+1] = alpha_j * U[n-1, 2:nx+2] + 2 * (1 - alpha_j) * U[n-1, 1:nx+1] + alpha_j * U[n-1, 0:nx] - U[n-2, 1:nx+1]
    
    return X, U

def calculChampPML(lambda0:float,S:float,l:float,nx:int,cl_gauche:Callable[[float,float],float],
                  cl_droite:Callable[[float,float],float],epsilon:Callable[[float,float,float],float]
                  ) -> Tuple[np.ndarray[float], np.ndarray[np.ndarray[float]]]:
    """Calcul du champ en 1D avec PML à droite

    Args:
        lambda0 (float): longueur d'onde [m]
        S (float): facteur de stabilité
        l (float): longueur du domaine [m]
        nx (int): nombre de points spatiaux à calculer
        cl_gauche (Callable[[float,float],float]): condition aux limites à gauche du domaine
        cl_droite (Callable[[float,float],float]): condition aux limites à droite du domaine
        epsilon (Callable[[float,float,float],float]): valeur de epsilon

    Returns:
        Tuple[np.ndarray[float], np.ndarray[np.ndarray[float]]]: vecteurs positions (1D) [m], champ associé (2D)
    """

    # Paramètres et constantes
    c = 299792458
    T = lambda0 / c
    dx = l / nx
    dt = S * dx / c
    nt = int(2 * nx / S) # simulation sur un aller-retour
    nbPML = 10
    facteurPML = 0.05

    # Initialisation des valeurs de return
    X = np.linspace(0, l, nx + 2)
    U = np.zeros((nt + 2, nx + 2))
    
    # Calcul de alpha_j = S^2 / epsilon
    alpha_j = np.array([S**2 / epsilon(dx*(j+1),l,lambda0) for j in range(1,nx+1,1)])

    # Ajout des CL
    for n in range(nt):
        U[n, 0] = cl_gauche(n * dt, T)
        U[n, nx + 1] = cl_droite(n * dt,T)

    # Calcul de U
    for n in range(2, nt + 2, 1):
        U[n, 1:nx+1] = alpha_j * U[n-1, 2:nx+2] + 2 * (1 - alpha_j) * U[n-1, 1:nx+1] + alpha_j * U[n-1, 0:nx] - U[n-2, 1:nx+1]
        U[n, nx+2-nbPML:] = (1 - facteurPML) * U[n-1, nx-nbPML+1:nx+1] + facteurPML * U[n-2, nx-nbPML+1:nx+1]
    
    return X, U

def epsilon_vide(x:float,l:float,lambda0:float) -> float:
    """Fonction epsilon pour deux milieux d'indices différents
    Indice n=1 à gauche et n=1.45 à droite

    Args:
        x (float): position x du calcul de epsilon [m]
        l (float): longueure totale du domaine de calcul [m]
        lambda0 (float): longueur d'onde de l'onde EM [m]

    Returns:
        float: valeur de epsilon
    """
    
    return 1.

def epsilon_dm(x:float,l:float,lambda0:float) -> float:
    """Fonction epsilon pour deux milieux d'indices différents
    Indice n=1 à gauche et n=1.45 à droite

    Args:
        x (float): position x du calcul de epsilon [m]
        l (float): longueure totale du domaine de calcul [m]
        lambda0 (float): longueur d'onde de l'onde EM [m]

    Returns:
        float: valeur de epsilon
    """
    
    indice_lame = 1.45
    if x < l / 2:
        return 1.
    else:
        return indice_lame**2

def epsilon_lame(x:float,l:float,lambda0:float) -> float:
    """Fonction epsilon pour une lame au centre
    Indice n=1.45 pour la lame et n=1 à l'exterieur

    Args:
        x (float): position x du calcul de epsilon
        l (float): longueure totale du domaine de calcul
        lambda0 (float): longueur d'onde de l'onde EM

    Returns:
        float: valeur de epsilon
    """
    
    # Paramètres lame
    indice_lame = 1.45
    lambda_lame = lambda0 / indice_lame
    largeur_lame = lambda_lame / 2
    
    # Calcul de epsilon
    if l / 2 - largeur_lame / 2 < x < l / 2 + largeur_lame / 2:
        return indice_lame ** 2
    else:
        return 1.

def cl_gauss(t:float, T:float) -> float:
    """Condition aux limites suivant la loi normale

    Args:
        t (float): instant de calcul [s]
        T (float): temps caractéristique [s]

    Returns:
        float: valeur du champ
    """
    
    return np.cos(2*np.pi*(t-8*T)/T)*np.exp(-((t-8*T)/T/3)**2)

def cl_metal(t:float, T:float) -> float:
    """Condition aux limites du métal

    Args:
        t (float): instant de calcul [s]
        T (float): temps caractéristique [s]

    Returns:
        float: valeur du champ
    """
    
    return 0

def coefR(n1:float,n2:float) -> float:
    """
    Calcul du coefficient de réflexion de Fresnel pour une onde incidente normale

    Args:
        n1 (float): indice de réfraction du premier milieu (milieu d'incidence)
        n2 (float): indice de réfraction du deuxième milieu (milieu de transmission)

    Returns:
        float: coefficient de réflexion de Fresnel (perpendiculaire)
    """
    
    r = (n2 - n1) / (n2 + n1)
    
    return r

def coefT(n1:float,n2:float) -> float:
    """
    Calcul du coefficient de transmission de Fresnel pour une onde incidente normale

    Args:
        n1 (float): indice de réfraction du premier milieu (milieu d'incidence)
        n2 (float): indice de réfraction du deuxième milieu (milieu de transmission)

    Returns:
        float: coefficient de transmission de Fresnel
    """
    
    t = 2 * n1 / (n1 + n2)
    
    return t

def affichageChamp(Xc:np.ndarray[float],U:np.ndarray[np.ndarray[float]],dt:float) -> None:
    """Affichage du champ avec FuncAnimation

    Args:
        Xc (np.ndarray[float]): vecteur positions [m]
        U (np.ndarray[np.ndarray[float]]): matrice du champ
        dt (float): pas de temps du calcul [s]

    Returns:
        None: affichage
    """
    
    # Conversion (μm et fs) et paramètres
    X = np.copy(Xc)
    X *= 1e6
    l = np.max(X)
    dt *= 1e15
    nt = U.shape[0] - 2
    
    # Création de la figure et des axes de l'animation
    fig, ax = plt.subplots()
    line, = ax.plot(X, U[3, :], label='n=3')  # Utilisez X pour les valeurs de l'axe x
    ax.set_xlim(0, l)
    ax.set_ylim(np.min(U),np.max(U))
    ax.set_xlabel(r'$x$ [$\mu$m]')
    ax.set_ylabel(r'$u(x)$ [u.a.]')

    # Définition de la fonction d'affichage
    duration_text = ax.text(0.1, 0.9, '', transform=ax.transAxes)
    def update(frame):
        line.set_ydata(U[frame, :])
        ax.set_title(f'Animation de la composante z du champ électrique')
        # Sauvegarde du texte d'affichage de la durée
        duration_text.set_text(f'Durée : {int(frame * dt)} fs')  # Modify this as needed
        
        return line, duration_text

    # Création de l'animation
    ani = FuncAnimation(fig, update, frames=range(nt + 2), blit=True, interval=10)

    plt.show()