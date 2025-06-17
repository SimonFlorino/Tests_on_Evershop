*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${ADMIN_URL}         http://localhost:3000/admin/login
${PRODUCTS_URL}      http://localhost:3000/admin/products
${NEW_PRODUCT_URL}   http://localhost:3000/admin/products/new

${ADMIN_EMAIL}       admin@admin.com
${ADMIN_PASSWORD}    admin123

# Données produit pour la création
${P_NAME}            Cravate
${P_SKU}             Tie_mickey
${P_PRICE}           20
${P_WEIGHT}          0.1
${P_QTY}             100
${P_URL_KEY}         ties
${P_META_TITLE}      Belle cravate
${P_META_KEYWORDS}   tie
${P_META_DESC}       tie
${P_IMAGE_REL}       images/tie.png
${P_IMAGE}           ${CURDIR}/${P_IMAGE_REL}

# Données produit pour la modification
${P_EDIT_NAME}       Cravate Mickey
${P_EDIT_PRICE}      25
${P_EDIT_URL_KEY}    tie-mickey
${P_EDIT_META_TITLE}  Cravate Mickey
${P_EDIT_META_KEYWORDS}  tie mickey
${P_EDIT_META_DESC}  tie mickey

*** Test Cases ***
Créer un nouveau produit
    [Tags]    create
    Connexion Admin
    Go To    ${PRODUCTS_URL}
    Click Link    New Product
    Location Should Be    ${NEW_PRODUCT_URL}
    Remplir formulaire produit (création)
    Cliquer Save et vérifier succès
    Close Browser

Modifier le produit existant
    [Tags]    edit
    Connexion Admin
    Go To    ${PRODUCTS_URL}
    # Recherche par nom
    Input Text    id=keyword    ${P_NAME}
    Press Keys    id=keyword    ENTER
    Wait Until Page Contains Element    css:table.listing tbody tr
    Click Link    ${P_NAME}
    Remplir formulaire produit (modification)
    Cliquer Save et vérifier succès
    Close Browser

Supprimer le produit
    [Tags]    delete
    Connexion Admin
    Go To    ${PRODUCTS_URL}
    Input Text    id=keyword    ${P_EDIT_NAME}
    Press Keys    id=keyword    ENTER
    Wait Until Page Contains Element    css:table.listing tbody tr
    # Sélectionner la première checkbox de la ligne trouvée
    Click Element    css:table.listing tbody tr td input[type="checkbox"]
    # Cliquer sur Delete dans la barre d'action
    Click Element    xpath=//table[contains(@class,'listing')]//td[contains(@colspan,'')]//a[.//span[translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='delete']]
    Wait Until Element Is Visible    css:.modal .button.critical
    Click Button    css:.modal .button.critical
    # Rafraîchir la liste et vérifier absence
    Sleep    1s
    Clear Element Text    id=keyword
    Press Keys    id=keyword    ENTER
    Wait Until Page Does Not Contain    ${P_EDIT_NAME}
    Close Browser

*** Keywords ***
Connexion Admin
    Open Browser    ${ADMIN_URL}    chrome
    Maximize Browser Window
    Input Text    id=username    ${ADMIN_EMAIL}
    Input Text    id=password    ${ADMIN_PASSWORD}
    Click Button    id=login-button
    Wait Until Location Contains    /admin

Remplir formulaire produit (création)
    Input Text    id=name        ${P_NAME}
    Input Text    id=sku         ${P_SKU}
    Input Text    id=price       ${P_PRICE}
    Input Text    id=weight      ${P_WEIGHT}
    Input Text    id=qty         ${P_QTY}
    Input Text    id=urlKey      ${P_URL_KEY}
    Input Text    id=metaTitle   ${P_META_TITLE}
    Input Text    id=metaKeywords    ${P_META_KEYWORDS}
    Input Text    id=meta_description    ${P_META_DESC}
    Choose File    css:input[type='file']    ${P_IMAGE}
    Wait Until Page Contains Element    css:div.image-list div.image img

Remplir formulaire produit (modification)
    Input Text    id=name        ${P_EDIT_NAME}
    Input Text    id=price       ${P_EDIT_PRICE}
    Input Text    id=urlKey      ${P_EDIT_URL_KEY}
    Input Text    id=metaTitle   ${P_EDIT_META_TITLE}
    Input Text    id=metaKeywords    ${P_EDIT_META_KEYWORDS}
    Input Text    id=meta_description    ${P_EDIT_META_DESC}

Cliquer Save et vérifier succès
    Click Button    xpath=//button[contains(@class,'button') and contains(@class,'primary') and translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='save']
    Wait Until Page Contains Element    css:.Toastify__toast-body    timeout=10s
