import pandas as pd
import requests



def getNames(years = range(2010,2015), number = 'p', female = True, top = 10):
    url = 'https://www.ssa.gov/cgi-bin/popularnames.cgi'
    data = [0]*len(years)
    names = []

    for i in range(0, len(years)):
        payload = {'year': years[i], 'number': number, 'top': top}
        page = requests.post(url, data=payload)
        data[i] = pd.read_html(page.text)[2].drop(top)

        if (female == True):
            names += list(data[i]['Female name'])
        else:
            names += list(data[i]['Male name'])

    names = list(set(names))

    stats = {'Names' : names}
    ranks = {'Names' : names}

    for i in range(0, len(years)):
        if (female == True):
            tempnames = list(data[i]['Female name'])
            if (number == 'p'):
                tempstats = list(data[i]['Percent oftotal females'])
            else:
                tempstats = list(data[i]['Number of females'])
        else:
            tempnames = list(data[i]['Male name'])
            if (number == 'p'):
                tempstats = list(data[i]['Percent oftotal males'])
            else:
                tempstats = list(data[i]['Number of males'])      

        statsvec = ['NA']*len(names)
        ranksvec = ['NA']*len(names)

        for j in range(0,len(names)):
            if names[j] in tempnames:
                ind = tempnames.index(names[j])
                statsvec[j] = tempstats[ind]
                ranksvec[j] = ind+1

        stats[str(years[i])] = statsvec
        ranks[str(years[i])] = ranksvec

        stats = pd.DataFrame(stats)
        ranks = pd.DataFrame(ranks)
            
    return stats, ranks