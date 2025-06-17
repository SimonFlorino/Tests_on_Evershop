*** Settings ***

# Ici on inclut les librairies requises

Library    SeleniumLibrary
Test Setup    Open Browser    http://localhost:3000/    chrome
Test Teardown    Close Browser

*** Variables ***
# Ici on définit les variables au besoin

${URL}         http://localhost:3000/admin/login
${USER}        admin@mail.com
${PASSWORD}    admin123

*** Test Cases ***

Test
    Créer produit 

*** Keywords ***
Login Success
    Go To    http://localhost:3000/admin/login
    Input Text      name=email    admin@mail.com
    Input Text      name=password    admin123
    Click Button    css: .button.primary
    Wait Until Page Contains     Dashboard

# Login Fail
#     Go To    ${URL}
#     Input Text      name=email    ${USER}
#     Input Text      name=password    password
#     Click Button    css: .button.primary
#     Wait Until Page Contains Element    css=div.text-critical.py-4

Créer produit
    Login Success
    Wait Until Element Is Visible    xpath=//a[contains(., 'Products')]    5s
    Click Element                    xpath=//a[contains(., 'Products')]