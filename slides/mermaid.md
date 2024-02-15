Palette:
https://coolors.co/palette/003049-d62828-f77f00-fcbf49-eae2b7

003049  blue
D62828  red
F77F00  orange
FCBF49  yellow
EAE2B7  beige

Packaging:

```mermaid
%%{init: {"flowchart": {"defaultRenderer": "elk"}} }%%
graph LR

dev[Developer<br>sources] --build--> Package --upload--> pypi[(Package<br>Index)]
pypi --discover &<br>download--> p2[Package] --> iswheel{is wheel?} 
iswheel --yes--> wheel[wheel] --Install-->t[Target<br>environment]
iswheel --"no? Build!"--> wheel

classDef default fill:#ddd,stroke:#ddd,stroke-width:0px;
classDef artifact fill:#FCBF49,stroke-width:0px;
classDef env fill:#003049,color:#fff;
class dev,t,pypi env;
class p2,Package,wheel artifact;
```
