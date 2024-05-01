Pico 8 BBS cart webscraper - for those who like retro-style fantasy-console gaming

# Get started
Install:
<ul>
  <li>Python ≥ 3.12
  <li>Python package <code>beautifulsoup4</code>, installed via <code>pip install beautifulsoup4</code></li>
</ul>

To run <code>pico8bb.py</code>, call

```
python pico8bb.py ...
```

or, if you set <code>.py</code> files to open with Python by default, simply call

```
pico8bb.py ...
```

The script can be run straight away without arguments but there are options to customize its behaviour. For help, call the script with option <code>-h</code> like so.

```
pico8bb.py -h
```

Help text:

```
usage: pico8bb.py [-h] [--dir DIR] [--p P] [--th TH] [--step STEP]

Download PICO-8 game carts from the official billboard, hosted at: https://www.lexaloffle.com/bbs/

options:
  -h, --help   show this help message and exit
  --dir DIR    directory to which to download the carts
               Defaults to C:\Users\ec01046a\Downloads\PICO-8 Carts.
  --p P        billboard page at which to start scraping
               Defaults to 1 (the 1st page).
  --th TH      nr of threads to start
               Defaults to 8.
  --step STEP  how many pages to jump between each request
               May be useful in very specific cases but, usually, best left as default (1 = no over-stepping).
```
