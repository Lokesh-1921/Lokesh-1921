"""Build original profile modules from shared design primitives and verified content."""
from profile_design.shared import (
    PROFILE, PALETTES, text, surface, svg, variants, save,
)
from profile_design.hero import hero, closing
from profile_design.panels import role, section_header, technical_systems, exploring, connect_button
from profile_design.projects import project_card


def main():
    variants('hero/hero',hero,'HUMAN // LOKESH — Intelligence in Motion',
             'Lokesh. AI engineering, machine learning, generative AI. Turning curiosity into intelligent systems. Original orbit artwork, not measured model internals.')
    variants('modules/role-strip',role,'Aspiring AI Engineer',
             'Python, machine learning, generative AI. One immutable role heading; only decorative geometry animates.')
    for number,data in enumerate(PROFILE['sections'],1):
        variants(f'modules/section-{number:02}-{data["key"]}',
                 lambda p,m,n=number,d=data: section_header(p,m,n,d),
                 f'{number:02} / '+data['title'],'An animated section signal with stationary, accessible typography.')
    variants('dashboards/technical-systems',technical_systems,'Tools used in public projects',
             'Python at the core. Generative AI and retrieval, data and backend, numerical tools, applications and workflow. Tool usage is not a claim of mastery.')
    for number,project in enumerate(PROFILE['projects'],1):
        variants('projects/'+project['key'],
                 lambda p,m,d=project,n=number: project_card(p,m,d,n),
                 project['title'],' '.join(project['lines'])+' '+project['status']+'. Original conceptual schematic, not an application screenshot.')
    variants('modules/currently-exploring',exploring,'The Intelligence Lab',
             'Learning directions: machine learning foundations, grounded generation, agentic systems. Computer vision is a side exploration.')
    variants('modules/closing-banner',closing,'Curiosity drives the code. Impact shapes the system.',
             'HUMAN // LOKESH. An invitation to build something useful.')
    for name,label in [('linkedin','LinkedIn'),('github','GitHub')]:
        w,h,body=connect_button(PALETTES['dark'],name,label)
        save(f'modules/connect-{name}.svg',w,h,body,label,'Connect with Lokesh on '+label+'.')
    print('Built modular HUMAN hero, role, six headers, technical systems, four project cards, exploring panel, and closing.')


if __name__=='__main__':
    main()
