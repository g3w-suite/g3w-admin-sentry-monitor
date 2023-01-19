# G3W-ADMIN-SENTRY-MONITOR

G3W-SUITE module for application performance monitoring and error tracking via [sentry.io](https://sentry.io/).

![sentry-dashboard](https://user-images.githubusercontent.com/9614886/213207306-f23be240-2af2-4ce1-8671-0bb1d102444f.png)

## Installation

Install `sentry_monitor` module into [`g3w-admin`](https://github.com/g3w-suite/g3w-admin/tree/v.3.5.x/g3w-admin) applications folder:

```sh
# Install module from github (v1.0.0)
pip3 install git+https://github.com/g3w-suite/g3w-admin-sentry-monitor.git@v1.0.0

# Install module from github (master branch)
# pip3 install git+https://github.com/g3w-suite/g3w-admin-sentry-monitor.git@master

# Install module from local folder (git development)
# pip3 install -e /shared-volume/g3w-admin-sentry-monitor

# Install module from PyPi (not yet available)
# pip3 install g3w-admin-sentry-monitor
```

Enable `'sentry_monitor'` module adding it to `G3W_LOCAL_MORE_APPS` list:

```py
# local_settings.py

G3WADMIN_LOCAL_MORE_APPS = [
    ...
    'sentry_monitor'
    ...
]
```

Refer to [g3w-suite-docker](https://github.com/g3w-suite/g3w-suite-docker) repository for more info about running this on a docker instance.

**NB** On Ubuntu Jammy you could get an `UNKNOWN` package install instead of `g3w-admin-sentry-monitor`, you can retry installing it as follows to fix it:

```sh
# Fix: https://github.com/pypa/setuptools/issues/3269#issuecomment-1254507377
export DEB_PYTHON_INSTALL_LAYOUT=deb_system

# And then install again the module
pip3 install ...
```

## Configuration

The following packages are included in this module:

- [sentry_sdk](https://pypi.org/project/sentry-sdk/)
- [sentry-cdn.com/bundle.min.js](https://docs.sentry.io/platforms/javascript/install/cdn/)

Refer to the official docs for a more comprehensive list of the available settings:

```py
# Update your Sentry project DSN (Data Source Name)
#
# see: https://docs.sentry.io/product/sentry-basics/dsn-explainer/
# -------------------------------------------

SENTRY_JS_DSN = "https://your-javascript-dsn@sentry.example.com/1"
SENTRY_PY_DSN = "https://your-python-dsn@sentry.example.com/2"
```

```html
<!--
  Include javascript tracking script within all html pages you want to monitor

  see: https://docs.djangoproject.com/en/2.2/topics/templates/#the-django-template-language
-->
<html>
<body>
   ...
  {% if SETTINGS.SENTRY_JS %}
    {{ SETTINGS.SENTRY_JS | safe }}
  {% endif %}
  ...
</html>
```

For the default settings currently applied by this module, see also: [`sentry_monitor/__init__.py`](sentry_monitor/__init__.py)

## Check tracker integration

Intentionally trigger a javascript error within a django page (html template) and then login into your [sentry.io](https://sentry.io/) account for viewing the trace log

```html
<html>
<body>
   ...
  {% if SETTINGS.SENTRY_JS %}
    {{ SETTINGS.SENTRY_JS | safe }}
  {% endif %}
  ...
  <script>
    myUndefinedFunction(); // Intentionally trigger a javascript error
  </script>
</html>
```

## Contributing

Steps to follow for local development of this module.

Clone `g3w-admin` and `g3w-admin-sentry-monitor` repositories into two adjacent folders:

```sh
cd /path/to/your/development/workspace

git clone https://github.com/g3w-suite/g3w-admin.git
git clone https://github.com/g3w-suite/g3w-admin-sentry-monitor.git
```

So your folder structure should matches the following:

```sh
.
├── g3w-admin/
│   ├── g3w-admin/
│   │   ├── base/
│   │   ├── core/
│   │   ├── ...
│   │   └── manage.py
│   └── README.md
│
└── g3w-admin-sentry-monitor/
    ├── sentry_monitor/
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── urls.py
    │   ├── views.py
    │   └── ...
    ├── pyproject.toml
    └── README.md
```

Install the `g3w-admin-sentry-monitor` module in editable mode starting from your `g3w-admin` folder:

```sh
cd g3w-admin

python3 -m pip install -e ../g3w-admin-sentry-monitor
```

Then activate the `'sentry_monitor'` module as usual by adding it to `G3W_LOCAL_MORE_APPS` list.

## Publish

Create a new `git tag` that is appropriate for the version you intend to publish, eg:

```sh
git tag -a v1.0.1
git push origin v1.0.1
```

<details>
<summary> Publishing on the Python Package Index </summary>

Steps to follow when releasing a new software version on [PyPi](https://pypi.org/).

First make sure you have the latest versions of `pip`, `build` and `twine` installed:

```sh
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine
```

Build the `dist` folder starting from the same directory where `pyproject.toml` is located:

```sh
python3 -m build
```

Upload all to [PyPI](https://pypi.org/) and verify things look right:

```sh
twine upload dist/*
```

</details>

## TODO

Find out a way to install this module through the [`INSTALLED_APPS`](https://docs.djangoproject.com/en/2.2/ref/settings/#installed-apps) (ie. much earlier than [`G3W_LOCAL_MORE_APPS`](https://github.com/g3w-suite/g3w-admin/blob/537be844475043468fa0f792b33fe9cc88b76f31/g3w-admin/base/settings/__init__.py#L14)) variable in order to correctly activate the monitoring python as well (ref: `SENTRY_PY_DSN`).

```py
# local_settings.py

from django.conf import settings

# As per g3w-admin@v3.5 the below variable assignment is currently not
# possible because the INSTALLED_APPS variable is alwayse overridden 
# regardless of the value assigned in here

INSTALLED_APPS = ['sentry_monitor'] + settings.INSTALLED_APPS

# A temporary workaround could be using the THIRD_PARTY_APPS variable:

THIRD_PARTY_APPS = ['sentry_monitor'] + settings.THIRD_PARTY_APPS
```

```py
# /g3w-admin/g3w-admin/base/settings/__init__.py#L14 (v3.5)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + G3WADMIN_APPS + G3WADMIN_PROJECT_APPS
```


## Related resources

Sentry integrations:

- [javascript](https://docs.sentry.io/platforms/javascript) + [vue](https://docs.sentry.io/platforms/javascript/guides/vue/)
- [python](https://docs.sentry.io/platforms/python) + [django](https://docs.sentry.io/platforms/python/guides/django/)

---

**Compatibile with:**
[![g3w-admin version](https://img.shields.io/badge/g3w--admin-3.5-1EB300.svg?style=flat)](https://github.com/g3w-suite/g3w-admin/tree/v.3.5.x)
[![g3w-suite-docker version](https://img.shields.io/badge/g3w--suite--docker-3.5-1EB300.svg?style=flat)](https://github.com/g3w-suite/g3w-suite-docker/tree/v3.5.x)

---

**License:** MPL-2
