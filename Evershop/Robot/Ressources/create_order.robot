*** Settings ***
Library    SeleniumLibrary
Library    Collections
Library    String

Resource    ../Ressources/login_admin.robot
Resource    ../Ressources/create_product.robot
Resource    ../Ressources/browser.robot


*** Variables ***

#Données de test
${COUPON_CODE}       FREESHIPPING
${FULL_NAME}         John Doe
${TELEPHONE}         0612345678
${ADDRESS_1}         10 rue Exemple
${CITY}              Paris
${COUNTRY}           France
${PROVINCE}          Ile-de-France
${POSTCODE}          75000
${CARD_NUMBER}       4242424242424242
${CARD_EXPIRY}       12/30
${CARD_CVC}          123
${PAYMENT_SUCCESS}   True
${has_address}=     Set Variable    False


*** Keywords ***

Selectionner un produit
    Wait Until Page Contains    Chaussette
    Click Element    name=qty
    Clear Element Text    name=qty
    Input Text    name=qty    2
    Click Element    xpath=//button[@type="button"]//span[text()="ADD TO CART"]

Aller Au Panier
    Wait Until Element Is Visible    css=div.toast-mini-cart    timeout=5s
    Click Element    css=.add-cart-popup-button

Appliquer Code Promo
    Wait Until Element Is Visible    css=input[name="coupon"]    timeout=5s
    Input Text    css=input[name="coupon"]    ${COUPON_CODE}    
    Click Element    css=button.button.primary
    Wait Until Element Is Visible    css=div.Toastify__toast-body    timeout=5s
    Click Element    xpath=//a[span[text()="CHECKOUT"]]
    
Vérifier Et Remplir Adresse Si Nécessaire
    ${address_rows}=    Get WebElements    css=div.grid-cols-4
    ${has_address}=     Set Variable    False
    FOR    ${row}    IN    @{address_rows}
        ${element}=    Call Method    ${row}    find_element    xpath    .//div[contains(@class,"col-span-1")]/span
        ${title}=      Get Text    ${element}
        Run Keyword If    '${title}' == 'Ship to'    Vérifier Adresse Dans Row    ${row}
        Exit For Loop If    ${has_address} == True
    END
    Run Keyword If    not ${has_address}    Remplir Adresse

Vérifier Adresse Dans Row
    [Arguments]    ${row}
    ${element}=    Call Method    ${row}    find_element    xpath    .//div[contains(@class,"col-span-2")]/span
    ${address}=    Get Text    ${element}
    ${is_not_empty}=    Run Keyword And Return Status    Should Not Be Empty    ${address}
    Set Test Variable    ${has_address}    ${is_not_empty}
Remplir Adresse
    Wait Until Element Is Visible    css=input[name="address[full_name]"]    timeout=5s
    Input Text    css=input[name="address[full_name]"]    ${FULL_NAME}
    Input Text    css=input[name="address[telephone]"]    ${TELEPHONE}
    Input Text    css=input[name="address[address_1]"]    ${ADDRESS_1}
    Input Text    css=input[name="address[city]"]         ${CITY}
    Select From List By Label    css=select[name="address[country]"]    ${COUNTRY}
    Select From List By Label    css=select[name="address[province]"]   ${PROVINCE}
    Input Text    css=input[name="address[postcode]"]     ${POSTCODE}
    #Selection du mode de livraison
    Wait Until Element Is Visible    xpath=//label[span[contains(text(),"Colissimo")]]    timeout=10s
    Click Element    css=label[for="method0"]
    Click Element    xpath=//button[span[text()="Continue to payment"]]

Choisir Paiement Stripe
    Wait Until Element Is Visible    css=.border-divider.payment-method-list:nth-of-type(3) a    timeout=10s
    Click Element    css=.border-divider.payment-method-list:nth-of-type(3) a

Remplir Coordonnées Carte
    Select Frame    css=iframe[name^="__privateStripeFrame"]
    Wait Until Element Is Visible    id=Field-numberInput    timeout=10s
    Input Text    id=Field-numberInput   ${CARD_NUMBER}
    Input Text    id=Field-expiryInput      ${CARD_EXPIRY}
    Input Text    id=Field-cvcInput           ${CARD_CVC}
    Unselect Frame

Valider Commande
    Wait Until Element Is Visible    xpath=//button[span[text()="Place Order"]]    timeout=10s
    Scroll Element Into View    xpath=//button[span[text()="Place Order"]]
    Click Button    xpath=//button[span[text()="Place Order"]]

Vérifier Résultat Paiement
    IF    '${PAYMENT_SUCCESS}' == 'True'
        ${Order_number}=    Vérifier Confirmation Commande
    ELSE
        Vérifier Erreur Paiement
        ${Order_number}=    Set Variable    0
    END
    RETURN    ${Order_number}

Vérifier Confirmation Commande
    Wait Until Page Contains    Order #
    ${full_text}=    Get Text    xpath=//div[@class="self-center"]/span
    ${Order_number}=   Get Substring    ${full_text}    7
    RETURN    ${Order_number}

Vérifier Erreur Paiement
    Wait Until Element Is Visible    css=.toast-error
    ${error_text}=    Get Text    css=.toast-error
    Should Contain    ${error_text}    Payment failed

Vérifier Paiement de la Commande
    [Arguments]    ${number}
    Ouvrir Navigateur Personnalisé
    Login Admin Success    ${USER}    ${PASSWORD}
    Wait Until Page Contains    Dashboard    timeout=10s
    Wait Until Element Is Visible    xpath=//a[contains(text(), 'Orders')]    timeout=10s
    Click Element    xpath=//a[contains(text(), 'Orders')]
    Wait Until Element Is Visible    id=keyword    timeout=10s
    Input Text    id=keyword    ${number}
    Press Keys    id=keyword    ENTER

    # Vérifier qu'il y a une seule ligne de commande (hors header et ligne vide)
    ${rows}=    Get Element Count    xpath=//table[contains(@class,"listing")]//tbody/tr[.//a[contains(@href,"/admin/order/edit/")]]
    Should Be Equal As Integers    ${rows}    1

    # Récupérer le texte de l'état de paiement (6e colonne)
    ${payment_status}=    Get Text    xpath=//table[contains(@class,"listing")]//tbody/tr[.//a[contains(@href,"/admin/order/edit/")]]/td[6]//span[contains(@class,"title")]

    # Vérifier que le paiement est "Authorized" (ou autre valeur attendue)
    Should Be Equal    ${payment_status}    Authorized
    Fermer Navigateur Personnalisé
