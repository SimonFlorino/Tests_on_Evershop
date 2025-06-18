*** Settings ***

# Ici on inclut les librairies requises

Library    SeleniumLibrary
Library    OperatingSystem
Test Setup    Open Browser    http://localhost:3000/    chrome
Test Teardown    Close Browser

*** Variables ***
#Données de login
${URL}         http://localhost:3000/admin/login
${USER}        admin@mail.com
${PASSWORD}    admin123

${NEW_PRODUCT_URL}   http://localhost:3000/admin/products/new
${PRODUCTS_URL}   http://localhost:3000/admin/products

# Données produit pour la création
${P_NAME}            Chaussette
${P_SKU}             sock_123
${P_PRICE}           20
${P_WEIGHT}          0.1
${P_QTY}             100
${P_URL_KEY}         socks
${P_META_TITLE}      Belle chaussette
${P_META_KEYWORDS}   sock
${P_META_DESC}       sock
${P_IMAGE}           C:/Tools/Tests_Selenium/Evershop/Images/sock.png

*** Test Cases ***

Test
    Créer produit

*** Keywords ***
Login Success
    Go To    ${URL}
    Input Text      name=email    ${USER}
    Input Text      name=password    ${PASSWORD}
    Click Button    css: .button.primary
    Wait Until Page Contains     Dashboard

Login Fail
    Go To    ${URL}
    Input Text      name=email    ${USER}
    Input Text      name=password    password
    Click Button    css: .button.primary
    Wait Until Page Contains Element    css=div.text-critical.py-4


Créer produit
    Login Success
    Wait Until Element Is Visible    xpath=//a[contains(., 'Products')]    5s
    Click Element                    xpath=//a[contains(., 'Products')]
    Location Should Be    ${PRODUCTS_URL}
    Click Link    New Product
    Location Should Be    ${NEW_PRODUCT_URL}
    # Remplir les champs
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

    #Save et vérifier succès
    Click Button    xpath=//button[contains(@class,'button') and contains(@class,'primary') and translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')='save']
    Wait Until Page Contains Element    css:.Toastify__toast-body    timeout=10s