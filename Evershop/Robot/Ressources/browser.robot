*** Settings ***
Library    SeleniumLibrary

*** Keywords ***
Ouvrir Navigateur Personnalisé
    ${prefs}=    Create Dictionary
    ...    profile.default_content_setting_values.notifications=2
    ...    profile.default_content_setting_values.geolocation=2
    ...    profile.default_content_setting_values.popups=2

    ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${options}    add_argument    --incognito
    Call Method    ${options}    add_argument    --disable-popup-blocking
    Call Method    ${options}    add_argument    --disable-notifications
    Call Method    ${options}    add_experimental_option    prefs    ${prefs}
    
    Create WebDriver    Chrome    options=${options}
    Go To    http://localhost:3000/
    Maximize Browser Window

Fermer Navigateur Personnalisé
    Close Browser
