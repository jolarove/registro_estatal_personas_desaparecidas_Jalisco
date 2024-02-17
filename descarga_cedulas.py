import chromedriver_autoinstaller
from selenium import webdriver
import pandas as pd
import time
import requests

root = 'https://version-publica-repd.jalisco.gob.mx' #url raíz
website = f'{root}/cedulas-de-busqueda' #url donde están las cédulas
repdUrl = f'{root}/estadisticas' #url donde se descarga el repd en versión pública

chromedriver_autoinstaller.install() #instalamos el driver
driver = webdriver.Chrome()

mesDescarga = 'enero' #Modificar cada mes previo a la descarga
rutaSalida = f'cedulas_jalisco/2024/{mesDescarga}' #definimos ruta de salida de las bases de datos

#intentamos abrir la base de datos de las cédulas, sino existe, la creamos
try:
     cedulasPublicadas = pd.read_csv(f'{rutaSalida}/cedulas_publicadas_{mesDescarga}.csv')
except:
     columnas = ['Nombre', 'Estatus', 'Fecha desaparición', 'Lugar', 'Edad', 'Sexo', 
                 'Género', 'Complexión', 'Estatura', 'Tez', 'Cabello', 'Ojos', 'Vestimenta', 
                 'Señas Particulares']
     cedulasPublicadas = pd.DataFrame(columns = columnas)
     cedulasPublicadas.to_csv(f'{rutaSalida}/cedulas_publicadas_{mesDescarga}.csv', index=False)

#tratamos de obtener el último registro en la base de datos cedulasPublicadas, sino existe, ponemos Sin información
try:
     ultimoRegistro = cedulasPublicadas['Nombre'].iloc[0]
     print(ultimoRegistro)
except:
     ultimoRegistro = 'Sin información'

#Abrimos el sitio donde están las cédulas, maximizamos ventana y esperamos a que cargue
driver.get(website)
driver.maximize_window()
time.sleep(5) #si da error, aumentar el tiempo de espera

#Ya que cargó, damos clic en el botón buscar para que muestre todas las cédulas y esperamos que cargue
buscar = driver.find_element(by="xpath", value="//button[@class='MuiButtonBase-root MuiIconButton-root MuiIconButton-sizeMedium css-18mwzm8']")
buscar.click()
time.sleep(10) #si da error, aumentar el tiempo de espera

#creamos las listas donde se almacenarán los datos extraidos
estatus = []
imagenes = []
nombres = []
edades = []
sexos = []
generos =[]
complexiones =[]
estaturas = []
teces = []
cabellos = []
ojos_ced = []
fechas = []
lugares = []
vestimentas = []
senias_des = []

#buscamos el panel de paginación y definimos el límite para el ciclo
paginacion = driver.find_element(by='xpath', value='//ul[@class="MuiPagination-ul css-nhb8h9"]')
paginas = paginacion.find_elements(by='tag name', value='li')
ultimaPagina = int(paginas[-2].text)
paginaActual = 1

#comenzamos la navegación y descargamos todo lo descargable
while paginaActual <= ultimaPagina:
    print(f'{paginaActual} {ultimaPagina}')
    try:
        cajaCedulas = driver.find_element(by='xpath', value='//div[1]/div[1]/div[2]/div/div[2]/div[2]')
        cedulas = cajaCedulas.find_elements(by='xpath', value='.//div[@class="MuiBox-root css-13pkf70"]')
        for cedula in cedulas:
            nombre = cedula.find_element(by='xpath', value='(.//div[contains(@class, "css-apx2uo")]//p[contains(@class, "css-445tfr")])[1]').text
            if nombre == ultimoRegistro:
                 print(f'{ultimoRegistro} {nombre}')
                 paginaActual = ultimaPagina
                 break
            else:
                nombres.append(nombre)
            estado = cedula.find_element(by='xpath', value='.//p[contains(@class, "css-k2vnwu")]').text
            estatus.append(estado)
            edad = cedula.find_element(by='xpath', value='(.//div[contains(@class, "css-apx2uo")]//p[contains(@class, "css-445tfr")])[2]').text
            edades.append(edad)
            sexo = cedula.find_element(by='xpath', value='(.//div[contains(@class, "css-1fwfo5s")]//table//tr[1]//td[2]//p)[1]').text
            sexos.append(sexo)
            genero = cedula.find_element(by='xpath', value='(.//div[contains(@class, "css-1fwfo5s")]//table//tr[1]//td[4]//p)[1]').text
            generos.append(genero)
            complexion = cedula.find_element(by='xpath', value='(.//div[contains(@class, "css-1fwfo5s")]//table//tr[2]//td[2]//p)[1]').text
            complexiones.append(complexion)
            estatura = cedula.find_element(by='xpath', value='(.//div[contains(@class, "css-1fwfo5s")]//table//tr[2]//td[4]//p)[1]').text
            estaturas.append(estatura)
            tez = cedula.find_element(by='xpath', value='(.//div[contains(@class, "css-1fwfo5s")]//table//tr[3]//td[2]//p)[1]').text
            teces.append(tez)
            cabello = cedula.find_element(by='xpath', value='(.//div[contains(@class, "css-1fwfo5s")]//table//tr[3]//td[4]//p)[1]').text
            cabellos.append(cabello)
            ojos = cedula.find_element(by='xpath', value='(.//div[contains(@class, "css-1fwfo5s")]//table//tr[4]//td[2]//p)[1]').text
            ojos_ced.append(ojos)
            fecha = cedula.find_element(by='xpath', value='(.//div[contains(@class, "css-1fwfo5s")]//table//tr[1]//td[2]//p)[2]').text
            fechas.append(fecha)
            lugar = cedula.find_element(by='xpath', value='(.//div[contains(@class, "css-1fwfo5s")]//table//tr[2]//td[2]//p)[2]').text
            lugares.append(lugar)
            vestimenta = cedula.find_element(by='xpath', value='(.//div[contains(@class, "css-1fwfo5s")]//table//tr[3]//td[2]//p)[2]').text
            vestimentas.append(vestimenta)
            try:
                senias = cedula.find_element(by='xpath', value='(.//div[contains(@class, "css-1fwfo5s")]//table//tr[4]//td[2]//p)[2]').text
                senias_des.append(senias)
            except:
                  senias_des.append('SIN DATOS')
            img = cedula.find_element(by='xpath', value='.//img[@alt="Imagen"]').get_attribute('src')
            imagenes.append(img)
        #damos clic en el botón siguiente página, siempre y cuando no estemos en la última
        if paginaActual != ultimaPagina:
            botonSiguiente = paginacion.find_element(by='xpath', value='.//li//button[@aria-label="Go to next page"]')
            botonSiguiente.click()
        paginaActual += 1
        time.sleep(1)
        

    except Exception as e:
            print(f'Error: {e}')

#Ahora abrimos el sitio donde se puede descargar la versión pública del repd y descargamos la base de datos xls
driver.get(repdUrl)
time.sleep(3)
link = driver.find_element(by='xpath', value='//div[contains(@class, "css-juyhm1")]//a').get_attribute('href')
respuesta = requests.get(link)
try:
     with open(f'{rutaSalida}/versión-pública_repd_{mesDescarga}.xls', 'wb') as archivo:
          archivo.write(respuesta.content)
except:
     print('No se pudo descargar el registro')

#cerramos el navegador web
driver.quit()

#creamos la base de datos con lo extraído de las cédulas de búsqueda
df = pd.DataFrame({'Nombre': nombres, 'Estatus':estatus, 'Fecha desaparición': fechas, 'Lugar': lugares, 'Edad': edades,
                   'Sexo': sexos, 'Género': generos, 'Complexión': complexiones, 'Estatura': estaturas,
                   'Tez': teces, 'Cabello': cabellos, 'Ojos': ojos_ced, 'Vestimenta': vestimentas,
                   'Señas Particulares': senias_des})
dfCedulas = pd.concat([df, cedulasPublicadas], ignore_index=True)
dfCedulas.to_csv(f'{rutaSalida}/cedulas_publicadas_{mesDescarga}.csv', index=False)

#Filtramos para generar una base de datos con personas localizadas
#Ojo, englobamos localizadas con y sin vida
dfLocalizadas = dfCedulas[(dfCedulas['Estatus'] == 'LOCALIZADA CON VIDA') \
                           | (dfCedulas['Estatus'] =='LOCALIZADA SIN VIDA')]
#Ahora filtramos para generar una base de datos sólo con personas localizadas sin vida
dfLocalizadasSinVida = dfCedulas[(dfCedulas['Estatus'] == 'LOCALIZADA SIN VIDA')]
#Por último, filtramos para generar la base de datos de las personas aún desaparecidas
dfDesaparecidos = dfCedulas[(dfCedulas['Estatus'] == 'SIN LOCALIZAR')]
#Guardamos las bases de datos en formato csv
dfLocalizadas.to_csv(f'{rutaSalida}/personas_localizadas_{mesDescarga}.csv', index=False)
dfLocalizadasSinVida.to_csv(f'{rutaSalida}/personas_localizadas_sin_vida_{mesDescarga}.csv', index=False)
dfDesaparecidos.to_csv(f'{rutaSalida}/personas_desaparecidas_{mesDescarga}.csv', index=False)