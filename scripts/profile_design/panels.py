"""Reusable role, navigation, technical-system, and learning modules."""
from .shared import PROFILE, text, rect, path, circle, surface, motion, trace, icon, arrow


def role(p, compact):
    w,h=(600,212) if compact else (1200,156)
    body=surface(p,w,h)+motion(w)
    x=32 if compact else 40
    body+=text(x,39 if compact else 33,'CURRENT DIRECTION',19,p['cyan'],600,'letter-spacing="1.8"')
    body+=text(x,91 if compact else 81,PROFILE['role'],36 if compact else 40,p['text'],600,'letter-spacing=".4" data-role-title="true"')
    body+=text(x,132 if compact else 121,PROFILE['support'],23,p['muted'])
    if compact:
        body+=trace(p,32,177,536,3)
        for x in (32,300,568):body+=circle(x,177,3,p['cyan'])
    else:
        body+=path('M800 82H1128',p['border'],'stroke-width="1.5"')
        for i,label in enumerate(('Python','ML','GenAI')):
            x=790+i*120
            body+=rect(x,58,100,54,p['panel'],p['border'],12)
            body+=rect(x,58,100,54,'none',p['cyan'],12,f'class="pulse" opacity=".35" style="animation-delay:-{i*3}s"')
            body+=text(x+50,92,label,21,p['text'],500,'text-anchor="middle"')
        body+=trace(p,790,129,340,3)
    return w,h,body


def section_header(p, compact, number, data):
    w,h=(600,136) if compact else (1200,104)
    body=surface(p,w,h)+motion(w)
    body+=rect(24,29 if compact else 25,62,50,p['cyan'],radius=12,extra='fill-opacity=".07"')
    body+=text(55,63 if compact else 59,f'{number:02}',25,p['cyan'],600,'text-anchor="middle"')
    lines=data['mobile'] if compact else [data['title']]
    for i,line in enumerate(lines):
        y=(63+i*37 if len(lines)>1 else 76) if compact else 62
        body+=text(108 if compact else 116,y,line,28 if compact else 32,p['text'],600,'letter-spacing=".3" data-section-title="true"')
    body+=trace(p,24,h-12,w-48,number*2)
    if not compact:
        body+=circle(1140,49,4,p['cyan'],'class="pulse" opacity=".5"')
        body+=circle(1160,49,3,p['violet'])
    return w,h,body


def technical_systems(p, compact):
    w,h=(600,1060) if compact else (1200,640)
    body=surface(p,w,h)+motion(w)
    body+=text(28,43,'TOOLS IN PUBLIC PROJECTS',22,p['cyan'],600,'letter-spacing="1"')
    body+=rect(28,76,w-56,212 if compact else 134,p['panel'],p['border'])
    body+=icon('python',44,112 if compact else 106,68)
    body+=text(132,156 if compact else 140,'Python',40,p['text'],600)
    body+=text(132,188 if compact else 177,'PRIMARY LANGUAGE',19,p['muted'],500,'letter-spacing="1"')
    for i,(name,label) in enumerate([('typescript','TypeScript'),('javascript','JavaScript'),('java','Java')]):
        x=44+i*177 if compact else 725+i*145
        y=228 if compact else 105
        body+=icon(name,x,y,28 if compact else 38)
        body+=text(x+37 if compact else x+19,249 if compact else 177,label,21,p['text'],500,'' if compact else 'text-anchor="middle"')
    groups=[
        ('GENERATIVE AI + RETRIEVAL',['LangGraph · LangChain','FAISS · BM25'],p['violet']),
        ('DATA + BACKEND',['FastAPI · PostgreSQL','SQLAlchemy · Redis'],p['cyan']),
        ('AI / ML + NUMERICS',['NumPy · SciPy · Matplotlib','OpenCV in the vision project'],p['cyan']),
        ('APPLICATIONS + WORKFLOW',['React · Git · Vite','pytest · Vitest · Tailwind CSS'],p['violet']),
    ]
    for i,(label,lines,color) in enumerate(groups):
        x,y=(28,314+i*177) if compact else (28+(i%2)*586,246+(i//2)*178)
        cw=544 if compact else 558
        body+=rect(x,y,cw,155,p['panel'],p['border'])
        body+=rect(x+1,y+25,3,106,color,radius=1,extra='opacity=".7"')
        body+=text(x+24,y+38,label,23,p['text'],600)
        for j,line in enumerate(lines):body+=text(x+24,y+83+j*32,line,24,p['muted'])
        body+=path(f'M{x+cw-60} {y+30}H{x+cw-24}',color,'stroke-width="2" class="pulse" opacity=".4"')
    body+=trace(p,28,h-57,w-56,6)
    body+=text(28,h-24,'Applied in projects. Always learning.',21,p['muted'])
    return w,h,body


def exploring(p, compact):
    w,h=(600,882) if compact else (1200,410)
    body=surface(p,w,h,True)+motion(w)
    body+=text(32,44,'THE INTELLIGENCE LAB',23,p['text'],600,'letter-spacing="1"')
    if not compact:body+=text(1168,44,'LEARNING DIRECTIONS',20,p['cyan'],500,'text-anchor="end" letter-spacing="1"')
    topics=[
        ('ML FOUNDATIONS',['Measure. Learn.','Refine.'],['Data, evaluation,','and model fundamentals.']),
        ('GROUNDED GENERATION',['Context before','answers.'],['Retrieval and generative','workflows with source context.']),
        ('AGENTIC SYSTEMS',['Tools with clear','boundaries.'],['Routing, explicit context,','and useful actions.']),
    ]
    for i,(label,title,lines) in enumerate(topics):
        x,y=(32,82+i*234) if compact else (32+i*392,82)
        cw=536 if compact else 352
        body+=rect(x,y,cw,218 if compact else 244,p['panel'],p['border'])
        color=p['violet'] if i==1 else p['cyan']
        body+=text(x+22,y+36,label,21,p['muted'],600,'letter-spacing=".5"')
        for j,line in enumerate(title):body+=text(x+22,y+81+j*34,line,31 if compact else 28,p['text'],600)
        for j,line in enumerate(lines):body+=text(x+22,y+152+j*28,line,23 if compact else 21,p['muted'])
        body+=trace(p,x+22,y+(199 if compact else 220),cw-44,i*4)
        body+=circle(x+cw-23,y+36,3,color,'class="pulse" opacity=".5"')
    if compact:
        body+=text(32,815,'SIDE EXPLORATION / COMPUTER VISION',22,p['muted'],500)
        body+=text(32,850,'Learning through stereo geometry and motion.',22,p['muted'])
    else:
        body+=text(32,374,'SIDE EXPLORATION / COMPUTER VISION',21,p['muted'],500)
        body+=text(1168,374,'Learning through stereo geometry and motion.',21,p['muted'],400,'text-anchor="end"')
    return w,h,body


def connect_button(p, name, label):
    w,h=224,60
    body=surface(p,w,h)
    body+=rect(1,1,w-2,h-2,p['bg'],p['border'],22)
    body+=path('M22 59H202','url(#spectrum)','stroke-opacity=".55"')
    body+=icon(name,19,17,25,color=p['text'] if name=='github' else None)
    body+=text(57,37,label,20,p['text'],500)
    body+=arrow(p,182,23,12)
    return w,h,body
