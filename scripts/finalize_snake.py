"""Add accessible labels and a reduced-motion rule to generated snk SVGs."""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]


def main():
    for theme in ('dark','light'):
        file=ROOT/'assets/generated'/f'contribution-snake-{theme}.svg'
        body=file.read_text()
        label='<title>Lokesh / animated contribution calendar</title>'
        motion='<style>@media(prefers-reduced-motion:reduce){*{animation:none!important}}</style>'
        body=body.replace(label,'').replace(motion,'')
        start=body.index('>')+1
        body=body[:start]+label+body[start:]
        body=body.replace('</svg>',motion+'</svg>')
        ET.fromstring(body)
        file.write_text(body+'\n')


if __name__=='__main__':
    main()
