Changes
=========
```
normalize_country_name -> match
match_country_name -> add
del_country_name -> del
```

Install
=========

```sh
git clone .../country_normalizer.git
cd country_normalizer
python3 setup.py sdist --formats=gztar
pip3 install dist/country_normalizer-{VERSION}.tar.gz
```

Usage
=======
```python
from country_normalizer.country import CountryNormalizer

with CountryNormalizer() as country_norm:
    ...
    country_norm.add(..)
    ...
    country_norm.match(..)
