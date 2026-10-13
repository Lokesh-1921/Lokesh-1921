"""A matching animated dashboard; metric values and charts stay immutable."""
from collections import Counter
from .shared import PALETTES, text, rect, path, circle, surface, motion, trace, svg


def project_languages(data):
    return Counter(repo['language'] for repo in data['repositories']
                   if not repo['fork'] and repo['language']
                   and not repo.get('is_profile',repo.get('name','').lower()==data['owner'].lower()))


def dashboard(data, theme, mobile=False):
    p=PALETTES[theme]
    w,h=(600,940) if mobile else (1200,620)
    days=data['days']
    values=[('PUBLIC REPOSITORIES',len(data['repositories'])),
            ('CONTRIBUTIONS / LAST YEAR',sum(d['count'] for d in days)),
            ('ACTIVE CALENDAR DAYS',sum(d['count']>0 for d in days))]
    labels=[['PUBLIC','REPOSITORIES'],['CONTRIBUTIONS','LAST YEAR'],['ACTIVE DAYS','IN THE CALENDAR']]
    body=surface(p,w,h)+motion(w)
    body+=text(28,44,'PUBLIC GITHUB / DAILY SNAPSHOT',22,p['cyan'],600,'letter-spacing="1"')
    for i,(_,value) in enumerate(values):
        x,y=(28,76+i*136) if mobile else (28+i*390,80)
        body+=rect(x,y,544 if mobile else 364,115 if mobile else 174,p['panel'],p['border'])
        display=f'{value:,}'
        size=min(64,310/max(1,len(display))) if mobile else 64
        body+=text(x+22,y+(77 if mobile else 83),display,size,p['text'],600)
        for j,label in enumerate(labels[i]):
            body+=text(x+214 if mobile else x+22,y+(46 if mobile else 120)+j*29,label,22 if mobile else 20,p['muted'],500)
        body+=circle(x+(519 if mobile else 337),y+23,3,p['cyan'],'class="pulse" opacity=".4"')
    languages=project_languages(data);total=sum(languages.values())
    ly=514 if mobile else 299
    body+=text(28,ly,'PRIMARY PROJECT LANGUAGES',22,p['muted'],600,'letter-spacing=".7"')
    colors=[p['cyan'],p['violet'],'#49AFC4','#7D6BAD','#7FA3B8','#557A91']
    x=28
    for i,(language,count) in enumerate(languages.most_common()):
        width=(w-56)*count/total if total else 0
        body+=rect(round(x,2),ly+22,round(width,2),14,colors[i%len(colors)],radius=0)
        x+=width
        lx=28+(i%2)*280 if mobile else 28+(i%5)*230
        yy=ly+77+(i//2)*35 if mobile else ly+81+(i//5)*30
        body+=circle(lx+4,yy-7,4,colors[i%len(colors)])
        body+=text(lx+17,yy,f'{language} · {count}/{total}',22,p['text'])
    cy=725 if mobile else 438
    body+=text(28,cy,'WEEKLY CONTRIBUTIONS / LAST YEAR',20,p['muted'],500,'letter-spacing=".5"')
    weekly=Counter()
    for day in days:weekly[day.get('x',0)]+=day['count']
    n=max(weekly,default=0)+1;maximum=max(weekly.values(),default=0)
    step=(w-56)/n;floor=cy+110
    for y in (floor-80,floor-40,floor):body+=path(f'M28 {y}H{w-28}',p['border'],'stroke-opacity=".6"')
    for week,count in sorted(weekly.items()):
        if count:
            bh=78*count/maximum
            body+=f'<g><title>Calendar week {week+1}: {count} contributions</title>'+rect(round(28+week*step,2),round(floor-bh,2),round(max(1,step-4),2),round(bh,2),p['cyan'],radius=2,extra='fill-opacity=".62"')+'</g>'
    # A moving scan accent crosses the chart; bars do not grow or invent activity.
    if maximum:
        body+='<g clip-path="url(#panel-clip)">'+rect(28,cy+27,2,84,p['cyan'],radius=1,extra='class="scan" opacity=".06"')+'</g>'
    body+=trace(p,28,h-57,w-56,9)
    body+=text(28,h-25,'SNAPSHOT / '+data['updated_at'][:10]+' UTC',21 if mobile else 19,p['muted'])
    if not mobile:body+=text(w-28,h-25,'PUBLIC DATA / NO RANKS / NO ESTIMATES',18,p['muted'],400,'text-anchor="end"')
    desc='; '.join(f'{label.lower()}: {value}' for label,value in values)
    desc+='. Primary languages count non-fork project repositories and exclude this profile. Weekly bars show actual calendar contribution counts. Updated '+data['updated_at'][:10]+'.'
    return svg(w,h,body,'HUMAN / GitHub intelligence dashboard',desc)
