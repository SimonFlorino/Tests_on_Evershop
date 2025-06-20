*** Variables ***

${URL_NEW_PRODUCT}   http://localhost:3000/admin/products/new
${URL_PRODUCTS}   http://localhost:3000/admin/products
${URL_ADMIN_LOGIN}         http://localhost:3000/admin/login
${URL_SOCKS}         http://localhost:3000/socks
${URL_USER_LOGIN}   http://localhost:3000/account/login
${URL_ACCOUNT}        http://localhost:3000/account

#Données de login admin
${USER}        admin@mail.com
${PASSWORD}    admin123

#Données de login client
${USER_CLIENT}        simon@simon.com
${PASSWORD_CLIENT}    simon123



#Variables Selenium
${BY}    selenium.webdriver.common.by.By