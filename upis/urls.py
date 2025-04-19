from django.urls import path
from . import views
# from .views import BandListView, AlbumListView, SongListView, SampleListView, SourceSampleListView, SourceListView

urlpatterns = [
    path('', views.home, name='upis-home'),
    path('register/', views.register, name='register'),

    # path('search/', views.search, name='samples-search'),
    # path('search/song-search', views.song_search_view, name='song-search-results'),
    # path('search/sample-search', views.sample_search_view, name='samples-search-results'),
    # path('contribute/', views.contribute, name='samples-contribute'),
    # path('browse/', views.browse, name='browse-letters'),
    # path('browse/<str:letter>/', BandListView.as_view(), name='browse-bands'),
    # path('browse/sources/<str:letter>/', SourceListView.as_view(), name='browse-sources'),
    # path('browse/band/<str:band>/', AlbumListView.as_view(), name='browse-albums'),
    # path('browse/album/<str:album>/', SongListView.as_view(), name='browse-songs'),
    # path('browse/source/<str:source>/', SourceSampleListView.as_view(), name='browse-source'),
    # path('browse/song/<str:song>/', SampleListView.as_view(), name='browse-samples'),
]

