
*** Settings ***

Library    SeleniumLibrary
Resource    ../Ressources/login_admin.robot
Resource    ../Ressources/create_product.robot
Resource    ../Ressources/create_order.robot
Resource    ../Ressources/login_user.robot
Resource    ../Ressources/browser.robot


*** Variables ***



*** Test Cases ***

Commander
    Ouvrir Navigateur Personnalisé
    #CONNEXION CLIENT
    Login Client Success    ${USER_CLIENT}    ${PASSWORD_CLIENT}
    #SELECTION PRODUIT
    Wait Until Element Is Visible    xpath=//a[img[@alt="Chaussette"]]    timeout=10s
    Click Element    xpath=//a[img[@alt="Chaussette"]]
    Wait Until Location Contains    /socks    timeout=5s
    Selectionner un produit    
    #GESTION DE LA COMMANDE
    Aller Au Panier
    Appliquer Code Promo  
    Vérifier Et Remplir Adresse Si Nécessaire
    Choisir Paiement Stripe
    Remplir Coordonnées Carte
    Valider Commande
    ${numCommande} =    Vérifier Résultat Paiement
    Fermer Navigateur Personnalisé
    #Vérification côté admin
    Vérifier Paiement de la Commande    ${numCommande}
    
    