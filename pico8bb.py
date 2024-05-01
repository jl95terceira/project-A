# standard
import itertools
import os
import os.path
import re
import threading
from   urllib.request import urlopen
# third-party
import bs4

_WEBSITE          = "https://www.lexaloffle.com"
_POSTS_N_EXPECTED = 30

def run(dump_dir    :str, 
        page_n_start:int, 
        page_n_step :int):

    print("Begin cart scraping run on Lexaloffle BBS")
    carts_saved_n = 0
    no_posts_n    = 0
    for page_n in itertools.count(page_n_start, step=page_n_step):

        page_url = f"{_WEBSITE}/bbs/?sub=0&page={page_n}&mode=carts&cat=7"
        print(f"Requesting page #{page_n}: {repr(page_url)}")
        try:
        
            page = urlopen(page_url).read().decode()
        
        except Exception as exc:

            print(f"  Error on request for page #{page_n}: {exc}\n  Moving on...")

        post_ids:list[str] = list(re.findall("\\?tid=([0-9]+)", page))
        if not post_ids:

            no_posts_n += 1

        else:

            no_posts_n = 0

        if no_posts_n >= 5:

            print("  No posts found for a few pages consecutively\n  Probably, no more posts to be had")
            break

        if len(post_ids) != _POSTS_N_EXPECTED:

            print(f"  Number of posts different than usual on page #{page_n} - {len(post_ids)} instead of {_POSTS_N_EXPECTED}")

        for post_id in post_ids:

            post_url = f"{_WEBSITE}/bbs/?tid={post_id}"
            print(f"  Requesting post #{post_id}: {repr(post_url)}")
            try:
            
                post = urlopen(post_url)

            except Exception as exc:

                print(f"    Error on request for post #{post_id} at {post_url}: {exc}\n    Moving on...")
                continue
            
            cart_element = bs4.BeautifulSoup(post, "html.parser").find("a", {"title": "Open Cartridge File"})
            if cart_element is None:

                print(f"    Cart element not found in post #{post_id}")

            try:
            
                cart_href  = cart_element["href"]

            except:

                print(f"    Cart URL not found in supposed cart element in post #{post_id}")
                continue
                
            cart_url       = f"{_WEBSITE}{cart_href}"
            cart_file_name = os.path.join(dump_dir, cart_url.split("/")[-1])
            if os.path.exists(cart_file_name): 
                
                continue

            os.makedirs(dump_dir, exist_ok=True)
            print(f"    Requesting cart at {repr(cart_url)}")
            try:
            
                cart = urlopen(cart_url).read()

            except Exception as exc:

                print(f"      Error on request for cart at {repr(cart_url)}: {exc} - moving on")
                continue
                
            try:
            
                with open(cart_file_name, "wb") as cart_file:

                    cart_file.write(cart)

            except Exception as exc:

                print(f"      Error on saving cart to {repr(cart_file_name)}: {exc} - moving on")
                continue
            
            print(f"      Saved cart at {repr(cart_url)} to {repr(cart_file_name)}")
            carts_saved_n += 1
                        
    print(f"End\nNumber of carts saved during this run: {carts_saved_n}")
    return carts_saved_n

def run_multi(dump_dir   :str,
              page_start :int,
              threads_n  :int=1,
              step_factor:int=1):
    
    n = 0
    for i in range(threads_n):

        threading.Thread(target=lambda: run(dump_dir, 
                                            page_n_start=i+page_start, 
                                            page_n_step =step_factor*threads_n)).start()

if __name__ == "__main__":

    import argparse

    class A:

        DOWNLOAD_DIRECTORY = 'dir'
        PAGE_START         = 'p'
        THREADS_N          = 'th'
        STEP_FACTOR        = 'step'

    class DEFAULTS:

        THREADS_N           = 8
        DOWNLOADS_DIRECTORY = os.path.join(os.path.expanduser('~'), 'Downloads', 'PICO-8 Carts')

    def assertInt(value:str|int):

        try:    return int(value)
        except: raise argparse.ArgumentTypeError(f'given value {repr(value)} is not integer-like')

    p = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                description    ='Download PICO-8 game carts from the official billboard, hosted at: https://www.lexaloffle.com/bbs/')
    p.add_argument(f'--{A.DOWNLOAD_DIRECTORY}',
                   help   =f'directory to which to download the carts\nDefaults to {DEFAULTS.DOWNLOADS_DIRECTORY}.',
                   default=DEFAULTS.DOWNLOADS_DIRECTORY)
    p.add_argument(f'--{A.PAGE_START}',
                   help   =f'billboard page at which to start scraping\nDefaults to 1 (the 1st page).',
                   type   =assertInt,
                   default=1)
    p.add_argument(f'--{A.THREADS_N}',
                   help   =f'nr of threads to start\nDefaults to {DEFAULTS.THREADS_N}.',
                   type   =assertInt,
                   default=DEFAULTS.THREADS_N)
    p.add_argument(f'--{A.STEP_FACTOR}',
                   help   =f'how many pages to jump between each request\nMay be useful in very specific cases but, usually, best left as default (1 = no over-stepping).',
                   type   =assertInt,
                   default=1)
    # parse args
    def get(a:str, _args=p.parse_args()): return getattr(_args,a)
    # do it
    run_multi(dump_dir   =get(A.DOWNLOAD_DIRECTORY), 
              page_start =get(A.PAGE_START), 
              threads_n  =get(A.THREADS_N),
              step_factor=get(A.STEP_FACTOR))
