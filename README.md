## Différents tests automatisés effectués sur le site d'Evershop
Prérequis :
  - install Docker et importer le projet dans un conteneur
  - créer un profil administrateur (commande dans le conteneur de Docker)
  - créer un profil client (sur le site en lui même)
D'abord avec Selenium Python (pytest) :
  - création d'un fichier de config pour le chargement du browser avec d'autres fonctionnalités outils
  - login admin
  - login client
  - création d'un produit
  - création d'une collection
  - création d'une catégorie
  - création d'une commande avec le paiement
Avec RobotFramework :
  - ouverture du browser
  - login admin
  - login client
  - création d'un produit
  - création d'une commande avec paiement + vérification du paiement
  
