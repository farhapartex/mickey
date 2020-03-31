## DJ-Blog


DJ-Blog is a Django package to create a blog site quickly and easily. DJ-Blog provide severals public REST APIs
which can be integrated with frontend which are for such as Category List, Tag List, Post List etc.
DJ-Blog also provide a little bit customized Django admin from where user can easily create groups, site information,
category, sub category, blog posts and media images.

Below are the detail information to install the app.

Quick start
-----------

1. Install django rest framework first from here https://www.django-rest-framework.org/#installation and 
    add it to INSTALLED_APPS

2. Add "djBlog" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'djBlog',
    ]

3. Add a middleware 'djBlog.middleware.CurrentUserMiddleware' at the very bottom of the MIDDLEWARE list this::

    MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djBlog.middleware.CurrentUserMiddleware'
]

4. In your project root folder import djBlog urls like as::

    from django.urls import path, re_path, include
    from djBlog import urls as blog_urls

5. Include the djBlog URLconf in your project urls.py like this::

    re_path(r"^api/v1/", include(blog_urls)),

6. Add media url in settings.py file like as :: MEDIA_URL = "/media/"

7. Run ``python manage.py makemigrations`` and ``python manage.py migrate`` to create all models.

8. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

9. Create Category, Subcategory, Tags, Media files and blog posts from django admin.

10. Public REST APIs endpoints are::

    'categories':       'http://localhost:8000/api/v1/public/categories/',
    'tags':             'http://localhost:8000/api/v1/public/tags/'
    'posts':            'http://localhost:8000/api/v1/public/posts/',
    'reacts':           'http://localhost:8000/api/v1/public/reacts/',
    'comments':         'http://localhost:8000/api/v1/public/comments/',
    'site-information': 'http://localhost:8000/api/v1/public/site-information/'

11. For any problem create issue or email me at ``hasan08sust@gmail.com``

In DJ-Blog, image need to choose in time of creation a blog post. Hence there is a media browser named Media. 
To use any image, first need to upload images from Media. In each time of uploading a single image, DJ-Blog created
extra 2 copy of same image with different size which are mainly medium and small size.
By default the medium and small size are (768,1024) and (265, 300).

But you can override the size from settings.py file which is your root app folder. To change, create two variable
in your setting.py file named `MID_IMAGE_SIZE` and `SM_IMAGE_SIZE` and assign to them image sizes as a tuple.

Example ::

MID_IMAGE_SIZE = (768, 1024)
SM_IMAGE_SIZE = (264, 300)