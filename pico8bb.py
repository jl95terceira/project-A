import bs4
import itertools
import os
import os.path
import re
import threading
from   urllib.request import urlopen as urlopen

_ROOT             = "https://www.lexaloffle.com"
_POSTS_N_EXPECTED = 30

def run(dump_dir    :str, 
        page_n_start:int, 
        page_n_step :int):

    print("Begin cart scraping run on Lexaloffle BBS")
    no_posts_count = 0
    for page_n in itertools.count(page_n_start, step=page_n_step):

        page_url = f"{_ROOT}/bbs/?sub=0&page={page_n}&mode=carts&cat=7"
        print(f"Requesting page #{page_n}: {repr(page_url)}")
        try:
        
            page = urlopen(page_url).read().decode()
        
        except Exception as exc:

            print(f"  Error on request for page #{page_n}: {exc}\n  Moving on...")

        post_ids:list[str] = list(re.findall("\\?tid=([0-9]+)", page))
        if not post_ids:

            no_posts_count += 1

        else:

            no_posts_count = 0

        if no_posts_count >= 5:

            print("  No posts found for a few pages consecutively\n  Probably, no more posts to be had")
            break

        if len(post_ids) != _POSTS_N_EXPECTED:

            print(f"  Number of posts different than expected on page #{page_n} - {len(post_ids)} instead of {_POSTS_N_EXPECTED}")

        for post_id in post_ids:

            post_url = f"{_ROOT}/bbs/?tid={post_id}"
            print(f"  Requesting post #{post_id}: {repr(post_url)}")
            try:
            
                post = urlopen(post_url)

            except Exception as exc:

                print(f"    Error on request for post #{post_id}: {exc}\n    Moving on...")
                continue
            
            cart_el  = bs4.BeautifulSoup(post, "html.parser").find("a", {"title": "Open Cartridge File"})
            if cart_el is None:

                print(f"    Cart element not found in post #{post_id}")

            try:
            
                cart_hr  = cart_el["href"]

            except:

                print(f"    Cart URL not found in supposed cart element in post #{post_id}")
                continue
                
            cart_url = f"{_ROOT}{cart_hr}"
            cart_fn  = os.path.join(dump_dir, cart_url.split("/")[-1])
            if os.path.exists(cart_fn): 
                
                continue

            os.makedirs(dump_dir, exist_ok=True)
            print(f"    Requesting cart at {repr(cart_url)}")
            try:
            
                cart = urlopen(cart_url).read()

            except Exception as exc:

                print(f"      Error on request for cart at {repr(cart_url)}: {exc} - moving on")
                continue
                
            try:
            
                with open(cart_fn, "wb") as fd:

                    fd.write(cart)

            except Exception as exc:

                print(f"      Error on saving cart to {repr(cart_fn)}: {exc} - moving on")
                continue
            
            print(f"      Saved cart at {repr(cart_url)} to {repr(cart_fn)}")
                        
    print("End")

def run_multi(dump_dir   :str,
              page_start :int=1,
              threads_n  :int=20,
              step_factor:int=1):
    
    for i in range(threads_n):

        threading.Thread(target=lambda: run(
            dump_dir, 
            page_n_start=i+page_start, 
            page_n_step =step_factor*threads_n
            )).start()

if __name__ == "__main__":

    import sys
    run_multi(
        dump_dir   =    sys.argv[1], 
        page_start =int(sys.argv[2]), 
        threads_n  =int(sys.argv[3]),
        step_factor=int(sys.argv[4]),
        )
