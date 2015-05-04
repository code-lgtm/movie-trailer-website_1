import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Movie-Trailers</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet"
        href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet"
        href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script
        src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js">
    </script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
        .carousel-inner > .item > img,
        .carousel-inner > .item > a > img {
            width: 70%;
            margin: auto;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal',
        function (event) {
            // Remove the src so the player itself gets removed,
            //as this is the only reliable way to ensure the video stops
            //playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' +
                trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>",
            {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal"
          aria-hidden="true">
            <img
                src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Project - Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''

# Default active item for carousal indicator.
ordered_list_active = '''
    <li data-target="#myCarousel" data-slide-to="{slide_number}"
    class="active"></li>
'''
# Non active carousal indicators
ordered_list = '''
    <li data-target="#myCarousel" data-slide-to="{slide_number}"></li>
'''

# Default active carousal item
inner_image_active = '''
    <div class="item active movie-tile"
    data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal"
        data-target="#trailer">
        <img src="{movie_poster_url}">
        <div class="carousel-caption">
            <h2>{movie_title}</h2>
        </div>
    </div>
'''

# Non Active carousal items
inner_image = '''
    <div class="item movie-tile" data-trailer-youtube-id="{trailer_youtube_id}"
    data-toggle="modal"
        data-target="#trailer">
        <img src="{movie_poster_url}">
        <div class="carousel-caption">
            <h2>{movie_title}</h2>
        </div>
    </div>
'''

# bootstarp carousal implementation
movie_tile_content = '''
<div class="carousel" id="myCarousel" data-ride="carousel"
data-interval="false">
        <ol class="carousel-indicators">
            {list_item}
        </ol>

        <div class="carousel-inner" role="listbox">
            {img_item}
        </div>

        <a class="left carousel-control" href="#myCarousel" role="button"
        data-slide="prev">
            <span class="glyphicon glyphicon-chevron-left" aria-hidden="true">
            </span>
            <span class="sr-only">Previous
            </span>
        </a>

        <a class="right carousel-control" href="#myCarousel" role="button"
        data-slide="next">
            <span class="glyphicon glyphicon-chevron-right" aria-hidden="true">
            </span>
            <span class="sr-only">Next
            </span>
        </a>
</div>
'''


def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    list_content = ''
    img_content = ''
    index = 0

    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match1 = re.search(r'(?<=v=)[^&#]+',
                                      movie.trailer_youtube_url)
        youtube_id_match2 = re.search(r'(?<=be/)[^&#]+',
                                      movie.trailer_youtube_url)
        youtube_id_match = youtube_id_match1 or youtube_id_match2
        youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        if index == 0:
            # add active carousal-indicator
            list_content += ordered_list_active.format(slide_number=index)
        else:
            # non active carousal indicators
            list_content += ordered_list.format(slide_number=index)

        if index == 0:
            # default carousal item
            img_content += inner_image_active.format(
                movie_poster_url=movie.poster_image_url,
                trailer_youtube_id=youtube_id,
                movie_title=movie.title)
        else:
            # non active carousal items
            img_content += inner_image.format(
                movie_poster_url=movie.poster_image_url,
                trailer_youtube_id=youtube_id,
                movie_title=movie.title)
        index += 1

    # add carousal items and carousal indicators dynamically
    content = movie_tile_content.format(
            list_item=list_content,
            img_item=img_content)

    return content


def open_movies_page(movies):
    # Create or overwrite the output file
    output_file = open('movie_trailers.html', 'w')

    # Replace the placeholder for the movie tiles with the actual
    # dynamically generated content
    rendered_content = main_page_content.format(
        movie_tiles=create_movie_tiles_content(movies))

    # Output the file
    output_file.write(main_page_head + rendered_content)
    output_file.close()

    # open the output file in the browser
    url = os.path.abspath(output_file.name)
    webbrowser.open('file://' + url, new=2)  # open in a new tab, if possible


class Movie:
    def __init__(self, title, poster_image_url, trailer_youtube_url):
        self.title = title
        self.poster_image_url = poster_image_url
        self.trailer_youtube_url = trailer_youtube_url

url = 'http://upload.wikimedia.org/wikipedia/en/d/df/3_idiots_poster.jpg'
movie0 = Movie('3 Idiots',
               url,
               'https://www.youtube.com/watch?v=xvszmNXdM4w')

url = 'http://upload.wikimedia.org/wikipedia/en/3/3d/Zindaginamilegidobara.jpg'
movie1 = Movie('Zindagi na Milegi Dobara',
               url,
               'https://www.youtube.com/watch?v=ifIBOKCfjVs')

url = 'http://upload.wikimedia.org/wikipedia/en/8/81/The_Lunchbox_poster.jpg'
movie2 = Movie('Lunchbox',
               url,
               'https://www.youtube.com/watch?v=Enq9nNGnMFY')

movies = [movie0, movie1, movie2]
open_movies_page(movies)
