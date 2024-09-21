# OMDB (Offline Movie Database)

OMDB is a Python project that provides IMDB (Internet Movie Database) experiments from their local computer. With OMDB, users can search, add, rate, and comment on their favorite actors and movies. Also, users can create and share their watchlists.


## Features

- **Create Personal Account**: To use the application, create your own account.
- **Search Movies and Actors**: Search through 344276 movies and 1044499 actors from your local database, and see their associated actors and movies.
- **Add Movies and Actors**: If the movie or actor you want does not exist in the database, add them by clicking the "add" button.
- **Match Movies and Actors**: If the actor in a movie does not match in database, match them by clicking the "match" button.
- **Rate and Comment on Movies and Actors**: Users are able to rate and comment on movies and actors, and they are able to share their opinions with other users.
- **Create Watchlists**: Users can to create their watchlists and share with other users.


## Tables In Database

1. **accounts_data**
    - username (TEXT)
    - password (TEXT)
    - id (INT)
2. **movies**
    - id (TEXT)
    - title (TEXT)
    - year (TEXT)
3. **people**
    - id (TEXT)
    - name (TEXT)
    - birth (TEXT)
4. **stars**
    - person_id (TEXT)
    - movie_id (TEXT)
5. **commentrating**
    - account_id (TEXT)
    - movie_or_actor_id (TEXT)
    - rating (INT)
    - comment (TEXT)
6. **watchlists**
    - user_id (TEXT)
    - watchlist_id (INT)
    - watchlist_name (TEXT)
7. **watch**
    - watchlist_id (INT)
    - movie_id (TEXT)


## Classes in Project

1. **User**
    - user_id (str)
    - user_name (str)
2. **Actor**
    - **Attributes**
        - `actor_id` (str)
        - `actor_name` (str)
        - `actor_born` (str)
        - `actor_movies` (list)
        - `actor_associatives` (list)
        - `actor_rating` (float)
    - **Functions**
        - `get_info`: Get attributes of the actor
        - `get_rating`: Get rating of the actor
        - `load_movies`: Get movies of the actor
        - `get_associative`: Get associatives of the actor
3. **Movie**
    - **Attributes**
        - `movie_id` (str)
        - `movie_title` (str)
        - `movie_year` (str)
        - `movie_actors` (list)
        - `movie_rating` (float)
    - **Functions**
        - `get_info`: Get attributes of the movie
        - `get_rating`: Get rating of the movie
        - `load_actors`: Get actors of the movie


## Functions of the Project

- **load_frame1**: Loads the user_account entry frame. With this frame users are able to log in and create accounts.

- **load_frame2**: Loads the search frame. With this frame users can search movies and actors. Also this functions activates options menubar. This menubar includes 6 functions:
    - `Match M2A`: calls load_M2A_frame
    - `Match A2M`: calls load_A2M_frame
    - `Add Actor`: calls load_add_actor_frame
    - `Add Movie`: calls load_movie_actor_frame
    - `Create Watchlist`: calls load_create_watchlist_frame
    - `Watchlist`: calls load_watchlists_frame

- **load_actor_frame(actor_id)**: This function takes an actor_id variable. Loads the selected actor frame. With this frame users can see associated actors and movies. Also this frame provides two buttons; one of them lets the user comment on actor and the other one shows every comment related to actor.

- **load_movie_frame(movie_id)**: This function takes a movie_id variable. Loads the selected movie frame. With this frame users can see associated actors. Also this frame provides two buttons; one of them lets user comment on the movie and the other one shows every comment related to movie.

- **load_watchlists_frame**: Loads the watchlists frame. With this frame users can see watchlists created by themselves and other users.

- **create_watchlist(movie_list, name_of_wathclist)**: This function takes two variables and creates a watchlist. Watchlists are stored in the database.

- **load_create_watchlist_frame**:  Loads the frame in which users can create watchlists.

- **load_movie_add_frame**: Loads the frame with which users can add new movies to database.

- **load_actor_add_frame**: Loads the frame with which users can add new actors to database.

- **load_A2M_frame**: Loads the frame in which users can match selected actor with selected movies.

- **load_M2A_frame**: Loads the frame in which users can match selected movie with selected actors.

- **load_comments(movie_or_actor_id)**: Loads the frame in which users can see the comments related to the actor or the movie that is selected.

- **load_comment(movie_or_actor_id)**: Loads the frame in which users can comment on actors or movies and rate them.

- **destroy_frames**: Destroys all frames before opening a new one.

- **There are also some small functions that handle the tasks of creating new widgets to frames, matching movies and actors, loading data, adding new data to database, and functions bound to buttons and tree elements.**


## Requirements

1. This project is created on `python version 3.10.3` and does not includes any external packages.
2. `spider.png` image file that is in the same zip with the code.
3. `database1.db` database that is in the same zip with the code.


## How To Use?

1. Make sure requriments are satisfied.

2. Execute the code.

3. If not already created, create an account.

4. `Search Screen`: Enter the movie or actor that you want to find in the search box. Use the spinbox to choose how many results you want to see, and select one of radio boxes to search actor or movie. Then, click the button. Select one of the results. (Loading the other frame can take a while due to high amount of data)

5. `Actor or Movie Screen`: In this screen you can access informations about the actor or the movie. By clicking one of the movies or actors you can visit their screen. By clicking "Comment" button, you can leave a comment and rate them. By clicking "Comments" you can see other peoples comments and ratings.

6. `Match Movie to Actors`: From options menubar, click "Match M2A" option. In this screen search your movie and select it, search actors to match and select them. When you are finished, click done. By clicking the "Back" button you can return to the search screen.

7. `Match Actor to Movies`: From options menubar, click "Match A2M" option. In this screen search your actor and select it, search movies to match and select them. When you are finished, click done. By clicking the "Back" button you can return to the search screen.

8. `Adding Actor or Movie`: From options menubar, click one of the "Add" options (add movie or add actor). Fill the blanks about the movie or actor. Click the "Add" button to add a movie or an actor. By clicking the "Back" button you can return to the search screen.

9. `Create Watchlist`: From options menubar, click "Create Watchlist" option. Provide the name of the watchlist. Search your movies and click them to add to the wathclist. Movies you selected will be listed in tree in the screen. When you are finished click the "Done" button. By clicking "Back" button you can return to search screen.

10. `See Watchlist`: From options menubar, click "Watchlists" option. In this screen you can see every created watchlist. By clicking the "Back" button you can return to the search screen.

11. `Enjoy`: Most importantly do not forget to enjoy 😊.