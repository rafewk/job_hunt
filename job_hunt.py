from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests

remoteOptions = ['y', 'n']
experienceOptions = ['j', 'm', 's']
availablePositions = ['tester', 'data']

onlyRemote = None
experienceLevel = None
position = None

justJoinURL = 'https://justjoin.it/'
noFluffURL = 'https://nofluffjobs.com'
bulldogURL = 'https://bulldogjob.pl/companies/jobs/s/'
solidURL = 'https://solid.jobs/offers/it;'

justJoinFullUrl = None
noFluffFullUrl = None
bulldogFullUrl = None
solidFullUrl = None

justJoin = []
noFluff = []
bulldog = []
solid = []


def printLogoAndTitle():
    print('\n        (⌐■_■)︻╦╤─ - - - $$')
    print('++++++++++|| JOB HUNT ||++++++++++\n')


def printFinalMsg():
    print('\n++++++++++|| LET THE HUNT BEGIN ||++++++++++')


def getUserInput():
    global onlyRemote
    global experienceLevel
    global position

    invalidRemote = 'Invalid input for remote option - try again!'
    invalidExp = 'Invalid input for exp level - try again!'
    invalidPosition = 'Invalid input for position - try again!'

    remoteMsg = 'Only remote jobs? (y/n): '
    expMsg = 'Exp level (j/m/s): '
    positionMsg = 'Pick a position: '
    positions = 'Available positions:\n-tester\n-data'

    onlyRemote = input(remoteMsg)
    while onlyRemote not in remoteOptions:
        print(invalidRemote)
        onlyRemote = input(remoteMsg)

    experienceLevel = input(expMsg)
    while experienceLevel not in experienceOptions:
        print(invalidExp)
        experienceLevel = input(expMsg)

    print(positions)
    position = input(positionMsg)
    while position not in availablePositions:
        print(invalidPosition)
        print(positions)
        position = input(positionMsg)


def getJustJoinFullUrl():
    print('\n  ~Creating a url for JustJoinIt...')
    global justJoinFullUrl
    if position == 'tester':
        if onlyRemote == 'y':
            if experienceLevel == 'j':
                endpoint = 'remote/testing/junior'
            elif experienceLevel == 'm':
                endpoint = 'remote/testing/mid'
            else:
                endpoint = 'remote/testing/senior'
        else:
            if experienceLevel == 'j':
                endpoint = 'all/testing/junior'
            elif experienceLevel == 'm':
                endpoint = 'all/testing/mid'
            else:
                endpoint = 'all/testing/senior'
    elif position == 'data':
        if onlyRemote == 'y':
            if experienceLevel == 'j':
                endpoint = 'remote/data/junior'
            elif experienceLevel == 'm':
                endpoint = 'remote/data/mid'
            else:
                endpoint = 'remote/data/senior'
        else:
            if experienceLevel == 'j':
                endpoint = 'all/data/junior'
            elif experienceLevel == 'm':
                endpoint = 'all/data/mid'
            else:
                endpoint = 'all/data/senior'
    justJoinFullUrl = justJoinURL + endpoint
    print('\n  ~JustJoinIt url created')


def getJustJoinData():
    print('\n  ~Getting data from JustJoinIt...')
    global justJoin
    linksLocator = 'div.css-110u7ph div.css-110u7ph a'
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(justJoinFullUrl)

    linkTags = driver.find_elements(By.CSS_SELECTOR, linksLocator)
    for i in range(len(linkTags)):
        justJoin.append(linkTags[i].get_attribute("href"))
    if len(justJoin) > 0:
        print('\n  ~JustJoinIt data fetched')
    else:
        print("\n [ERROR] Fetching data from JustJoinIt has failed - check the locator")
    driver.quit()


def getNoFluffFullUrl():
    print('\n  ~Creating a url for NoFluffJobs...')
    global noFluffFullUrl
    if position == 'tester':
        if onlyRemote == 'y':
            if experienceLevel == 'j':
                endpoint = '/pl/praca-zdalna/testing?criteria=seniority%3Djunior'
            elif experienceLevel == 'm':
                endpoint = '/pl/praca-zdalna/testing?criteria=seniority%3Dmid'
            else:
                endpoint = '/pl/praca-zdalna/testing?criteria=seniority%3Dsenior'
        else:
            if experienceLevel == 'j':
                endpoint = '/pl/testing?criteria=seniority%3Djunior'
            elif experienceLevel == 'm':
                endpoint = '/pl/testing?criteria=seniority%3Dmid'
            else:
                endpoint = '/pl/testing?criteria=seniority%3Dsenior'
    elif position == 'data':
        if onlyRemote == 'y':
            if experienceLevel == 'j':
                endpoint = '/pl/praca-zdalna/business-intelligence?criteria=category%3Dbusiness-analyst%20seniority%3Djunior'
            elif experienceLevel == 'm':
                endpoint = '/pl/praca-zdalna/business-intelligence?criteria=category%3Dbusiness-analyst%20seniority%3Dmid'
            else:
                endpoint = '/pl/praca-zdalna/business-intelligence?criteria=category%3Dbusiness-analyst%20seniority%3Dsenior'
        else:
            if experienceLevel == 'j':
                endpoint = '/pl/business-intelligence?criteria=category%3Dbusiness-analyst%20seniority%3Djunior'
            elif experienceLevel == 'm':
                endpoint = '/pl/business-intelligence?criteria=category%3Dbusiness-analyst%20seniority%3Dmid'
            else:
                endpoint = '/pl/business-intelligence?criteria=category%3Dbusiness-analyst%20seniority%3Dsenior'
    noFluffFullUrl = noFluffURL + endpoint
    print('\n  ~NoFluffJobs url created')


def getNoFluffData():
    print('\n  ~Getting data from NoFluffJobs...')
    global noFluff
    linksLocator = 'div.list-container a.posting-list-item'
    src = requests.get(noFluffFullUrl)
    checkStatus = src.status_code
    if checkStatus != 200:
        print(f'\n [ERROR] Fetching data from JustJoinIt has failed with a status_code: {checkStatus}')
    else:
        pageContent = src.content
        soup = bs(pageContent, 'lxml')
        noFluffLinks = soup.select(linksLocator)

        for link in noFluffLinks:
            noFluff.append(noFluffURL + link.attrs['href'])
        if len(noFluff) > 0:
            print('\n  ~NoFluffJobs data fetched')
        else:
            print('\n [ERROR] Fetching data from JustJoinIt has failed - check the locator')


def getBulldogFullUrl():
    print('\n  ~Creating a url for BulldogJob...')
    global bulldogFullUrl
    if position == 'tester':
        if onlyRemote == 'y':
            if experienceLevel == 'j':
                endpoint = 'city,Remote/role,qa,tester/experienceLevel,junior'
            elif experienceLevel == 'm':
                endpoint = 'city,Remote/role,qa,tester/experienceLevel,medium'
            else:
                endpoint = 'city,Remote/role,qa,tester/experienceLevel,senior'
        else:
            if experienceLevel == 'j':
                endpoint = 'role,qa,tester/experienceLevel,junior'
            elif experienceLevel == 'm':
                endpoint = 'role,qa,tester/experienceLevel,medium'
            else:
                endpoint = 'role,qa,tester/experienceLevel,senior'
    elif position == 'data':
        if onlyRemote == 'y':
            if experienceLevel == 'j':
                endpoint = 'city,Remote/role,analyst,data/experienceLevel,junior'
            elif experienceLevel == 'm':
                endpoint = 'city,Remote/role,analyst,data/experienceLevel,medium'
            else:
                endpoint = 'city,Remote/role,analyst,data/experienceLevel,senior'
        else:
            if experienceLevel == 'j':
                endpoint = 'role,analyst,data/experienceLevel,junior'
            elif experienceLevel == 'm':
                endpoint = 'role,analyst,data/experienceLevel,medium'
            else:
                endpoint = 'role,analyst,data/experienceLevel,senior'
    bulldogFullUrl = bulldogURL + endpoint
    print('\n  ~BulldogJob url created')


def getBulldogData():
    print('\n  ~Getting data from BulldogJob...')
    global bulldog
    linksLocator = 'div.container a:not(.h-full)'
    src = requests.get(bulldogFullUrl)
    checkStatus = src.status_code
    if checkStatus != 200:
        print(f'\n [ERROR] Fetching data from BulldogJob has failed with a status_code: {checkStatus}')
    else:
        pageContent = src.content
        soup = bs(pageContent, 'lxml')
        bulldogLinks = soup.select(linksLocator)

        for link in bulldogLinks:
            bulldog.append(link.attrs['href'])
        if len(bulldog) > 0:
            print('\n  ~BulldogJob data fetched')
        else:
            print('\n [ERROR] Fetching data from BulldogJob has failed - check the locator')


def getSolidFullUrl():
    print('\n  ~Creating a url for SolidJobs...')
    global solidFullUrl
    if position == 'tester':
        if onlyRemote == 'y':
            if experienceLevel == 'j':
                endpoint = 'cities=Praca%20zdalna;categories=Tester;experiences=Junior'
            elif experienceLevel == 'm':
                endpoint = 'cities=Praca%20zdalna;categories=Tester;experiences=Regular'
            else:
                endpoint = 'cities=Praca%20zdalna;categories=Tester;experiences=Senior'
        else:
            if experienceLevel == 'j':
                endpoint = 'categories=Tester;experiences=Junior'
            elif experienceLevel == 'm':
                endpoint = 'categories=Tester;experiences=Regular'
            else:
                endpoint = 'categories=Tester;experiences=Senior'
    elif position == 'data':
        if onlyRemote == 'y':
            if experienceLevel == 'j':
                endpoint = 'cities=Praca%20zdalna;categories=Analityk;experiences=Junior'
            elif experienceLevel == 'm':
                endpoint = 'cities=Praca%20zdalna;categories=Analityk;experiences=Regular'
            else:
                endpoint = 'cities=Praca%20zdalna;categories=Analityk;experiences=Senior'
        else:
            if experienceLevel == 'j':
                endpoint = 'categories=Analityk;experiences=Junior'
            elif experienceLevel == 'm':
                endpoint = 'categories=Analityk;experiences=Regular'
            else:
                endpoint = 'categories=Analityk;experiences=Senior'
    solidFullUrl = solidURL + endpoint
    print('\n  ~SolidJobs url created')


def getSolidData():
    print('\n  ~Getting data from SolidJobs...')
    global solid
    linksLocator = 'offer-list-item h2 a'

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(solidFullUrl)

    linkTags = driver.find_elements(By.CSS_SELECTOR, linksLocator)
    for i in range(len(linkTags)):
        solid.append(linkTags[i].get_attribute("href"))
    if len(solid) > 0:
        print('\n  ~SolidJobs data fetched')
    else:
        print("\n [ERROR] Fetching data from SolidJobs has failed - check the locator")
    driver.quit()


def openLinksInBrowser(linksList: list):
    if len(linksList) != 0:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(linksList[0])

        if len(linksList) > 1 and len(linksList) > 5:
            for i in range(1, 5):
                driver.execute_script('window.open()')
                driver.switch_to.window(driver.window_handles[i])
                driver.get(linksList[i])
        elif 1 < len(linksList) <= 5:
            for i in range(1, len(linksList)):
                driver.execute_script('window.open()')
                driver.switch_to.window(driver.window_handles[i])
                driver.get(linksList[i])


if __name__ == "__main__":
    printLogoAndTitle()

    getUserInput()

    getJustJoinFullUrl()
    getNoFluffFullUrl()
    getBulldogFullUrl()
    getSolidFullUrl()

    getJustJoinData()
    getNoFluffData()
    getBulldogData()
    getSolidData()

    openLinksInBrowser(justJoin)
    openLinksInBrowser(noFluff)
    openLinksInBrowser(bulldog)
    openLinksInBrowser(solid)

    printFinalMsg()


