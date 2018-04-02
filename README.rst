============
 lwn2pocket
============

This program is designed to weekly import LWN.net_ article to your Pocket_
account.

.. _LWN.net: https://lwn.net
.. _Pocket: https://pocket.co

How to use it
-------------

1. Install it using `python setup.py` or any method you like
2. You need to obtain a Pocket access token. Run `get-pocket-token.py` and
   follow the instructions.
3. Export those variables in your environment:

    export LWNNET_USERNAME=<username>
    export LWNNET_PASSWORD=<password>
    export POCKET_ACCESS_TOKEN=<token from get-pocket-token.py>

4. Run `lwn2pocket.py`


Contributions
-------------

This has been written has a neat hack during a sunny afternon in Sevilla. I
don't plan to make it perfect, but I'll be happy to get contributions and
improvements.
