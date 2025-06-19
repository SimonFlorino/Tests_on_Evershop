*** Settings ***

Library    SeleniumLibrary
Resource    variables_environnement.robot

*** Variables ***

${SUBMIT_BUTTON}      css=button[type='submit']
${ERROR_MESSAGE}      css=div.field-error span.text-critical
${ACCOUNT_TITLE}      css=h1.page-heading-title
${USER_NAME}          css=div.account-details-name div:nth-child(2)

${ERROR_EMPTY_FIELD}  This field can not be empty
${ERROR_INVALID_EMAIL}  Invalid email

${VALID_EMAIL}        simon@simon.com
${VALID_PASSWORD}     simon123
${VALID_NAME}         Simon


*** Keywords ***

Login Client Success
    [Arguments]    ${user}    ${pwd}
    Go To    ${URL_USER_LOGIN}
    Wait Until Page Contains    Login
    Input Text      name=email    ${user}
    Input Text      name=password    ${pwd}
    Click Button    css=.button.primary
    # Go To    ${URL_ACCOUNT}
    # Vérifier Connexion Réussie

Vérifier Connexion Réussie
    Wait Until Location Contains    ${URL_ACCOUNT}    timeout=10s
    ${title}=    Wait Until Element Is Visible    ${ACCOUNT_TITLE}    timeout=10s
    Should Contain    ${title.text}    My Account
    ${name}=    Wait Until Element Is Visible    ${USER_NAME}    timeout=10s
    Should Be Equal    ${name.text}    ${VALID_NAME}

Vérifier Message D'erreur
    [Arguments]    ${expected_message}
    ${error}=    Wait Until Element Is Visible    ${ERROR_MESSAGE}    timeout=10s
    Should Be Equal    ${error.text}    ${expected_message}