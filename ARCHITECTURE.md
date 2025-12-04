# Architecture django-virtualqueryset

## 📁 Structure du projet

```
virtualqueryset/
├── queryset/
│   ├── __init__.py
│   ├── base.py          # InMemoryQuerySet - Core implementation
│   ├── config.py        # ConfigQuerySet - Django settings
│   ├── api.py           # APIQuerySet - External APIs
│   ├── json_qs.py       # JSONQuerySet - JSON data
│   └── cached.py        # CachedQuerySet - With caching
├── managers.py          # VirtualManager and specific managers
├── models.py            # VirtualModel base classes
├── apps.py              # Django app config
└── admin.py             # Admin utilities (TODO)
```

## 🎯 Types de QuerySet implémentés

### 1. **InMemoryQuerySet** (base.py)

QuerySet de base pour toutes les données en mémoire.

**Fonctionnalités** :
- ✅ Filtering avec lookups Django :
  - `exact`, `icontains`, `contains`
  - `in`, `gt`, `gte`, `lt`, `lte`
  - `isnull`, `startswith`, `istartswith`
  - `endswith`, `iendswith`
- ✅ `order_by()`, `reverse()`
- ✅ `filter()`, `exclude()`, `get()`
- ✅ `count()`, `exists()`, `first()`, `last()`
- ✅ `all()`, `none()`, `distinct()`
- ✅ `values()`, `values_list()`
- ✅ Slicing `[start:end]`
- ✅ Iteration

**Usage** :
```python
from virtualqueryset.queryset.base import InMemoryQuerySet

data = [MyModel(name="Alice", age=30), MyModel(name="Bob", age=25)]
qs = InMemoryQuerySet(model=MyModel, data=data)

# Django ORM-like API
qs.filter(age__gte=25).order_by('-age')
qs.get(name="Alice")
qs.count()
```

### 2. **ConfigQuerySet** (config.py)

Pour afficher les settings Django comme des modèles.

**Usage** :
```python
from virtualqueryset.queryset.config import ConfigQuerySet
from virtualqueryset.managers import ConfigQuerySetManager

class InstalledApp(VirtualModel):
    name = models.CharField(max_length=255)
    
    objects = ConfigQuerySetManager('INSTALLED_APPS')

# Dans l'admin, affiche la liste des apps installées
```

**Méthodes** :
- ✅ `reload()` - Recharge depuis settings
- ✅ Support dict, list, tuple depuis settings

### 3. **APIQuerySet** (api.py)

Pour données d'API externe avec cache automatique.

**Usage** :
```python
from virtualqueryset.managers import APIQuerySetManager
import requests

def fetch_github_repos():
    resp = requests.get('https://api.github.com/users/django/repos')
    return resp.json()

class GitHubRepo(VirtualModel):
    name = models.CharField(max_length=255)
    stars = models.IntegerField()
    
    objects = APIQuerySetManager(
        fetch_func=fetch_github_repos,
        cache_timeout=300  # 5 minutes
    )
```

**Fonctionnalités** :
- ✅ Cache automatique (default: 5 minutes)
- ✅ `refresh()` - Force reload depuis API
- ✅ Retry logic avec fallback sur cache

### 4. **JSONQuerySet** (json_qs.py)

Pour données JSON (fichiers ou dicts).

**Usage** :
```python
from virtualqueryset.managers import JSONQuerySetManager

class Product(VirtualModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField()
    
    # Depuis un fichier
    objects = JSONQuerySetManager('data/products.json')
    
    # Avec extraction de chemin
    objects = JSONQuerySetManager(
        'data/api_response.json',
        json_path='results.items'
    )
```

**Fonctionnalités** :
- ✅ Chargement depuis fichier JSON
- ✅ Parse de string JSON
- ✅ Support dict Python
- ✅ Extraction JSONPath simple (dot notation)
- ✅ `reload()` - Recharge depuis source

### 5. **CachedQuerySet** (cached.py)

Wrapper générique avec cache pour n'importe quelle source.

**Usage** :
```python
from virtualqueryset.managers import CachedQuerySetManager

def expensive_operation():
    # Calcul coûteux ou appel API lent
    return process_data()

class ExpensiveData(VirtualModel):
    result = models.CharField(max_length=255)
    
    objects = CachedQuerySetManager(
        fetch_func=expensive_operation,
        cache_key='my_expensive_data',
        cache_timeout=3600  # 1 hour
    )
```

**Fonctionnalités** :
- ✅ Cache in-memory (dict)
- ✅ Support cache externe (Redis, Memcached via backend)
- ✅ TTL configurable
- ✅ `refresh()` - Bypass cache
- ✅ `invalidate_cache()` - Vider le cache
- ✅ Auto-génération de cache key

## 🎨 Managers

### VirtualManager (base)

```python
from virtualqueryset.managers import VirtualManager

class MyManager(VirtualManager):
    def get_data(self):
        # Override pour fournir les données
        return [MyModel(id=1), MyModel(id=2)]

class MyModel(VirtualModel):
    objects = MyManager()
```

### Managers spécialisés

- **ConfigQuerySetManager** - Pour settings Django
- **APIQuerySetManager** - Pour APIs externes
- **JSONQuerySetManager** - Pour fichiers JSON
- **CachedQuerySetManager** - Avec cache

## 🏗️ Modèles de base

### VirtualModel

```python
from virtualqueryset.models import VirtualModel

class MyVirtualModel(VirtualModel):
    name = models.CharField(max_length=255)
    
    objects = MyCustomManager()
    
    class Meta:
        managed = False  # Pas de table DB
```

**Caractéristiques** :
- ✅ `managed = False` - Pas de migrations
- ✅ `save()` raise `NotImplementedError` par défaut
- ✅ `delete()` raise `NotImplementedError` par défaut
- ✅ Compatible Django admin
- ✅ Override save/delete si besoin de persistence custom

### ReadOnlyVirtualModel

```python
from virtualqueryset.models import ReadOnlyVirtualModel

class ReadOnlyData(ReadOnlyVirtualModel):
    # Explicitement en lecture seule
    # Messages d'erreur plus clairs
```

## 📊 Cas d'usage

### 1. Afficher des settings dans l'admin

```python
class InstalledApp(VirtualModel):
    name = models.CharField(max_length=255)
    objects = ConfigQuerySetManager('INSTALLED_APPS')
    
    def __str__(self):
        return self.name
```

### 2. Afficher des données d'API

```python
def fetch_users():
    return requests.get('https://api.example.com/users').json()

class ExternalUser(VirtualModel):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    
    objects = APIQuerySetManager(fetch_users, cache_timeout=600)
```

### 3. Charger des données JSON

```python
class Country(VirtualModel):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=100)
    
    objects = JSONQuerySetManager('data/countries.json')
```

### 4. Provider info (comme dans django-missive)

```python
class ProviderInfo(VirtualModel):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    
    objects = CustomProviderManager()  # Charge depuis pymissive
```

## 🧪 Tests

**18 tests implémentés** couvrant :
- ✅ Initialization
- ✅ Filter (exact, icontains, in, gt, etc.)
- ✅ Order by (asc/desc)
- ✅ Get (single, not found, multiple)
- ✅ Slicing
- ✅ First, last, exists
- ✅ Values, values_list
- ✅ Exclude, none

## 🚀 Prochaines extensions possibles

### MultiSourceQuerySet
Combiner plusieurs sources :
```python
# Combine DB + API + JSON
qs = MultiSourceQuerySet(
    sources=[db_qs, api_qs, json_qs]
)
```

### PaginatedAPIQuerySet
Pour grandes APIs avec pagination :
```python
# Auto-fetch next pages
qs = PaginatedAPIQuerySet(
    api_url='https://api.example.com/items',
    page_size=100
)
```

### FileSystemQuerySet
Pour parcourir des fichiers :
```python
# List files as models
qs = FileSystemQuerySet(path='/var/log/*.log')
```

## 📚 Documentation

Voir aussi :
- `README.md` - Vue d'ensemble
- Tests dans `tests/test_base_queryset.py`
- Exemples dans django-missive (ProviderInfo, AddressBackendInfo)

