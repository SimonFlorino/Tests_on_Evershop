*** Settings ***

# Ici on inclut les librairies requises

Library    SeleniumLibrary
Resource    variables_environnement.robot


*** Keywords ***

Login Admin Success
    [Arguments]    ${user}    ${pwd}
    Go To    ${URL_ADMIN_LOGIN}
    Input Text      name=email    ${user}
    Input Text      name=password    ${pwd}
    Click Button    css=.button.primary
    Wait Until Page Contains     Dashboard

Login Admin Fail
    [Arguments]    ${user} 
    Go To    ${URL_ADMIN_LOGIN}
    Input Text      name=email    ${user}
    Input Text      name=password    passwordFAIL
    Click Button    css=.button.primary
    Wait Until Page Contains Element    css=div.text-critical.py-4

