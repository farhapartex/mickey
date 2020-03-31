Mickey
-------


Mickey is a Django package to create a blog site quickly and easily. Mickey provide severals public REST APIs
which can be integrated with frontend which are for such as Category List, Tag List, Post List etc.
Mickey also provide a little bit customized Django admin from where user can easily create groups, site information,
category, sub category, blog posts and media images.

Features
--------

* Add category and Subcategory
* Add tags 
* Add images 
* Add posts (as public/ archive)


Below are the detail information to install the app.

Quick start
-----------

1. Install django rest framework first from here https://www.django-rest-framework.org/#installation and 
    add it to INSTALLED_APPS

2. Add "mickey" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'mickey',
    ]

3. Add a middleware 'mickey.middleware.CurrentUserMiddleware' at the very bottom of the MIDDLEWARE list this::

    MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'mickey.middleware.CurrentUserMiddleware'
    ]

4. In your project root folder import mickey urls like as::

    from django.urls import path, re_path, include
    from django.conf.urls import url
    from django.conf import settings
    from django.conf.urls.static import static
    from mickey import urls as blog_urls

5. Include the mickey URLconf in your project urls.py like this::

    re_path(r"^api/v1/", include(blog_urls)),

6. At the bottom of the urls.py file add this::

    if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

7. Add media url in settings.py file like as :: 

    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media/images/")
    STATIC_ROOT = os.path.join(BASE_DIR, "static")

8. Run ``python manage.py makemigrations`` and ``python manage.py migrate`` to create all models.

9. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

10. Create Category, Subcategory, Tags, Media files and blog posts from django admin.

11. Public REST APIs endpoints are::

    'categories':       'http://localhost:8000/api/v1/public/categories/',
    'tags':             'http://localhost:8000/api/v1/public/tags/'
    'posts':            'http://localhost:8000/api/v1/public/posts/',
    'reacts':           'http://localhost:8000/api/v1/public/reacts/',
    'comments':         'http://localhost:8000/api/v1/public/comments/',
    'site-information': 'http://localhost:8000/api/v1/public/site-information/'



Advance options
---------------

Mickey provide APIs for public post and archive post. ``/api/v1/public/posts/`` and ``/api/v1/public/posts/?type=published``
both API endpoints fetch all posts which are published and not archive. ``/api/v1/public/posts/?type=archive`` To make a post 
archive, mark check box archive in django admin. Remember a archive post is also a published post but in a different scheme. 
To get all posts for a single tag use the API endpoint ``/api/v1/public/posts/?tag=``


In Mickey, image need to choose in time of creation a blog post. Hence there is a media browser named Media. 
To use any image, first need to upload images from Media. In each time of uploading a single image, Mickey created
extra 2 copy of same image with different size which are mainly medium and small size.
By default the medium and small size are (768,1024) and (265, 300).

But you can override the size from settings.py file which is your root app folder. To change, create two variable
in your setting.py file named `MID_IMAGE_SIZE` and `SM_IMAGE_SIZE` and assign to them image sizes as a tuple.

Example ::

    MID_IMAGE_SIZE = (768, 1024)
    SM_IMAGE_SIZE = (264, 300)