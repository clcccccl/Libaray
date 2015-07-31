from django.conf.urls import patterns, include, url
from library.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    ('^home/$',home),
    ('^login/$',login),
    ('^changepassword/$',changePassword),
    ('^submitreturn/$',submitReturn),

    ('^manage/$',manage),
    ('^student/$',student),
    ('^teacher/$',teacher),

    ('^addclass/$',addclass),
    ('^adduser/$',adduser),
    ('^addpay/$',addpay),
    ('^commentbook/$',commentOneBook),

    ('^showclass/$',showclass),
    ('^showuser/$',showuser),
    ('^showpay/$',showpay),
    ('^showpay/$',showpay),
    ('^showcomment/$',showComment),

    ('^getbooks/$',getBooks),
    ('^getonebook/$',getOneBook),
    ('^getborrow/$',getBorrow),
    ('^getstudents/$',getStudents),

    ('^searchbooks/$',searchBooks),

    ('^startborrowbook/$',startBorrowBook),
    ('^borrowbooksearch/$',borrowBookSearch),
    ('^submitborrow/$',submitBorrow),
    ('^returnbook/$',returnBook),

    ('^bookupdate/$',bookupdate),
    ('^downbook/$',downBook),

    # Examples:
    # url(r'^$', 'library.views.home', name='home'),
    # url(r'^library/', include('library.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
