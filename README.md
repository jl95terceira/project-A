Pico 8 BBS cart webscraper

# Get started
Tools to run this script:
<ul>
  <li>Python 3 - any more recent version with <code>typing</code></li>
  <li>Python package <code>beautifulsoup4</code>, installed via <code>pip install beautifulsoup4</code></li>
</ul>

The script is run like a Python script i.e.

<code>python pico8bb.py ...</code>

Arguments (positional):
<ol>
  <li>name of directory to which to save the carts</li>
  <li>index of page at which to start</li>
  <li>number of threads</li>
  <li>step factor, for if skipping pages makes sense (which it usually does not - better leave this at <code>1</code>)</li>
</ol>
